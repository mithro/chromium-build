# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

DEPS = [
  'file',
  'recipe_engine/context',
  'recipe_engine/path',
  'recipe_engine/properties',
  'repo',
  'recipe_engine/step',
]

_TARGET_DEVICE_MAP = {
    'volantis-armv7': {
      'bitness': 32,
      'make_jobs': 2,
      'product': 'arm_krait',
      },
    'volantis-armv8': {
      'bitness': 64,
      'make_jobs': 2,
      'product': 'armv8',
      },
    'angler-armv7': {
      'bitness': 32,
      'make_jobs': 4,
      'product': 'arm_krait',
      },
    'fugu': {
      'bitness': 32,
      'make_jobs': 4,
      'product': 'silvermont',
      },
    'mips32': {
      'bitness': 32,
      'make_jobs': 2,
      'product': 'mips32r2_fp_xburst',
      },
    'angler-armv8': {
      'bitness': 64,
      'make_jobs': 4,
      'product': 'armv8',
      },
    }

_ANDROID_CLEAN_DIRS = ['/data/local/tmp', '/data/art-test',
                       '/data/nativetest', '/data/nativetest64',
                       '/data/misc/trace/*']

def checkout(api):
  api.repo.init('https://android.googlesource.com/platform/manifest',
      '-b', 'master-art')
  api.repo.sync()

def full_checkout(api):
  api.repo.init('https://android.googlesource.com/platform/manifest',
      '-b', 'master')
  api.repo.sync()

def clobber(api):
  # buildbot sets 'clobber' to the empty string which is falsey, check with 'in'
  if 'clobber' in api.properties:
    api.file.rmtree('clobber', api.path['start_dir'].join('out'))

def setup_host_x86(api, debug, bitness, concurrent_collector=True,
    heap_poisoning=False):
  with api.step.defer_results():
    checkout(api)
    clobber(api)

    build_top_dir = api.path['start_dir']
    art_tools = api.path['start_dir'].join('art', 'tools')
    env = { 'TARGET_PRODUCT': 'sdk',
            'TARGET_BUILD_VARIANT': 'eng',
            'TARGET_BUILD_TYPE': 'release',
            'SOONG_ALLOW_MISSING_DEPENDENCIES': 'true',
            'ANDROID_BUILD_TOP': build_top_dir,
            'JACK_SERVER': 'false',
            'JACK_REPOSITORY': str(build_top_dir.join('prebuilts', 'sdk',
                                                      'tools', 'jacks')),
            'PATH': str(build_top_dir.join('out', 'host', 'linux-x86', 'bin')) +
                        api.path.pathsep +
                        '/usr/lib/jvm/java-8-openjdk-amd64/bin/' +
                        api.path.pathsep + '%(PATH)s',
            'ART_TEST_RUN_TEST_2ND_ARCH': 'false',
            'ART_TEST_FULL': 'false',
            'ART_TEST_KEEP_GOING': 'true' }

    if bitness == 32:
      env.update({ 'HOST_PREFER_32_BIT' : 'true' })

    if not debug:
      env.update({ 'ART_TEST_RUN_TEST_NDEBUG' : 'true' })
      env.update({ 'ART_TEST_RUN_TEST_DEBUG' : 'false' })

    if concurrent_collector:
      env.update({ 'ART_USE_READ_BARRIER' : 'true' })
    else:
      env.update({ 'ART_USE_READ_BARRIER' : 'false' })

    if heap_poisoning:
      env.update({ 'ART_HEAP_POISONING' : 'true' })
    else:
      env.update({ 'ART_HEAP_POISONING' : 'false' })


    with api.context(env=env):
      api.step('build sdk-eng',
               [art_tools.join('buildbot-build.sh'), '-j8', '--host'])

      api.step('test gtest',
          ['make', '-j8', 'test-art-host-gtest%d' % bitness])

      api.step('test optimizing', ['./art/test/testrunner/testrunner.py',
                                   '-j8',
                                   '--optimizing',
                                   '--debuggable',
                                   '--ndebuggable',
                                   '--host',
                                   '--verbose'])
      # Use a lower -j number for interpreter, some tests take a long time
      # to run on it.
      api.step('test interpreter', ['./art/test/testrunner/testrunner.py',
                                    '-j5',
                                    '--interpreter',
                                    '--host',
                                    '--verbose'])

      api.step('test jit', ['./art/test/testrunner/testrunner.py',
                            '-j8',
                            '--jit',
                            '--host',
                            '--verbose'])

      api.step('test speed-profile', ['./art/test/testrunner/testrunner.py',
                                      '-j8',
                                      '--speed-profile',
                                      '--host',
                                      '--verbose'])

      libcore_command = [art_tools.join('run-libcore-tests.sh'),
                         '--mode=host',
                         '--variant=X%d' % bitness]
      if debug:
        libcore_command.append('--debug')
      api.step('test libcore', libcore_command)

      jdwp_command = [art_tools.join('run-jdwp-tests.sh'),
                      '--mode=host',
                      '--variant=X%d' % bitness]
      if debug:
        jdwp_command.append('--debug')
      api.step('test jdwp jit', jdwp_command)

      jdwp_command = [art_tools.join('run-jdwp-tests.sh'),
                      '--mode=host',
                      '--variant=X%d' % bitness,
                      '--no-jit']
      if debug:
        jdwp_command.append('--debug')
      api.step('test jdwp aot', jdwp_command)

def setup_target(api,
    serial,
    debug,
    device,
    concurrent_collector=True,
    heap_poisoning=False):
  build_top_dir = api.path['start_dir']
  art_tools = api.path['start_dir'].join('art', 'tools')
  android_root = '/data/local/tmp/system'

  env = {'TARGET_BUILD_VARIANT': 'eng',
         'TARGET_BUILD_TYPE': 'release',
         'SOONG_ALLOW_MISSING_DEPENDENCIES': 'true',
         'ANDROID_SERIAL': serial,
         'ANDROID_BUILD_TOP': build_top_dir,
         'PATH': str(build_top_dir.join('out', 'host', 'linux-x86', 'bin')) +
                     api.path.pathsep +
                     '/usr/lib/jvm/java-8-openjdk-amd64/bin/' +
                     api.path.pathsep + '%(PATH)s',
         'JACK_SERVER': 'false',
         'JACK_REPOSITORY': str(build_top_dir.join('prebuilts', 'sdk', 'tools',
                                                   'jacks')),
         'ART_TEST_RUN_TEST_2ND_ARCH': 'false',
         'ART_TEST_FULL': 'false',
         'ART_TEST_ANDROID_ROOT': android_root,
         'USE_DEX2OAT_DEBUG': 'false',
         'ART_BUILD_HOST_DEBUG': 'false',
         'ART_TEST_KEEP_GOING': 'true'}

  if not debug:
    env.update({ 'ART_TEST_RUN_TEST_NDEBUG' : 'true' })
    env.update({ 'ART_TEST_RUN_TEST_DEBUG' : 'false' })

  if concurrent_collector:
    env.update({ 'ART_USE_READ_BARRIER' : 'true' })
  else:
    env.update({ 'ART_USE_READ_BARRIER' : 'false' })

  if heap_poisoning:
    env.update({ 'ART_HEAP_POISONING' : 'true' })
  else:
    env.update({ 'ART_HEAP_POISONING' : 'false' })


  bitness = _TARGET_DEVICE_MAP[device]['bitness']
  make_jobs = _TARGET_DEVICE_MAP[device]['make_jobs']
  env.update(
      {'TARGET_PRODUCT': _TARGET_DEVICE_MAP[device]['product'],
       'ANDROID_PRODUCT_OUT': build_top_dir.join('out','target', 'product',
         _TARGET_DEVICE_MAP[device]['product'])
      })

  if bitness == 32:
    env.update({ 'CUSTOM_TARGET_LINKER': '%s/bin/linker' % android_root  })
  else:
    env.update({ 'CUSTOM_TARGET_LINKER': '%s/bin/linker64' % android_root  })

  checkout(api)
  clobber(api)

  # Decrease the number of parallel tests, as some tests eat lots of memory.
  if debug and device == 'fugu':
    make_jobs = 1

  with api.step.defer_results():
    with api.context(env=env):
      api.step('build target', [art_tools.join('buildbot-build.sh'),
                                '-j8', '--target'])

      api.step('setup device', [art_tools.join('setup-buildbot-device.sh')])

      api.step('device cleanup', ['adb', 'shell', 'rm', '-rf'] +
                                 _ANDROID_CLEAN_DIRS)

      api.step('sync target', ['make', 'test-art-target-sync'])

    def test_logging(api, test_name):
      with api.context(env=env):
        api.step(test_name + ': adb logcat',
                 ['adb', 'logcat', '-d', '-v', 'threadtime'])
        api.step(test_name + ': crashes',
                 [art_tools.join('symbolize-buildbot-crashes.sh')])
        api.step(test_name + ': adb clear log', ['adb', 'logcat', '-c'])

    test_env = env.copy()
    test_env.update({ 'ART_TEST_NO_SYNC': 'true' })
    test_env.update({ 'ANDROID_ROOT': android_root })

    with api.context(env=test_env):
      api.step('test gtest', ['make', '-j%d' % (make_jobs),
        'test-art-target-gtest%d' % bitness])
    test_logging(api, 'test gtest')

    optimizing_make_jobs = make_jobs
    # Decrease the number of parallel tests for fugu/optimizing, as some tests
    # eat lots of memory.
    if not debug and device == 'fugu':
      optimizing_make_jobs = 1

    with api.context(env=test_env):
      api.step('test optimizing', ['./art/test/testrunner/testrunner.py',
                                   '-j%d' % (optimizing_make_jobs),
                                   '--optimizing',
                                   '--debuggable',
                                   '--ndebuggable',
                                   '--target',
                                   '--verbose'])
    test_logging(api, 'test optimizing')

    with api.context(env=test_env):
      api.step('test interpreter', ['./art/test/testrunner/testrunner.py',
                                    '-j%d' % (make_jobs),
                                    '--interpreter',
                                    '--target',
                                    '--verbose'])
    test_logging(api, 'test interpreter')

    with api.context(env=test_env):
      api.step('test jit', ['./art/test/testrunner/testrunner.py',
                            '-j%d' % (make_jobs),
                            '--jit',
                            '--target',
                            '--verbose'])
    test_logging(api, 'test jit')

    with api.context(env=test_env):
      api.step('test speed-profile', ['./art/test/testrunner/testrunner.py',
                                      '-j%d' % (make_jobs),
                                      '--speed-profile',
                                      '--target',
                                      '--verbose'])
    test_logging(api, 'test speed-profile')

    libcore_command = [art_tools.join('run-libcore-tests.sh'),
                       '--mode=device',
                       '--variant=X%d' % bitness]
    if debug:
      libcore_command.append('--debug')
    with api.context(env=test_env):
      api.step('test libcore', libcore_command)
    test_logging(api, 'test libcore')

    jdwp_command = [art_tools.join('run-jdwp-tests.sh'),
                    '--mode=device',
                    '--variant=X%d' % bitness]
    if debug:
      jdwp_command.append('--debug')
    with api.context(env=test_env):
      api.step('test jdwp jit', jdwp_command)
    test_logging(api, 'test jdwp jit')

    jdwp_command = [art_tools.join('run-jdwp-tests.sh'),
                    '--mode=device',
                    '--variant=X%d' % bitness,
                    '--no-jit']
    if debug:
      jdwp_command.append('--debug')
    with api.context(env=test_env):
      api.step('test jdwp aot', jdwp_command)
    test_logging(api, 'test jdwp aot')

def setup_aosp_builder(api, read_barrier):
  full_checkout(api)
  clobber(api)
  builds = ['x86', 'x86_64', 'arm', 'arm64']
  build_top_dir = api.path['start_dir']
  with api.step.defer_results():
    for build in builds:
      env = { 'TARGET_PRODUCT': 'aosp_%s' % build,
              'TARGET_BUILD_VARIANT': 'eng',
              'TARGET_BUILD_TYPE': 'release',
              'ANDROID_BUILD_TOP': build_top_dir,
              'PATH': '/usr/lib/jvm/java-8-openjdk-amd64/bin/' +
                      api.path.pathsep + '%(PATH)s',
              'JACK_SERVER': 'false',
              'JACK_REPOSITORY': str(build_top_dir.join('prebuilts', 'sdk',
                                                        'tools', 'jacks')),
              'ART_USE_READ_BARRIER': 'true' if read_barrier else 'false'}
      with api.context(env=env):
        api.step('Clean oat %s' % build, ['make', '-j8', 'clean-oat-host'])
        api.step('build %s' % build, ['make', '-j8'])

def setup_valgrind_runner(api, bitness):
  checkout(api)
  clobber(api)
  build_top_dir = api.path['start_dir']
  run = api.path['start_dir'].join('art', 'test', 'testrunner', 'run_build_test_target.py')
  with api.step.defer_results():
    env = { 'TARGET_PRODUCT': 'sdk',
            'TARGET_BUILD_VARIANT': 'eng',
            'TARGET_BUILD_TYPE': 'release',
            'ANDROID_BUILD_TOP': build_top_dir,
            'PATH': '/usr/lib/jvm/java-8-openjdk-amd64/bin/' +
                    api.path.pathsep + '%(PATH)s',
            'JACK_SERVER': 'false',
            'JACK_REPOSITORY': str(build_top_dir.join('prebuilts', 'sdk',
                                                      'tools', 'jacks')) }
    if bitness == 32:
      env.update({ 'HOST_PREFER_32_BIT' : 'true' })

    with api.context(env=env):
      api.step('run valgrind tests', [run, '-j8', 'art-gtest-valgrind%d' % bitness])


_CONFIG_MAP = {
  'client.art': {

    'x86': {
      'host-x86-ndebug': {
        'debug': False,
        'bitness': 32,
      },
      'host-x86-debug': {
        'debug': True,
        'bitness': 32,
      },
      'host-x86_64-ndebug': {
        'debug': False,
        'bitness': 64,
      },
      'host-x86_64-debug': {
        'debug': True,
        'bitness': 64,
      },
      'host-x86-cms': {
        'debug': True,
        'bitness': 32,
        'concurrent_collector': False,
      },
      'host-x86_64-cms': {
        'debug': True,
        'bitness': 64,
        'concurrent_collector': False,
      },
      'host-x86-poison-debug': {
        'debug': True,
        'bitness': 32,
        'heap_poisoning': True,
      },
      'host-x86_64-poison-debug': {
        'debug': True,
        'bitness': 64,
        'heap_poisoning': True,
      },
    },

    'target': {
      'angler-armv7-ndebug': {
        'serial': '84B7N16728001148',
        'device': 'angler-armv7',
        'debug': False,
      },
      'angler-armv7-debug': {
        'serial': '84B7N15B03000729',
        'device': 'angler-armv7',
        'debug': True,
      },
      'volantis-armv7-poison-debug': {
        'serial': 'HT591JT00517',
        'device': 'volantis-armv7',
        'debug': True,
        'heap_poisoning': True
      },
      'volantis-armv8-poison-ndebug': {
        'serial': 'HT4CTJT03670',
        'device': 'volantis-armv8',
        'debug': False,
        'heap_poisoning': True,
      },
      'volantis-armv8-poison-debug': {
        'serial': 'HT49CJT00070',
        'device': 'volantis-armv8',
        'debug': True,
        'heap_poisoning': True
      },
      'fugu-ndebug': {
        'serial': '0BCDB85D',
        'device': 'fugu',
        'debug': False,
      },
      'fugu-debug': {
        'serial': 'E6B27F19',
        'device': 'fugu',
        'debug': True,
      },
      'angler-armv7-cms': {
        'serial': '84B7N15B03000329',
        'device': 'angler-armv7',
        'debug': True,
        'concurrent_collector': False,
      },
      'angler-armv8-ndebug': {
        'serial': '84B7N16728001142',
        'device': 'angler-armv8',
        'debug': False,
      },
      'angler-armv8-debug': {
        'serial': '84B7N15B03000660',
        'device': 'angler-armv8',
        'debug': True,
      },
      'angler-armv8-cms': {
        'serial': '84B7N15B03000641',
        'device': 'angler-armv8',
        'debug': True,
        'concurrent_collector': False,
      },
    },

    'aosp': {
      'aosp-builder-cms': {
        'read_barrier': False
      },
      'aosp-builder-cc': {
        'read_barrier': True
      },
    },

    'valgrind': {
      'host-x86-valgrind': {
        'bitness': 32
      },
      'host-x86_64-valgrind': {
        'bitness': 64
      },
    },
  },
}

_CONFIG_DISPATCH_MAP = {
  'client.art': {
    'x86': setup_host_x86,
    'target': setup_target,
    'aosp': setup_aosp_builder,
    'valgrind': setup_valgrind_runner,
  }
}

def RunSteps(api):
  if api.properties['mastername'] not in _CONFIG_MAP: # pragma: no cover
    error = "Master not found in recipe's local config!"
    raise KeyError(error)

  builder_found = False
  config = _CONFIG_MAP[api.properties['mastername']]
  for builder_type in config:
    if api.properties['buildername'] in config[builder_type]:
      builder_found = True
      builder_dict = config[builder_type][api.properties['buildername']]
      _CONFIG_DISPATCH_MAP[api.properties['mastername']][builder_type](api,
          **builder_dict)
      break

  if not builder_found: # pragma: no cover
    error = "Builder not found in recipe's local config!"
    raise KeyError(error)

def GenTests(api):
  for mastername, config_dict in _CONFIG_MAP.iteritems():
    for builders in config_dict.values():
      for buildername in builders:
        for clb in (None, True):
          yield (
              api.test("%s__ON__%s__%s" % (buildername, mastername,
                ("" if clb else "no") + "clobber")) +
              api.properties(
                mastername=mastername,
                buildername=buildername,
                bot_id='TestSlave',
                # Buildbot uses clobber='' to mean clobber, however
                # api.properties(clobber=None) will set clobber=None!
                # so we have to not even mention it to avoid our
                # 'clobber' in api.properties logic triggering above.
              ) + (api.properties(clobber='') if clb else api.properties())
            )
  yield (
      api.test('x86_32_test_failure') +
      api.properties(
        mastername='client.art',
        buildername='host-x86-ndebug',
        bot_id='TestSlave',
      ) +
      api.step_data('test jdwp aot', retcode=1))
  yield (
      api.test('target_angler_setup_failure') +
      api.properties(
        mastername='client.art',
        buildername='angler-armv7-ndebug',
        bot_id='TestSlave',
      )
      + api.step_data('setup device', retcode=1))
  yield (
      api.test('target_angler_test_failure') +
      api.properties(
        mastername='client.art',
        buildername='angler-armv7-ndebug',
        bot_id='TestSlave',
      ) +
      api.step_data('test jdwp aot', retcode=1))
  yield (
      api.test('target_angler_device_cleanup_failure') +
      api.properties(
        mastername='client.art',
        buildername='angler-armv7-ndebug',
        bot_id='TestSlave',
      ) +
      api.step_data('device cleanup', retcode=1))
  yield (
      api.test('aosp_x86_build_failure') +
      api.properties(
        mastername='client.art',
        buildername='aosp-builder-cms',
        bot_id='TestSlave',
      ) +
      api.step_data('build x86', retcode=1))
#  These tests *should* exist, but can't be included as they cause the recipe
#  simulation to error out, instead of showing that the build should become
#  purple instead. This may need to be fixed in the simulation test script.
#  yield (
#      api.test('invalid mastername') +
#      api.properties(
#        mastername='client.art.does_not_exist',
#        buildername='aosp-builder-cms',
#        bot_id='TestSlave',
#      )
#    )
#  yield (
#      api.test('invalid buildername') +
#      api.properties(
#        mastername='client.art',
#        buildername='builder_does_not_exist',
#        bot_id='TestSlave',
#      )
#    )
