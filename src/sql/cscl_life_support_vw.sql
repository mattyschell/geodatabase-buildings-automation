create or replace force view
    building_vw
as 
select
     CAST(OBJECTID AS INTEGER) as OBJECTID
    ,CAST(BIN AS INTEGER) AS BIN
    ,SHAPE AS SHAPE
from TABLE(cscl_life_support.bldg_doitt_edit());