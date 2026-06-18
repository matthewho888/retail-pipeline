{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'raw_geolocation') }}
),

cleaned as (
    select
        geolocation_zip_code_prefix::text as geolocation_zip_code_prefix,
        geolocation_lat,
        geolocation_lng,
        geolocation_city,
        geolocation_state
    from source
    where geolocation_zip_code_prefix is not null 
)

select * from cleaned