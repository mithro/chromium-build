#!/usr/bin/env python
# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import atexit
import collections
import imp
import json
import os
import re
import signal
import socket
import sys
import tempfile
import threading
import unittest

from cStringIO import StringIO
from subprocess import check_call, Popen, PIPE
from textwrap import dedent


BUILD_DIR = os.path.realpath(os.path.join(
    os.path.dirname(__file__), '..'))
BOT_UPDATE_PATH = os.path.join(BUILD_DIR, 'scripts', 'slave', 'bot_update.py')
SLAVE_DIR = os.path.join(BUILD_DIR, 'slave')
CACHE_DIR = os.path.join(SLAVE_DIR, 'cache_dir')

chromium_utils = imp.load_source(
    'chromium_utils',
    os.path.join(BUILD_DIR, 'scripts', 'common', 'chromium_utils.py'))


def find_free_port():
  '''Find an avaible port on localhost.'''
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(('', 0))
  port = sock.getsockname()[1]
  sock.close()
  return port


class LocalGitServer(object):
  '''A git server daemon running on localhost.'''
  def __init__(self, root):
    self.root = root
    self.port = find_free_port()
    self.url = 'git://localhost:%s' % self.port
    self.devnull = open(os.devnull, 'w')
    os.makedirs(root)
    self.proc = Popen(
        ['git', 'daemon', '--export-all', '--reuseaddr', '--listen=localhost',
         '--port=%d' % self.port, '--base-path=%s' % root,  root],
        stdout=self.devnull, stderr=self.devnull)

  def stop(self):
    try:
      self.proc.terminate()
      self.devnull.close()
    except Exception:
      pass


class LocalSvnServer(object):
  '''An svnserve daemon running on localhost.'''
  def __init__(self, root):
    self.root = root
    self.pid_file = os.path.join(root, 'svnserve.pid')
    self.port = find_free_port()
    self.url = 'svn://localhost:%d/svn' % self.port
    self.devnull = open(os.devnull, 'w')
    os.makedirs(self.root)
    check_call(
        ['svnadmin', 'create', root], stdout=self.devnull, stderr=self.devnull)
    with open(os.path.join(root, 'conf', 'svnserve.conf'), 'w') as fh:
      fh.write(dedent('''\
          [general]
          anon-access = write
          '''))
    check_call(
        ['svnserve', '-d', '-r', self.root, '--listen-port=%d' % self.port,
         '--pid-file=%s' % self.pid_file],
        stdout=self.devnull, stderr=self.devnull)
    with open(self.pid_file) as fh:
      self.pid = int(fh.read().strip())
    atexit.register(self.stop)

  def stop(self):
    try:
      if self.pid:
        os.kill(self.pid, signal.SIGKILL)
        self.pid = None
      if self.devnull:
        self.devnull.close()
        self.devnull = None
    except Exception:
      pass


class BotUpdateTest(unittest.TestCase):

  '''
  POPULATE_DATA = {
    'TEST METHOD': [
      ('REPO NAME', [
        ('COMMENT', { 'FILE NAME': 'FILE CONTENTS', ... }),  # First commit
        ('COMMENT', { 'FILE NAME': 'FILE CONTENTS', ... }),  # Second commit
        ...
      ]),
      ...
    ],
    ...
  }

  'FILE CONTENTS' can be a string template using named parameters.  As each
  repo is processed, the dict used to complete template parameters is
  updated with the url to the repo.  As each commit is processed, the dict
  is updated with the revision of the resulting commit.  After this is
  processed:

      ('MyRepo', [
        { 'file1.txt' : 'Some contents.' },
        { 'file2.txt' : 'Some other contents.' },
      ]),

  ... the template completion dict will be updated with these values:

    { 'MyRepo_url': 'FULL URL TO REPO',
      'MyRepo_revision_0': 'REVISION OF FIRST COMMIT',
      'MyRepo_revision_1': 'REVISION OF SECOND COMMIT' }

  ... which can be referred to in subsequent entries:

    ('MyOtherRepo', [
      { 'url.txt': 'The url of MyRepo is %(MyRepo_url)s.' },
      { 'rev.txt': 'The first revision in MyRepo is %(MyRepo_revision_0)s.' }
    ])

  When SVN_POPULATE_DATA is processed, it additionally creates a git mirror
  of each repo, and adds template parameters for the git mirror url and
  git revisions:

    ('MyOtherRepo', [
      { 'git_url.txt': 'The git mirror url is %(MyRepo_git_url)s.' },
      { 'git_rev.txt': 'The first git hash is %(MyRepo_git_revision_0)s.' }
    ])

  NOTE that commits are additive; subsequent commits don't have to contain the
  contents of files from previous commits, and there is no syntax for deletion.
  In the example, after MyRepo is processed, its tip-of-tree will contain two
  files: [file1.txt, file2.txt].
  '''

  SVN_POPULATE_DATA = {
    'test_002_svn': [
      ('dep1', [
        ('First commit', { 'path1/file1.txt': 'dep1 file 1 line 1.' }),
        ('Second commit', { 'path2/file2.txt': 'dep1 file 2 line 1.' }),
      ]),
      ('dep2', [
        ('First commit', { 'path1/file1.txt': 'dep2 file 1 line 1.' }),
        ('Second commit', { 'path2/file2.txt': 'dep2 file 2 line 1.' }),
      ]),
      ('top', [
        ('DEPS commit', {
          'file1.txt': 'top file 1 line 1.',
          'DEPS': dedent('''\
              vars = {
                'dep1_revision': '%(dep1_revision_0)s',
                'dep2_revision': '%(dep2_revision_1)s',
              }
              deps = {
                'top/ext/dep1': '%(dep1_url)s@' + Var('dep1_revision'),
                'top/ext/dep2': '%(dep2_url)s@' + Var('dep2_revision'),
              }
              ''') }),
        ('.DEPS.git commit', { '.DEPS.git': dedent('''\
             vars = {
               'dep1_revision': '%(dep1_git_revision_0)s',
               'dep2_revision': '%(dep2_git_revision_1)s',
             }
             deps = {
               'top/ext/dep1': '%(dep1_mirror_url)s@' + Var('dep1_revision'),
               'top/ext/dep2': '%(dep2_mirror_url)s@' + Var('dep2_revision'),
             }
             ''') }),
      ]),
    ],
  }

  GIT_POPULATE_DATA = {
    'test_001_simple': [
      ('dep1', [
        ('First commit', { 'path1/file1.txt': 'dep1 file 1 line 1.' }),
        ('Second commit', { 'path2/file2.txt': 'dep1 file 2 line 1.' }),
      ]),
      ('dep2', [
        ('First commit', { 'path1/file1.txt': 'dep2 file 1 line 1.' }),
        ('Second commit', { 'path2/file2.txt': 'dep2 file 2 line 1.' }),
      ]),
      ('top', [
        ('DEPS commit', {
          'file1.txt': 'top file 1 line 1.',
          'DEPS': dedent('''\
              vars = {
                'dep1_revision': '%(dep1_revision_0)s',
                'dep2_revision': '%(dep2_revision_1)s',
              }
              deps = {
                'top/ext/dep1': '%(dep1_url)s@' + Var('dep1_revision'),
                'top/ext/dep2': '%(dep2_url)s@' + Var('dep2_revision'),
              }
              ''') }),
      ]),
    ],
  }

  # Used to store the result of a subprocess invocation.
  SUBPROCESS_RESULT = collections.namedtuple(
      'SUBPROCESS_RESULT', ['cmd', 'cwd', 'status', 'stdout', 'stderr'])

  # Used to store information about a repository.
  #   path: relative path from the repository root.
  #   url: canonical url for repository.
  #   populate_dir: A working dir used to populate the repository.
  #   serve_dir: Directory on localhost where the repository is hosted.
  #   revisions: Revision data from *_POPULATE_DATA.
  REPO = collections.namedtuple(
      'REPO',
      ['path', 'url', 'populate_dir', 'serve_dir', 'revisions'])

  @staticmethod
  def dump_subproc(result):
    '''Pretty-prints a SUBPROCESS_RESULT object.'''
    sep = '\n' + ('#' * 80) + '\n'
    print sep, 'Subprocess failed with status %d.\n' % result.status
    print result.cmd, '\n\n... in %s\n' % result.cwd
    print sep, '# stdout\n', sep, result.stdout, '\n'
    print sep, '# stderr\n', sep, result.stderr, '\n', sep

  def subproc(self, cmd, cwd=None, stdin=None, timeout=15):
    '''Runs a subprocess with a hard time limit.'''
    if not cwd:
      cwd = self.workdir
    stdin_arg = PIPE if stdin else None
    p = Popen(cmd, stdin=stdin_arg, stdout=PIPE, stderr=PIPE, cwd=cwd)
    def _thread_main():
      thr = threading.current_thread()
      (stdout, stderr) = p.communicate(stdin)
      thr.stdout = stdout
      thr.stderr = stderr
    thr = threading.Thread(target=_thread_main)
    thr.daemon = True
    thr.start()
    thr.join(timeout)
    if thr.isAlive():
      p.terminate()
      msg = 'Subprocess timed out after %d seconds:\n%r' % (timeout, cmd)
      self.fail(msg)
    return self.SUBPROCESS_RESULT(
        cmd, cwd, p.returncode, thr.stdout, thr.stderr)

  def assertSubproc(self, cmd, cwd=None, stdin=None, timeout=15):
    '''Runs a subprocess and asserts that it exits with zero status.'''
    result = self.subproc(cmd, cwd, stdin, timeout)
    self.assertEqual(result.status, 0)
    return result

  @staticmethod
  def get_files(d):
    '''Walks a directory tree, skipping any .git directories, and return all
    regular files in it.
    '''
    result = []
    for dirpath, dirnames, filenames in os.walk(d):
      for f in filenames:
        result.append(
            os.path.join(dirpath.replace(d, '').lstrip('/'), f))
      try:
        dirnames.remove('.git')
      except ValueError:
        pass
    return result

  @classmethod
  def setUpClass(cls):
    cls.server_root = tempfile.mkdtemp(prefix=cls.__name__)
    cls.git_server = LocalGitServer(os.path.join(cls.server_root, 'git'))
    cls.svn_server = LocalSvnServer(os.path.join(cls.server_root, 'svn'))

  @classmethod
  def tearDownClass(cls):
    try:
      for d in os.listdir(CACHE_DIR):
        try:
          if d.lower().startswith(
              'localhost:%d-botupdatetest' % cls.git_server.port):
            chromium_utils.RemoveDirectory(os.path.join(CACHE_DIR, d))
        except Exception:
          pass
    except Exception:
      pass
    cls.git_server.stop()
    cls.svn_server.stop()
    chromium_utils.RemoveDirectory(cls.server_root)

  def _populate_svn_repo(self, repo):
    '''Takes a repository described in SVN_POPULATE_DATA and instantiates it on
    the local svn server.
    '''
    self.template_dict['%s_url' % repo.path] = repo.url

    # Create the top-level path for the repository.
    self.assertSubproc(
        ['svn', 'mkdir', '-F', '-', '--parents', repo.url],
        stdin='Create parent directories.')

    # Populate revision history
    if not os.path.exists(os.path.dirname(repo.populate_dir)):
      os.makedirs(os.path.dirname(repo.populate_dir))
    self.assertSubproc(
        ['svn', 'co', repo.url, repo.populate_dir])
    for i, (comment, file_changes) in enumerate(repo.revisions):
      for filename, contents in file_changes.iteritems():
        contents = contents % self.template_dict
        filedir = os.path.join(repo.populate_dir, os.path.dirname(filename))
        if not os.path.exists(filedir):
          os.makedirs(filedir)
        with open(os.path.join(repo.populate_dir, filename), 'w') as fh:
          fh.write(contents)
        self.assertSubproc(
            ['svn', 'add', '--parents', filename], repo.populate_dir)
      self.assertSubproc(
          ['svn', 'commit', '-F', '-'],
          repo.populate_dir, stdin=comment)

      # Record revision number in template_dict
      self.assertSubproc(['svn', 'up'], repo.populate_dir)
      (_, _, _, svn_info, _) = self.subproc(['svn', 'info'], repo.populate_dir)
      svn_revision = [x[len('Revision: '):] for x in svn_info.splitlines()
                      if x.startswith('Revision: ')]
      self.assertEqual(len(svn_revision), 1)
      self.template_dict['%s_revision_%d' % (repo.path, i)] = svn_revision[0]

  def _populate_svn_git_mirror(self, repo, mirror):
    '''Mirrors an svn repository in to a git repository.'''
    self.template_dict['%s_mirror_url' % repo.path] = mirror.url

    # Create and initialize the repository on the server
    os.makedirs(mirror.serve_dir)
    self.assertSubproc(['git', 'init', '--bare'], mirror.serve_dir)

    # Populate the repository using git-svn
    os.makedirs(mirror.populate_dir)
    self.assertSubproc(['git', 'init'], mirror.populate_dir)
    self.assertSubproc(['git', 'svn', 'init', repo.url], mirror.populate_dir)
    self.assertSubproc(['git', 'svn', 'fetch'], mirror.populate_dir)
    self.assertSubproc(['git', 'push', mirror.serve_dir,
                        'refs/remotes/git-svn:refs/heads/master'],
                       mirror.populate_dir)

    # Update template_dict with the git hash corresponding to each svn commit.
    for i in xrange(len(repo.revisions)):
      svn_rev = self.template_dict['%s_revision_%d' % (repo.path, i)]
      result = self.assertSubproc(
          ['git', 'svn', 'find-rev', 'r%s' % svn_rev], mirror.populate_dir)
      sha1 = result.stdout.strip()
      self.assertTrue(re.match(r'[0-9a-fA-F]{40}', sha1))
      self.template_dict['%s_git_revision_%d' % (repo.path, i)] = sha1

  def _populate_git_repo(self, repo):
    '''Populates a pure-git repository as defined in GIT_POPULATE_DATA.'''
    self.template_dict['%s_url' % repo.path] = repo.url + '.git'

    # Create and initialize the repository on the server
    os.makedirs(repo.serve_dir)
    self.assertSubproc(['git', 'init', '--bare'], repo.serve_dir)

    # Populate repository with commits
    os.makedirs(repo.populate_dir)
    self.assertSubproc(['git', 'init'], repo.populate_dir)
    for i, (comment, file_changes) in enumerate(repo.revisions):
      for filename, contents in file_changes.iteritems():
        contents = contents % self.template_dict
        filedir = os.path.join(repo.populate_dir, os.path.dirname(filename))
        if not os.path.exists(filedir):
          os.makedirs(filedir)
        with open(os.path.join(repo.populate_dir, filename), 'w') as fh:
          fh.write(contents)
        self.assertSubproc(['git', 'add', filename], repo.populate_dir)
      self.assertSubproc(
          ['git', 'commit', '-F', '-'], repo.populate_dir, stdin=comment)
      result = self.assertSubproc(
          ['git', 'rev-parse', 'HEAD'], repo.populate_dir)
      sha1 = result.stdout.strip()
      self.assertTrue(re.match(r'[0-9a-fA-F]{40}', sha1))
      self.template_dict['%s_revision_%d' % (repo.path, i)] = sha1
    self.assertSubproc(['git', 'push', repo.serve_dir,
                        'HEAD:refs/heads/master'], repo.populate_dir)

  def populate_svn(self):
    '''Populates the local svn server with the repositories described in
    SVN_POPULATE_DATA for the current test method, and then creates git mirrors
    of the repositories on the local git server.

    The repository name is always prefixed with the test class and test method
    name being run, for disambiguation.  For example, if the method
    BotUpdateTest.test_999_horse defines a repo named 'feathers', it will be
    instantiated as <svn root>/BotUpdateTest/test_999_horse/feathers.
    '''
    test_prefix_parts = self.test_prefix.split('.')
    self.template_dict.update({
       'svn_server_url': self.svn_server.url,
       'test_prefix': self.test_prefix,
       'test_name': self.test_name,
    })
    for repo, revisions in self.SVN_POPULATE_DATA.get(self.test_name, []):
      repo_parts = repo.split('/')
      url = '/'.join(
          [self.svn_server.url] + test_prefix_parts + repo_parts)
      git_url = '/'.join(
          [self.git_server.url] + test_prefix_parts + repo_parts) + '.git'
      populate_dir = os.path.join(*([self.workdir] + repo_parts))
      git_populate_dir = populate_dir + '-mirror'
      git_serve_dir = os.path.join(
          *([self.git_server.root] + test_prefix_parts + repo_parts)) + '.git'
      repo = self.REPO(repo, url, populate_dir, None, revisions)
      mirror = self.REPO(
          repo, git_url, git_populate_dir, git_serve_dir, revisions)
      self._populate_svn_repo(repo)
      self._populate_svn_git_mirror(repo, mirror)

  def populate_git(self):
    '''Populates the local git server with the repositories described in
    GIT_POPULATE_DATA for the current test method.

    The repository name is always prefixed with the test class and test method
    name being run, for disambiguation.  For example, if the method
    BotUpdateTest.test_999_horse defines a repo named 'feathers', it will be
    instantiated as <git root>/BotUpdateTest/test_999_horse/feathers.
    '''
    test_prefix_parts = self.test_prefix.split('.')
    self.template_dict.update({
       'git_server_url': self.git_server.url,
       'test_prefix': self.test_prefix,
       'test_name': self.test_name,
    })
    for repo, revisions in self.GIT_POPULATE_DATA.get(self.test_name, []):
      if repo.endswith('.git'):
        repo = repo[:-4]
      repo_parts = repo.split('/')
      url = '/'.join([self.git_server.url] + test_prefix_parts + repo_parts)
      populate_dir = os.path.join(*([self.workdir] + repo_parts))
      serve_dir = os.path.join(
          *([self.git_server.root] + test_prefix_parts + repo_parts)) + '.git'
      repo = self.REPO(repo, url, populate_dir, serve_dir, revisions)
      self._populate_git_repo(repo)

  def setUp(self):
    self.test_prefix = self.id().lstrip('__main__.')
    self.test_name = self.test_prefix.split('.')[-1]
    self.workdir = tempfile.mkdtemp(dir=SLAVE_DIR, prefix=self.test_prefix)
    self.builddir = os.path.join(self.workdir, 'build')
    os.mkdir(self.builddir)
    self.bu_args = [
        BOT_UPDATE_PATH, '--force', '--output_json',
        os.path.join(self.builddir, 'out.json'), '--master',
        '%s_master' % self.test_name, '--builder_name',
        '%s_builder' % self.test_name, '--slave_name',
        '%s_slave' % self.test_name ]
    self.template_dict = {}
    self.populate_svn()
    self.populate_git()

  def tearDown(self):
    chromium_utils.RemoveDirectory(self.workdir)

  def run_bot_update(self, tweak_module_func=None):
    '''Runs the main() method of bot_update.py.

    This emulates a subprocess call, without actually shelling out.  That makes
    it easier to debug tests, as a debugger can step directly into
    bot_update.py.

    tweak_module_func can be used to modify the bot_udpate module before
    main() is invoked.  Since the module is unloaded at the end of this method,
    tweaks do not persist between invocations.
    '''

    old_sys = (sys.argv, sys.stdout, sys.stderr)
    sys.argv = self.bu_args
    sys.stdout = StringIO()
    sys.stderr = StringIO()
    os.chdir(self.builddir)
    bot_update = imp.load_source('bot_update', BOT_UPDATE_PATH)
    if tweak_module_func:
      tweak_module_func(bot_update)
    try:
      status = bot_update.main()
      if status is None:
        status = 0
    except Exception:
      status = 1
    del sys.modules['bot_update']
    del bot_update
    (stdout, stderr) = (sys.stdout, sys.stderr)
    (sys.argv, sys.stdout, sys.stderr) = old_sys
    return self.SUBPROCESS_RESULT(self.bu_args, self.builddir, status,
                                  stdout.getvalue(), stderr.getvalue())

  def test_001_simple(self):
    '''Tests a git solution with git-style DEPS, and no .DEPS.git.'''
    solution = {
        'name': 'top',
        'url': '%s/BotUpdateTest/test_001_simple/top.git' % self.git_server.url,
        'deps_file': 'DEPS'
    }
    gclient_spec = 'solutions=[%r]' % solution
    self.bu_args.extend([
        '--post-flag-day',
        '--specs', gclient_spec,
        '--revision', self.template_dict['top_revision_0']])
    result = self.run_bot_update()
    if bool(result.status):
      self.dump_subproc(result)
      self.fail('bot_update.py failed')
    expected_files = [
        'DEPS',
        'file1.txt',
        'ext/dep1/path1/file1.txt',
        'ext/dep2/path1/file1.txt',
        'ext/dep2/path2/file2.txt',
    ]
    topdir = os.path.join(self.builddir, 'top')
    self.assertItemsEqual(expected_files, self.get_files(topdir))
    expected_json = {
        'root': 'top',
        'properties': {},
        'did_run': True,
        'patch_root': None
    }
    with open(os.path.join(self.builddir, 'out.json')) as fh:
      actual_json = json.load(fh)
    self.assertDictContainsSubset(expected_json, actual_json)

  def test_002_svn(self):
    '''Tests an svn-based solution with svn DEPS and git .DEPS.git.'''
    solution = {
        'name': 'top',
        'url': '%s/BotUpdateTest/test_002_svn/top' % self.svn_server.url,
        'deps_file': 'DEPS'
    }
    gclient_spec = 'solutions=[%r]' % solution
    self.bu_args.extend([
        '--specs', gclient_spec,
        '--revision', self.template_dict['top_revision_1']])
    def _tweak(mod):
      repo_path = 'BotUpdateTest/test_002_svn/top'
      mod.RECOGNIZED_PATHS['/svn/%s' % repo_path] = (
          '/'.join((self.git_server.url, repo_path)) + '.git')
    result = self.run_bot_update(_tweak)
    if bool(result.status):
      self.dump_subproc(result)
      self.fail('bot_update.py failed')
    expected_files = [
        'DEPS',
        '.DEPS.git',
        'file1.txt',
        'ext/dep1/path1/file1.txt',
        'ext/dep2/path1/file1.txt',
        'ext/dep2/path2/file2.txt',
    ]
    topdir = os.path.join(self.builddir, 'top')
    self.assertItemsEqual(expected_files, self.get_files(topdir))
    expected_json = {
        'root': 'top',
        'properties': {},
        'did_run': True,
        'patch_root': None
    }
    with open(os.path.join(self.builddir, 'out.json')) as fh:
      actual_json = json.load(fh)
    self.assertDictContainsSubset(expected_json, actual_json)


if __name__ == '__main__':
  unittest.main()
