{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'raw_category_translation') }}
),

cleaned as (
    select
        product_category_name,
        product_category_name_english
    from source
    where product_category_name is not null 
)

select * from cleaned