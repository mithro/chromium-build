#!/usr/bin/env python
# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import cStringIO
import json
import logging
import os
import shutil
import sys
import tempfile
import unittest

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# For 'test_env'.
sys.path.insert(
    0, os.path.abspath(os.path.join(THIS_DIR, '..', '..', '..', 'unittests')))
# For 'standard_gtest_merge.py'.
sys.path.insert(
    0, os.path.abspath(os.path.join(THIS_DIR, '..', 'resources')))

# Imported for side effects on sys.path.
import test_env

# In depot_tools/
from testing_support import auto_stub
import standard_gtest_merge


# gtest json output for successfully finished shard #0.
GOOD_GTEST_JSON_0 = {
  'all_tests': [
    'AlignedMemoryTest.DynamicAllocation',
    'AlignedMemoryTest.ScopedDynamicAllocation',
    'AlignedMemoryTest.StackAlignment',
    'AlignedMemoryTest.StaticAlignment',
  ],
  'disabled_tests': [
    'ConditionVariableTest.TimeoutAcrossSetTimeOfDay',
    'FileTest.TouchGetInfo',
    'MessageLoopTestTypeDefault.EnsureDeletion',
  ],
  'global_tags': ['CPU_64_BITS', 'MODE_DEBUG', 'OS_LINUX', 'OS_POSIX'],
  'per_iteration_data': [{
    'AlignedMemoryTest.DynamicAllocation': [{
      'elapsed_time_ms': 0,
      'losless_snippet': True,
      'output_snippet': 'blah\\n',
      'output_snippet_base64': 'YmxhaAo=',
      'status': 'SUCCESS',
    }],
    'AlignedMemoryTest.ScopedDynamicAllocation': [{
      'elapsed_time_ms': 0,
      'losless_snippet': True,
      'output_snippet': 'blah\\n',
      'output_snippet_base64': 'YmxhaAo=',
      'status': 'SUCCESS',
    }],
  }],
}


# gtest json output for successfully finished shard #1.
GOOD_GTEST_JSON_1 = {
  'all_tests': [
    'AlignedMemoryTest.DynamicAllocation',
    'AlignedMemoryTest.ScopedDynamicAllocation',
    'AlignedMemoryTest.StackAlignment',
    'AlignedMemoryTest.StaticAlignment',
  ],
  'disabled_tests': [
    'ConditionVariableTest.TimeoutAcrossSetTimeOfDay',
    'FileTest.TouchGetInfo',
    'MessageLoopTestTypeDefault.EnsureDeletion',
  ],
  'global_tags': ['CPU_64_BITS', 'MODE_DEBUG', 'OS_LINUX', 'OS_POSIX'],
  'per_iteration_data': [{
    'AlignedMemoryTest.StackAlignment': [{
      'elapsed_time_ms': 0,
      'losless_snippet': True,
      'output_snippet': 'blah\\n',
      'output_snippet_base64': 'YmxhaAo=',
      'status': 'SUCCESS',
    }],
    'AlignedMemoryTest.StaticAlignment': [{
      'elapsed_time_ms': 0,
      'losless_snippet': True,
      'output_snippet': 'blah\\n',
      'output_snippet_base64': 'YmxhaAo=',
      'status': 'SUCCESS',
    }],
  }],
}


# GOOD_GTEST_JSON_0 and GOOD_GTEST_JSON_1 merged.
GOOD_GTEST_JSON_MERGED = {
  'all_tests': [
    'AlignedMemoryTest.DynamicAllocation',
    'AlignedMemoryTest.ScopedDynamicAllocation',
    'AlignedMemoryTest.StackAlignment',
    'AlignedMemoryTest.StaticAlignment',
  ],
  'disabled_tests': [
    'ConditionVariableTest.TimeoutAcrossSetTimeOfDay',
    'FileTest.TouchGetInfo',
    'MessageLoopTestTypeDefault.EnsureDeletion',
  ],
  'global_tags': ['CPU_64_BITS', 'MODE_DEBUG', 'OS_LINUX', 'OS_POSIX'],
  'missing_shards': [],
  'per_iteration_data': [{
    'AlignedMemoryTest.DynamicAllocation': [{
      'elapsed_time_ms': 0,
      'losless_snippet': True,
      'output_snippet': 'blah\\n',
      'output_snippet_base64': 'YmxhaAo=',
      'status': 'SUCCESS',
    }],
    'AlignedMemoryTest.ScopedDynamicAllocation': [{
      'elapsed_time_ms': 0,
      'losless_snippet': True,
      'output_snippet': 'blah\\n',
      'output_snippet_base64': 'YmxhaAo=',
      'status': 'SUCCESS',
    }],
    'AlignedMemoryTest.StackAlignment': [{
      'elapsed_time_ms': 0,
      'losless_snippet': True,
      'output_snippet': 'blah\\n',
      'output_snippet_base64': 'YmxhaAo=',
      'status': 'SUCCESS',
    }],
    'AlignedMemoryTest.StaticAlignment': [{
      'elapsed_time_ms': 0,
      'losless_snippet': True,
      'output_snippet': 'blah\\n',
      'output_snippet_base64': 'YmxhaAo=',
      'status': 'SUCCESS',
    }],
  }],
  'swarming_summary': {
    u'shards': [
      {
        u'state': u'COMPLETED',
        u'outputs_ref': {
          u'view_url': u'blah',
        },
      }
      ],
  },
}


# Only shard #1 finished. UNRELIABLE_RESULTS is set.
BAD_GTEST_JSON_ONLY_1_SHARD = {
  'all_tests': [
    'AlignedMemoryTest.DynamicAllocation',
    'AlignedMemoryTest.ScopedDynamicAllocation',
    'AlignedMemoryTest.StackAlignment',
    'AlignedMemoryTest.StaticAlignment',
  ],
  'disabled_tests': [
    'ConditionVariableTest.TimeoutAcrossSetTimeOfDay',
    'FileTest.TouchGetInfo',
    'MessageLoopTestTypeDefault.EnsureDeletion',
  ],
  'global_tags': [
    'CPU_64_BITS',
    'MODE_DEBUG',
    'OS_LINUX',
    'OS_POSIX',
    'UNRELIABLE_RESULTS',
  ],
  'missing_shards': [0],
  'per_iteration_data': [{
    'AlignedMemoryTest.StackAlignment': [{
      'elapsed_time_ms': 0,
      'losless_snippet': True,
      'output_snippet': 'blah\\n',
      'output_snippet_base64': 'YmxhaAo=',
      'status': 'SUCCESS',
    }],
    'AlignedMemoryTest.StaticAlignment': [{
      'elapsed_time_ms': 0,
      'losless_snippet': True,
      'output_snippet': 'blah\\n',
      'output_snippet_base64': 'YmxhaAo=',
      'status': 'SUCCESS',
    }],
  }],
}


class _StandardGtestMergeTest(auto_stub.TestCase):

  def setUp(self):
    super(_StandardGtestMergeTest, self).setUp()
    self.temp_dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.temp_dir)
    super(_StandardGtestMergeTest, self).tearDown()

  def _write_temp_file(self, path, content):
    abs_path = os.path.join(self.temp_dir, path.replace('/', os.sep))
    if not os.path.exists(os.path.dirname(abs_path)):
      os.makedirs(os.path.dirname(abs_path))
    with open(abs_path, 'w') as f:
      if isinstance(content, dict):
        json.dump(content, f)
      else:
        assert isinstance(content, str)
        f.write(content)
    return abs_path


class LoadShardJsonTest(_StandardGtestMergeTest):

  def test_double_digit_jsons(self):
    jsons_to_merge = []
    for i in xrange(15):
      json_dir = os.path.join(self.temp_dir, str(i))
      json_path = os.path.join(json_dir, 'output.json')
      if not os.path.exists(json_dir):
        os.makedirs(json_dir)
      with open(json_path, 'w') as f:
        json.dump({'all_tests': ['LoadShardJsonTest.test%d' % i]}, f)
      jsons_to_merge.append(json_path)

    content, err = standard_gtest_merge.load_shard_json(0, jsons_to_merge)
    self.assertEqual({'all_tests': ['LoadShardJsonTest.test0']}, content)
    self.assertIsNone(err)

    content, err = standard_gtest_merge.load_shard_json(12, jsons_to_merge)
    self.assertEqual({'all_tests': ['LoadShardJsonTest.test12']}, content)
    self.assertIsNone(err)


class MergeShardResultsTest(_StandardGtestMergeTest):
  """Tests for merge_shard_results function."""

  def setUp(self):
    super(MergeShardResultsTest, self).setUp()
    self.summary = None
    self.test_files = []

  def stage(self, summary, files):
    self.summary = self._write_temp_file('summary.json', summary)
    for path, content in files.iteritems():
      abs_path = self._write_temp_file(path, content)
      self.test_files.append(abs_path)

  def call(self, exit_code=0):
    stdout = cStringIO.StringIO()
    self.mock(sys, 'stdout', stdout)
    merged = standard_gtest_merge.merge_shard_results(
        self.summary, self.test_files)
    return merged, stdout.getvalue().strip()

  def test_ok(self):
    # Two shards, both successfully finished.
    self.stage({
      u'shards': [
        {
          u'state': u'COMPLETED',
        },
        {
          u'state': u'COMPLETED',
        },
      ],
    },
    {
      '0/output.json': GOOD_GTEST_JSON_0,
      '1/output.json': GOOD_GTEST_JSON_1,
    })
    merged, stdout = self.call()
    merged['swarming_summary'] = {
      'shards': [
        {
          u'state': u'COMPLETED',
          u'outputs_ref': {
            u'view_url': u'blah',
          },
        }
      ],
    }
    self.assertEqual(GOOD_GTEST_JSON_MERGED, merged)
    self.assertEqual('', stdout)

  def test_missing_summary_json(self):
    # summary.json is missing, should return None and emit warning.
    self.summary = os.path.join(self.temp_dir, 'summary.json')
    merged, output = self.call()
    self.assertEqual(None, merged)
    self.assertIn('@@@STEP_WARNINGS@@@', output)
    self.assertIn('summary.json is missing or can not be read', output)

  def test_unfinished_shards(self):
    # Only one shard (#1) finished. Shard #0 did not.
    self.stage({
      u'shards': [
        None,
        {
          u'state': u'COMPLETED',
        },
      ],
    },
    {
      u'1/output.json': GOOD_GTEST_JSON_1,
    })
    merged, stdout = self.call(1)
    merged.pop('swarming_summary')
    self.assertEqual(BAD_GTEST_JSON_ONLY_1_SHARD, merged)
    self.assertIn(
        '@@@STEP_WARNINGS@@@\nsome shards did not complete: 0\n', stdout)
    self.assertIn(
        '@@@STEP_LOG_LINE@some shards did not complete: 0@'
        'Missing results from the following shard(s): 0@@@\n', stdout)

  def test_missing_output_json(self):
    # Shard #0 output json is missing.
    self.stage({
      u'shards': [
        {
          u'state': u'COMPLETED',
        },
        {
          u'state': u'COMPLETED',
        },
      ],
    },
    {
      u'1/output.json': GOOD_GTEST_JSON_1,
    })
    merged, stdout = self.call(1)
    merged.pop('swarming_summary')
    self.assertEqual(BAD_GTEST_JSON_ONLY_1_SHARD, merged)
    self.assertIn(
        '@@@STEP_WARNINGS@@@\nTask ran but no result was found: '
        'shard 0 test output was missing', stdout)

  def test_large_output_json(self):
    # a shard is too large.
    self.stage({
      u'shards': [
        {
          u'state': u'COMPLETED',
        },
        {
          u'state': u'COMPLETED',
        },
      ],
    },
    {
      '0/output.json': GOOD_GTEST_JSON_0,
      '1/output.json': GOOD_GTEST_JSON_1,
    })
    old_json_limit = standard_gtest_merge.OUTPUT_JSON_SIZE_LIMIT
    len0 = len(json.dumps(GOOD_GTEST_JSON_0))
    len1 = len(json.dumps(GOOD_GTEST_JSON_1))
    large_shard = "0" if len0 > len1 else "1"
    try:
      # Override max output.json size just for this test.
      standard_gtest_merge.OUTPUT_JSON_SIZE_LIMIT = min(len0,len1)
      merged, stdout = self.call(1)
      merged.pop('swarming_summary')
      self.assertEqual(BAD_GTEST_JSON_ONLY_1_SHARD, merged)
      self.assertIn(
          '@@@STEP_WARNINGS@@@\nTask ran but no result was found: '
          'shard %s test output exceeded the size limit' % large_shard, stdout)
    finally:
      standard_gtest_merge.OUTPUT_JSON_SIZE_LIMIT = old_json_limit


if __name__ == '__main__':
  logging.basicConfig(
      level=logging.DEBUG if '-v' in sys.argv else logging.ERROR)
  if '-v' in sys.argv:
    unittest.TestCase.maxDiff = None
  unittest.main()
