#!/usr/bin/env python
# Copyright (c) 2011 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

""" Source file for gatekeeper testcases."""

import unittest

import test_env  # pylint: disable=W0611

import mock
from master import gatekeeper


class GateKeeperTest(unittest.TestCase):
  def setUp(self):
    class PasswordMock(mock.Mock):  # pylint: disable=W0232
      def GetPassword(self):
        mock.Mock.__getattr__(self, 'GetPassword')
        return 'testpw'
    self.old_gkgpp = gatekeeper.get_password.Password
    gatekeeper.get_password.Password = (lambda file: PasswordMock())

  def tearDown(self):
    gatekeeper.get_password.Password = self.old_gkgpp

  def testGateKeeperCreation(self):
    notifier = gatekeeper.GateKeeper(
        fromaddr='buildbot@test',
        mode='failing',
        forgiving_steps=[],
        lookup='test',
        sendToInterestedUsers=False,
        extraRecipients=['extra@test'],
        status_header='Failure on test.',
        tree_status_url='http://localhost/')
    self.assertTrue(notifier)


if __name__ == '__main__':
  unittest.main()
