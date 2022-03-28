#!/usr/bin/python
import os
import time
import sys

"""
Remove pidfile in *basedir* not accessed within *limit* minutes
:param basedir: directory to clean
:param limit: minutes
:param filename: archive name
"""

basedir = '/tmp'
filename = 'mydaemon.pid'
pidfile = os.path.join(basedir, filename)
if os.path.isfile(pidfile):

    limit = 15 * 60
    atime_limit = time.time() - limit
    print filename
    print basedir
    count = 0
    path = os.path.join(basedir, filename)
    print path
    if os.path.getatime(path) < atime_limit:
        os.remove(path)
        count += 1
        print("Removed {} files.".format(count))
    else:
        print "%s already exists, exiting" % pidfile
        sys.exit()

print 'ejecuta este codigo'
