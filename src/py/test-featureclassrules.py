import unittest
from unittest.mock import patch
import io
import os
import shutil

import time
start_time = time.time()
print("importing arcpy")
import arcpy
import_duration = time.time() - start_time
print(f"f me today it takes : {import_duration} seconds to import arcpy")

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

        # future. not yet used
        self.expecteddir = os.path.join(self.testdir
                                       ,'expected')

        # test source data is test/in/xxx.gdb.zip
        self.ingdbzipped = os.path.join(self.indir
                                       ,'bldg.gdb.zip')
        self.constrainedgdbzipped = os.path.join(self.indir
                                                ,'constrained.gdb.zip')

        # we will extract and work in /test/work/xxx.gdb
        self.testgdb = os.path.join(self.workdir
                                   ,'bldg.gdb')
        self.constrainedgdb = os.path.join(self.workdir
                                          ,'constrained.gdb')

        shutil.unpack_archive(self.ingdbzipped
                             ,self.workdir)  

        shutil.unpack_archive(self.constrainedgdbzipped
                             ,self.workdir)

        self.building_historic = \
            featureclassrulemanager.featureclass(self.testgdb
                                                ,'building_historic')

        self.building_historic_constrained = \
            featureclassrulemanager.featureclass(self.constrainedgdb
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
        # no rules yet. So no prints from describe
        self.assertEqual(mock_stdout.getvalue().strip()
                        ,'')

    def test_bapplyhistoricrules(self):

        # Apply rules to building_historic
        # my wrapper code should succeed and return True
        self.assertTrue(self.building_historic.applyrules(self.building_historic_csv))

    def test_crejecthistoricbaddies(self):

        query = "DOITT_ID = 1"

        misdeed = 'Violated attribute constraint rule'
        # errors look like this
        #    RuntimeError: Violated attribute constraint rule. [
        #    Rule name: demolition-year-1626-present,
        #    Triggering event: Insert,
        #    Class name: building_historic,
        #    GlobalID: {454C9977-04BB-474A-B280-CD860537DA52},
        #    Error number: 1,
        #    Error message: building_historic.demolition_year must be between 1626 and today]

        with arcpy.da.SearchCursor(self.building_historic_constrained.featureclass
                                  ,["*"]
                                  ,query) as search_cursor:
            for row in search_cursor:
                # the assert raises "context manager" says expect runtime error
                with self.assertRaises(RuntimeError) as context:
                    with arcpy.da.InsertCursor(self.building_historic.featureclass
                                              ,search_cursor.fields) as insert_cursor:
                        insert_cursor.insertRow(row)
                # and here is the so-called context
                # check that the runtime error is an attribute rule
                # not some other madness
                self.assertTrue(str(context.exception).startswith(misdeed))

if __name__ == '__main__':
    unittest.main()
