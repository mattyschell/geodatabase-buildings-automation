CREATE OR REPLACE PACKAGE CSCL_LIFE_SUPPORT
AUTHID CURRENT_USER
AS

type 
    building_vw_rec 
is record (
     objectid integer
    ,bin      integer
    ,shape    mdsys.sdo_geometry
 );

type 
    building_vw_tab 
is table of 
    building_vw_rec;

procedure create_bldg_doitt_edit_vw;

-- create or replace force view building_vw as
-- SELECT * FROM TABLE(cscl_life_support.bldg_doitt_edit());

function bldg_doitt_edit
return cscl_life_support.building_vw_tab pipelined;

function brooklyn_doitt_edit
return cscl_life_support.building_vw_tab pipelined;



END CSCL_LIFE_SUPPORT;
/