# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# Contains the bulk of the WebRTC builder configurations so they can be reused
# from multiple recipes.

from infra.libs.infra_types import freeze

RECIPE_CONFIGS = freeze({
  'webrtc': {
    'chromium_config': 'webrtc_standalone',
    'gclient_config': 'webrtc',
    'test_suite': 'webrtc',
  },
  'webrtc_baremetal': {
    'chromium_config': 'webrtc_standalone',
    'gclient_config': 'webrtc',
    'test_suite': 'webrtc_baremetal',
  },
  'webrtc_clang': {
    'chromium_config': 'webrtc_clang',
    'gclient_config': 'webrtc',
    'test_suite': 'webrtc',
  },
  'webrtc_parallel': {
    'chromium_config': 'webrtc_standalone',
    'gclient_config': 'webrtc',
    'test_suite': 'webrtc_parallel',
  },
  'webrtc_parallel_clang': {
    'chromium_config': 'webrtc_clang',
    'gclient_config': 'webrtc',
    'test_suite': 'webrtc_parallel',
  },
  'webrtc_android': {
    'chromium_config': 'android',
    'chromium_android_config': 'webrtc',
    'gclient_config': 'webrtc',
    'gclient_apply_config': ['android'],
    'test_suite': 'android',
  },
  'webrtc_android_clang': {
    'chromium_config': 'android_clang',
    'chromium_android_config': 'webrtc',
    'gclient_config': 'webrtc',
    'gclient_apply_config': ['android'],
  },
  'webrtc_ios32': {
    'chromium_config': 'webrtc_ios32',
    'gclient_config': 'webrtc_ios',
  },
  'webrtc_ios64': {
    'chromium_config': 'webrtc_ios64',
    'gclient_config': 'webrtc_ios',
  },
  'chromium_webrtc': {
    'chromium_config': 'chromium',
    'chromium_apply_config': ['dcheck', 'blink_logging_on'],
    'gclient_config': 'chromium_webrtc',
    'compile_targets': ['chromium_builder_webrtc'],
    'test_suite': 'chromium',
  },
  'chromium_webrtc_tot': {
    'chromium_config': 'chromium',
    'chromium_apply_config': ['dcheck', 'blink_logging_on'],
    'gclient_config': 'chromium_webrtc_tot',
    'compile_targets': ['chromium_builder_webrtc'],
    'test_suite': 'chromium',
  },
  # Temporary config to try out the complicated FYI builders pre-Git switch
  # (runs a tiny compile target and no test to save time and resources).
  'chromium_webrtc_tot_git_switch_testing': {
    'chromium_config': 'chromium',
    'gclient_config': 'chromium_webrtc_tot',
    'compile_targets': ['gtest'],
  },
  'chromium_webrtc_tot_gn': {
    'chromium_config': 'chromium',
    'chromium_apply_config': ['gn'],
    'gclient_config': 'chromium_webrtc_tot',
    'compile_targets': ['all'],
  },
  'chromium_webrtc_android': {
    'chromium_config': 'android',
    'chromium_android_config': 'base_config',
    'gclient_config': 'chromium_webrtc',
    'gclient_apply_config': ['android'],
    'compile_targets': ['android_builder_chromium_webrtc'],
    'test_suite': 'chromium',
  },
  'chromium_webrtc_tot_android': {
    'chromium_config': 'android',
    'chromium_android_config': 'base_config',
    'gclient_config': 'chromium_webrtc_tot',
    'gclient_apply_config': ['android'],
    'compile_targets': ['android_builder_chromium_webrtc'],
    'test_suite': 'chromium',
  },
  'chromium_webrtc_tot_android_gn': {
    'chromium_config': 'android',
    'chromium_apply_config': ['gn', 'gn_minimal_symbols'],
    'gclient_config': 'chromium_webrtc_tot',
    'gclient_apply_config': ['android'],
    'compile_targets': ['chrome_shell_apk'],
  },
})

WEBRTC_REVISION_PERF_CONFIG = '{\'a_default_rev\': \'r_webrtc_rev\'}'

BUILDERS = freeze({
  'chromium.webrtc': {
    'builders': {
      'Win Builder': {
        'recipe_config': 'chromium_webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder',
        'build_gs_archive': 'win_rel_archive',
        'testing': {'platform': 'win'},
        'triggers': [
          'WinXP Tester',
          'Win7 Tester',
          'Win8 Tester',
        ],
      },
      'WinXP Tester': {
        'recipe_config': 'chromium_webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-rel-xp',
        },
        'bot_type': 'tester',
        'build_gs_archive': 'win_rel_archive',
        'disable_runhooks': True,
        'parent_buildername': 'Win Builder',
        'testing': {'platform': 'win'},
      },
      'Win7 Tester': {
        'recipe_config': 'chromium_webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-rel-7',
        },
        'bot_type': 'tester',
        'build_gs_archive': 'win_rel_archive',
        # TODO(kjellander): Disable the hooks on Win7 as soon we've moved away
        # from downloading test resources in that step.
        'disable_runhooks': False,
        'parent_buildername': 'Win Builder',
        'testing': {'platform': 'win'},
      },
      'Win8 Tester': {
        'recipe_config': 'chromium_webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-rel-win8',
        },
        'bot_type': 'tester',
        'build_gs_archive': 'win_rel_archive',
        # TODO(kjellander): Disable the hooks on Win7 as soon we've moved away
        # from downloading test resources in that step.
        'disable_runhooks': False,
        'parent_buildername': 'Win Builder',
        'testing': {'platform': 'win'},
      },
      'Mac Builder': {
        'recipe_config': 'chromium_webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder',
        'build_gs_archive': 'mac_rel_archive',
        'testing': {'platform': 'mac'},
        'triggers': ['Mac Tester'],
      },
      'Mac Tester': {
        'recipe_config': 'chromium_webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-rel-mac',
        },
        'bot_type': 'tester',
        'build_gs_archive': 'mac_rel_archive',
        'parent_buildername': 'Mac Builder',
        'testing': {'platform': 'mac'},
      },
      'Linux Builder': {
        'recipe_config': 'chromium_webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder',
        'build_gs_archive': 'linux_rel_archive',
        'testing': {'platform': 'linux'},
        'triggers': ['Linux Tester'],
      },
      'Linux Tester': {
        'recipe_config': 'chromium_webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-rel-linux',
        },
        'bot_type': 'tester',
        'build_gs_archive': 'linux_rel_archive',
        'parent_buildername': 'Linux Builder',
        'testing': {'platform': 'linux'},
      },
    },
  },
  'chromium.webrtc.fyi': {
    'settings': {
      'PERF_CONFIG': WEBRTC_REVISION_PERF_CONFIG,
    },
    'builders': {
      'Win Builder': {
        'recipe_config': 'chromium_webrtc_tot',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-trunk-tot-rel-win',
        },
        'bot_type': 'builder',
        'build_gs_archive': 'win_rel_archive_fyi',
        'testing': {'platform': 'win'},
        'triggers': [
          'WinXP Tester',
          'Win7 Tester',
        ],
      },
      'WinXP Tester': {
        'recipe_config': 'chromium_webrtc_tot',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-trunk-tot-rel-winxp',
        },
        'bot_type': 'tester',
        'build_gs_archive': 'win_rel_archive_fyi',
        'disable_runhooks': True,
        'parent_buildername': 'Win Builder',
        'testing': {'platform': 'win'},
      },
      'Win7 Tester': {
        'recipe_config': 'chromium_webrtc_tot',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-trunk-tot-rel-win7',
        },
        'bot_type': 'tester',
        'build_gs_archive': 'win_rel_archive_fyi',
        # TODO(kjellander): Disable the hooks on Win7 as soon we've moved away
        # from downloading test resources in that step.
        'disable_runhooks': False,
        'parent_buildername': 'Win Builder',
        'testing': {'platform': 'win'},
      },
      'Win GN': {
        'recipe_config': 'chromium_webrtc_tot_gn',
        'chromium_apply_config': ['gn_minimal_symbols'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder',
        'testing': {'platform': 'win'},
      },
      'Win GN (dbg)': {
        'recipe_config': 'chromium_webrtc_tot_gn',
        'chromium_apply_config': ['gn_minimal_symbols'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder',
        'testing': {'platform': 'win'},
      },
      'Mac': {
        'recipe_config': 'chromium_webrtc_tot',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-trunk-tot-rel-mac',
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'Mac GN': {
        'recipe_config': 'chromium_webrtc_tot_gn',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'Mac GN (dbg)': {
        'recipe_config': 'chromium_webrtc_tot_gn',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'Linux': {
        'recipe_config': 'chromium_webrtc_tot',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-trunk-tot-rel-linux',
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'Linux GN': {
        'recipe_config': 'chromium_webrtc_tot_gn',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
      'Linux GN (dbg)': {
        'recipe_config': 'chromium_webrtc_tot_gn',
        'chromium_apply_config': ['gn_component_build'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
      'Android Builder (dbg)': {
        'recipe_config': 'chromium_webrtc_tot_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-trunk-tot-dbg-android',
        },
        'bot_type': 'builder',
        'build_gs_archive': 'android_dbg_archive_fyi',
        'testing': {'platform': 'linux'},
        'triggers': [
          'Android Tests (dbg) (L Nexus5)',
          'Android Tests (dbg) (L Nexus7.2)',
        ],
      },
      'Android Builder ARM64 (dbg)': {
        'recipe_config': 'chromium_webrtc_tot_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 64,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-trunk-tot-dbg-android-arm64',
        },
        'bot_type': 'builder',
        'build_gs_archive': 'android_dbg_archive_arm64_fyi',
        'testing': {'platform': 'linux'},
        'triggers': [
          'Android Tests (dbg) (L Nexus9)',
        ],
      },
      'Android Tests (dbg) (L Nexus5)': {
        'recipe_config': 'chromium_webrtc_tot_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-trunk-tot-dbg-android-nexus5',
        },
        'bot_type': 'tester',
        'build_gs_archive': 'android_dbg_archive_fyi',
        'parent_buildername': 'Android Builder (dbg)',
        'testing': {'platform': 'linux'},
      },
      'Android Tests (dbg) (L Nexus7.2)': {
        'recipe_config': 'chromium_webrtc_tot_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'chromium-webrtc-trunk-tot-dbg-android-nexus72',
        },
        'bot_type': 'tester',
        'build_gs_archive': 'android_dbg_archive_fyi',
        'parent_buildername': 'Android Builder (dbg)',
        'testing': {'platform': 'linux'},
      },
      'Android Tests (dbg) (L Nexus9)': {
        'recipe_config': 'chromium_webrtc_tot_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 64,
        },
        'bot_type': 'tester',
        'build_gs_archive': 'android_dbg_archive_arm64_fyi',
        'parent_buildername': 'Android Builder ARM64 (dbg)',
        'testing': {'platform': 'linux'},
      },
      'Android GN': {
        'recipe_config': 'chromium_webrtc_tot_android_gn',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
      'Android GN (dbg)': {
        'recipe_config': 'chromium_webrtc_tot_android_gn',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },

    },
  },
  'client.webrtc': {
    'settings': {
      'PERF_CONFIG': WEBRTC_REVISION_PERF_CONFIG,
    },
    'builders': {
      'Win32 Debug': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'Win32 Release': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'Win64 Debug': {
        'recipe_config': 'webrtc',
        'chromium_apply_config': ['static_library'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'Win64 Release': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'Win64 Debug (GN)': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'win'},
      },
      'Win64 Release (GN)': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'win'},
      },
      'Win32 Release [large tests]': {
        'recipe_config': 'webrtc_baremetal',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'webrtc-win-large-tests',
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'Win DrMemory Full': {
        'recipe_config': 'webrtc',
        'chromium_apply_config': ['drmemory_full'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'Win DrMemory Light': {
        'recipe_config': 'webrtc',
        'chromium_apply_config': ['drmemory_light'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'Mac32 Debug': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'Mac32 Release': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'Mac64 Debug': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'Mac64 Release': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'Mac64 Debug (GN)': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'Mac64 Release (GN)': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'Mac Asan': {
        'recipe_config': 'webrtc_clang',
        'chromium_apply_config': ['asan'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'Mac32 Release [large tests]': {
        'recipe_config': 'webrtc_baremetal',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'webrtc-mac-large-tests',
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'iOS Debug': {
        'recipe_config': 'webrtc_ios32',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
          'TARGET_ARCH': 'arm',
          'TARGET_PLATFORM': 'ios',
        },
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'iOS Release': {
        'recipe_config': 'webrtc_ios32',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
          'TARGET_ARCH': 'arm',
          'TARGET_PLATFORM': 'ios',
        },
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'iOS ARM64 Debug': {
        'recipe_config': 'webrtc_ios64',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
          'TARGET_ARCH': 'arm',
          'TARGET_PLATFORM': 'ios',
        },
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'iOS ARM64 Release': {
        'recipe_config': 'webrtc_ios64',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
          'TARGET_ARCH': 'arm',
          'TARGET_PLATFORM': 'ios',
        },
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'Linux32 Debug': {
        'recipe_config': 'webrtc_parallel',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'Linux32 Release': {
        'recipe_config': 'webrtc_parallel',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'Linux64 Debug': {
        'recipe_config': 'webrtc_parallel',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'Linux64 Release': {
        'recipe_config': 'webrtc_parallel',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'Linux64 Debug (GN)': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
      'Linux64 Release (GN)': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
      'Linux Asan': {
        'recipe_config': 'webrtc_clang',
        'chromium_apply_config': ['asan', 'lsan'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'Linux Memcheck': {
        'recipe_config': 'webrtc',
        'chromium_apply_config': ['memcheck'],
        'gclient_apply_config': ['valgrind'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'Linux MSan': {
        'recipe_config': 'webrtc_clang',
        'chromium_apply_config': ['msan', 'msan_full_origin_tracking',
                                  'instrumented_libraries'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'Linux Tsan v2': {
        'recipe_config': 'webrtc_clang',
        'chromium_apply_config': ['tsan2'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'Linux64 Release [large tests]': {
        'recipe_config': 'webrtc_baremetal',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'webrtc-linux-large-tests',
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'Android Builder': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder',
        'build_gs_archive': 'android_apk_rel_archive',
        'testing': {'platform': 'linux'},
      },
      'Android Builder (dbg)': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder',
        'build_gs_archive': 'android_apk_dbg_archive',
        'testing': {'platform': 'linux'},
      },
      'Android ARM64 Builder (dbg)': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder',
        'build_gs_archive': 'android_apk_arm64_dbg_archive',
        'testing': {'platform': 'linux'},
      },
      'Android Clang (dbg)': {
        'recipe_config': 'webrtc_android_clang',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
      'Android GN': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
      'Android GN (dbg)': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
      'Android Tests (L Nexus5)(dbg)': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'tester',
        'parent_buildername': 'Android Builder (dbg)',
        'build_gs_archive': 'android_apk_dbg_archive',
        'testing': {'platform': 'linux'},
      },
      'Android Tests (L Nexus5)': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'webrtc-android-tests-nexus5',
        },
        'bot_type': 'tester',
        'parent_buildername': 'Android Builder',
        'build_gs_archive': 'android_apk_rel_archive',
        'testing': {'platform': 'linux'},
      },
      'Android Tests (L Nexus7.2)(dbg)': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'tester',
        'parent_buildername': 'Android Builder (dbg)',
        'build_gs_archive': 'android_apk_dbg_archive',
        'testing': {'platform': 'linux'},
      },
      'Android Tests (L Nexus7.2)': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'webrtc_config_kwargs': {
          'PERF_ID': 'webrtc-android-tests-nexus72',
        },
        'bot_type': 'tester',
        'parent_buildername': 'Android Builder',
        'build_gs_archive': 'android_apk_rel_archive',
        'testing': {'platform': 'linux'},
      },
      'Android Tests (L Nexus9)(dbg)': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 64,
        },
        'bot_type': 'tester',
        'parent_buildername': 'Android ARM64 Builder (dbg)',
        'build_gs_archive': 'android_apk_arm64_dbg_archive',
        'testing': {'platform': 'linux'},
      },
    },
  },
  'client.webrtc.fyi': {
    'builders':  {
      'Win32 Debug (parallel)': {
        'recipe_config': 'webrtc_parallel',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'Win32 Release (parallel)': {
        'recipe_config': 'webrtc_parallel',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'Win64 Debug (parallel)': {
        'recipe_config': 'webrtc_parallel',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'Win64 Release (parallel)': {
        'recipe_config': 'webrtc_parallel',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'Win SyzyASan': {
        'recipe_config': 'webrtc',
        'chromium_apply_config': ['syzyasan'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'Mac64 Debug (parallel)': {
        'recipe_config': 'webrtc_parallel',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'Mac64 Release (parallel)': {
        'recipe_config': 'webrtc_parallel',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'Mac Asan (parallel)': {
        'recipe_config': 'webrtc_parallel_clang',
        'chromium_apply_config': ['asan'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'Linux Asan Builder': {
        'recipe_config': 'webrtc_parallel_clang',
        'chromium_apply_config': ['asan', 'lsan'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder',
        'build_gs_archive': 'fyi_linux_asan_archive',
        'testing': {'platform': 'linux'},
        'triggers': [
          'Linux Asan Tester (parallel)',
        ],
      },
      'Linux Asan Tester (parallel)': {
        'recipe_config': 'webrtc_parallel_clang',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'tester',
        'build_gs_archive': 'fyi_linux_asan_archive',
        'parent_buildername': 'Linux Asan Builder',
        'testing': {'platform': 'linux'},
      },
      'Linux Chromium Builder': {
        'recipe_config': 'chromium_webrtc_tot_git_switch_testing',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder',
        'build_gs_archive': 'fyi_linux_chromium_rel_archive',
        'testing': {'platform': 'linux'},
        'triggers': [
          'Linux Chromium Tester',
        ],
      },
      'Linux Chromium Tester': {
        'recipe_config': 'chromium_webrtc_tot_git_switch_testing',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'tester',
        'build_gs_archive': 'fyi_linux_chromium_rel_archive',
        'parent_buildername': 'Linux Chromium Builder',
        'testing': {'platform': 'linux'},
      },
      'Android Builder (dbg)': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder',
        'build_gs_archive': 'fyi_android_apk_dbg_archive',
        'testing': {'platform': 'linux'},
        'triggers': [
          'Android Tests (Samsung S3)(dbg)',
          'Android Tests (Samsung S4)(dbg)',
          'Android Tests (Samsung S5)(dbg)',
        ],
      },
      'Android Tests (Samsung S3)(dbg)': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'tester',
        'parent_buildername': 'Android Builder (dbg)',
        'build_gs_archive': 'fyi_android_apk_dbg_archive',
        'testing': {'platform': 'linux'},
      },
      'Android Tests (Samsung S4)(dbg)': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'tester',
        'parent_buildername': 'Android Builder (dbg)',
        'build_gs_archive': 'fyi_android_apk_dbg_archive',
        'testing': {'platform': 'linux'},
      },
      'Android Tests (Samsung S5)(dbg)': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'tester',
        'parent_buildername': 'Android Builder (dbg)',
        'build_gs_archive': 'fyi_android_apk_dbg_archive',
        'testing': {'platform': 'linux'},
      },
    },
  },
  'tryserver.webrtc': {
    'builders': {
      'win': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'win_rel': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'win_x64_rel': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'win_x64_gn': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'win'},
      },
      'win_x64_gn_rel': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'win'},
      },
      'win_baremetal': {
        'recipe_config': 'webrtc_baremetal',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'win_drmemory_light': {
        'recipe_config': 'webrtc',
        'chromium_apply_config': ['drmemory_light'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'win_drmemory_full': {
        'recipe_config': 'webrtc',
        'chromium_apply_config': ['drmemory_full'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'win'},
      },
      'mac': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'mac_rel': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'mac_x64': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'mac_x64_rel': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'mac_x64_gn': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'mac_x64_gn_rel': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'mac_asan': {
        'recipe_config': 'webrtc_clang',
        'chromium_apply_config': ['asan'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'mac_baremetal': {
        'recipe_config': 'webrtc_baremetal',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'mac'},
      },
      'ios': {
        'recipe_config': 'webrtc_ios32',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 32,
          'TARGET_ARCH': 'arm',
          'TARGET_PLATFORM': 'ios',
        },
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'ios_rel': {
        'recipe_config': 'webrtc_ios32',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 32,
          'TARGET_ARCH': 'arm',
          'TARGET_PLATFORM': 'ios',
        },
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'ios_arm64': {
        'recipe_config': 'webrtc_ios64',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
          'TARGET_ARCH': 'arm',
          'TARGET_PLATFORM': 'ios',
        },
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'ios_arm64_rel': {
        'recipe_config': 'webrtc_ios64',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
          'TARGET_ARCH': 'arm',
          'TARGET_PLATFORM': 'ios',
        },
        'bot_type': 'builder',
        'testing': {'platform': 'mac'},
      },
      'linux': {
        'recipe_config': 'webrtc_parallel',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'linux_rel': {
        'recipe_config': 'webrtc_parallel',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'linux_gn': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_BITS': 64,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
      'linux_gn_rel': {
        'recipe_config': 'webrtc',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
      'linux_asan': {
        'recipe_config': 'webrtc_clang',
        'chromium_apply_config': ['asan', 'lsan'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'linux_memcheck': {
        'recipe_config': 'webrtc',
        'chromium_apply_config': ['memcheck'],
        'gclient_apply_config': ['valgrind'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'linux_msan': {
        'recipe_config': 'webrtc_clang',
        'chromium_apply_config': ['msan', 'msan_full_origin_tracking',
                                  'instrumented_libraries'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'linux_tsan2': {
        'recipe_config': 'webrtc_clang',
        'chromium_apply_config': ['tsan2'],
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'linux_baremetal': {
        'recipe_config': 'webrtc_baremetal',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'android': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'android_rel': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'android_clang': {
        'recipe_config': 'webrtc_android_clang',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
      'android_arm64': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 64,
        },
        'bot_type': 'builder_tester',
        'testing': {'platform': 'linux'},
      },
      'android_gn': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Debug',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
      'android_gn_rel': {
        'recipe_config': 'webrtc_android',
        'chromium_config_kwargs': {
          'BUILD_CONFIG': 'Release',
          'TARGET_PLATFORM': 'android',
          'TARGET_ARCH': 'arm',
          'TARGET_BITS': 32,
        },
        'chromium_apply_config': ['webrtc_gn'],
        'bot_type': 'builder',
        'testing': {'platform': 'linux'},
      },
    },
  },
})

