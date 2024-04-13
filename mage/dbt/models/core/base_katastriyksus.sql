{{ 
    config(
        materialized='table',
        partition_by={
                "field": "registration_date_year",
                "data_type": "int64",
                "range": {
                    "start": 0,
                    "end": 9999,
                    "interval": 1
                }
            },
        cluster_by=["county_name"]
    ) 
}}

with data as (

    -- Select data from the external table
    SELECT
        TUNNUS as unit_id,
        cast(HKOOD as INTEGER) as settlement_id,
        MK_NIMI	as county_name,
        OV_NIMI	as municipality_name,
        AY_NIMI as settlements_name,
        L_AADRESS as address,
        cast(REGISTR as DATE) as registration_date,
        --new column
        cast(EXTRACT(YEAR FROM REGISTR) as INTEGER) AS registration_date_year,
        cast(MUUDET as DATE) as amendment_date,
        SIHT1 as use1,
        SIHT2 as use2,
        SIHT3 as use3,	
        cast(SO_PRTS1 as INTEGER) as use1_percent,
        cast(SO_PRTS2 as INTEGER) as use2_percent,   
        cast(SO_PRTS3 as INTEGER) as use3_percent,
        PINDALA	as area,	
        RUUMPIND as spatial_area,	
        REG_YHIK as area_unit,
        cast(HARITAV as INTEGER) as cultivated_area,
        cast(ROHUMAA as INTEGER) as natural_grassland,
        cast(METS as INTEGER) as forest,	
        cast(OUEMAA as INTEGER)	as courtyard,
        cast(MUUMAA as INTEGER)	as other_land,
        KINNISTU as registered_immovable_number,
        MOOTVIIS as cadastral_unit_form,
        MOOTJA as surveyor,
        cast(MOODUST as DATE) as survey_date,
        OMVIIS as formation_manner,
        OMVORM as ownership_type,
        cast(MAKS_HIND as INTEGER) as assessed_value,
        MARKETEKST as note,
        cast(EKSPORT as DATE) as export_date	

    FROM {{ source('staging', 'stg_katastriyksus_ext') }}

)

SELECT * FROM data