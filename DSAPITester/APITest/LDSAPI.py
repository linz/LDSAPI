'''
Created on 23/12/2013

@author: jramsay
'''

#https://koordinates.com/services/api/v1/sources/1/

import cookielib
import unittest
import urllib2
from urllib2 import Request, urlopen, base64
from json import dumps


url = {'lds-t':'data-test.linz.govt.nz','apiary':'private-cbd7-koordinates.apiary.io','koordinates':'koordinates.com'}
pxy = {'linz':'webproxy1.ad.linz.govt.nz:3128','local':'127.0.0.1:3128'}

gets = ('/services/api/v1/sources/','services/api/v1/sources/1/metadata/')



#import urllib2, base64

#request = urllib2.Request("http://api.foursquare.com/v1/user")
#base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
#request.add_header("Authorization", "Basic %s" % base64string)   
#result = urllib2.urlopen(request)

sampledata = (
    ("Alices' Mapinfo Server", "mapinfo", "No Proxy - No Auth", [], 3, "alice", "alicespassword", "https://alice.example.com/Mapinfo/rest/services", "@hourly"),
    ("Bob's ArcGIS 10 Server", "arcgis",  "Proxy (CNTLM) - No Auth", [], 3, "bob", "bobspassword", "https://bob.example.com/ArcGIS/rest/services", "@daily"),
    ("Carol's PostGIS 8 Server", "postgis",  "Proxy (Corp Web) - No Auth", [], 3, "carol", "carols password", "https://carol.example.com/PostGis/rest/services", "@weekly"),
    ("Dan's SpatiaLite 4 Server", "spatialite", "No Proxy - Auth (aio)", [], 3, "dan", "danspassword", "https://dan.example.com/SpatiaLite/rest/services", "@yearly"),
    ("Erin's Grass 12 server", "grass", "Proxy (CNTLM) - Auth (aio)", [], 3, "erin", "erinspassword", "https://erin.example.com/Grass/rest/services", "@quarterly"),
    ("Frank's FileGDB 2 Server", "filegdb", "Proxy (Corp Web) - Auth (aio)", [], 3, "frank", "frankspassword", "https://frank.example.com/FileGDB/rest/services", "@occasionally")
)

class LDSAPI(object):
    def __init__(self):
        self.path = gets[0]
        self.host = url['lds-t']
        
        self.cookies = cookielib.LWPCookieJar()
        
        aauth = ('jramsay@linz.govt.nz','wednesday123')
        pauth = ('jramsay@linz.govt.nz','pineapple_100')
        
        self.b64a = self.appAuth(aauth)
        self.b64p = self.pxyAuth(pauth)
        
        self.openerstrs_linz = (pxy['linz'],pauth[0],pauth[1])
        self.openerstrs_ntlm = (pxy['local'])
        
        
    def opener(self,purl, puser=None, ppass=None, pscheme="http"):

        handlers = [
                    urllib2.HTTPHandler(),
                    urllib2.HTTPSHandler(),
                    urllib2.HTTPCookieProcessor(self.cookies)
                ]
        if purl:
            handlers += [urllib2.ProxyHandler({pscheme: purl}),]
        
        if puser and ppass:
            pm = urllib2.HTTPPasswordMgrWithDefaultRealm()
            pm.add_password(None, purl, puser, ppass)
            handlers += [urllib2.ProxyBasicAuthHandler(pm),]
        
        return urllib2.build_opener(*handlers)
    
    def appAuth(self,auth):
        return base64.encodestring('%s:%s' % (auth[0], auth[1])).replace('\n', '')    
    
    def pxyAuth(self,auth):
        return base64.encodestring('%s:%s' % (auth[0], auth[1])).replace('\n', '')
    
    def dispReq(self,req):
        print req.get_full_url(),'auth',req.get_header('Authorization')
        
    def dispRes(self,res):
        print res.info()

    def populate(self,data):
        return dumps({"name": data[0],"type": data[1],"description": data[2], 
                      "categories": data[3], "user": data[4], "options":{"username": data[5],"password": data[6]},
                      "url_remote": data[7],"scan_schedule": data[8]})
        
        
        
class ConnectionTester(unittest.TestCase):
    
    def setUp(self):
        self.con = LDSAPI()
        
    def tearDown(self):
        self.con = None
        
#     def test_01_Raw(self):
#         return
#         req = Request("https://private-c694-sources1.apiary.io/services/api/v1/sources/1/")
#         self.da.dispReq(req)
#         res = urlopen(req).read()
#         self.da.dispRes(res)
#     
#     def test_11_GetNoProxyNoAuth(self):
#         return
#         req = Request('https://{}{}'.format(self.da.host,self.da.path+'2/'))
#         self.da.dispReq(req)
#         res = urlopen(req).read()
#         self.da.dispRes(res)
#         
#     def test_12_GetNTLMProxyNoAuth(self):
#         return
#         req = Request('https://{}{}'.format(self.da.host,self.da.path+'3/'))
#         self.da.dispReq(req)
#         urllib2.install_opener(self.da.opener_ntlm)
#         res = urllib2.urlopen(req).read()
#         self.da.dispRes(res)          
#         
#     def test_13_GetWebProxyNoAuth(self):
#         return
#         req = Request('https://{}{}'.format(self.da.host,self.da.path))
#         self.da.dispReq(req)
#         urllib2.install_opener(self.da.opener_linz)
#         res = urllib2.urlopen(req).read()
#         self.da.dispRes(res)      
         
         
    def test_21_GetNoProxyAuth(self):
        req = Request('https://{}{}'.format(self.da.host,self.da.path))
        req.add_header("Authorization", "Basic %s" % self.da.b64p)  
        self.da.dispReq(req)
        urllib2.install_opener(self.da.opener(self.da.openerstrs_ntlm))
        res = urllib2.urlopen(req)
        self.da.dispRes(res)
#         
#     def test_22_GetNTLMProxyAuth(self):
#         req = Request('https://{}{}'.format(self.da.host,self.da.path))
#         req.add_header("Authorization", "Basic %s" % self.da.b64a)  
#         self.da.dispReq(req)
#         urllib2.install_opener(self.da.opener_ntlm)
#         res = urllib2.urlopen(req).read()
#         self.da.dispRes(res)          
#         
#     def test_23_GetWebProxyAuth(self):
#         req = Request('https://{}{}'.format(self.da.host,self.da.path))
#         req.add_header("Authorization", "Basic %s" % self.da.b64a)  
#         self.da.dispReq(req)
#         urllib2.install_opener(self.da.opener_linz)
#         res = urllib2.urlopen(req).read()
#         self.da.dispRes(res)  
        
        
        
#     def test_30_Puts(self):
#         hdr = {"Content-Type": "application/json"}
#         for d in sampledata:
#             dta = self.da.populate(d)
#             req = Request('https://{}{}'.format(self.da.host,self.da.path), data=dta, headers=hdr)
#             req.add_header("Authorization", "Basic %s" % self.da.b64a)   
#             self.da.dispReq(req)
#             urllib2.install_opener(self.da.opener(self.da.openerstrs_ntlm))
#             res = urllib2.urlopen(req)
#             self.da.dispRes(res.read())

    
if __name__ == '__main__':
    unittest.main()