# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# This file was generated from
# scripts/tools/buildbot_tool_templates/master_site_config.py
# by "../../build/scripts/tools/buildbot-tool gen .".
# DO NOT EDIT BY HAND!


"""ActiveMaster definition."""

from config_bootstrap import Master

class ClientV8Clusterfuzz(Master.Master3a):
  project_name = 'ClientV8Clusterfuzz'
  master_port = 21303
  slave_port = 31303
  master_port_alt = 26303
  buildbot_url = 'https://build.chromium.org/p/client.v8.clusterfuzz/'
  buildbucket_bucket = None
  service_account_file = None
  # To enable outbound pubsub event streaming.
  pubsub_service_account_file = 'service-account-luci-milo.json'
  pubsub_topic = 'projects/luci-milo/topics/public-buildbot'
  name = 'client.v8.clusterfuzz'
