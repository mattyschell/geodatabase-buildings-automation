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
-- lineage_id though?
--
SELECT
        b.doitt_id,
        b.SHAPE,
        b.OBJECTID ,
        b.SE_ANNO_CAD_DATA
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
                l.lineage_name = 11186        --:LINEAGE_NAME1
            AND l.lineage_id <= 11268)        --:STATE_ID1
        AND SDE_STATE_ID = 0 )
UNION ALL
    SELECT
        a.doitt_id,
        a.SHAPE,
        a.OBJECTID ,
        a.SE_ANNO_CAD_DATA
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
                l.lineage_name = 11186         --:LINEAGE_NAME2
            AND l.lineage_id <= 11268))        --:STATE_ID2
    AND a.SDE_STATE_ID = SL.lineage_id
    AND a.SDE_STATE_ID > 0
    AND SL.lineage_name = 11186                --:LINEAGE_NAME3
    AND SL.lineage_id <= 11268                 --:STATE_ID3