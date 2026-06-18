{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'raw_order_reviews') }}
),

cleaned as (
    select
        review_id,
        order_id,
        review_score,
        review_comment_title,
        review_comment_message,
        review_creation_date::timestamp as review_creation_at,
        review_answer_timestamp::timestamp as review_answer_at
    from source
    where review_id is not null and order_id is not null
)

select * from cleaned