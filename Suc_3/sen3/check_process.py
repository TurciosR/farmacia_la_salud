#!/usr/bin/python
import os


class Process:
    def get_process(self):
        rp = os.popen("ps ax |grep sentinel.py")
        res = rp.read().split("\n")
        return str(len(res))

# proc = Process()
# print proc.get_process()
