import logging
NEW = (
    '--- /dev/null\n'
    '+++ foo\n'
    '@@ -0,0 +1 @@\n'
    '+bar\n')


    self.assertEquals(c.is_binary, False)
    self.assertEquals(c.is_delete, True)
    self.assertEquals(c.is_new, False)
    self.assertEquals(c.is_binary, True)
    self.assertEquals(c.is_delete, True)
    self.assertEquals(c.is_new, False)
    c = patch.FilePatchBinary('foo', 'data', [], is_new=False)
    self.assertEquals(c.filename, 'foo')
    self.assertEquals(c.is_delete, False)
    self.assertEquals(c.is_new, False)
    self.assertEquals(c.get(), 'data')

  def testFilePatchBinaryNew(self):
    c = patch.FilePatchBinary('foo', 'data', [], is_new=True)
    self.assertEquals(c.is_binary, True)
    self.assertEquals(c.is_delete, False)
    self.assertEquals(c.is_new, True)
    self.assertEquals(c.is_binary, False)
    self.assertEquals(c.is_delete, False)
    self.assertEquals(c.is_new, False)

  def testFilePatchDiffHeaderMode(self):
    self.assertEquals(c.is_binary, False)
    self.assertEquals(c.is_delete, False)
    self.assertEquals(c.is_new, False)

  def testFilePatchDiffHeaderModeIndex(self):
    self.assertEquals(c.is_binary, False)
    self.assertEquals(c.is_delete, False)
    self.assertEquals(c.is_new, False)
  def testFilePatchDiffSvnNew(self):
    # The code path is different for git and svn.
    c = patch.FilePatchDiff('foo', NEW, [])
    self.assertEquals(c.filename, 'foo')
    self.assertEquals(c.is_binary, False)
    self.assertEquals(c.is_delete, False)
    self.assertEquals(c.is_git_diff, False)
    self.assertEquals(c.is_new, True)
    self.assertEquals(c.patchlevel, 0)
    self.assertEquals(c.get(), NEW)

  def testFilePatchDiffGitNew(self):
    # The code path is different for git and svn.
    c = patch.FilePatchDiff('foo', GIT_NEW, [])
    self.assertEquals(c.filename, 'foo')
    self.assertEquals(c.is_binary, False)
    self.assertEquals(c.is_delete, False)
    self.assertEquals(c.is_git_diff, True)
    self.assertEquals(c.is_new, True)
    self.assertEquals(c.patchlevel, 1)
    self.assertEquals(c.get(), GIT_NEW)

  def testFilePatchDiffBad(self):
  def testFilePatchDiffEmpty(self):
  def testFilePatchDiffNone(self):
    except patch.UnsupportedPatchFormat, e:
      self.assertEquals(
          "Can't process patch for file foo.\nUnexpected diff: chrome/file.cc.",
          str(e))

  def testFilePatchDiffBadHeader(self):
    try:
      diff = (
        '+++ b/foo\n'
        '@@ -0,0 +1 @@\n'
        '+bar\n')
      patch.FilePatchDiff('foo', diff, [])
      self.fail()
  def testFilePatchDiffBadGitHeader(self):
    try:
      diff = (
        'diff --git a/foo b/foo\n'
        '+++ b/foo\n'
        '@@ -0,0 +1 @@\n'
        '+bar\n')
      patch.FilePatchDiff('foo', diff, [])
      self.fail()
    except patch.UnsupportedPatchFormat:
      pass

  def testFilePatchDiffBadHeaderReversed(self):
    try:
      diff = (
        '+++ b/foo\n'
        '--- b/foo\n'
        '@@ -0,0 +1 @@\n'
        '+bar\n')
      patch.FilePatchDiff('foo', diff, [])
      self.fail()
    except patch.UnsupportedPatchFormat:
      pass

  def testFilePatchDiffGitBadHeaderReversed(self):
    try:
      diff = (
        'diff --git a/foo b/foo\n'
        '+++ b/foo\n'
        '--- b/foo\n'
        '@@ -0,0 +1 @@\n'
        '+bar\n')
      patch.FilePatchDiff('foo', diff, [])
      self.fail()
    except patch.UnsupportedPatchFormat:
      pass

  def testFilePatchDiffInvalidGit(self):
        patch.FilePatchBinary('bar', 'data', [], is_new=False),
  def testRelPathEmpty(self):
    patches = patch.PatchSet([
        patch.FilePatchDiff('chrome\\file.cc', SVN_PATCH, []),
        patch.FilePatchDelete('other\\place\\foo', True),
    ])
    patches.set_relpath('')
    self.assertEquals(
        ['chrome/file.cc', 'other/place/foo'],
        [f.filename for f in patches])

  def testOnlyHeader(self):
    p = patch.FilePatchDiff('file_a', '--- file_a\n+++ file_a\n', [])
    self.assertTrue(p)

  def testSmallest(self):
    p = patch.FilePatchDiff(
        'file_a', '--- file_a\n+++ file_a\n@@ -0,0 +1 @@\n+foo\n', [])
    self.assertTrue(p)

  def testInverted(self):
    try:
      patch.FilePatchDiff(
        'file_a', '+++ file_a\n--- file_a\n@@ -0,0 +1 @@\n+foo\n', [])
      self.fail()
    except patch.UnsupportedPatchFormat:
      pass

  def testInvertedOnlyHeader(self):
    try:
      patch.FilePatchDiff('file_a', '+++ file_a\n--- file_a\n', [])
      self.fail()
    except patch.UnsupportedPatchFormat:
      pass

  def testRenameOnlyHeader(self):
    p = patch.FilePatchDiff('file_b', '--- file_a\n+++ file_b\n', [])
    self.assertTrue(p)

  def testGitCopy(self):
    diff = (
        'diff --git a/wtf b/wtf2\n'
        'similarity index 98%\n'
        'copy from wtf\n'
        'copy to wtf2\n'
        'index 79fbaf3..3560689 100755\n'
        '--- a/wtf\n'
        '+++ b/wtf2\n'
        '@@ -1,4 +1,4 @@\n'
        '-#!/usr/bin/env python\n'
        '+#!/usr/bin/env python1.3\n'
        ' # Copyright (c) 2010 The Chromium Authors. All rights reserved.\n'
        ' # blah blah blah as\n'
        ' # found in the LICENSE file.\n')
    p = patch.FilePatchDiff('wtf2', diff, [])
    self.assertTrue(p)

  def testGitExe(self):
    diff = (
        'diff --git a/natsort_test.py b/natsort_test.py\n'
        'new file mode 100755\n'
        '--- /dev/null\n'
        '+++ b/natsort_test.py\n'
        '@@ -0,0 +1,1 @@\n'
        '+#!/usr/bin/env python\n')
    self.assertEquals(
        [('svn:executable', '*')],
        patch.FilePatchDiff('natsort_test.py', diff, []).svn_properties)
    diff = (
        'diff --git a/natsort_test.py b/natsort_test.py\n'
        'new file mode 100644\n'
        '--- /dev/null\n'
        '+++ b/natsort_test.py\n'
        '@@ -0,0 +1,1 @@\n'
        '+#!/usr/bin/env python\n')
    self.assertEquals(
        [], patch.FilePatchDiff('natsort_test.py', diff, []).svn_properties)

  logging.basicConfig(level=
      [logging.WARNING, logging.INFO, logging.DEBUG][
        min(2, sys.argv.count('-v'))])