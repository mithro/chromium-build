# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""This file contains buildbucket service client."""

import json
import logging
import sys

from master import auth
from master.buildbucket import common
from master.deferred_resource import DeferredResource

from oauth2client.client import SignedJwtAssertionCredentials
import httplib2
import apiclient


BUILDBUCKET_HOSTNAME = 'cr-buildbucket.appspot.com'


def buildbucket_api_discovery_url(hostname=None):
  return (
      'https://%s/_ah/api/discovery/v1/apis/{api}/{apiVersion}/rest' % hostname)

def create_buildbucket_service(master, hostname=None):
  """Asynchronously creates buildbucket API resource.

  Returns:
    A DeferredResource as Deferred.
  """
  return DeferredResource.build(
      'buildbucket',
      'v1',
      http_factory=lambda: auth.create_http(master),
      discoveryServiceUrl=buildbucket_api_discovery_url(hostname),
      verbose=True,
      log_prefix=common.LOG_PREFIX,
  )
