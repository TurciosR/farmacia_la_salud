#!/usr/bin/python

import os
import sys
import sentinel
import random
import time
sys.setrecursionlimit(10**6)
pid = str(os.getpid())

basedir = '/tmp'
filename = 'mydaemon.pid'
pidfile = os.path.join(basedir, filename)
if os.path.isfile(pidfile):

    limit = 90 * 60
    atime_limit = time.time() - limit
    print filename
    print basedir
    count = 0
    path = os.path.join(basedir, filename)
    print path
    # remueve el archivo pid si es muy viejo
    if os.path.getatime(path) < atime_limit:
        os.remove(path)
        count += 1
        print("Removed {} files.".format(count))
    else:
        print "%s already exists, exiting" % pidfile
        sys.exit()

try:
    file(pidfile, 'w').write(pid)
    prime = sentinel.Sentinel()
    connect = prime.check_connect()
    if connect:
        prime.check_server("check")
    else:
        print "No conecta"
except ValueError:
    print "error de ejecucion de sentinel"
except:
    print "Final de ejecucion"
finally:
    print "Borrar pid"
    os.unlink(pidfile)
