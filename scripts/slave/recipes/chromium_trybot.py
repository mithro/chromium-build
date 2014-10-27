# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

DEPS = [
  'bot_update',
  'chromium',
  'chromium_tests',
  'gclient',
  'isolate',
  'itertools',
  'json',
  'path',
  'platform',
  'properties',
  'python',
  'raw_io',
  'step',
  'swarming',
  'test_utils',
  'tryserver',
]


BUILDERS = {
  'tryserver.chromium.linux': {
    'builders': {
      'linux_arm': {
        'GYP_DEFINES': {
          'arm_float_abi': 'hard',
          'test_isolation_mode': 'archive',
        },
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': True,
        'exclude_compile_all': True,
        'testing': {
          'platform': 'linux',
          'test_spec_file': 'chromium_arm.json',
        },
        'use_isolate': True,
      },
      'linux_arm_compile': {
        'GYP_DEFINES': {
          'arm_float_abi': 'hard',
          'test_isolation_mode': 'archive',
        },
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': True,
        'exclude_compile_all': True,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_dbg': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_rel': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'enable_swarming': True,
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_rel_ng': {
        'based_on_main_waterfall': {
          'mastername': 'chromium.linux',
          'buildername': 'Linux Builder',
          'testers': ['Linux Tests'],
        },
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_asan_rel': {
        'add_telemetry_tests': False,
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'enable_swarming': True,
        'exclude_compile_all': True,
        'chromium_config': 'chromium_linux_asan',
        'compile_only': False,
        'testing': {
          'platform': 'linux',
          'test_spec_file': 'chromium_memory_trybot.json',
        },
      },
      # Fake builder to provide testing coverage for non-bot_update.
      'linux_no_bot_update': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_compile_dbg': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium',
        'compile_only': True,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_compile_rel': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium',
        'compile_only': True,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_clang_dbg': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium_clang',
        'compile_only': True,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_clang_rel': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium_clang',
        'compile_only': True,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_chromeos_dbg': {
        'add_telemetry_tests': False,
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium_chromeos',
        'compile_only': False,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_chromeos_rel': {
        'add_telemetry_tests': False,
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'enable_swarming': True,
        'chromium_config': 'chromium_chromeos',
        'compile_only': False,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_chromeos_clang_dbg': {
        'add_telemetry_tests': False,
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium_chromeos_clang',
        'compile_only': True,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_chromeos_clang_rel': {
        'add_telemetry_tests': False,
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium_chromeos_clang',
        'compile_only': True,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_chromeos_ozone_rel': {
        'add_telemetry_tests': False,
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium_chromeos_ozone',
        'compile_only': False,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_chromeos_ozone_dbg': {
        'add_telemetry_tests': False,
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium_chromeos_ozone',
        'compile_only': False,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_chromeos_athena_rel': {
        'add_nacl_integration_tests': False,
        'add_telemetry_tests': False,
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium_chromeos_athena',
        'compile_only': False,
        'compile_targets': [
          'chrome',
        ],
        'testing': {
          'platform': 'linux',
          'test_spec_file': 'chromium_athena.json',
        },
      },
      'linux_chromium_chromeos_athena_dbg': {
        'add_nacl_integration_tests': False,
        'add_telemetry_tests': False,
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium_chromeos_athena',
        'compile_only': False,
        'compile_targets': [
          'chrome',
        ],
        'testing': {
          'platform': 'linux',
          'test_spec_file': 'chromium_athena.json',
        },
      },
      'linux_chromium_trusty_dbg': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_trusty_rel': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_trusty32_dbg': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_trusty32_rel': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'linux',
        },
      },
      'linux_chromium_compile_dbg_32': {
         'chromium_config_kwargs': {
           'BUILD_CONFIG': 'Debug',
           'TARGET_BITS': 32,
         },
         'chromium_config': 'chromium',
         'compile_only': True,
         'testing': {
           'platform': 'linux',
         },
       },
    },
  },
  'tryserver.chromium.mac': {
    'builders': {
      'mac_chromium_dbg': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'mac',
        },
      },
      'mac_chromium_rel': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'enable_swarming': True,
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'mac',
        },
      },
      'mac_chromium_rel_ng': {
        'based_on_main_waterfall': {
          'mastername': 'chromium.mac',
          'buildername': 'Mac Builder',
          'testers': ['Mac10.7 Tests (1)'],
        },
        'testing': {
          'platform': 'mac',
        },
      },
      'mac_chromium_compile_dbg': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': True,
        'testing': {
          'platform': 'mac',
        },
      },
      'mac_chromium_compile_rel': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': True,
        'testing': {
          'platform': 'mac',
        },
      },
      'mac_chromium_openssl_dbg': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'GYP_DEFINES': {
          'use_openssl': '1',
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'mac',
        },
      },
      'mac_chromium_openssl_rel': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'GYP_DEFINES': {
          'use_openssl': '1',
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'mac',
        },
      },
    },
  },
  'tryserver.chromium.win': {
    'builders': {
      'win_chromium_dbg': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'win',
        },
      },
      'win_chromium_rel': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'enable_swarming': True,
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'win',
        },
      },
      'win_chromium_rel_ng': {
        'based_on_main_waterfall': {
          'mastername': 'chromium.win',
          'buildername': 'Win Builder',
          'testers': [
            'Win7 Tests (1)',
          ],
        },
        'testing': {
          'platform': 'win',
        },
      },
      'win_chromium_compile_dbg': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': True,
        'testing': {
          'platform': 'win',
        },
      },
      'win_chromium_compile_rel': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': True,
        'testing': {
          'platform': 'win',
        },
      },
      'win_chromium_x64_dbg': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'win',
        },
      },
      'win_chromium_x64_rel': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'enable_swarming': True,
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'win',
        },
      },
      'win_chromium_x64_rel_ng': {
        'based_on_main_waterfall': {
          'mastername': 'chromium.win',
          'buildername': 'Win x64 Builder',
          'testers': [
            'Win 7 Tests x64 (1)',
          ],
        },
        'testing': {
          'platform': 'win',
        },
      },
      'win8_chromium_dbg': {
        'add_telemetry_tests': False,
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'win',
          'test_spec_file': 'chromium_win8_trybot.json',
        },
        'swarming_dimensions': {
          'os': 'Windows-6.2',
        },
      },
      'win8_chromium_rel': {
        'add_telemetry_tests': False,
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'win',
          'test_spec_file': 'chromium_win8_trybot.json',
        },
        'swarming_dimensions': {
          'os': 'Windows-6.2',
        },
      },
      # Fake builder to provide testing coverage for non-bot_update.
      'win_no_bot_update': {
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'chromium_config': 'chromium',
        'compile_only': False,
        'testing': {
          'platform': 'win',
        },
      },
    },
  },
}


def get_test_names(tests):
  """Returns the names of each of the tests in |tests|."""
  return [test.name for test in tests]


def filter_tests(possible_tests, needed_tests):
  """Returns a list of all the tests in |possible_tests| whose name is in
  |needed_tests|."""
  result = []
  for test in possible_tests:
    if test.name in needed_tests:
      result.append(test)
  return result


def tests_in_compile_targets(api, compile_targets, tests):
  """Returns the tests in |tests| that have at least one of their compile
  targets in |compile_targets|."""
  # The target all builds everything.
  if 'all' in compile_targets:
    return tests

  result = []
  for test in tests:
    test_compile_targets = test.compile_targets(api)

    # Always return tests that don't require compile. Otherwise we'd never
    # run them.
    if ((set(compile_targets).intersection(set(test_compile_targets))) or
        not test_compile_targets):
      result.append(test)

  return result


def all_compile_targets(api, tests):
  """Returns the compile_targets for all the Tests in |tests|."""
  return sorted(set(x
                    for test in tests
                    for x in test.compile_targets(api)))


def find_test_named(test_name, tests):
  """Returns a list with all tests whose name matches |test_name|."""
  return [test for test in tests if test.name == test_name]


def build_to_priority(build_properties):
  """Returns the Swarming task priority for the build.

  Does this by determining the build type. Lower is higher priority.
  """
  requester = build_properties.get('requester')
  if requester == 'commit-bot@chromium.org':
    # Commit queue job.
    return 30
  # Normal try job.
  return 50


def GenSteps(api):
  def swarming_shards_from_test_spec(test_spec, test_name):
    if isinstance(test_spec, dict):
      gtest_tests_spec = test_spec.get('gtest_tests', [])
    else:
      # TODO(phajdan.jr): Convert test step data and remove this.
      gtest_tests_spec = test_spec

    for test in gtest_tests_spec:
      if not isinstance(test, dict):
        continue

      if test['test'] == test_name:
        swarming_spec = test.get('swarming', {})
        if not swarming_spec.get('can_use_on_swarming_builders'):
          continue
        return (True, swarming_spec.get('shards', 1))

    return (False, -1)

  def parse_test_spec(test_spec, enable_swarming, should_use_test):
    """Returns a list of tests to run and additional targets to compile.

    Uses 'should_use_test' callback to figure out what tests should be skipped.

    Returns tuple (compile_targets, gtest_tests) where
      gtest_tests is a list of GTestTest
    """
    compile_targets = []
    gtest_tests_spec = []
    if isinstance(test_spec, dict):
      compile_targets = test_spec.get('compile_targets', [])
      gtest_tests_spec = test_spec.get('gtest_tests', [])
    else:
      # TODO(phajdan.jr): Convert test step data and remove this.
      gtest_tests_spec = test_spec

    gtest_tests = []
    for test in gtest_tests_spec:
      test_name = None
      test_dict = None

      # Read test_dict for the test, it defines where test can run.
      if isinstance(test, unicode):
        test_name = test.encode('utf-8')
        test_dict = {}
      elif isinstance(test, dict):
        if 'test' not in test:  # pragma: no cover
          raise ValueError('Invalid entry in test spec: %r' % test)
        test_name = test['test'].encode('utf-8')
        test_dict = test
      else:  # pragma: no cover
        raise ValueError('Unrecognized entry in test spec: %r' % test)

      # Should skip it completely?
      if not test_name or not should_use_test(test_dict):
        continue

      # If test can run on swarming, test_dict has a section that defines when
      # swarming should be used, in same format as main test dict.
      use_swarming = False
      swarming_shards = 1
      if enable_swarming:
        use_swarming, swarming_shards = swarming_shards_from_test_spec(
            test_spec, test_name)

      test_args = test_dict.get('args')
      if isinstance(test_args, basestring):
        test_args = [test_args]

      if use_swarming:
        test = api.chromium.steps.GTestTest(
            test_name, test_args, enable_swarming=True,
            swarming_shards=swarming_shards)
        assert test.uses_swarming
      else:
        test = api.chromium.steps.GTestTest(test_name, test_args)
        assert not test.uses_swarming

      gtest_tests.append(test)

    return compile_targets, gtest_tests

  def get_bot_config(mastername, buildername):
    master_dict = BUILDERS.get(mastername, {})
    return master_dict.get('builders', {}).get(buildername)

  def get_test_spec(mastername, buildername, name='read test spec',
                    step_test_data=None):
    bot_config = get_bot_config(mastername, buildername)

    test_spec_file = bot_config['testing'].get('test_spec_file',
                                               'chromium_trybot.json')
    test_spec_path = api.path.join('testing', 'buildbot', test_spec_file)
    if not step_test_data:
      step_test_data = lambda: api.json.test_api.output([
        'base_unittests',
        {
          'test': 'mojo_common_unittests',
          'platforms': ['linux', 'mac'],
        },
        {
          'test': 'sandbox_linux_unittests',
          'platforms': ['linux'],
          'chromium_configs': [
            'chromium_chromeos',
            'chromium_chromeos_clang',
            'chromium_chromeos_ozone',
          ],
          'args': ['--test-launcher-print-test-stdio=always'],
        },
        {
          'test': 'browser_tests',
          'exclude_builders': ['tryserver.chromium.win:win_chromium_x64_rel'],
        },
      ])
    step_result = api.json.read(
        name,
        api.path['checkout'].join(test_spec_path),
        step_test_data=step_test_data
    )
    step_result.presentation.step_text = 'path: %s' % test_spec_path
    return step_result.json.output

  def compile_and_return_tests(mastername, buildername):
    bot_config = get_bot_config(mastername, buildername)
    assert bot_config, (
        'Unrecognized builder name %r for master %r.' % (
            buildername, mastername))

    # Make sure tests and the recipe specify correct and matching platform.
    assert api.platform.name == bot_config.get('testing', {}).get('platform')

    api.chromium.set_config(bot_config['chromium_config'],
                            **bot_config.get('chromium_config_kwargs', {}))
    # Settings GYP_DEFINES explicitly because chromium config constructor does
    # not support that.
    api.chromium.c.gyp_env.GYP_DEFINES.update(bot_config.get('GYP_DEFINES', {}))
    if bot_config['compile_only']:
      api.chromium.c.gyp_env.GYP_DEFINES['fastbuild'] = 2
    api.chromium.apply_config('trybot_flavor')
    api.gclient.set_config('chromium')
    api.step.auto_resolve_conflicts = True

    bot_update_step = api.bot_update.ensure_checkout(force=True)

    test_spec = get_test_spec(mastername, buildername)

    def should_use_test(test):
      """Given a test dict from test spec returns True or False."""
      if 'platforms' in test:
        if api.platform.name not in test['platforms']:
          return False
      if 'chromium_configs' in test:
        if bot_config['chromium_config'] not in test['chromium_configs']:
          return False
      if 'exclude_builders' in test:
        if '%s:%s' % (mastername, buildername) in test['exclude_builders']:
          return False
      return True

    # Parse test spec file into list of Test instances.
    compile_targets, gtest_tests = parse_test_spec(
        test_spec,
        bot_config.get('enable_swarming'),
        should_use_test)
    compile_targets.extend(bot_config.get('compile_targets', []))
    # TODO(phajdan.jr): Also compile 'all' on win, http://crbug.com/368831 .
    # Disabled for now because it takes too long and/or fails on Windows.
    if not api.platform.is_win and not bot_config.get('exclude_compile_all'):
      compile_targets = ['all'] + compile_targets

    scripts_compile_targets = \
        api.chromium.get_compile_targets_for_scripts().json.output

    # Tests that are only run if their compile_targets are going to be built.
    conditional_tests = []
    if bot_config.get('add_nacl_integration_tests', True):
      conditional_tests += [api.chromium.steps.NaclIntegrationTest()]
    if bot_config.get('add_telemetry_tests', True):
      conditional_tests += [
          api.chromium.steps.ScriptTest(
              'telemetry_unittests', 'telemetry_unittests.py',
              scripts_compile_targets),
          api.chromium.steps.TelemetryPerfUnitTests()
      ]

    # See if the patch needs to compile on the current platform.
    # Don't run analyze for other projects, such as blink, as there aren't that
    # many try jobs for them.
    requires_compile = True
    if isinstance(test_spec, dict) and api.properties.get('root') == 'src':
      analyze_config_file = bot_config['testing'].get('analyze_config_file',
                                         'trybot_analyze_config.json')
      requires_compile, matching_exes, compile_targets = \
          api.chromium_tests.analyze(
              get_test_names(gtest_tests) +
                  all_compile_targets(api, conditional_tests),
              compile_targets,
              analyze_config_file)

      gtest_tests = filter_tests(gtest_tests, matching_exes)

    tests = []
    # TODO(phajdan.jr): Re-enable checkdeps on Windows when it works with git.
    if not api.platform.is_win:
      tests.append(api.chromium.steps.ScriptTest(
          'checkdeps', 'checkdeps.py', scripts_compile_targets))
    if api.platform.is_linux:
      tests.extend([
          api.chromium.steps.CheckpermsTest(),
          api.chromium.steps.ChecklicensesTest(),
      ])

    conditional_tests = tests_in_compile_targets(
        api, compile_targets, conditional_tests)
    tests.extend(find_test_named('telemetry_unittests', conditional_tests))
    tests.extend(find_test_named(api.chromium.steps.TelemetryPerfUnitTests.name,
                                 conditional_tests))
    tests.extend(gtest_tests)
    tests.extend(find_test_named(api.chromium.steps.NaclIntegrationTest.name,
                                 conditional_tests))

    if api.platform.is_win:
      tests.append(api.chromium.steps.MiniInstallerTest())

    if not requires_compile:
      # Even though the patch doesn't require compile, we'd still like to
      # run tests not depending on compiled targets (that's obviously not
      # covered by the "analyze" step).
      tests = [t for t in tests if not t.compile_targets(api)]
      return tests, bot_update_step

    has_swarming_tests = any(t.uses_swarming for t in tests)

    # Swarming uses Isolate to transfer files to swarming bots.
    # set_isolate_environment modifies GYP_DEFINES to enable test isolation.
    if bot_config.get('use_isolate') or has_swarming_tests:
      api.isolate.set_isolate_environment(api.chromium.c)

    # If going to use swarming_client (pinned in src/DEPS), ensure it is
    # compatible with what recipes expect.
    if has_swarming_tests:
      api.swarming.check_client_version()

    try:
      api.chromium.runhooks(name='runhooks (with patch)')
    except api.step.StepFailure:
      # As part of deapplying patch we call runhooks without the patch.
      api.chromium_tests.deapply_patch(bot_update_step)
      raise

    if bot_config.get('use_isolate') or has_swarming_tests:
      api.isolate.clean_isolated_files(api.chromium.output_dir)

    compile_targets.extend(api.itertools.chain(
        *[t.compile_targets(api) for t in tests]))
    # Remove duplicate targets.
    compile_targets = sorted(set(compile_targets))
    try:
      api.chromium.compile(compile_targets, name='compile (with patch)')
    except api.step.StepFailure:
      api.chromium_tests.deapply_patch(bot_update_step)
      try:
        api.chromium.compile(
            compile_targets, name='compile (without patch)')

        # TODO(phajdan.jr): Set failed tryjob result after recognizing infra
        # compile failures. We've seen cases of compile with patch failing
        # with build steps getting killed, compile without patch succeeding,
        # and compile with patch succeeding on another attempt with same patch.
      except api.step.StepFailure:
        api.tryserver.set_transient_failure_tryjob_result()
        raise
      raise

    # Collect *.isolated hashes for all isolated targets, used when triggering
    # tests on swarming.
    if bot_config.get('use_isolate') or has_swarming_tests:
      api.isolate.find_isolated_tests(api.chromium.output_dir)

    if bot_config['compile_only']:
      tests = []

    return tests, bot_update_step

  mastername = api.properties.get('mastername')
  buildername = api.properties.get('buildername')
  bot_config = get_bot_config(mastername, buildername)
  api.swarming.set_default_dimension('pool', 'Chrome')
  api.swarming.default_priority = build_to_priority(api.properties)
  api.swarming.add_default_tag('project:chromium')
  api.swarming.add_default_tag('purpose:pre-commit')
  api.swarming.default_idempotent = True

  # Differentiate between try jobs and CQ jobs. Always find out who made the CL.
  requestor = api.properties.get('requestor')
  if requestor == 'commit-bot@chromium.org':
    api.swarming.add_default_tag('purpose:CQ')
    blamelist = api.properties.get('blamelist')
    if len(blamelist) == 1:
      requestor = blamelist[0]
  else:
    api.swarming.add_default_tag('purpose:ManualTS')
  api.swarming.default_user = requestor

  # TODO(phajdan): uncomment once we have XP or 10.6 trybots.
  #os_dimension = bot_config.get('swarming_dimensions', {}).get('os')
  #if os_dimension:
  #  api.swarming.set_default_dimension('os', os_dimension)

  main_waterfall_config = bot_config.get('based_on_main_waterfall')
  if main_waterfall_config:
    bot_update_step, master_dict, test_spec = \
        api.chromium_tests.sync_and_configure_build(
            main_waterfall_config['mastername'],
            main_waterfall_config['buildername'],
            override_bot_type='builder_tester',
            enable_swarming=True)

    tests = api.chromium_tests.tests_for_builder(
        main_waterfall_config['mastername'],
        main_waterfall_config['buildername'],
        bot_update_step,
        master_dict,
        override_bot_type='builder_tester')
    for tester in main_waterfall_config['testers']:
      tests.extend(api.chromium_tests.tests_for_builder(
          main_waterfall_config['mastername'],
          tester,
          bot_update_step,
          master_dict,
          override_bot_type='builder_tester'))

    trybot_test_spec = get_test_spec(
        mastername,
        buildername,
        name='read trybot test spec',
        step_test_data=lambda: api.json.test_api.output([
            {
              'test': 'base_unittests',
              'swarming': {
                'can_use_on_swarming_builders': True,
                'shards': 5,
              },
            },
        ]))
    for test in tests:
      use_swarming, swarming_shards = swarming_shards_from_test_spec(
          trybot_test_spec, test.name)
      if use_swarming:
        test.force_swarming(swarming_shards)

    compile_targets, tests_including_triggered = \
        api.chromium_tests.get_compile_targets_and_tests(
            main_waterfall_config['mastername'],
            main_waterfall_config['buildername'],
            master_dict,
            override_bot_type='builder_tester',
            override_tests=tests)

    requires_compile, _, compile_targets = \
        api.chromium_tests.analyze(
            all_compile_targets(api, tests + tests_including_triggered),
            compile_targets,
            'trybot_analyze_config.json')

    if requires_compile:
      tests = tests_in_compile_targets(api, compile_targets, tests)
      tests_including_triggered = tests_in_compile_targets(
          api, compile_targets, tests_including_triggered)

      api.chromium_tests.compile_specific_targets(
          main_waterfall_config['mastername'],
          main_waterfall_config['buildername'],
          bot_update_step,
          master_dict,
          test_spec,
          compile_targets,
          tests_including_triggered,
          override_bot_type='builder_tester')
    else:
      # Even though the patch doesn't require compile, we'd still like to
      # run tests not depending on compiled targets (that's obviously not
      # covered by the "analyze" step).
      tests = [t for t in tests if not t.compile_targets(api)]

  else:
    # TODO(phajdan.jr): Remove the legacy trybot-specific codepath.
    tests, bot_update_step = compile_and_return_tests(
        mastername, buildername)

  def deapply_patch_fn(failing_tests):
    api.chromium_tests.deapply_patch(bot_update_step)
    compile_targets = list(api.itertools.chain(
        *[t.compile_targets(api) for t in failing_tests]))
    if compile_targets:
      # Remove duplicate targets.
      compile_targets = sorted(set(compile_targets))
      # Search for *.isolated only if enabled in bot config or if some
      # swarming test is being recompiled.
      bot_config = get_bot_config(mastername, buildername)
      has_failing_swarming_tests = [
          t for t in failing_tests if t.uses_swarming]
      if bot_config.get('use_isolate') or has_failing_swarming_tests:
        api.isolate.clean_isolated_files(api.chromium.output_dir)
      try:
        api.chromium.compile(
            compile_targets, name='compile (without patch)')
      except api.step.StepFailure:
        api.tryserver.set_transient_failure_tryjob_result()
        raise
      if bot_config.get('use_isolate') or has_failing_swarming_tests:
        api.isolate.find_isolated_tests(api.chromium.output_dir)

  return api.test_utils.determine_new_failures(api, tests, deapply_patch_fn)


def _sanitize_nonalpha(text):
  return ''.join(c if c.isalnum() else '_' for c in text)


def GenTests(api):
  canned_checkdeps = {
    True: {'valid': True, 'failures': []},
    False: {'valid': True, 'failures': ['foo: bar']},
  }
  canned_test = api.json.canned_gtest_output
  def props(config='Release', mastername='tryserver.chromium.linux',
            buildername='linux_chromium_rel', **kwargs):
    kwargs.setdefault('revision', None)
    return api.properties.tryserver(
      build_config=config,
      mastername=mastername,
      buildername=buildername,
      **kwargs
    )

  # While not strictly required for coverage, record expectations for each
  # of the configs so we can see when and how they change.
  for mastername, master_config in BUILDERS.iteritems():
    for buildername, bot_config in master_config['builders'].iteritems():
      test_name = 'full_%s_%s' % (_sanitize_nonalpha(mastername),
                                  _sanitize_nonalpha(buildername))
      yield (
        api.test(test_name) +
        api.platform(bot_config['testing']['platform'],
                     bot_config.get(
                         'chromium_config_kwargs', {}).get('TARGET_BITS', 64)) +
        props(mastername=mastername, buildername=buildername)
      )

  yield (
    api.test('force_swarming') +
    api.platform('linux', 64) +
    api.properties.generic(mastername='tryserver.chromium.linux',
                           buildername='linux_chromium_rel_ng') +
    api.override_step_data('read test spec', api.json.output({
        'Linux Tests': {
          'gtest_tests': [
            'base_unittests',
          ],
        },
      })
    )
  )

  # It is important that even when steps related to deapplying the patch
  # fail, we either print the summary for all retried steps or do no
  # retries at all.
  yield (
    api.test('persistent_failure_and_runhooks_2_fail_test') +
    props(buildername='win_chromium_rel', mastername='tryserver.chromium.win') +
    api.platform.name('win') +
    api.override_step_data('base_unittests (with patch)',
                           canned_test(passing=False)) +
    api.override_step_data('base_unittests (without patch)',
                           canned_test(passing=False)) +
    api.step_data('gclient runhooks (without patch)', retcode=1)
  )

  yield (
    api.test('invalid_json_without_patch') +
    props(buildername='linux_chromium_rel') +
    api.platform.name('linux') +
    api.override_step_data('checkdeps (with patch)',
                           api.json.output(canned_checkdeps[False])) +
    api.override_step_data('checkdeps (without patch)',
                           api.json.output(None))
  )

  for step in ('bot_update', 'gclient runhooks (with patch)'):
    yield (
      api.test(_sanitize_nonalpha(step) + '_failure') +
      props(buildername='win_no_bot_update',
            mastername='tryserver.chromium.win') +
      api.platform.name('win') +
      api.step_data(step, retcode=1)
    )

  yield (
    api.test('runhooks_failure') +
    props(buildername='win_chromium_rel',
          mastername='tryserver.chromium.win') +
    api.platform.name('win') +
    api.step_data('gclient runhooks (with patch)', retcode=1) +
    api.step_data('gclient runhooks (without patch)', retcode=1)
  )

  yield (
    api.test('runhooks_failure_ng') +
    api.platform('linux', 64) +
    props(mastername='tryserver.chromium.linux',
          buildername='linux_chromium_rel_ng') +
    api.step_data('gclient runhooks (with patch)', retcode=1)
  )

  yield (
    api.test('compile_failure') +
    props(buildername='win_chromium_rel',
          mastername='tryserver.chromium.win') +
    api.platform.name('win') +
    api.step_data('compile (with patch)', retcode=1)
  )

  yield (
    api.test('compile_failure_without_patch') +
    props(buildername='win_chromium_rel',
          mastername='tryserver.chromium.win') +
    api.platform.name('win') +
    api.step_data('compile (with patch)', retcode=1) +
    api.step_data('compile (without patch)', retcode=1)
  )

  yield (
    api.test('deapply_compile_failure_linux') +
    props(buildername='linux_no_bot_update') +
    api.platform.name('linux') +
    api.override_step_data('base_unittests (with patch)',
                           canned_test(passing=False)) +
    api.step_data('compile (without patch)', retcode=1)
  )

  yield (
    api.test('compile_failure_ng') +
    api.platform('linux', 64) +
    props(mastername='tryserver.chromium.linux',
          buildername='linux_chromium_rel_ng') +
    api.override_step_data('read filter exclusion spec', api.json.output({
        'base': {
          'exclusions': ['f.*'],
        },
        'chromium': {
          'exclusions': [],
        },
     })) +
    api.step_data('compile (with patch)', retcode=1)
  )

  yield (
    api.test('compile_failure_without_patch_ng') +
    api.platform('linux', 64) +
    props(mastername='tryserver.chromium.linux',
          buildername='linux_chromium_rel_ng') +
    api.override_step_data('read filter exclusion spec', api.json.output({
        'base': {
          'exclusions': ['f.*'],
        },
        'chromium': {
          'exclusions': [],
        },
     })) +
    api.step_data('compile (with patch)', retcode=1) +
    api.step_data('compile (without patch)', retcode=1)
  )

  yield (
    api.test('arm') +
    api.properties.generic(
        mastername='tryserver.chromium.linux',
        buildername='linux_arm',
        requestor='commit-bot@chromium.org',
        blamelist='joe@chromium.org',
        blamelist_real=['joe@chromium.org']) +
    api.platform('linux', 64) +
    api.override_step_data('read test spec', api.json.output({
        'compile_targets': ['browser_tests_run'],
        'gtest_tests': [
          {
            'test': 'browser_tests',
            'args': '--gtest-filter: *NaCl*.*',
          }, {
            'test': 'base_tests',
            'args': ['--gtest-filter: *NaCl*.*'],
          },
        ],
      })
    )
  )

  yield (
    api.test('checkperms_failure') +
    props() +
    api.platform.name('linux') +
    api.override_step_data(
        'checkperms (with patch)',
        api.json.output([
            {
                'error': 'Must not have executable bit set',
                'rel_path': 'base/basictypes.h',
            },
        ]))
  )

  yield (
    api.test('check_swarming_version_failure') +
    props(buildername='linux_chromium_rel') +
    api.platform.name('linux') +
    api.step_data('swarming.py --version', retcode=1) +
    api.override_step_data('read test spec', api.json.output({
        'gtest_tests': [
          {
            'test': 'base_unittests',
            'swarming': {'can_use_on_swarming_builders': True},
          },
        ],
      })
      ) +
    api.override_step_data('read filter exclusion spec', api.json.output({
        'base': {
          'exclusions': ['f.*'],
        },
        'chromium': {
          'exclusions': [],
        },
     }))
  )

  yield (
    api.test('checklicenses_failure') +
    props() +
    api.platform.name('linux') +
    api.override_step_data('checklicenses', retcode=1) +
    api.override_step_data(
        'checklicenses (with patch)',
        api.json.output([
            {
                'filename': 'base/basictypes.h',
                'license': 'UNKNOWN',
            },
        ]))
  )

  # Successfully compiling, isolating and running two targets on swarming for a
  # commit queue job.
  yield (
    api.test('swarming_basic_cq') +
    props(buildername='linux_chromium_rel') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({
        'gtest_tests': [
          {
            'test': 'base_unittests',
            'swarming': {'can_use_on_swarming_builders': True},
          },
          {
            'test': 'browser_tests',
            'swarming': {
              'can_use_on_swarming_builders': True,
              'shards': 5,
              'platforms': ['linux'],
            },
          },
        ],
      })
    ) +
    api.override_step_data('read filter exclusion spec', api.json.output({
        'base': {
          'exclusions': ['f.*'],
        },
        'chromium': {
          'exclusions': [],
        },
     })) +
    api.override_step_data(
        'find isolated tests',
        api.isolate.output_json(['base_unittests', 'browser_tests']))
  )

  # Successfully compiling, isolating and running two targets on swarming for a
  # manual try job.
  yield (
    api.test('swarming_basic_try_job') +
    props(
        buildername='linux_chromium_rel',
        requester='joe@chromium.org') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({
        'gtest_tests': [
          {
            'test': 'base_unittests',
            'swarming': {'can_use_on_swarming_builders': True},
          },
          {
            'test': 'browser_tests',
            'swarming': {
              'can_use_on_swarming_builders': True,
              'shards': 5,
              'platforms': ['linux'],
            },
          },
        ],
      })
    ) +
    api.override_step_data('read filter exclusion spec', api.json.output({
        'base': {
          'exclusions': ['f.*'],
        },
        'chromium': {
          'exclusions': [],
        },
     })) +
    api.override_step_data(
        'find isolated tests',
        api.isolate.output_json(['base_unittests', 'browser_tests']))
  )

  # One target (browser_tests) failed to produce *.isolated file.
  yield (
    api.test('swarming_missing_isolated') +
    props(buildername='linux_chromium_rel') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({
        'gtest_tests': [
          {
            'test': 'base_unittests',
            'swarming': {'can_use_on_swarming_builders': True},
          },
          {
            'test': 'browser_tests',
            'swarming': {'can_use_on_swarming_builders': True},
          },
        ],
      })
    ) +
    api.override_step_data('read filter exclusion spec', api.json.output({
        'base': {
          'exclusions': ['f.*'],
        },
        'chromium': {
          'exclusions': [],
        },
     })) +
    api.override_step_data(
        'find isolated tests',
        api.isolate.output_json(['base_unittests']))
  )

  # One test (base_unittest) failed on swarming. It is retried with
  # deapplied patch.
  yield (
    api.test('swarming_deapply_patch') +
    props(buildername='linux_chromium_rel') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({
        'gtest_tests': [
          {
            'test': 'base_unittests',
            'swarming': {'can_use_on_swarming_builders': True},
          },
          {
            'test': 'browser_tests',
            'swarming': {'can_use_on_swarming_builders': True},
          },
        ],
      })
    ) +
    api.override_step_data('read filter exclusion spec', api.json.output({
        'base': {
          'exclusions': ['f.*'],
        },
        'chromium': {
          'exclusions': [],
        },
     })) +
    api.override_step_data(
        'find isolated tests',
        api.isolate.output_json(['base_unittests', 'browser_tests'])) +
    api.override_step_data('base_unittests (with patch)',
                           canned_test(passing=False)) +
    api.override_step_data(
        'find isolated tests (2)',
        api.isolate.output_json(['base_unittests']))
  )

  yield (
    api.test('no_compile_because_of_analyze') +
    props(buildername='linux_chromium_rel') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({
      })
    )
  )

  # Verifies analyze skips projects other than src.
  yield (
    api.test('dont_analyze_for_non_src_project') +
    props(buildername='linux_chromium_rel') +
    props(root='blink') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({
      })
    )
  )

  # This should result in a compile.
  yield (
    api.test('compile_because_of_analyze_matching_exclusion') +
    props(buildername='linux_chromium_rel') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({})) +
    api.override_step_data('read filter exclusion spec', api.json.output({
        'base': {
          'exclusions': ['f.*'],
        },
        'chromium': {
          'exclusions': [],
        },
     })
    )
  )

  # This should result in a compile.
  yield (
    api.test('compile_because_of_analyze') +
    props(buildername='linux_chromium_rel') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({
      })
    ) +
    api.override_step_data(
      'analyze',
      api.json.output({'status': 'Found dependency', 'targets': [],
                       'build_targets': []}))
  )

  yield (
    api.test('compile_because_of_analyze_with_filtered_tests_no_builder') +
    props(buildername='linux_chromium_rel') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({
        'gtest_tests': [
          {
            'test': 'base_unittests',
            'swarming': {'can_use_on_swarming_builders': True},
          },
          {
            'test': 'browser_tests',
          },
          {
            'test': 'unittests',
          },
        ],
      })
    ) +
    api.override_step_data(
      'analyze',
      api.json.output({'status': 'Found dependency',
                       'targets': ['browser_tests', 'base_unittests'],
                       'build_targets': ['browser_tests', 'base_unittests']}))
  )

  yield (
    api.test('compile_because_of_analyze_with_filtered_tests') +
    props(buildername='linux_chromium_rel') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({
        'gtest_tests': [
          {
            'test': 'base_unittests',
            'swarming': {'can_use_on_swarming_builders': True},
          },
          {
            'test': 'browser_tests',
          },
          {
            'test': 'unittests',
          },
        ],
      })
    ) +
    api.override_step_data(
      'analyze',
      api.json.output({'status': 'Found dependency',
                       'targets': ['browser_tests', 'base_unittests'],
                       'build_targets': ['browser_tests', 'base_unittests']}))
  )

  # Tests compile_target portion of analyze module.
  yield (
    api.test('compile_because_of_analyze_with_filtered_compile_targets') +
    props(buildername='linux_chromium_rel') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({
        'gtest_tests': [
          {
            'test': 'base_unittests',
            'swarming': {'can_use_on_swarming_builders': True},
          },
          {
            'test': 'browser_tests',
          },
          {
            'test': 'unittests',
          },
        ],
      })
    ) +
    api.override_step_data(
      'analyze',
      api.json.output({'status': 'Found dependency',
                       'targets': ['browser_tests', 'base_unittests'],
                       'build_targets': ['chrome', 'browser_tests',
                                         'base_unittests']}))
  )

  # Tests compile_targets portion of analyze with a bot that doesn't include the
  # 'all' target.
  yield (
    api.test(
      'compile_because_of_analyze_with_filtered_compile_targets_exclude_all') +
    props(buildername='linux_chromium_asan_rel') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({
        'compile_targets': ['base_unittests'],
        'gtest_tests': [
          {
            'test': 'browser_tests',
            'args': '--gtest-filter: *NaCl*.*',
          }, {
            'test': 'base_tests',
            'args': ['--gtest-filter: *NaCl*.*'],
          },
        ],
      })
    ) +
    api.override_step_data(
      'analyze',
      api.json.output({'status': 'Found dependency',
                       'targets': ['browser_tests', 'base_unittests'],
                       'build_targets': ['base_unittests']}))
  )

  # Tests compile_targets portion of analyze with a bot that doesn't include the
  # 'all' target.
  yield (
    api.test(
      'analyze_finds_invalid_target') +
    props(buildername='linux_chromium_asan_rel') +
    api.platform.name('linux') +
    api.override_step_data('read test spec', api.json.output({
        'compile_targets': ['base_unittests'],
        'gtest_tests': [
          {
            'test': 'browser_tests',
            'args': '--gtest-filter: *NaCl*.*',
          }, {
            'test': 'base_tests',
            'args': ['--gtest-filter: *NaCl*.*'],
          },
        ],
      })
    ) +
    api.override_step_data(
      'analyze',
      api.json.output({'invalid_targets': 'invalid target'}))
  )
