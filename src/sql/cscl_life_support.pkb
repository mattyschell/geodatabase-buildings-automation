CREATE OR REPLACE PACKAGE BODY CSCL_LIFE_SUPPORT
AS

   FUNCTION bldg_doitt_edit 
   RETURN cscl_life_support.building_vw_tab PIPELINED
   AS

    -- yes i know this is nutty
    
    buildingchunk   cscl_life_support.building_vw_tab;
    psql            varchar2(4000);
    my_cursor       sys_refcursor;

   BEGIN

        sde.version_util.set_current_version('BLDG.BLDG_DOITT_EDIT');

        psql := 'select objectid, bin, shape from bldg.building_evw';
        
        BEGIN
            
            open my_cursor for psql;
            loop

                fetch my_cursor bulk collect into buildingchunk limit 10000;
                exit when buildingchunk.COUNT = 0;

                for i in 1 .. buildingchunk.count
                loop

                    PIPE ROW(buildingchunk(i));

                end loop;

            end  loop;            

        END;

        close my_cursor;

   END bldg_doitt_edit;

-- you love to see it
END CSCL_LIFE_SUPPORT;
/