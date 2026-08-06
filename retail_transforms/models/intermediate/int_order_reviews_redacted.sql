SELECT
    order_id,
    review_score,
    regexp_replace(
        regexp_replace(
            review_comment_message,
            '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  -- emails
            '[REDACTED]',
            'g'
        ),
        '\+?\d[\d\s().-]{7,}\d',  -- phone numbers (loose match)
        '[REDACTED]',
        'g'
    ) AS review_comment_redacted

FROM {{ ref('stg_order_reviews') }}