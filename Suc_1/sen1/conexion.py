#! /usr/bin/ python
# -*- coding: UTF-8 -*--
import mysql.connector as pymysql


class Database:
    def __init__(self, db):
        # recibe como parametro el nombre de la bd
        self.db = db
        self.host = "localhost"
        self.user = "root"
        self.passwd = "admin$2021**."
        self.port = 3306
        self.connection = pymysql.connect(host="localhost", port=self.port, user=self.user,passwd=self.passwd, db=self.db)
        self.cursor = self.connection.cursor()

    def query(self, q, data_param, typequery):
        self.typequery = typequery
        cursor = self.cursor
        self.data_param = data_param
        if self.typequery == 'S':
            # S: Select SQL
            # print q, self.typequery,self.data_param
            if self.data_param == '':
                cursor.execute(q)
            else:
                cursor.execute(q, data_param)
            rows = cursor.fetchall()
            return rows
        elif self.typequery == 'SL':
            # SL: SQL Select for like
            dato = (data_param,)
            # print q, dato
            cursor.execute(q, dato)
            rows = cursor.fetchall()
            return rows
        elif self.typequery == 'U':
            # U: update operation SQL
            if self.data_param == '':
                cursor.execute(q)
            else:
                cursor.execute(q, data_param)
            self.connection.commit()
        elif self.typequery == 'I':
            # I: insert operation SQL
            if self.data_param == '':
                cursor.execute(q)
            else:
                cursor.execute(q, data_param)
            self.connection.commit()
        elif self.typequery == 'D':
            # D: Delete operation SQL
            if self.data_param == '':
                cursor.execute(q)
            else:
                cursor.execute(q, data_param)
            self.connection.commit()

    def __del__(self):
        self.connection.close()

# conex = Database("campina_cliente")
# sql = "SELECT id_sucursal, hash FROM access_conf WHERE id_conf = %s"
# data_param = ("1",)
# type_sql = "S"
# rows = conex.query(sql, data_param, type_sql)
# print rows
