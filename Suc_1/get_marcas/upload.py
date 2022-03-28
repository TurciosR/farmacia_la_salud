import requests
import urllib2
import urllib
import pycurl
import uuid
from datetime import date
from datetime import datetime
from datetime import timedelta

hoy = datetime.now()
antes = hoy + timedelta(days=-15)

fin = hoy.strftime('%Y-%m-%d')
fini = antes.strftime('%Y-%m-%d')
print fini
print fin

crl = pycurl.Curl()
crl.setopt(crl.URL, 'http://farmasaludsv.com.sv/server/reciver.php')
values = [
     ('id_sucursal',"1"),
     ('file', (crl.FORM_FILE, "/home/user/get_marcas/marcas/e0208fb4-3263-42a7-ac7a-d0ee114dca74.dat"))
]
crl.setopt(crl.HTTPPOST,values)
crl.perform()
crl.close()
