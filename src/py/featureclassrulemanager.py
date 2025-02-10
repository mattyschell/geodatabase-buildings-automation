import time
start_time = time.time()
print("importing arcpy")
import arcpy
#from arcpy.management import ImportAttributeRules
#from arcpy import Describe
#from arcpy import ExecuteError
import_duration = time.time() - start_time
print(f"f me today it takes : {import_duration} seconds to import arcpy")
import os

class validationrule(object):

    def __init__(self):

        pass


class featureclass(object):

    def __init__(self
                ,geodatabase
                ,name):

         self.geodatabase  = geodatabase
         self.name         = name
         self.featureclass = os.path.join(self.geodatabase
                                         ,self.name)

    def applyrules(self
                  ,incsv):

        try:
            arcpy.management.ImportAttributeRules(self.featureclass
                                                 ,incsv)
        except arcpy.ExecuteError as e:
            print(f"An error occurred: {e} importing {inscv}")
            raise e
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e

        return True

    def exportrules(self
                   ,outcsv):

        pass

    def createrulesequence(self
                          ,sequencename
                          ,start = 1) -> None:

        try:
            arcpy.management.CreateDatabaseSequence(self.geodatabase
                                                   ,sequencename
                                                   ,start)
        except arcpy.ExecuteError as e:
            print(f"An error occurred: {e} creating sequence {inssequencenamecv}")
            raise e
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e

    def describerules(self):

        # copy paste
        # https://pro.arcgis.com/en/pro-app/latest/arcpy/functions/attribute-rule-properties.htm
        allrules = arcpy.Describe(self.featureclass).attributeRules

        for ar in allrules:    
            if "Calculation" in ar.type:       
                print("- Calculation Rule:")
                print(f" Name: {ar.name}")
                print(f" Creation time: {ar.creationTime}")
                print(f" Field: {ar.fieldName}")
                print(f" Subtype code: {ar.subtypeCode}")
                print(f" Description: {ar.description}")
                print(f" Is editable: {ar.userEditable}")
                print(f" Is enabled: {ar.isEnabled}")
                print(f" Evaluation order: {ar.evaluationOrder}")
                print(f" Exclude from client evaluation: {ar.excludeFromClientEvaluation}")
                print(f" Triggering events: {ar.triggeringEvents}")
                print(f" Triggering fields: {ar.triggeringfields}\n")
                print(f" Script expression: {ar.scriptExpression}\n")
                print(f" Is flagged as a batch rule: {ar.batch}\n")
                print(f" Severity: {ar.severity}\n")
                print(f" Tags: {ar.tags}\n")

            elif "Constraint" in ar.type:       
                print("- Constraint Rule:")
                print(f" Name: {ar.name}")
                print(f" Creation time: {ar.creationTime}")
                print(f" Subtype code: {ar.subtypeCode}")
                print(f" Description: {ar.description}")
                print(f" Is editable: {ar.userEditable}")
                print(f" Is enabled: {ar.isEnabled}")
                print(f" Error number: {ar.errorNumber}")
                print(f" Error message: {ar.errorMessage}")
                print(f" Exclude from client evaluation: {ar.excludeFromClientEvaluation}")
                print(f" Triggering events: {ar.triggeringEvents}")
                print(f" Triggering fields: {ar.triggeringfields}\n")
                print(f" Script expression: {ar.scriptExpression}\n")
                print(f" Tags: {ar.tags}\n")

            elif "Validation" in ar.type: 
                print("CARTHAGE AND BRANCH VERSIONING MUST BE DESTROYED")
                print(f" Name: {ar.name}")