# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import collections

from . import steps


_builders = collections.defaultdict(dict)


SPEC = {
  'builders': {},
  'settings': {
    'build_gs_bucket': 'chrome-perf',
    # Bucket for storing builds for manual bisect
    'bisect_build_gs_bucket': 'chrome-test-builds',
    'bisect_build_gs_extra': 'official-by-commit',
    'bisect_builders': []
  },
}


def _BaseSpec(bot_type, config_name, disable_tests,
              platform, target_bits, tests):
  spec = {
    'bot_type': bot_type,
    'chromium_config': config_name,
    'chromium_config_kwargs': {
      'BUILD_CONFIG': 'Release',
      'TARGET_BITS': target_bits,
    },
    'disable_tests': disable_tests,
    'gclient_config': config_name,
    'testing': {
      'platform': 'linux' if platform == 'android' else platform,
    },
    'tests': tests,
  }

  if platform == 'android':
    spec['android_config'] = 'chromium_perf'
    spec['chromium_apply_config'] = ['android']
    spec['chromium_config_kwargs']['TARGET_ARCH'] = 'arm'
    spec['chromium_config_kwargs']['TARGET_PLATFORM'] = 'android'
    spec['gclient_apply_config'] = ['android']

  return spec


def BuildSpec(config_name, perf_id, platform, target_bits):
  if platform == 'android':
    # TODO: Run sizes on Android.
    tests = []
  else:
    tests = [steps.SizesStep('https://chromeperf.appspot.com', perf_id)]

  spec = _BaseSpec(
      bot_type='builder',
      config_name=config_name,
      disable_tests=True,
      platform=platform,
      target_bits=target_bits,
      tests=tests,
  )

  spec['compile_targets'] = ['chromium_builder_perf']

  return spec


def _TestSpec(config_name, parent_builder, perf_id, platform, target_bits,
              max_battery_temp, shard_index, num_host_shards,
              num_device_shards):
  spec = _BaseSpec(
      bot_type='tester',
      config_name=config_name,
      disable_tests=platform == 'android',
      platform=platform,
      target_bits=target_bits,
      tests=[steps.DynamicPerfTests(
        perf_id, platform, target_bits, max_battery_temp=max_battery_temp,
        num_device_shards=num_device_shards, num_host_shards=num_host_shards,
        shard_index=shard_index)],
  )

  spec['parent_buildername'] = parent_builder
  spec['perf-id'] = perf_id
  spec['results-url'] = 'https://chromeperf.appspot.com'

  if platform != 'android':
    # TODO: Remove disable_tests and run test_generators on Android.
    spec['test_generators'] = [steps.generate_script]
    spec['test_spec_file'] = 'chromium.perf.json'

  return spec


def _AddBuildSpec(name, platform, target_bits=64, add_to_bisect=False):
  if target_bits == 64:
    perf_id = platform
  else:
    perf_id = '%s-%d' % (platform, target_bits)

  SPEC['builders'][name] = BuildSpec(
      'chromium_perf', perf_id, platform, target_bits)
  assert target_bits not in _builders[platform]
  _builders[platform][target_bits] = name
  if add_to_bisect:
    SPEC['settings']['bisect_builders'].append(name)


def _AddTestSpec(name, perf_id, platform, target_bits=64,
                 max_battery_temp=350, num_host_shards=1, num_device_shards=1):
  parent_builder = _builders[platform][target_bits]
  for shard_index in xrange(num_host_shards):
    builder_name = '%s (%d)' % (name, shard_index + 1)
    SPEC['builders'][builder_name] = _TestSpec(
        'chromium_perf', parent_builder, perf_id, platform, target_bits,
        max_battery_temp, shard_index, num_host_shards, num_device_shards)


_AddBuildSpec('Android Builder', 'android', target_bits=32)
_AddBuildSpec('Android arm64 Builder', 'android')
_AddBuildSpec('Win Builder', 'win', target_bits=32)
_AddBuildSpec('Win x64 Builder', 'win')
_AddBuildSpec('Mac Builder', 'mac')
_AddBuildSpec('Linux Builder', 'linux', add_to_bisect=True)


_AddTestSpec('Android Galaxy S5 Perf', 'android-galaxy-s5', 'android',
             target_bits=32, num_device_shards=7, num_host_shards=3)
_AddTestSpec('Android Nexus5 Perf', 'android-nexus5', 'android',
             target_bits=32, num_device_shards=7, num_host_shards=3)
_AddTestSpec('Android Nexus5X Perf', 'android-nexus5X', 'android',
             target_bits=32, num_device_shards=7, num_host_shards=3)
_AddTestSpec('Android Nexus6 Perf', 'android-nexus6', 'android',
             target_bits=32, num_device_shards=7, num_host_shards=3)
_AddTestSpec('Android Nexus7v2 Perf', 'android-nexus7v2', 'android',
             target_bits=32, num_device_shards=7, num_host_shards=3)
_AddTestSpec('Android Nexus9 Perf', 'android-nexus9', 'android',
             num_device_shards=7, num_host_shards=3)
_AddTestSpec('Android One Perf', 'android-one', 'android',
             target_bits=32, num_device_shards=7, num_host_shards=3)


_AddTestSpec('Win Zenbook Perf', 'win-zenbook', 'win',
             num_host_shards=5)
_AddTestSpec('Win 10 Perf', 'chromium-rel-win10', 'win',
             num_host_shards=5)
_AddTestSpec('Win 8 Perf', 'chromium-rel-win8-dual', 'win',
             num_host_shards=5)
_AddTestSpec('Win 7 Perf', 'chromium-rel-win7-dual', 'win',
             target_bits=32, num_host_shards=5)
_AddTestSpec('Win 7 x64 Perf', 'chromium-rel-win7-x64-dual', 'win',
             num_host_shards=5)
_AddTestSpec('Win 7 ATI GPU Perf', 'chromium-rel-win7-gpu-ati', 'win',
             num_host_shards=5)
_AddTestSpec('Win 7 Intel GPU Perf', 'chromium-rel-win7-gpu-intel', 'win',
             num_host_shards=5)
_AddTestSpec('Win 7 Nvidia GPU Perf', 'chromium-rel-win7-gpu-nvidia', 'win',
             num_host_shards=5)


_AddTestSpec('Mac 10.11 Perf', 'chromium-rel-mac11', 'mac',
             num_host_shards=5)
_AddTestSpec('Mac 10.10 Perf', 'chromium-rel-mac10', 'mac',
             num_host_shards=5)
_AddTestSpec('Mac Retina Perf', 'chromium-rel-mac-retina', 'mac',
             num_host_shards=5)
_AddTestSpec('Mac HDD Perf', 'chromium-rel-mac-hdd', 'mac',
             num_host_shards=5)


_AddTestSpec('Linux Perf', 'linux-release', 'linux',
             num_host_shards=5)
