#!/usr/bin/python
# -*- coding: UTF-8 -*-
class Auth:
    def get_data(self):
        data = {'bios': {'version': 'F.02',
                         'vendor': 'Insyde'},
                'processor': {'version': 'Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz',
                              'family': 'Core i5',
                              'manufacturer': 'Intel(R) Corporation'},
                'chassis': {'serial-number': 'CND82827K2',
                            'type': 'Notebook'},
                'board': {'serial-number': 'PHJEVE3MYB2ZWN',
                          'product-name': '84A6'},
                'system': {'serial-number': 'CND82827K2',
                           'product-name': 'HP Laptop 15-da0xxx2',
                           'version': 'Type1ProductConfigId', 'manufacturer': 'HP'}
                }
        return data
#auth = Auth()
#print auth.get_data()
