# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from recipe_engine.types import freeze

DEPS = [
  'build',
  'chromium',
  'commit_position',
  'depot_tools/bot_update',
  'depot_tools/gclient',
  'depot_tools/git',
  'file',
  'goma',
  'depot_tools/gsutil',
  'recipe_engine/context',
  'recipe_engine/json',
  'recipe_engine/path',
  'recipe_engine/properties',
  'recipe_engine/python',
  'recipe_engine/raw_io',
  'recipe_engine/step',
]

BUCKET_NAME = 'chrome-codesearch'
CHROMIUM_GIT_URL = 'https://chromium.googlesource.com'

# Lists the additional repositories that should be checked out to be included
# in the source archive that is indexed by Codesearch.
ADDITIONAL_REPOS = freeze({
  'infra': '%s/infra/infra' % CHROMIUM_GIT_URL,
  'tools/chrome-devtools-frontend':\
      '%s/chromium/tools/chrome-devtools-frontend' % CHROMIUM_GIT_URL,
  'tools/chromium-jobqueue':\
      '%s/chromium/tools/chromium-jobqueue' % CHROMIUM_GIT_URL,
  'tools/chromium-shortener':\
      '%s/chromium/tools/chromium-shortener' % CHROMIUM_GIT_URL,
  'tools/command_wrapper/bin':\
      '%s/chromium/tools/command_wrapper/bin' % CHROMIUM_GIT_URL,
  'tools/depot_tools': '%s/chromium/tools/depot_tools' % CHROMIUM_GIT_URL,
  'tools/gsd_generate_index':\
      '%s/chromium/tools/gsd_generate_index' % CHROMIUM_GIT_URL,
  'tools/perf': '%s/chromium/tools/perf' % CHROMIUM_GIT_URL,
})

GENERATED_REPO = '%s/chromium/src/out' % CHROMIUM_GIT_URL
GENERATED_AUTHOR_EMAIL = 'git-generated-files-sync@chromium.org'
GENERATED_AUTHOR_NAME = 'Automatic Generated Files Sync'

SPEC = freeze({
  # The builders have the following parameters:
  # - compile_targets: the compile targets.
  # - package_filename: The prefix of the name of the source archive.
  # - platform: The platform for which the code is compiled.
  # - sync_generated_files: Whether to sync generated files into a git repo.
  # - corpus: Kythe corpus to generate index packs under.
  # - gen_repo_branch: Which branch in the generated files repo to sync to.
  'builders': {
    'codesearch-gen-chromium-linux': {
      'compile_targets': [
        'all',
      ],
      'package_filename': 'chromium-src',
      'platform': 'linux',
      'sync_generated_files': True,
      'gen_repo_branch': 'master',
      'corpus': 'chromium-linux',
    },
    'codesearch-gen-chromium-chromiumos': {
      # TODO(emso): Get the below compile targets.
      # from the chromium_tests recipe module.
      # Compile targets used by the 'Linux ChromiumOS Full' builder (2016-12-16)
      'compile_targets': [
        'app_list_unittests',
        'aura_builder',
        'base_unittests',
        'browser_tests',
        'cacheinvalidation_unittests',
        'chromeos_unittests',
        'components_unittests',
        'compositor_unittests',
        'content_browsertests',
        'content_unittests',
        'crypto_unittests',
        'dbus_unittests',
        'device_unittests',
        'gcm_unit_tests',
        'google_apis_unittests',
        'gpu_unittests',
        'interactive_ui_tests',
        'ipc_tests',
        'jingle_unittests',
        'media_unittests',
        'message_center_unittests',
        'nacl_loader_unittests',
        'net_unittests',
        'ppapi_unittests',
        'printing_unittests',
        'remoting_unittests',
        'sandbox_linux_unittests',
        'sql_unittests',
        'ui_base_unittests',
        'unit_tests',
        'url_unittests',
        'views_unittests',
      ],
      'package_filename': 'chromiumos-src',
      'platform': 'chromeos',
      'sync_generated_files': True,
      'gen_repo_branch': 'chromiumos',
      'corpus': 'chromium-chromeos',
    },
    'codesearch-gen-chromium-android': {
      'compile_targets': [
        'all',
      ],
      'package_filename': 'chromium-android-src',
      'platform': 'android',
      'sync_generated_files': True,
      'gen_repo_branch': 'android',
      'corpus': 'chromium-android',
    },
  },
})

def GenerateCompilationDatabase(api, debug_path, targets, platform):
  mastername = api.properties.get('mastername')
  buildername = api.properties.get('buildername')
  api.chromium.run_mb(mastername,
                      buildername,
                      build_dir=debug_path,
                      phase=platform,
                      name='generate build files for %s' % platform)
  command = ['ninja', '-C', debug_path] + list(targets)
  # Add the parameters for creating the compilation database.
  command += ['-t', 'compdb', 'cc', 'cxx', 'objc', 'objcxx']

  command += ['-j', api.goma.recommended_goma_jobs]

  # TODO(tikuta): Support returning step result in api.goma.build_with_goma
  api.goma.start()

  ninja_log_exit_status = 1
  try:
    step_result = api.step('generate compilation database for %s' % platform,
                           command, stdout=api.raw_io.output_text())
    ninja_log_exit_status = step_result.retcode
  except api.step.StepFailure as e:
    ninja_log_exit_status = e.retcode
    raise e
  finally:
    api.goma.stop(ninja_log_outdir=debug_path,
                  ninja_log_command=command,
                  ninja_log_compiler='goma',
                  ninja_log_exit_status=ninja_log_exit_status)

  return step_result

def RunSteps(api):
  buildername = api.properties.get('buildername')

  bot_config = SPEC.get('builders', {}).get(buildername)
  platform = bot_config.get('platform', 'linux')

  # Checkout the repositories that are either directly needed or should be
  # included in the source archive.
  gclient_config = api.gclient.make_config('chromium')
  if platform == 'android':
    gclient_config.target_os = ['android']
  for name, url in ADDITIONAL_REPOS.iteritems():
    solution = gclient_config.solutions.add()
    solution.name = name
    solution.url = url
  api.gclient.c = gclient_config
  update_step = api.bot_update.ensure_checkout()
  api.chromium.set_build_properties(update_step.json.output['properties'])

  # Remove the llvm-build directory, so that gclient runhooks will download
  # the pre-built clang binary and not use the locally compiled binary from
  # the 'compile translation_unit clang tool' step.
  api.file.rmtree('llvm-build',
                  api.path['checkout'].join('third_party', 'llvm-build'))

  debug_path = api.path['checkout'].join('out', 'Debug')
  targets = bot_config.get('compile_targets', [])
  api.chromium.set_config('codesearch', BUILD_CONFIG='Debug')
  api.chromium.ensure_goma()
  # CHROME_HEADLESS makes sure that running 'gclient runhooks' doesn't require
  # entering 'y' to agree to a license.
  with api.context(env={'CHROME_HEADLESS': '1'}):
    api.chromium.runhooks()

  result = GenerateCompilationDatabase(api, debug_path, targets, platform)

  try:
    api.chromium.compile(targets, use_goma_module=True)
  except api.step.StepFailure as f: # pragma: no cover
    # Even if compilation fails, the Grok indexer may still be able to extract
    # (almost) all cross references. And the downside of failing on compile
    # error is that Codesearch gets stale.
    pass

  # Copy the created output to the correct directory. When running the clang
  # tool, it is assumed by the scripts that the compilation database is in the
  # out/Debug directory, and named 'compile_commands.json'.
  api.step('copy compilation database',
           ['cp', api.raw_io.input_text(data=result.stdout),
            debug_path.join('compile_commands.json')])

  if platform == 'chromeos':
    result = GenerateCompilationDatabase(api, debug_path, targets, 'linux')
    api.build.python('Filter out duplicate compilation units',
        api.package_repo_resource('scripts', 'slave', 'chromium',
                                  'filter_compilations.py'),
        ['--compdb-input', debug_path.join('compile_commands.json'),
         '--compdb-filter', api.raw_io.input_text(data=result.stdout),
         '--compdb-output', debug_path.join('compile_commands.json')])
  # Compile the clang tool
  script_path = api.path.sep.join(['tools', 'clang', 'scripts', 'update.py'])
  with api.context(cwd=api.path['checkout']):
    api.step('compile translation_unit clang tool',
             [script_path, '--force-local-build', '--without-android',
              '--extra-tools', 'translation_unit'])

  # Run the clang tool
  args = ['--tool', api.path['checkout'].join('third_party', 'llvm-build',
                                    'Release+Asserts', 'bin',
                                    'translation_unit'),
          '-p', debug_path, '--all']
  try:
    api.python(
        'run translation_unit clang tool',
        api.path['checkout'].join('tools', 'clang', 'scripts', 'run_tool.py'),
        args)
  except api.step.StepFailure as f:
    # For some files, the clang tool produces errors. This is a known issue,
    # but since it only affects very few files (currently 9), we ignore these
    # errors for now. At least this means we can already have cross references
    # support for the files where it works.
    api.step.active_result.presentation.step_text = f.reason_message()
    api.step.active_result.presentation.status = api.step.WARNING

  got_revision_cp = api.chromium.build_properties.get('got_revision_cp')
  commit_position = api.commit_position.parse_revision(got_revision_cp)
  got_revision = api.chromium.build_properties.get('got_revision')

  corpus = bot_config.get('corpus', 'chromium-linux')

  # Create the kythe index pack
  index_pack_kythe_name = 'index_pack_%s_kythe.zip' % platform
  index_pack_kythe_name_with_revision = 'index_pack_%s_kythe_%s.zip' % (
      platform, commit_position)
  api.build.python('create kythe index pack',
      api.package_repo_resource('scripts', 'slave', 'chromium',
                                'package_index.py'),
      ['--path-to-compdb', debug_path.join('compile_commands.json'),
       '--path-to-archive-output',
       debug_path.join(index_pack_kythe_name),
       '--index-pack-format', 'kythe',
       '--corpus', corpus,
       '--revision', got_revision])

  # Upload the kythe index pack
  api.gsutil.upload(
      name='upload kythe index pack',
      source=debug_path.join(index_pack_kythe_name),
      bucket=BUCKET_NAME,
      dest='prod/%s' % index_pack_kythe_name_with_revision
  )

  if bot_config.get('sync_generated_files', False):
    # Check out the generated files repo.
    generated_repo_dir = api.path['start_dir'].join('generated')
    api.git.checkout(
        GENERATED_REPO,
        ref=bot_config.get('gen_repo_branch', 'master'),
        dir_path=generated_repo_dir,
        submodules=False)
    with api.context(cwd=generated_repo_dir):
      api.git('config', 'user.email', GENERATED_AUTHOR_EMAIL)
      api.git('config', 'user.name', GENERATED_AUTHOR_NAME)

    # Sync the generated files into this checkout.
    api.build.python('sync generated files',
        api.package_repo_resource('scripts','slave',
                                  'sync_generated_files_codesearch.py'),
        ['--message',
         'Generated files from "%s" build %s, revision %s' % (
             api.properties.get('buildername'),
             api.properties.get('buildnumber'),
             api.chromium.build_properties.get('got_revision')),
         '--dest-branch',
         bot_config.get('gen_repo_branch', 'master'),
         'src/out',
         generated_repo_dir])


def _sanitize_nonalpha(text):
  return ''.join(c if c.isalnum() else '_' for c in text)


def GenTests(api):
  for buildername, config in SPEC['builders'].iteritems():
    platform = config.get('platform')
    test = api.test('full_%s' % (_sanitize_nonalpha(buildername)))
    test += api.step_data('generate compilation database for %s' % platform,
                          stdout=api.raw_io.output_text('some compilation data'))
    if platform == 'chromeos':
      test += api.step_data('generate compilation database for linux',
                            stdout=api.raw_io.output_text('some compilation data'))
    test += api.properties.generic(buildername=buildername,
                                   mastername='chromium.infra.codesearch')

    yield test

  yield (
    api.test(
        'full_%s_fail' % _sanitize_nonalpha('codesearch-gen-chromium-chromiumos')) +
    api.step_data('generate compilation database for chromeos',
                  stdout=api.raw_io.output_text('some compilation data')) +
    api.step_data('generate compilation database for linux',
                  stdout=api.raw_io.output_text('some compilation data')) +
    api.step_data('run translation_unit clang tool', retcode=2) +
    api.properties.generic(buildername='codesearch-gen-chromium-chromiumos',
                           mastername='chromium.infra.codesearch')
  )

  yield (
    api.test(
        'full_%s_gen_compile_fail' %
        _sanitize_nonalpha('codesearch-gen-chromium-chromiumos')) +
    api.step_data('generate compilation database for chromeos',
                  stdout=api.raw_io.output_text('some compilation data'),
                  retcode=1) +
    api.properties.generic(buildername='codesearch-gen-chromium-chromiumos',
                           mastername='chromium.infra.codesearch')
  )
