# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# This file is meant to be included into a target to provide a rule
# to build APK based test suites.
#
# To use this, create a gyp target with the following form:
# {
#   'target_name': 'test_suite_name_apk',
#   'type': 'none',
#   'variables': {
#     'test_suite_name': 'test_suite_name',  # string
#     'input_shlib_path' : '/path/to/test_suite.so',  # string
#     'input_jars_paths': ['/path/to/test_suite.jar', ... ],  # list
#   },
#   'includes': ['path/to/this/gypi/file'],
# }
#

{
  'dependencies': [
    '<(DEPTH)/base/base.gyp:base_java',
    '<(DEPTH)/tools/android/android_tools.gyp:android_tools',
  ],
  'variables': {
    'intermediate_dir': '<(PRODUCT_DIR)/<(test_suite_name)_apk/',
    'generate_native_test_stamp': '<(intermediate_dir)/generate_native_test.stamp',
  },
  'target_conditions': [
    ['_toolset == "target"', {
      'conditions': [
        ['OS == "android" and gtest_target_type == "shared_library"', {
          'actions': [{
            'action_name': 'apk_<(test_suite_name)',
            'message': 'Building <(test_suite_name) test apk.',
            'inputs': [
              '<(DEPTH)/testing/android/AndroidManifest.xml',
              '<(DEPTH)/testing/android/generate_native_test.py',
              '<(input_shlib_path)',
              '>@(input_jars_paths)',
            ],
            'outputs': [
              '<(generate_native_test_stamp)',
            ],
            'action': [
              '<(DEPTH)/testing/android/generate_native_test.py',
              '--native_library',
              '<(input_shlib_path)',
              '--output',
              '<(intermediate_dir)',
              '--strip-binary=<(android_strip)',
              '--app_abi',
              '<(android_app_abi)',
              '--stamp-file',
              '<(generate_native_test_stamp)',
              '--no-compile',
            ],
          },
          {
            'action_name': 'ant_apk_<(test_suite_name)',
            'message': 'Building <(test_suite_name) test apk.',
            'inputs': [
              '<(DEPTH)/build/android/gyp/util/build_utils.py',
              '<(DEPTH)/build/android/gyp/ant.py',
              '<(generate_native_test_stamp)',
            ],
            'outputs': [
              '<(PRODUCT_DIR)/<(test_suite_name)_apk/<(test_suite_name)-debug.apk',
            ],
            'action': [
              'python', '<(DEPTH)/build/android/gyp/ant.py',
              '-quiet',
              '-DPRODUCT_DIR=<(ant_build_out)',
              '-DANDROID_SDK=<(android_sdk)',
              '-DANDROID_SDK_ROOT=<(android_sdk_root)',
              '-DANDROID_SDK_TOOLS=<(android_sdk_tools)',
              '-DANDROID_SDK_VERSION=<(android_sdk_version)',
              '-DANDROID_GDBSERVER=<(android_gdbserver)',
              '-DCHROMIUM_SRC=<(ant_build_out)/../..',
              '-DINPUT_JARS_PATHS=>(input_jars_paths)',
              '-DAPP_ABI=<(android_app_abi)',
              '-buildfile', '<(intermediate_dir)/native_test_apk.xml',
            ],
          }],
        }],  # 'OS == "android" and gtest_target_type == "shared_library"
      ],  # conditions
    }],
  ],  # target_conditions
}
