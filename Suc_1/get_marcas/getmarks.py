#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import urllib2
import urllib
import pycurl
import uuid
from datetime import date
from datetime import datetime
from datetime import timedelta

def check_connect():
    try:
        urllib2.urlopen("http://192.168.1.201/", timeout=10)
        return True
    except urllib2.URLError as err:
        return False

connect = check_connect()
if connect:
    print "Hay conexion a biometrico"
    try:
        hoy = datetime.now()
        antes = hoy + timedelta(days=-15)

        fin = hoy.strftime('%Y-%m-%d')
        fini = antes.strftime('%Y-%m-%d')
        print fini
        print fin

        uid = "";
        for x in range(0, 50):
            uid =  uid +"&uid="+str(x)
        archive = str("/home/user/get_marcas/marcas/")+str(uuid.uuid4())+str(".dat")
        file = open(archive,'wb')
        crl = pycurl.Curl()
        crl.setopt(crl.URL, 'http://192.168.1.201/form/Download')
        data = {
        'sdate': fini,
        'edate': fin,
        'period': '0',
        }
        pf = urllib.urlencode(data)
        crl.setopt(crl.POSTFIELDS, pf+uid)
        crl.setopt(crl.WRITEDATA, file)
        crl.perform()
        crl.close()
        file.close()

        #send data
        crl = pycurl.Curl()
        crl.setopt(crl.URL, 'http://farmasaludsv.com.sv/server/reciver.php')
        print archive
        values = [
             ('id_sucursal',"3"),
             ('file', (crl.FORM_FILE,str(archive)))
        ]
        crl.setopt(crl.HTTPPOST,values)
        crl.perform()
        crl.close()
    except ValueError:
        print "No Response"
else:
    print "No conecta"
