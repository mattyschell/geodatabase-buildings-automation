CREATE OR REPLACE PACKAGE BODY CSCL_LIFE_SUPPORT
AS

    PROCEDURE create_bldg_doitt_edit_vw
    AS

        psql      varchar2(4000);
        regid     number;
        bldgowner varchar2(32) := 'BLDG';
        bldgtab   varchar2(32) := 'BUILDING';
        bldgver   varchar2(32) := 'BLDG_DOITT_EDIT';

        -- SQL> begin
        -- 2    cscl_life_support.create_bldg_doitt_edit_vw();
        -- 3    end;
        -- 4    /

        -- a version (sde.versions) has a state_id (ex 11271)
        -- state_id joins to state_id in sde.states
        -- states.lineage_name joins to one or more 
        --    sde.state_lineages (lineage_name, lineage_id) pairs
        -- all lower lineage_ids are children, granchildren, etc of the parent lineage
        -- dont overthink, use the original sde.versions.state_id as parent lineage_id
        --    (note the ESRI bind variable "l.lineage_id <= :STATE_ID1")
        -- lineage name seems pretty stable for bldg_doitt_edit

        -- check yourself

        -- select 
        --    lineage_name 
        -- from 
        --    sde.STATE_LINEAGES
        -- where 
        --    lineage_id = (select 
        --                      state_id 
        --                  from 
        --                      sde.versions
        --                  where 
        --                      owner = 'BLDG'
        --                  and name = 'BLDG_DOITT_EDIT')

    BEGIN

        psql := 'select '
             || '   registration_id '
             || 'from '
             || '   sde.table_registry '
             || 'where '
             || '   table_name = :p1 '
             || 'and '
             || '   owner = :p2 ';

        execute immediate psql into regid using bldgtab
                                               ,bldgowner;
        
        psql := 'create or replace force view '
             || '    bldg_doitt_edit_vw as  '
             || 'WITH ancestor AS ( '
             || '    SELECT '
             || '        state_id '
             || '    FROM '
             || '        sde.versions '
             || '    WHERE '
             || '        owner = ''' || bldgowner || ''' '
             || '        AND name = ''' || bldgver || ''') '
             || 'SELECT '
             || '        b.objectid, '
             || '        b.doitt_id, '
             || '        b.bin, '
             || '        b.shape        '
             || 'FROM '
             || '        ' || bldgowner || '.' || bldgtab || ' b '
             || 'WHERE '
             || '     b.OBJECTID NOT IN ( '
             || '        SELECT '
             || '                /*+ HASH_AJ */ '
             || '            SDE_DELETES_ROW_ID '
             || '        FROM '
             || '                ' || bldgowner || '.D' || to_char(regid) || ' '
             || '        WHERE '
             || '            DELETED_AT IN ( '
             || '                SELECT '
             || '                        l.lineage_id '
             || '                FROM '
             || '                        SDE.state_lineages l '
             || '                WHERE '
             || '                    l.lineage_name = (select  '
             || '                                        lineage_name  '
             || '                                     from  '
             || '                                        sde.STATE_LINEAGES '
             || '                                     where  '
             || '                                        lineage_id = (select state_id from ancestor)) '
             || '                AND  '
             || '                    l.lineage_id <= (select state_id from ancestor) '
             || '            )        '
             || '        AND SDE_STATE_ID = 0  '
             || '        ) '
             || 'UNION ALL '
             || '    SELECT '
             || '        a.objectid, '
             || '        a.doitt_id, '
             || '        a.bin, '
             || '        a.shape   '
             || 'FROM '
             || '        ' || bldgowner || '.A' || to_char(regid) || ' a, '
             || '        SDE.state_lineages SL '
             || 'WHERE '
             || '     (a.OBJECTID, '
             || '      a.SDE_STATE_ID) NOT IN ( '
             || '        SELECT '
             || '                /*+ HASH_AJ */ '
             || '            SDE_DELETES_ROW_ID, '
             || '            SDE_STATE_ID '
             || '        FROM '
             || '            ' || bldgowner || '.D' || to_char(regid) || ' '
             || '        WHERE '
             || '            DELETED_AT IN ( '
             || '                SELECT '
             || '                        l.lineage_id '
             || '                FROM '
             || '                        SDE.state_lineages l '
             || '                WHERE '
             || '                        l.lineage_name = (select  '
             || '                                        lineage_name  '
             || '                                     from  '
             || '                                        sde.STATE_LINEAGES '
             || '                                     where  '
             || '                                        lineage_id = (select state_id from ancestor)) '
             || '                    AND l.lineage_id <= (select state_id from ancestor) '
             || '            ) '
             || '    )         '
             || '    AND a.SDE_STATE_ID = SL.lineage_id '
             || '    AND a.SDE_STATE_ID > 0 '
             || '    AND SL.lineage_name = (select  '
             || '                                lineage_name  '
             || '                             from  '
             || '                                sde.STATE_LINEAGES '
             || '                             where  '
             || '                                lineage_id = (select state_id from ancestor) '
             || '                          )                  '
             || '    AND SL.lineage_id <= (select state_id from ancestor) ';

        execute immediate psql;

        psql := 'grant select on bldg_doitt_edit_vw to "BLDG_READONLY"';

        execute immediate psql;

    END create_bldg_doitt_edit_vw;


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


   FUNCTION brooklyn_doitt_edit 
   RETURN cscl_life_support.building_vw_tab PIPELINED
   AS

    -- trash trash trash
    -- could add borough code as an input however see previous comment
    
    buildingchunk   cscl_life_support.building_vw_tab;
    psql            varchar2(4000);
    my_cursor       sys_refcursor;

    BEGIN

        sde.version_util.set_current_version('BLDG.BLDG_DOITT_EDIT');

        psql := 'select '
             || '   objectid, bin, shape '
             || 'from '
             || '   bldg.building_evw a '
             || 'where '
             || '   a.base_bbl like :p1 '
             || 'order by '
             || '   a.base_bbl ';
        
        BEGIN
            
            open my_cursor for psql using '3%';
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

    END brooklyn_doitt_edit;

-- you love to see it
END CSCL_LIFE_SUPPORT;
/