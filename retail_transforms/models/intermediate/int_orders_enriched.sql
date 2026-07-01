WITH orders AS (
    SELECT order_id, order_item_id, product_id, seller_id, price, shipping_limit_at
    FROM retail_transforms.stg_order_items
),

joined_product_info AS (
    SELECT
        one.order_id, one.order_item_id, one.seller_id, one.product_id,
        two.product_category_name, one.price, one.shipping_limit_at
    FROM orders one
    LEFT JOIN retail_transforms.stg_products two
        ON one.product_id = two.product_id
),

joined_order_shipping AS (
    SELECT
        two.order_id, two.order_item_id, three.customer_id, two.seller_id, two.product_id,
        two.product_category_name, two.price, two.shipping_limit_at,
        three.order_status, three.ordered_at, three.approved_at,
        three.shipped_at, three.delivered_at, three.estimated_delivery_at
    FROM joined_product_info two
    LEFT JOIN retail_transforms.stg_orders three
        ON two.order_id = three.order_id
),
joined_translation AS (
    SELECT
        three.order_id, three.order_item_id, three.customer_id, three.seller_id, three.product_id,
        four.product_category_name_english, three.price, three.shipping_limit_at,
        three.order_status, three.ordered_at, three.approved_at,
        three.shipped_at, three.delivered_at, three.estimated_delivery_at
    FROM joined_order_shipping three
    LEFT JOIN retail_transforms.stg_category_translation four
        ON three.product_category_name = four.product_category_name
),
joined_final AS (
	SELECT 
	    four.order_id, four.order_item_id, four.customer_id, five.customer_unique_id, four.seller_id, four.product_id,
        four.product_category_name_english, four.price, four.shipping_limit_at,
        four.order_status, four.ordered_at, four.approved_at,
        four.shipped_at, four.delivered_at, four.estimated_delivery_at
	FROM joined_translation four
	LEFT JOIN retail_transforms.stg_customers five
		ON four.customer_id = five.customer_id
)

SELECT *
FROM joined_final
ORDER BY order_id