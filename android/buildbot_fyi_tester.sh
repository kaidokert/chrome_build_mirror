#!/bin/bash -ex
# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# Buildbot annotator script for a FYI waterfall tester.
# Downloads and extracts a build from the builder and runs tests.

# SHERIFF: there should be no need to disable this bot.
# The FYI waterfall does not close the tree.

BB_SRC_ROOT="$(cd "$(dirname $0)/../.."; pwd)"
. "${BB_SRC_ROOT}/build/android/buildbot_functions.sh"

bb_baseline_setup "$BB_SRC_ROOT" "$@"
bb_install_build_deps "$BB_SRC_ROOT"
bb_extract_build
# TODO(ilevy): Reenable after we fix broken apk tests:
# base-unittests
#  -JNIAndroidTest.GetMethodIDFromClassNameCaching (crash)
# content-unittests
#  -AppCacheDatabaseTest.ReCreate (fail)
#  -AppCacheDatabaseTest.UpgradeSchema3to4 (crash)
# ipc-tests
#  -IPCChannelPosixTest.ResetState (fail)
#
# bb_run_apk_tests
