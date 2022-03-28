#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os
import random
import time
import conexion
import json
import requests
import sys
import time
import urllib2
import math
sys.setrecursionlimit(10**6)

class stock:
    def __init__(self):
        print time.strftime("%c")
        self.conex = conexion.Database("sistema")
        sql = "SELECT id_sucursal, hash FROM access_conf WHERE id_conf = %s"
        data_param = ("1",)
        type_sql = "S"
        rows = self.conex.query(sql, data_param, type_sql)
        data = rows[0]
        self.id_sucursal = data[0]
        self.hash = data[1]

        sql = "SELECT ruta FROM rutas WHERE descripcion = %s"
        data_param = ("stock",)
        type_sql = "S"
        rows = self.conex.query(sql, data_param, type_sql)
        data = rows[0]
        self.stock = data[0]


    def check_connect(self):
        try:
            urllib2.urlopen("http://demos.apps-oss.com", timeout=60)
            return True
        except urllib2.URLError as err:
            return False

    def get_stock(self):
        sql = """SELECT producto.unique_id,stock.stock FROM producto JOIN stock ON stock.id_producto=producto.id_producto"""
        data_param = ""
        type_sql = "S"
        rows = self.conex.query(sql, data_param, type_sql)
        id_sucursal = self.id_sucursal
        num_rows = len(rows)
	print "obteniendo stocks"
        if num_rows > 0:
            print "stock obtenido"
            stock_send=[ ]
            for row in rows:
                unique_id = row[0]
                stock = row[1]
                stock_send.append({"u":str(unique_id),"s":str(stock)})

            print "Enviado stocks al servidor"

            data = {
                    "process": "insert_Stocks",
                    "listado":  json.dumps(stock_send),
                    "id_sucursal": str(self.id_sucursal)
                    }
            try:
                post = requests.post(self.stock, data)
                print post.text
            except ValueError:
                print "No se han podido enviar los datos"


pid = str(os.getpid())
pidfile = "/tmp/stock.pid"
basedir = '/tmp'
filename = 'stock.pid'
if os.path.isfile(pidfile):
    print "%s already exists, exiting" % pidfile
    limit = 5 * 60
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
        print "Removed {} files.".format(count)
    else:
        print "%s already exists, exiting" % pidfile
        sys.exit()
file(pidfile, 'w').write(pid)
try:
    prime = stock()
    connect = prime.check_connect()
    if connect:
        prime.get_stock()
    else:
        print "No conecta"
except ValueError:
    print "error de ejecucion"
except:
    print "error no contemplado previamente debug necesario"
finally:
    os.unlink(pidfile)
