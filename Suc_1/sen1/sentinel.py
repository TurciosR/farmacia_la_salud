#!/usr/bin/python
# -*- coding: UTF-8 -*-

import conexion
import auth_client
import check_process
import json
import requests
import sys
import time
import urllib2
import math
sys.setrecursionlimit(10**6)


class Sentinel:
    def __init__(self):
        print time.strftime("%c")
        procss = check_process.Process()
        self.num_process = procss.get_process()
        self.conex = conexion.Database("sistema")
        sql = "SELECT ruta FROM rutas WHERE descripcion = %s"
        data_param = ("server",)
        type_sql = "S"
        rows = self.conex.query(sql, data_param, type_sql)
        data = rows[0]
        self.server = data[0]
        sql = "SELECT ruta FROM rutas WHERE descripcion = %s"
        data_param = ("local",)
        type_sql = "S"
        rows = self.conex.query(sql, data_param, type_sql)
        data = rows[0]
        self.local = data[0]
        sql = "SELECT id_sucursal, hash FROM access_conf WHERE id_conf = %s"
        data_param = ("1",)
        type_sql = "S"
        rows = self.conex.query(sql, data_param, type_sql)
        data = rows[0]
        self.id_sucursal = data[0]
        self.hash = data[1]
        auth = auth_client.Auth()
        self.auth_data = json.dumps(auth.get_data())

    def check_connect(self):
        try:
            urllib2.urlopen("http://farmasaludsv.com.sv", timeout=60)
            return True
        except urllib2.URLError as err:
            return False
        # return True

    def check_server(self, action):
        print "Check Server: "+str(action)
        data = {"hash": self.hash,
                "process": "availability",
                "num_process": self.num_process,
                "id_sucursal": self.id_sucursal,
                "action": action,
                "auth_data": self.auth_data
                }
        # print data
        try:
            post = requests.post(self.server, data)
            response = post.text
            print response
            if response == "available" or response == "crahsed-restart":
                self.upload_changes()
            elif response == "changes_availables":
                self.download_changes()
            elif response == "working":
                self.upload_changes()
                # print "Esta muerto"
            else:
                print "No hay mas cambios"
                sys.exit()
        except ValueError:
            print "No response en check server "

    def download_changes(self):
        data = {"hash": self.hash,
                "process": "search",
                "id_sucursal": self.id_sucursal,
                "auth_data": self.auth_data
                }
        try:
            post = requests.post(self.server, data)
            response = json.loads(post.text)
            table = response["table"]
            process = response["process"]
            data = response["data"]
            id_verf = response["id_verf"]
            id_server = response["id_server"]
            if table == "producto":
                self.download_productos(process, data, id_verf, id_server)
            elif table == "presentacion_producto":
                id_server_prod = response["id_server_prod"]
                self.download_presentacion_producto(process, data, id_verf, id_server, id_server_prod)
            elif table == "traslado":
                self.download_traslado(process, data, id_verf, id_server)
            elif table == "traslado_detalle_recibido":
                self.download_traslado_detalle_recibido(process, data, id_verf, id_server)
            else:
                self.download_gen(process, data, id_verf, id_server,table)
        except ValueError:
            print "No response download_changes"

    def download_productos(self, process, datas, id_verf, id_server):
        print "down productos "+process
        data = {"hash": self.hash,
                "process": process,
                "id_server": id_server,
                "table": "productos",
                "data": json.dumps(datas)
                }
        try:
            post = requests.post(self.local, data)
            response = post.text
            print response
            if response == "all changes commited":
                data1 = {"hash": self.hash,
                         "process": "confirm",
                         "id_sucursal": self.id_sucursal,
                         "id_verf": id_verf,
                         "auth_data": self.auth_data
                         }
                post1 = requests.post(self.server, data=data1)
                response1 = post1.text
                print response1
                connect = self.check_connect()
                if connect:
                    self.check_server("break")
            elif response == "sync_error":
                connect = self.check_connect()
                if connect:
                    self.check_server("break")
                else:
                    self.check_server("break")
        except ValueError:
            print "No Response download_productos"

    def download_presentacion_producto(self, process, datas, id_verf, id_server, id_server_prod):
        print "down presentacion productos "+process
        data = {"hash": self.hash,
                "process": process,
                "id_server": id_server,
                "id_server_prod": id_server_prod,
                "table": "presentacion_producto",
                "data": json.dumps(datas)
                }
        try:
            post = requests.post(self.local, data)
            response = post.text
            if response == "all changes commited":
                data1 = {"hash": self.hash,
                         "process": "confirm",
                         "id_sucursal": self.id_sucursal,
                         "id_verf": id_verf,
                         "auth_data": self.auth_data
                         }
                post1 = requests.post(self.server, data=data1)
                response1 = post1.text
                print response1
                connect = self.check_connect()
                if connect:
                    self.check_server("break")
            elif response == "sync_error":
                connect = self.check_connect()
                if connect:
                    self.check_server("break")
        except ValueError:
            print "No Response download_presentacion_producto"

    def upload_changes(self):
        print "Upload Changes"
        # aca se subiran los cambios solo de producto, traslado y presentacion_producto
        sql = """SELECT * FROM log_cambio_local WHERE subido="0" AND tabla IN ("producto","traslado","presentacion_producto") ORDER BY prioridad ASC"""
        data_param = ""
        type_sql = "S"
        rows = self.conex.query(sql, data_param, type_sql)

        num_rows = len(rows)

        if num_rows > 0:
            for row in rows:
                id_verf = row[0]
                process = row[2]
                table = row[3]
                print table
                id_primario = row[8]
                if table == "producto":
                    self.upload_productos(id_primario, process, id_verf)
                elif table == "presentacion_producto":
                    self.upload_presentacion_producto(id_primario, process, id_verf)
                elif table == "traslado":
                    self.upload_traslado(id_primario, process, id_verf)
                elif table == "traslado_detalle_recibido":
                    self.upload_traslado_detalle_recibido(id_primario, process, id_verf)
            connect = self.check_connect()
            if connect:
                self.check_server("break")

        # aca se subiran los updates de las tablas generadas por el sistema
        # si hay al menos un cambio disponible
        sql = """SELECT id_log_cambio FROM log_cambio_local WHERE subido="0" AND tabla NOT IN ("producto","traslado","presentacion_producto") ORDER BY prioridad ASC"""
        data_param = ""
        type_sql = "S"
        rows = self.conex.query(sql, data_param, type_sql)
        num_rows = len(rows)
        if num_rows > 0:
            json_size = 200
            division = float(num_rows)/float(json_size)
            # numero de post que se realizaran con un numero de datos definido
            nTimes = math.ceil(division)
            self.upload_gen(int(nTimes), json_size)

        # aca se subiran los inserts de las tablas catalogadas para replicacion
        sql = "SHOW TABLES"
        data_param = ""
        type_sql = "S"
        rows = self.conex.query(sql, data_param, type_sql)
        for row in rows:
            table = row[0]
            data = {"hash": self.hash,
                    "process": "constab",
                    "table": table
                    }
            try:
                post = requests.post(self.local, data)
                response = json.loads(post.text)
                result = table+" "+response["response"]
                print result
                if response["response"] == "OK":
                    array_json = json.dumps(response["data"])
                    count = response["count"]
                    pk = response["pk"]
                    print str(count)+" data to sync"
                    if count > 0:
                        data1 = {"hash": self.hash,
                                 "process": "sync",
                                 "table": table,
                                 "pk": pk,
                                 "data": array_json,
                                 "id_sucursal": self.id_sucursal,
                                 "auth_data": self.auth_data
                                 }
                        try:
                            post1 = requests.post(self.server, data1)
                            response = json.loads(post1.text)
                            for res in response:
                                id_server = res["id_server"]
                                pkr = res[pk]

                                sql = "UPDATE "+table+" SET id_server = %s WHERE "+pk+" = %s"
                                data_param = (id_server, pkr)
                                type_sql = "U"
                                self.conex.query(sql, data_param, type_sql)

                        except ValueError:
                            print "No response syncs_gen to server"
            except ValueError:
                print "No Response constab"
        connect = self.check_connect()
        if connect:
            self.check_server("break")

    def upload_productos(self, id, process, id_verf):
        if process == "insert":
            print "productos insert"
            data = {"hash": self.hash,
                    "process": "search",
                    "action": "insert",
                    "table": "productos",
                    "id": str(id)
                    }
            try:
                post = requests.post(self.local, data)
                array_json = post.text
                data1 = {"hash": self.hash,
                         "id_sucursal": self.id_sucursal,
                         "process": "insert",
                         "table": "productos",
                         "data": array_json,
                         "auth_data": self.auth_data
                        }
                try:
                    post1 = requests.post(self.server, data1)
                    response = json.loads(post1.text)
                    prod = response["producto"]
                    pres_prod = response["presentacion_producto"]
                    id_producto = prod["id_producto"]
                    id_server = prod["id_server"]

                    sql = "UPDATE producto SET id_server = %s WHERE id_producto = %s"
                    data_param = (id_server, id_producto)
                    type_sql = "U"
                    self.conex.query(sql, data_param, type_sql)

                    sql = "UPDATE log_cambio_local SET subido = %s, verificado = %s WHERE id_log_cambio = %s"
                    data_param = (1, 1, id_verf)
                    type_sql = "U"
                    self.conex.query(sql, data_param, type_sql)

                    for res in pres_prod:
                        id_server = res["id_server"]
                        id_presentacion = res["id_presentacion"]

                        sql = "UPDATE presentacion_producto SET id_server = %s WHERE id_pp = %s"
                        data_param = (id_server, id_presentacion)
                        type_sql = "U"
                        self.conex.query(sql, data_param, type_sql)

                except ValueError:
                    print "No Response upload_productos to server"
            except ValueError:
                print "No Response upload_productos slave"

        elif process == "update":
            print "productos update"
            data = {"hash": self.hash,
                    "process": "search",
                    "action": "update",
                    "table": "productos",
                    "id": str(id)
                    }
            try:
                post = requests.post(self.local, data)
                response = json.loads(post.text)
                id_server_prod = response["id_server"]
                array_json = json.dumps(response["data"])
                data1 = {"hash": self.hash,
                         "id_sucursal": self.id_sucursal,
                         "process": "update",
                         "table": "productos",
                         "id_server_prod": id_server_prod,
                         "data": array_json,
                         "auth_data": self.auth_data
                        }
                try:
                    post1 = requests.post(self.server, data1)
                    response1 = json.loads(post1.text)
                    prod = response1["producto"]

                    sql = "UPDATE log_cambio_local SET subido = %s WHERE id_log_cambio = %s"
                    data_param = (1, id_verf)
                    type_sql = "U"
                    self.conex.query(sql, data_param, type_sql)
                except ValueError:
                    print "No Response upload_productos server"
            except ValueError:
                print "No Response upload_productos update slave"

    def upload_presentacion_producto(self, id, process, id_verf):
        if process == "insert":
            print "presentacion producto insert"
            data = {"hash": self.hash,
                    "process": "search",
                    "table": "presentacion_producto",
                    "id": str(id)
                    }
            try:
                post = requests.post(self.local, data)
                response = json.loads(post.text)
                array_json = json.dumps(response["data"])
                id_server_prod = response["id_server_prod"]
                data1 = {"hash": self.hash,
                         "id_sucursal": self.id_sucursal,
                         "process": "insert",
                         "table": "presentacion_producto",
                         "data": array_json,
                         "id_server_prod": id_server_prod,
                         "auth_data": self.auth_data
                        }
                try:
                    post1 = requests.post(self.server, data1)
                    response1 = json.loads(post1.text)
                    pres_prod = response1["presentacion_producto"]

                    sql = "UPDATE log_cambio_local SET subido = %s, verificado = %s WHERE id_log_cambio = %s"
                    data_param = (1, 1, id_verf)
                    type_sql = "U"
                    self.conex.query(sql, data_param, type_sql)

                    for res in pres_prod:
                        id_server = res["id_server"]
                        id_presentacion = res["id_pp"]

                        sql = "UPDATE presentacion_producto SET id_server = %s WHERE id_pp = %s"
                        data_param = (id_server, id_presentacion)
                        type_sql = "U"
                        self.conex.query(sql, data_param, type_sql)
                except ValueError:
                    print "No Response upload_presentacion_producto server"
            except ValueError:
                print "No response upload_presentacion_producto slave"
        elif process == "update":
            print "presentacion producto update"
            data = {"hash": self.hash,
                    "process": "search",
                    "table": "presentacion_producto",
                    "id": str(id)
                    }
            try:
                post = requests.post(self.local, data)
                response = json.loads(post.text)
                array_json = json.dumps(response["data"])
                id_server_pp = response["id_server"]
                data1 = {"hash": self.hash,
                         "id_sucursal": self.id_sucursal,
                         "process": "update",
                         "table": "presentacion_producto",
                         "id_server_pp": id_server_pp,
                         "data": array_json,
                         "auth_data": self.auth_data
                        }
                try:
                    post1 = requests.post(self.server, data1)
                    response1 = json.loads(post1.text)
                    pres_prod = response1["presentacion_producto"]
                    sql = "UPDATE log_cambio_local SET subido = %s WHERE id_log_cambio = %s"
                    data_param = (1, id_verf)
                    type_sql = "U"
                    self.conex.query(sql, data_param, type_sql)
                except ValueError:
                    print "No response upload_presentacion_producto update server"
            except ValueError:
                print "No response upload_presentacion_producto update slave"

    def upload_traslado(self, id, process, id_verf):
        if process == "insert":
            print "traslado insert"
            data = {"hash": self.hash,
                    "process": "search",
                    "table": "traslado",
                    "action": "insert",
                    "id": str(id),
                    "id_verf": str(id_verf)}
            try:
                post = requests.post(self.local, data)
                array_json = post.text
                data = {"hash": self.hash,
                        "process": "insert",
                        "table": "traslado",
                        "data": array_json,
                        "auth_data": self.auth_data}
                try:
                    post = requests.post(url=self.server, data=data)
                    response = json.loads(post.text)
                    prod = response['traslado']
                    pres_prod = response['traslado_detalle']
                    id_traslado = prod['id_traslado']
                    id_server = prod["id_server"]
                    id_server_cambio = response['id_cambio_server']

                    sql = "UPDATE traslado SET id_server = %s WHERE id_traslado = %s"
                    data_param = (id_server, id_traslado)
                    type_sql = "U"
                    self.conex.query(sql, data_param, type_sql)

                    sql = "UPDATE log_cambio_local SET subido = %s, verificado = %s, id_server = %s WHERE id_log_cambio = %s"
                    data_param = (1, 1, id_server_cambio, id_verf)
                    type_sql = "U"
                    self.conex.query(sql, data_param, type_sql)

                    for res in pres_prod:
                        id_server = res["id_server"]
                        id_detalle_traslado = res["id_detalle_traslado"]

                        sql = "UPDATE traslado_detalle SET id_server = %s WHERE id_detalle_traslado = %s"
                        data_param = (id_server, id_detalle_traslado)
                        type_sql = "U"
                        self.conex.query(sql, data_param, type_sql)

                except ValueError:
                    print "No Response insert trasalo server"
            except ValueError:
                print "No response search traslado"
        elif process == "update":
            print "traslado update"
            data = {"hash": self.hash,
                    "process": "search",
                    "action": "update",
                    "table": "traslado",
                    "id": str(id)
                    }
            try:
                post = requests.post(self.local, data)
                response = json.loads(post.text)

                id_server_prod = response["id_server"]
                id_sucursal_envia = response["id_sucursal_envia"]
                id_sucursal_recive = response["id_sucursal_recive"]
                array_json = json.dumps(response["data"])
                data1 = {"hash": self.hash,
                         "process": "update",
                         "table": "traslado",
                         "id_sucursal": self.id_sucursal,
                         "id_server_prod": id_server_prod,
                         "id_sucursal_envia": id_sucursal_envia,
                         "id_sucursal_recive": id_sucursal_recive,
                         "data": array_json,
                         "auth_data": self.auth_data}
                try:
                    post1 = requests.post(self.server, data1)
                    response1 = json.loads(post1.text)
                    prod = response1["traslado"]

                    sql = "UPDATE log_cambio_local SET subido = %s, verificado = %s WHERE id_log_cambio = %s"
                    data_param = (1, 1, id_verf)
                    type_sql = "U"
                    self.conex.query(sql, data_param, type_sql)
                except ValueError:
                    print "No Response  upload_traslado update_traslado server"
            except ValueError:
                print "No Response upload_traslado update slave"

    def upload_traslado_detalle_recibido(self, id, process, id_verf):
        if process == "insert":
            print "traslado_detalle_recibido  insert"
            data = {"hash": self.hash,
                    "process": "search",
                    "table": "traslado_detalle_recibido",
                    "id": str(id)
                    }
            try:
                post = requests.post(self.local, data)
                response = json.loads(post.text)
                array_json = json.dumps(response["data"])
                id_sucursal_envia = response["id_sucursal_envia"]
                id_sucursal_recive = response["id_sucursal_recive"]
                data1 = {"hash": self.hash,
                         "process": "insert",
                         "table": "traslado_detalle_recibido",
                         "id_sucursal": self.id_sucursal,
                         "id_sucursal_envia": id_sucursal_envia,
                         "id_sucursal_recive": id_sucursal_recive,
                         "data": array_json,
                         "auth_data": self.auth_data}
                try:
                    post1 = requests.post(self.server, data1)
                    response1 = json.loads(post1.text)
                    pres_prod = response1["traslado_detalle_recibido"]
                    sql = "UPDATE log_cambio_local SET subido = %s, verificado = %s WHERE id_log_cambio = %s"
                    data_param = (1, 1, id_verf)
                    type_sql = "U"
                    self.conex.query(sql, data_param, type_sql)
                    for res in pres_prod:
                        id_server = res["id_server"]
                        id_presentacion = res["id_detalle_traslado_recibido"]
                        sql = "UPDATE traslado_detalle_recibido SET id_server = %s WHERE id_detalle_traslado_recibido  = %s"
                        data_param = (id_server, id_presentacion)
                        type_sql = "U"
                        self.conex.query(sql, data_param, type_sql)
                except ValueError:
                    print "No Response traslado_detalle_recibido server"
            except ValueError:
                print "No response traslado_detalle_recibido slave"

    def download_traslado_detalle_recibido(self, process, datas, id_verf, id_server):
        print "down traslado_detalle_recibido  "+process
        data = {"hash": self.hash,
                "process": process,
                "id_server": id_server,
                "table": "traslado_detalle_recibido",
                "data": json.dumps(datas)
                }
        try:
            post = requests.post(self.local, data)
            response = post.text
            print response
            if response == "all changes commited":
                data1 = {"hash": self.hash,
                         "process": "confirm",
                         "id_sucursal": self.id_sucursal,
                         "id_verf": id_verf,
                         "auth_data": self.auth_data
                         }
                post1 = requests.post(self.server, data=data1)
                post1.text
                self.check_server("break")
            elif response == "sync_error":
                self.check_server("break")
        except ValueError:
            print "No Response download_traslado_detalle_recibido"

    def download_traslado(self, process, datas, id_verf, id_server):
        print "down traslado "+process
        data = {"hash": self.hash,
                "process": process,
                "id_server": id_server,
                "table": "traslado",
                "data": json.dumps(datas)
                }
        try:
            post = requests.post(self.local, data)
            response = post.text
            print response
            if response == "all changes commited":
                data1 = {"hash": self.hash,
                         "process": "confirm",
                         "id_sucursal": self.id_sucursal,
                         "id_verf": id_verf,
                         "auth_data": self.auth_data
                         }
                post1 = requests.post(self.server, data=data1)
                response1 = post1.text
                print response1
                self.check_server("break")
            elif response == "sync_error":
                self.check_server("break")
        except ValueError:
            print "No Response download_traslado"

    def upload_gen(self, nTimes, json_size):
        print int(nTimes)
        print str(json_size)
        for x in range(nTimes):
            print x
            data = {"hash": self.hash,
                    "process": "search",
                    "action": "update",
                    "table": "generic",
                    "limit": str(json_size),
                    }
            try:
                post = requests.post(self.local, data)
                # print post.text
                response = json.loads(post.text)
                regs = json.dumps(response["regs"])
                # print regs

                if int(regs) > 0:
                    array_json = json.dumps(response["data"])
                    data1 = {"hash": self.hash,
                             "process": "update",
                             "table": "generic",
                             "id_sucursal": self.id_sucursal,
                             "data": array_json,
                             "auth_data": self.auth_data}
                    try:
                        post1 = requests.post(self.server, data1)
                        # print post1.text
                        response1 = json.loads(post1.text)
                        pres_prod = response1['ac']
                        for res in pres_prod:
                            id_verf = res["id"]
                            sql = "UPDATE log_cambio_local SET subido = %s, verificado = %s WHERE id_log_cambio = %s"
                            data_param = (1, 1, id_verf)
                            type_sql = "U"
                            self.conex.query(sql, data_param, type_sql)
                    except ValueError:
                        print "No Response upload_gen server"
            except ValueError:
                print "No Response upload_gen slave"

    def download_gen(self, process, datas, id_verf, id_server, table):
        print "down "+table+" "+process
        data = {"hash": self.hash,
                "process": process,
                "id_server": id_server,
                "table": table,
                "data": json.dumps(datas)
                }
        try:
            post = requests.post(self.local, data)
            response = json.loads(post.text)
            data1 = {"hash": self.hash,
                     "process": "confirm_all",
                     "id_sucursal": self.id_sucursal,
                     "auth_data": self.auth_data,
                     "data": json.dumps(response["ac"])
                     }
            post1 = requests.post(self.server, data=data1)
            print post1.text
            self.check_server("break")
        except ValueError:
            print "No Response download_gen slave general"

# prime = Sentinel()
# connect = prime.check_connect()
# if connect:
#     prime.check_server("check")
# else:
#     print "No conecta"
