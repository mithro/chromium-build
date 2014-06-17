#!/usr/bin/env python
# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""try_job_rietveld.py testcases."""

import test_env
from common import find_depot_tools

import datetime
import json
import os
import shutil
import tempfile
import unittest
import uuid

from testing_support import auto_stub
from twisted.internet import defer
from twisted.web import client

from master import try_job_rietveld


TEST_BASE_URL = ('https://codereview.chromium.org/get_pending_try_patchsets?'
                 'limit=1000&offset=1&master=tryserver.chromium')


# Create timestamps both with microseconds=0 and !=0.
# See http://crbug.com/380370.
utcnow = datetime.datetime.utcnow()
utcnow_rounded = datetime.datetime(
    utcnow.year, utcnow.month, utcnow.day, utcnow.hour,
    utcnow.minute, utcnow.second)
utcnow_microsec = datetime.datetime(
    utcnow.year, utcnow.month, utcnow.day, utcnow.hour,
    utcnow.minute, utcnow.second, 123456)


TEST_RIETVELD_PAGES = [
  [{'timestamp': datetime.datetime.utcnow(), 'key': 'test_key_1'}],
  [{'timestamp': (utcnow_rounded - datetime.timedelta(hours=5, minutes=59)),
    'key': 'test_key_2'},
   {'timestamp': (utcnow_microsec - datetime.timedelta(hours=6, minutes=1)),
    'key': 'test_key_3'}]
]


class MockBuildSetsDB(object):

    def __init__(self):
      self._buildset_props = {}

    def addBuildSetProperties(self, bsid, buildset_props):
      self._buildset_props[bsid] = buildset_props

    def getBuildsetProperties(self, bsid):
      return self._buildset_props[bsid]

    def getRecentBuildsets(self, count):
      bsids_desc = sorted(self._buildset_props.keys(), reverse=True)
      return [{'bsid': bsid} for bsid in bsids_desc][:count]


class MockDBCollection(object):

    buildsets = None

    def __init__(self):
      self.buildsets = MockBuildSetsDB()


class MockMaster(object):

  db = None

  def __init__(self):
    self.db = MockDBCollection()


class MockTryJobRietveld(object):

  def __init__(self):
    self.submitted_jobs = []

  def SubmitJobs(self, jobs):
    self.submitted_jobs.extend(jobs);
    return defer.succeed(None)

  def has_valid_user_list(self):
    return True

  def addService(self, service):
    pass

  def clear(self):
    self.submitted_jobs = []


class RietveldPollerWithCacheTest(auto_stub.TestCase):

  def _GetPage(self, url, **_):
    self.assertTrue(url.startswith(TEST_BASE_URL))
    self.assertIs(type(url), str)

    self._numRequests += 1

    if url == TEST_BASE_URL:
      cursor = str(uuid.uuid4())
      self._cursors[cursor] = 0
      jobs = TEST_RIETVELD_PAGES[0]
    else:
      prev_cursor = url[len(TEST_BASE_URL)+8:]
      self.assertIn(prev_cursor, self._cursors,
                    'Requested incorrect cursor %s. Available cursors: %s' %
                    (prev_cursor, self._cursors))
      if self._cursors[prev_cursor] + 1 < len(TEST_RIETVELD_PAGES):
        cursor = str(uuid.uuid4())
        self._cursors[cursor] = self._cursors[prev_cursor] + 1
        jobs = TEST_RIETVELD_PAGES[self._cursors[cursor]]
      else:
        cursor = prev_cursor
        jobs = []

    response = {'cursor': cursor, 'jobs': jobs}

    def date_handler(obj):
      if isinstance(obj, datetime.datetime):
        return str(obj)

    response_str = json.dumps(response, default=date_handler)
    return defer.succeed(response_str)

  def setUp(self):
    self.mock(client, 'getPage', self._GetPage)
    self._numRequests = 0
    self._cursors = {}
    self._mockTJR = MockTryJobRietveld()
    self._mockMaster = MockMaster()
    super(RietveldPollerWithCacheTest, self).setUp()

  def testRequestsAllPagesWithJobsFromRietveld(self):
    poller = try_job_rietveld._RietveldPollerWithCache(TEST_BASE_URL, 60)
    poller.master = self._mockMaster
    poller.setServiceParent(self._mockTJR)
    poller.poll()
    self.assertEqual(self._numRequests, len(TEST_RIETVELD_PAGES) + 1)

  def testSubmitsNewJobsAndIgnoresOldOnes(self):
    poller = try_job_rietveld._RietveldPollerWithCache(TEST_BASE_URL, 60)
    poller.master = self._mockMaster
    poller.setServiceParent(self._mockTJR)
    poller.poll()
    self.assertEqual(len(self._mockTJR.submitted_jobs), 2)
    self.assertEquals(self._mockTJR.submitted_jobs[0]['key'], 'test_key_1')
    self.assertEquals(self._mockTJR.submitted_jobs[1]['key'], 'test_key_2')

  def testDoesNotResubmitPreviousJobs(self):
    poller = try_job_rietveld._RietveldPollerWithCache(TEST_BASE_URL, 60)
    poller.master = self._mockMaster
    poller.setServiceParent(self._mockTJR)
    poller.poll()
    self._mockTJR.clear()
    poller.poll()
    self.assertEquals(len(self._mockTJR.submitted_jobs), 0)

  def testDoesNotResubmitJobsAlreadyOnMaster(self):
    poller = try_job_rietveld._RietveldPollerWithCache(TEST_BASE_URL, 60)
    self._mockMaster.db.buildsets.addBuildSetProperties(
        42, {'try_job_key': ('test_key_1', 'Try bot')})
    poller.master = self._mockMaster
    poller.setServiceParent(self._mockTJR)
    poller.poll()
    self.assertEquals(len(self._mockTJR.submitted_jobs), 1)
    self.assertEquals(self._mockTJR.submitted_jobs[0]['key'], 'test_key_2')

  def testShouldLimitNumberOfBuildsetsUsedForInit(self):
    self.mock(try_job_rietveld, 'MAX_RECENT_BUILDSETS_TO_INIT_CACHE', 1)
    poller = try_job_rietveld._RietveldPollerWithCache(TEST_BASE_URL, 60)
    self._mockMaster.db.buildsets.addBuildSetProperties(
        42, {'try_job_key': ('test_key_1', 'Try bot')})
    self._mockMaster.db.buildsets.addBuildSetProperties(
        55, {'try_job_key': ('test_key_2', 'Try bot')})
    poller.master = self._mockMaster
    poller.setServiceParent(self._mockTJR)
    poller.poll()
    self.assertEquals(len(self._mockTJR.submitted_jobs), 1)
    self.assertEquals(self._mockTJR.submitted_jobs[0]['key'], 'test_key_1')

  def testDoesNotPerformPollWhenThereAreNoValidUsers(self):
    self.mock(self._mockTJR, 'has_valid_user_list', lambda: False)
    poller = try_job_rietveld._RietveldPollerWithCache(TEST_BASE_URL, 60)
    poller.master = self._mockMaster
    poller.setServiceParent(self._mockTJR)
    poller.poll()
    self.assertEqual(len(self._mockTJR.submitted_jobs), 0)


if __name__ == '__main__':
  unittest.main()
