import arcpy
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

        pass

    def exportrules(self
                   ,outcsv):

        pass

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