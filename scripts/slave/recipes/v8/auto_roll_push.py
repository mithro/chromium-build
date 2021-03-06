# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

DEPS = [
  'depot_tools/bot_update',
  'chromium',
  'depot_tools/gclient',
  'recipe_engine/context',
  'recipe_engine/path',
  'recipe_engine/properties',
  'recipe_engine/python',
  'recipe_engine/raw_io',
  'recipe_engine/step',
  'recipe_engine/url',
  'v8',
]

def RunSteps(api):
  api.gclient.set_config('v8')
  api.bot_update.ensure_checkout(no_shallow=True)

  output = api.url.get_text(
      'https://v8-roll.appspot.com/status',
      step_name='check roll status',
      default_test_data='1',
    ).output
  api.step.active_result.presentation.logs['stdout'] = output.splitlines()
  if output.strip() != '1':
    api.step.active_result.presentation.step_text = "Pushing deactivated"
    return
  else:
    api.step.active_result.presentation.step_text = "Pushing activated"

  with api.context(cwd=api.path['checkout']):
    api.python(
        'push candidate',
        api.path['checkout'].join(
            'tools', 'release', 'auto_push.py'),
        ['--author', 'v8-autoroll@chromium.org',
         '--reviewer', 'v8-autoroll@chromium.org',
         '--push',
         '--work-dir', api.path['start_dir'].join('workdir')],
      )


def GenTests(api):
  yield api.test('standard') + api.properties.generic(
      mastername='client.v8.fyi')
  yield (api.test('rolling_deactivated') +
      api.properties.generic(mastername='client.v8.fyi') +
      api.url.text('check roll status', '0'))

