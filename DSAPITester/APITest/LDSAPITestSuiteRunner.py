'''
v.0.0.9

DSAPITester - LDSAPITestSuiteRunner

Copyright 2011 Crown copyright (c)
Land Information New Zealand and the New Zealand Government.
All rights reserved

This program is released under the terms of the new BSD license. See the 
LICENSE file for more information.

Test Suite runner

Created on 23/12/2013

@author: jramsay
'''
import unittest

from APITest.LDSAPI import LDSAPI as T1
from APITest.DataAPI import DataAPI as T2
from APITest.SourceAPI import SourceAPI as T3



class LDSAPITestSuite(unittest.TestSuite):

    def __init__(self):
        pass
    
    def suite(self):
        suites = ()
        #suites += unittest.makeSuite(T1)
        suites += unittest.makeSuite(T2)
        suites += unittest.makeSuite(T3)

        
        return unittest.TestSuite(suites)

    
def main():
    
    suite  = unittest.TestSuite()
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
if __name__ == "__main__":
    main()

    