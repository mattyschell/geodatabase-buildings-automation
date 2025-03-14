-- SAMPLE ONLY. FOR REFERENCE
-- this is 2 versions of the real bldg_doitt_edit view as tested in dev 
-- Database object names were only valid at that time not now
-- version 1 is close to what went into the ps/sql package
-- version 2 is closer to the original as sniffed from ArcGIS Pro
--    it includes :bind variables for reference
--
-- a version (sde.versions) has a state_id (ex 11271)
-- state_id joins to state_id in sde.states
-- states.lineage_name joins to one or more 
--    sde.state_lineages (lineage_name, lineage_id) pairs
-- all lower lineage_ids are children, granchildren, etc of the parent lineage
-- dont overthink, use the original sde.versions.state_id as parent lineage_id
--    (note the ESRI bind variable "l.lineage_id <= :STATE_ID1")
-- lineage name seems pretty stable for bldg_doitt_edit
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
create or replace force view 
    bldg_doitt_edit_vw as 
WITH ancestor AS (
    SELECT
        state_id
    FROM
        sde.versions
    WHERE
        owner = 'BLDG'
        AND name = 'BLDG_DOITT_EDIT')
SELECT
        b.OBJECTID,
        b.doitt_id,
        b.bin,
        b.SHAPE       
FROM
        BLDG.BUILDING b
WHERE
     b.OBJECTID NOT IN (
        SELECT
                /*+ HASH_AJ */
            SDE_DELETES_ROW_ID
        FROM
                BLDG.D5729
        WHERE
            DELETED_AT IN (
                SELECT
                        l.lineage_id
                FROM
                        SDE.state_lineages l
                WHERE
                    l.lineage_name = (select 
                                        lineage_name 
                                     from 
                                        sde.STATE_LINEAGES
                                     where 
                                        lineage_id = (select state_id from ancestor))        
                AND 
                    l.lineage_id <= (select state_id from ancestor)
            )       
        AND SDE_STATE_ID = 0 
        )
UNION ALL
    SELECT
        a.OBJECTID,
        a.doitt_id,
        a.bin,
        a.SHAPE  
FROM
        BLDG.A5729 a,
        SDE.state_lineages SL
WHERE
     (a.OBJECTID,
      a.SDE_STATE_ID) NOT IN (
        SELECT
                /*+ HASH_AJ */
            SDE_DELETES_ROW_ID,
            SDE_STATE_ID
        FROM
            BLDG.D5729
        WHERE
            DELETED_AT IN (
                SELECT
                        l.lineage_id
                FROM
                        SDE.state_lineages l
                WHERE
                        l.lineage_name = (select 
                                        lineage_name 
                                     from 
                                        sde.STATE_LINEAGES
                                     where 
                                        lineage_id = (select state_id from ancestor))         
                    AND l.lineage_id <= (select state_id from ancestor)
            )
    )        
    AND a.SDE_STATE_ID = SL.lineage_id
    AND a.SDE_STATE_ID > 0
    AND SL.lineage_name = (select 
                                lineage_name 
                             from 
                                sde.STATE_LINEAGES
                             where 
                                lineage_id = (select state_id from ancestor)
                          )                 
    AND SL.lineage_id <= (select state_id from ancestor);    
--
-----------------------------
-- SELECT only original play 
-----------------------------
--
    SELECT
        b.OBJECTID,
        b.doitt_id,
        b.bin,
        b.SHAPE       
FROM
        BLDG.BUILDING b
WHERE
     b.OBJECTID NOT IN (
    SELECT
            /*+ HASH_AJ */
        SDE_DELETES_ROW_ID
    FROM
            BLDG.D5729
    WHERE
        DELETED_AT IN (
        SELECT
                l.lineage_id
        FROM
                SDE.state_lineages l
        WHERE
            l.lineage_name = (select 
                                lineage_name 
                             from 
                                sde.STATE_LINEAGES
                             where 
                                lineage_id = (select 
                                                state_id 
                                              from 
                                                sde.versions
                                              where 
                                                 owner = 'BLDG'
                                               and name = 'BLDG_DOITT_EDIT'))        
        AND 
            l.lineage_id <= (select 
                                                state_id 
                                              from 
                                                sde.versions
                                              where 
                                                 owner = 'BLDG'
                                               and name = 'BLDG_DOITT_EDIT'))        --:STATE_ID1
        AND SDE_STATE_ID = 0 )
UNION ALL
    SELECT
        a.OBJECTID,
        a.doitt_id,
        a.bin,
        a.SHAPE  
FROM
        BLDG.A5729 a,
        SDE.state_lineages SL
WHERE
     (a.OBJECTID,
        a.SDE_STATE_ID) NOT IN (
    SELECT
            /*+ HASH_AJ */
        SDE_DELETES_ROW_ID,
            SDE_STATE_ID
    FROM
            BLDG.D5729
    WHERE
            DELETED_AT IN (
        SELECT
                l.lineage_id
        FROM
                SDE.state_lineages l
        WHERE
                l.lineage_name = (select 
                                lineage_name 
                             from 
                                sde.STATE_LINEAGES
                             where 
                                lineage_id = (select 
                                                state_id 
                                              from 
                                                sde.versions
                                              where 
                                                 owner = 'BLDG'
                                               and name = 'BLDG_DOITT_EDIT'))          --:LINEAGE_NAME2
            AND l.lineage_id <= (select 
                                                state_id 
                                              from 
                                                sde.versions
                                              where 
                                                 owner = 'BLDG'
                                               and name = 'BLDG_DOITT_EDIT')))        --:STATE_ID2
    AND a.SDE_STATE_ID = SL.lineage_id
    AND a.SDE_STATE_ID > 0
    AND SL.lineage_name = (select 
                                lineage_name 
                             from 
                                sde.STATE_LINEAGES
                             where 
                                lineage_id = (select 
                                                state_id 
                                              from 
                                                sde.versions
                                              where 
                                                 owner = 'BLDG'
                                               and name = 'BLDG_DOITT_EDIT'))                 --:LINEAGE_NAME3
    AND SL.lineage_id <= (select 
                                                state_id 
                                              from 
                                                sde.versions
                                              where 
                                                 owner = 'BLDG'
                                               and name = 'BLDG_DOITT_EDIT')                 --:STATE_ID3           