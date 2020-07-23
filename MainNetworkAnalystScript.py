"""
DEVELOPED BY Adam Martin and Brady Woods

"""



import arcpy
from arcpy import na
from arcpy import env
import os, sys , traceback

"Check if Network Analyst license if available. Fail if the Network Analyst license is not available"
if arcpy.CheckExtension("network") == "Available":
    arcpy.CheckOutExtension("network")
else:
    raise arcpy.ExecuteError("Network Analyst Extension license is not available.")

"Declare your workspace"
arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True
wrkMessage = "Current working directory: {0}".format(env.workspace)
arcpy.AddMessage(wrkMessage)

"""
Declare variables that will be used throughout the program
When building the script tool in ArcMap NetworkDataSet should be type Network Dataset,
Impedance attribute should be set to string, Facilities, Incidents, Line and Poly Barriers
should be set to Feature Layer, TravelDirection and UTurns should be set to string,
Outputfilepath and the backup out folder path should be set to workspace, OutputLayerName
and the backup out_name should be set to string
"""

NetworkDataSet = arcpy.GetParameterAsText(1)
ImpedanceAttr = arcpy.GetParameterAsText(2)
Facilities = arcpy.GetParameterAsText(3)
Incidents = arcpy.GetParameterAsText(4)
PolyBarriers = arcpy.GetParameterAsText(5)
PolyBarrierWeight = arcpy.GetParameterAsText(6)
LineBarriers = arcpy.GetParameterAsText(7)
LineBarrierWeight = arcpy.GetParameterAsText(8)
TravelDirection = "TRAVEL_TO"
UTurns = "ALLOW_UTURNS"
OutputLayerFilePath = arcpy.GetParameterAsText(9)
OutputLayerName = arcpy.GetParameterAsText(10)
"create backup directory"
out_folder_path = arcpy.GetParameterAsText(11)
out_name = arcpy.GetParameterAsText(12)


"""
Next get a count of the facilities, create the closest facility layer and store this in a variable
object 
"""

FacilityCount = arcpy.GetCount_management(Facilities)[0]
CFLayerObject = arcpy.na.MakeClosestFacilityLayer(NetworkDataSet, OutputLayerName, ImpedanceAttr, TravelDirection, "", FacilityCount, ImpedanceAttr , UTurns)
OutputNALayer = CFLayerObject.getOutput(0)

"""
Lastly get the class names for the NALayer, field map the polygon and line barrier layers
"""

#Incident and Facilities Layers
subLayerNames = arcpy.na.GetNAClassNames(OutputNALayer)
FacilitiesLayerNames = subLayerNames["Facilities"]
IncidentsLayerNames = subLayerNames["Incidents"]
RoutesLayerName = subLayerNames["CFRoutes"]

"""
Test if the Polygon and Line barrier layers have been added and map them if they are nonempty test for
further conditions regarding scaled cost and restriction values
"""
if PolyBarriers != "":
    #Polygon Barrier Layer
    FieldMappingBarrierNamePoly = subLayerNames["PolygonBarriers"]
    fieldMappingsBarrierPoly = arcpy.na.NAClassFieldMappings(OutputNALayer,FieldMappingBarrierNamePoly)        
    #******default value 0 == restriction, 1 == scaled cost**********
    if PolyBarrierWeight != "":
        PolygonList = PolyBarriers.split(";")
        PolyWeightList = PolyBarrierWeight.split(",")
        if len(PolygonList) == len(PolyWeightList):
            count = 0    
            for PB in PolygonList:
                pweight = PolyWeightList[count]
                if pweight.lower() == "r":
                    fieldMappingsBarrierPoly["BarrierType"].defaultValue = 0
                    arcpy.na.AddLocations(OutputNALayer,FieldMappingBarrierNamePoly , PB, fieldMappingsBarrierPoly,"5000 Meters","","","","APPEND","","","","")
                    polymessagerestrict = ("{} set to restriction".format(PB))
                    arcpy.AddMessage(polymessagerestrict)
                    count += 1
                else:
                    fieldMappingsBarrierPoly["BarrierType"].defaultValue = 1
                    pfloat = float(pweight)
                    fieldMappingsBarrierPoly["Attr_" + ImpedanceAttr].defaultValue = pfloat
                    arcpy.na.AddLocations(OutputNALayer,FieldMappingBarrierNamePoly , PB, fieldMappingsBarrierPoly,"5000 Meters","","","","APPEND","","","","")
                    polymessage = ("{} set to scaled cost, given weight {}".format(PB,pfloat))
                    arcpy.AddMessage(polymessage)
                    count += 1
        else:
            raise Exception("Number of Polygon layers does not match length of polygon weight list")
    else:
        arcpy.AddMessage("Setting All Polygon Barriers To Barrier Type Restriction")
        fieldMappingsBarrierPoly["BarrierType"].defaultValue = 0
        for PB in PolyBarriers.split(";"):
            arcpy.na.AddLocations(OutputNALayer,FieldMappingBarrierNamePoly , PB, fieldMappingsBarrierPoly,"5000 Meters","","","","APPEND","","","","")    
else:
    arcpy.AddMessage("No Polygon Barrier Layer Given")

if LineBarriers != "":
    #Line Barrier Layer
    FieldMappingBarrierNameLine = subLayerNames["PolylineBarriers"]
    fieldMappingsBarrierLine = arcpy.na.NAClassFieldMappings(OutputNALayer,FieldMappingBarrierNameLine)
    #******default value 0 == restriction, 1 == scaled cost**********
    if LineBarrierWeight != "":
        LineList = LineBarriers.split(";")
        LineWeightList = LineBarrierWeight.split(",")
        if len(LineList) == len(LineWeightList):
            counttwo = 0
            for LB in LineList:
                lweight = LineWeightList[counttwo]
                if lweight.lower() == "r":
                    fieldMappingsBarrierLine["BarrierType"].defaultValue = 0
                    arcpy.na.AddLocations(OutputNALayer,FieldMappingBarrierNameLine, LB, fieldMappingsBarrierLine,"5000 Meters","","","","APPEND","","","","")
                    linemessagerestrict = ("{} set to restriction".format(LB))
                    arcpy.AddMessage(linemessagerestrict)
                    counttwo += 1
                else:
                    fieldMappingsBarrierLine["BarrierType"].defaultValue = 1
                    lfloat = float(lweight)
                    fieldMappingsBarrierLine["Attr_" + ImpedanceAttr].defaultValue = lfloat
                    arcpy.na.AddLocations(OutputNALayer,FieldMappingBarrierNameLine, LB, fieldMappingsBarrierLine,"5000 Meters","","","","APPEND","","","","")
                    linemessage = ("{} set to scaled cost, given weight {}".format(LB,lfloat))
                    arcpy.AddMessage(linemessage)
                    counttwo += 1
        else:
            raise Exception("Number of Line layers does not match length of line weight list")
    else:
        arcpy.AddMessage("Setting All Line Barriers To Barrier Type Restriction")
        fieldMappingsBarrierLine["BarrierType"].defaultValue = 0
        for LB in LineBarriers.split(";"):
           arcpy.na.AddLocations(OutputNALayer,FieldMappingBarrierNameLine, LB, fieldMappingsBarrierLine,"5000 Meters","","","","APPEND","","","","") 
else:
    arcpy.AddMessage("No PolyLine Barrier Layer Given")

"""
attempt to run standard NA Solve function
"""
try:
    #Load facilities and incidents locations
    arcpy.na.AddLocations(OutputNALayer, FacilitiesLayerNames, Facilities, "", "")
    arcpy.na.AddLocations(OutputNALayer, IncidentsLayerNames, Incidents, "","")
    
    #solve CF Layer
    arcpy.na.Solve(OutputNALayer)

    #select route features
    sel = arcpy.mapping.ListLayers(OutputNALayer, RoutesLayerName)[0]

    #copy selected route features
    CopyRouteFeatures = arcpy.CopyFeatures_management(sel, OutputLayerFilePath + "\\"+ OutputLayerName)
    arcpy.AddMessage("Copying route features to main output directory")

except Exception as e:
    #if initial solve fails attempt to solve by iteration of incident points and then appends final routes
    # Execute CreateFileGDB for backup GDB
    if not arcpy.Exists(out_folder_path):
        arcpy.AddMessage("Creating backup output directory")
        arcpy.CreateFileGDB_management(out_folder_path, out_name)
        backup = out_folder_path + "\\" + out_name
        arcpy.AddMessage("Writing to backup output directory")

        #load facilities
        arcpy.na.AddLocations(OutputNALayer, FacilitiesLayerNames, Facilities, "", "")
       
        #create a counter, search cursor to iterate through table and an empty list to store route files to merge
        counter=0
        cursor = arcpy.da.SearchCursor(Incidents,["SHAPE@","OBJECTID"])
        to_merge = []
            
        for row in cursor:
            row_geom = row[0]
            arcpy.na.AddLocations(OutputNALayer, IncidentsLayerNames, row_geom, "","","","","","CLEAR")
            #arcpy.AddMessage('OBJECT ROW ADDED:'+str(row[1]))
            #solve CF Layer
            try:
                arcpy.na.Solve(OutputNALayer)
            except:
                arcpy.AddMessage("Object:"+str(row[1])+" failed to solve")
                continue
            #select and save route features
            sel2 = arcpy.mapping.ListLayers(OutputNALayer,RoutesLayerName)[0]
            CopyRouteFeatures = arcpy.CopyFeatures_management(sel2, str(backup.strip(".gdb") +"_"+ str(counter)))
            to_merge.append(CopyRouteFeatures)
            counter += 1
                
        #perform a merge of the route files and store to backup geodatabase
        arcpy.AddMessage("Merging backup routes layers")
        arcpy.Merge_management(to_merge, backup + "_Merged")
        arcpy.AddMessage("Merge of backup layers complete")
        

        # If an error occurs, print line number and error message, contact your python programmer
        import traceback, sys
        tb = sys.exc_info()[2]
        print("An error occurred on line %i" % tb.tb_lineno)
        print(str(e))
        
    else:
        arcpy.AddMessage("Backup output already exists")
        backup = out_folder_path + "\\" + out_name
        arcpy.AddMessage("Writing to backup output directory")

        #load facilities
        arcpy.na.AddLocations(OutputNALayer, FacilitiesLayerNames, Facilities, "", "")
       
        #create a counter, search cursor to iterate through table and an empty list to store route files to merge
        counter=0
        cursor = arcpy.da.SearchCursor(Incidents,["SHAPE@","OBJECTID"])
        to_merge = []
            
        for row in cursor:
            row_geom = row[0]
            arcpy.na.AddLocations(OutputNALayer, IncidentsLayerNames, row_geom, "","","","","","CLEAR")
            #arcpy.AddMessage('OBJECT ADDED:'+str(row[1]))
            #solve CF Layer
            try:
                arcpy.na.Solve(OutputNALayer)
            except:
                arcpy.AddMessage("Object:"+str(row[1])+" failed to solve")
                continue
            #select and save route features
            sel2 = arcpy.mapping.ListLayers(OutputNALayer,RoutesLayerName)[0]
            CopyRouteFeatures = arcpy.CopyFeatures_management(sel2, str(backup.strip(".gdb") +"_"+ str(counter)))
            to_merge.append(CopyRouteFeatures)
            counter += 1
                
        #perform a merge of the route files and store to backup geodatabase
        arcpy.AddMessage("Merging backup routes layers")
        arcpy.Merge_management(to_merge, backup + "_Merged")
        arcpy.AddMessage("Merge of backup layers complete")

        # If an error occurs, print line number and error message, contact your python programmer
        import traceback, sys
        tb = sys.exc_info()[2]
        print("An error occurred on line %i" % tb.tb_lineno)
        print(str(e))
