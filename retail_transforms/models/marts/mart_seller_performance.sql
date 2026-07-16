WITH seller_orders AS (
    SELECT
        orders.seller_id,
        orders.order_id,
        sellers.seller_zip_code_prefix,
        sellers.seller_city,
        sellers.seller_state,

        MAX(orders.ordered_at) AS ordered_at,
        SUM(orders.price) AS order_revenue

    FROM retail_transforms.int_orders_enriched AS orders

    LEFT JOIN retail_transforms.stg_sellers AS sellers
        ON orders.seller_id = sellers.seller_id

    GROUP BY
        orders.seller_id,
        orders.order_id,
        sellers.seller_zip_code_prefix,
        sellers.seller_city,
        sellers.seller_state
),

reviews_by_order AS (
    SELECT
        order_id,
        AVG(review_score) AS review_score

    FROM retail_transforms.stg_order_reviews

    GROUP BY order_id
)

SELECT
    seller_orders.seller_id,
    seller_orders.seller_state,
    seller_orders.seller_city,
    seller_orders.seller_zip_code_prefix,

    SUM(seller_orders.order_revenue) AS total_revenue,
    MAX(seller_orders.ordered_at) AS most_recent_sale,
    AVG(reviews_by_order.review_score) AS avg_review_score,
    COUNT(reviews_by_order.review_score) AS num_of_reviews

FROM seller_orders

LEFT JOIN reviews_by_order
    ON seller_orders.order_id = reviews_by_order.order_id

GROUP BY
    seller_orders.seller_id,
    seller_orders.seller_state,
    seller_orders.seller_city,
    seller_orders.seller_zip_code_prefix