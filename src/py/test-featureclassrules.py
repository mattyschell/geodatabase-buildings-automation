import unittest
from unittest.mock import patch
import io
import os
import shutil

import featureclassrulemanager


class RulesTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.testdir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))
                                                   ,'..'
                                                   ,'..'
                                                   ,'test'))

        self.indir = os.path.join(self.testdir
                                 ,'in')
        
        self.workdir = os.path.join(self.testdir
                                   ,'work')

        shutil.rmtree(self.workdir)
        os.makedirs(self.workdir) 

        self.expecteddir = os.path.join(self.testdir
                                       ,'expected')

        self.ingdbzipped = os.path.join(self.indir
                                       ,'bldg.gdb.zip')

        self.testgdb = os.path.join(self.workdir
                                   ,'bldg.gdb')

        shutil.unpack_archive(self.ingdbzipped
                             ,self.workdir)  

        self.building_historic = featureclassrulemanager.featureclass(self.testgdb
                                                                     ,'building_historic')

        self.ruledir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))
                                                   ,'..'
                                                   ,'..'
                                                   ,'src'
                                                   ,'rules'))        
        
        # a convention for the ages
        # \src\rules\building_historic.csv
        self.building_historic_csv = os.path.join(self.ruledir
                                                 ,'{0}.csv'.format(self.building_historic.name))

    def tearDown(self):

        pass

    @classmethod
    def tearDownClass(self):

        try:
            shutil.rmtree(self.workdir)
            os.makedirs(self.workdir)
        except:
            pass
            # grrr again with this
            # looks like locks remain for the  duration of the arcpy session
            # pre-clean workdir in setup instead
            # PermissionError: [WinError 32] The process cannot access the file 
            # because it is being used by another process:
            #   .. test\\work\\bldg.gdb\\_gdb.xxxx.139532.143220.sr.lock'
        

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_adescribe(self
                      ,mock_stdout):

        # fancy decorator above funnels prints into io string objects 
        self.building_historic.describerules()
        # no rules no describe
        self.assertEqual(mock_stdout.getvalue().strip()
                        ,'')

    def test_bapplyrule(self):

        self.assertTrue(self.building_historic.applyrules(self.building_historic_csv))
        #self.building_historic.describerules()

if __name__ == '__main__':
    unittest.main()
