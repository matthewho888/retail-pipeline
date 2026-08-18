SELECT
    customer_id,
    LEFT(customer_zip_code_prefix, 3) AS customer_zip_region,
    customer_city,
    customer_state
FROM {{ ref('stg_customers') }}