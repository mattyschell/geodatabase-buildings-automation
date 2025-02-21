-- we require the ability to read BUILDING BINS
-- into CSCL from Arcmap classic
--
-- the following describes my least favorite type of GIS work:
-- spelunking through all possible paths in old ESRI software
-- to find a path that does not error 
--
-- one complication with this spelunking is that some failures fail in
-- ways where its hard to know if cleanup works
-- is there still a building_vw registered somewhere causing future failures?
-- this is why building_vw## increments
--
-- another complication
-- many of the ArcMap tools hang unresponsively for 5-10 minutes
-- so any test requires not forgetting what you were doing
--   (or getting confused spelunking through a parallel path while waiting)
-- I *think* I was pretty attentive.  But realistically, no, its impossible
--
-- Approach1 (with several variations)
--   create view in SQL (created in both bldg and bldg_readonly)
--   register with geodatabse
--   Register with Pro - ArcMap errors with message about column data types
--   Register with ArcMap - Hangs for a long time before opening
--   Register tool fails with 99999 "underlying dbms error"
-- Approach 2 (with variations)
--   Create view with arcmap "create database view" tool
--   arcpy.CreateDatabaseView_management
--   runs for 10 minutes and completes
--   it just creates a view still have to register
--   Register with geodatabase - hangs for 10 minutes then opens
--   register throws 999999 and "underlying dbms error"
-- Approach 3 (the only one that does not error)
--    create view with SQL
--    use as "query layer" in arcmap
--    slow slow slow
--
-- tried with and without CASTs 
-- testing with minimum columns for now
-- we will add the other columns later. or never. 
create or replace force view
    building_vw
as 
select
     CAST(OBJECTID AS INTEGER) as OBJECTID
    --,NAME
    ,CAST(BIN AS INTEGER) AS BIN
    --,BASE_BBL
    --,CONSTRUCTION_YEAR
    --,GEOM_SOURCE
    --,LAST_STATUS_TYPE
    --,DOITT_ID
    --,HEIGHT_ROOF
    --,FEATURE_CODE
    --,GROUND_ELEVATION
    --,CREATED_USER
    --,CREATED_DATE
    --,LAST_EDITED_USER
    --,LAST_EDITED_DATE
    --,MAPPLUTO_BBL
    --,ALTERATION_YEAR
    ,CAST(SHAPE as MDSYS.SDO_GEOMETRY) AS SHAPE
from bldg.building_evw;
