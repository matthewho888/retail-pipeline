{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'raw_customers') }}
),

cleaned as (
    select
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix::text as customer_zip_code_prefix,
        customer_city,
        customer_state
    from source
    where customer_id is not null
)

select * from cleaned