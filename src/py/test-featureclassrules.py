import unittest
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
        

    def tearDown(self):

        pass

    #def remove_readonly(self
    #                   ,func
    #                   ,path
    #                   ,_):
        
    #    os.chmod(path, stat.S_IWRITE)
    #    func(path)

    @classmethod
    def tearDownClass(self):


        try:
            shutil.rmtree(self.workdir)
            os.makedirs(self.workdir)
        except:
            pass
        # grrr
        # PermissionError: [WinError 32] The process cannot access the file 
        # because it is being used by another process:
        #   .. test\\work\\bldg.gdb\\_gdb.xxxx.139532.143220.sr.lock'
        #             ,onerror=self.remove_readonly()) 
                     
        


    def test_adescribe(self):

        self.building_historic.describerules()

        

if __name__ == '__main__':
    unittest.main()
