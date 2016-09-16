#!/usr/bin/env python
# Copyright 2016 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Clang-format 3-way merge driver.

"""

import subprocess
import sys

import clang_format

def main():
  if len(sys.argv) < 6:
    print('usage: %s <base> <current> <others> <ignored> <path in the tree>' %
        sys.argv[0])
    sys.exit(1)

  base, current, others, _, file_name_in_tree = sys.argv[1:6]
  print '\nRunning clang-format 3-way merge driver on ' + file_name_in_tree

  try:
    tool = clang_format.FindClangFormatToolInChromiumTree()
    for fpath in base, current, others:
      subprocess.call([tool, '-i', '--style=chromium', fpath])
  except clang_format.NotFoundError, e:
    print e
    print 'Failed to find clang-format. Falling-back on standard 3-way merge'

  return subprocess.call(['git', 'merge-file', '-Lcurrent', '-Lbase', '-Lother',
                          current, base, others])

if __name__ == '__main__':
  sys.exit(main())
