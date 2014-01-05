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

from LDSAPI import LDSAPI

data_gets = ('/services/api/v1/data/','services/api/v1/data/1/metadata/')


class DataAPI(LDSAPI):
    def __init__(self):
        super(DataAPI,self).__init__()
        self.path = data_gets[0]
        
class DataTester(unittest.TestCase):
    
    def setUp(self):
        self.da = DataAPI()
        
    def tearDown(self):
        self.da = None
        
    def test_10_ReadBaseData(self):
        req = Request('https://{}{}'.format(self.da.host,self.da.path))
        #req.add_header("Authorization", "Basic %s" % self.da.b64p)  
        self.da.dispReq(req)
        urllib2.install_opener(self.da.opener(self.da.openerstrs_ntlm))
        res = urllib2.urlopen(req)
        self.da.dispRes(res)
        

    
if __name__ == '__main__':
    unittest.main()