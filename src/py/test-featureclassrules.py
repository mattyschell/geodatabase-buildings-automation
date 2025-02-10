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

        # test source data is test/in/...xxx.gdb.zip
        self.ingdbzipped = os.path.join(self.indir
                                       ,'bldg.gdb.zip')

        self.constrainedgdbzipped = os.path.join(self.indir
                                                ,'constraint'
                                                ,'constrained.gdb.zip')
        # havent gotten to this one yet
        #self.unconstrainedgdbzipped = os.path.join(self.indir
        #                                        ,'constraint'
        #                                        ,'unconstrained.gdb.zip')

        self.uncalculatedgdbzipped = os.path.join(self.indir
                                                 ,'calculation'
                                                 ,'uncalculated.gdb.zip')
        self.calculatedgdbzipped = os.path.join(self.indir
                                               ,'calculation'
                                               ,'calculated.gdb.zip')

        # we will extract and work in /test/work/xxx.gdb
        self.testgdb = os.path.join(self.workdir
                                   ,'bldg.gdb')

        self.constrainedgdb = os.path.join(self.workdir
                                          ,'constrained.gdb')
        #self.unconstrainedgdb = os.path.join(self.workdir
        #                                  ,'unconstrained.gdb')
        
        self.uncalculatedgdb = os.path.join(self.workdir
                                          ,'uncalculated.gdb')
        self.calculatedgdb = os.path.join(self.workdir
                                         ,'calculated.gdb')

        shutil.unpack_archive(self.ingdbzipped
                             ,self.workdir)  

        shutil.unpack_archive(self.constrainedgdbzipped
                             ,self.workdir)
        #shutil.unpack_archive(self.unconstrainedgdbzipped
        #                     ,self.workdir)
        
        shutil.unpack_archive(self.uncalculatedgdbzipped
                             ,self.workdir)        
        shutil.unpack_archive(self.calculatedgdbzipped
                             ,self.workdir)
        
        # testing target data
        self.building = \
            featureclassrulemanager.featureclass(self.testgdb
                                                ,'building')
        self.building_historic = \
            featureclassrulemanager.featureclass(self.testgdb
                                                ,'building_historic')

        # testing data that should be allowed or rejected by rules
        #self.building_constrained = \
        #    featureclassrulemanager.featureclass(self.constrainedgdb
        #                                        ,'building')
        self.building_historic_constrained = \
            featureclassrulemanager.featureclass(self.constrainedgdb
                                                ,'building_historic')

        # testing data that should be calculated by rules
        self.building_uncalculated = \
            featureclassrulemanager.featureclass(self.uncalculatedgdb
                                                ,'building')
        # not explicitly using this yet
        self.building_calculated = \
            featureclassrulemanager.featureclass(self.calculatedgdb
                                                ,'building')

        self.ruledir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))
                                                   ,'..'
                                                   ,'..'
                                                   ,'src'
                                                   ,'rules'))        
        # a convention for the ages
        # \src\rules\building_historic.csv
        self.building_historic_csv = os.path.join(self.ruledir
                                                 ,'{0}.csv'.format(self.building_historic.name))

        # \src\rules\building.csv
        self.building_csv = os.path.join(self.ruledir
                                        ,'{0}.csv'.format(self.building.name))

        self.doittidstart = 1000000000

        #########################
        # APPLY RULES IN SETUP?
        # or apply and remove (?) in each test?
        # currently applying in an early test is not great
        #######################

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

    def test_capplybuildingrules(self):

        # this is what a script to set up building rules will look like

        # sequence must exist before rule application
        # sequence name is specified in the rule csv
        # todo: think harder about this. sequence name should probably
        #       be specified in a resource in the rules directory
        self.building.createrulesequence("doittID"
                                        ,self.doittidstart)

        self.assertTrue(self.building.applyrules(self.building_csv))

    def test_drejecthistoricbaddies(self):

        # lets start at doitt id 1 in validation rules source test data
        # we'll set our calculated doitt_id sequence at a sufficiently hight
        # number to avoid conflicts
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

    def test_ecalculatedoittid(self):

        # insert a building row from uncalculated.gdb
        # into building in bldg.gdb
        # the source has no doitt_id
        # the test passes if the attribute rules create a doitt_id
        # with the start value we specified above

        # uncalculated dummy records start at bin 2000000
        query = "BIN = 2000000"
        expected = self.doittidstart 

        with arcpy.da.SearchCursor(self.building_uncalculated.featureclass
                                  ,["*"]
                                  ,query) as search_cursor:
            with arcpy.da.InsertCursor(self.building.featureclass
                                      ,search_cursor.fields) as insert_cursor:
                    for row in search_cursor:
                        insert_cursor.insertRow(row)

        with arcpy.da.SearchCursor(self.building.featureclass
                                  ,["doitt_id"]
                                  ,query) as search_cursor:
            for row in search_cursor:
                self.assertEqual(row[0],expected)
            

    
if __name__ == '__main__':
    unittest.main()
