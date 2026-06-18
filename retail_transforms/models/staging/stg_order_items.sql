{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'raw_order_items') }}
),

cleaned as (
    select
        order_id,
        order_item_id,
        product_id,
        seller_id,
        shipping_limit_date::timestamp as shipping_limit_at,
        freight_value
    from source
    where order_id is not null
)

select * from cleaned