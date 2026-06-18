{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'raw_sellers') }}
),

cleaned as (
    select
        seller_id,
        seller_zip_code_prefix::text as seller_zip_code_prefix,
        seller_city,
        seller_state
    from source
    where seller_id is not null
)

select * from cleaned