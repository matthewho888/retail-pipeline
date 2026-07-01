WITH orders_enriched_seller_info AS (
	SELECT one.seller_id, one.order_id,
		two.seller_zip_code_prefix, two.seller_city, two.seller_state, 
		one.ordered_at, one.price
	FROM retail_transforms.int_orders_enriched one
	LEFT JOIN retail_transforms.stg_sellers two
		ON one.seller_id = two.seller_id
),
combined_review AS (
	SELECT two.seller_id, two.order_id,
		two.seller_zip_code_prefix, two.seller_city, two.seller_state, 
		two.ordered_at, two.price, three.review_score
	FROM orders_enriched_seller_info two
	LEFT JOIN retail_transforms.stg_order_reviews three
		ON two.order_id = three.order_id
)
SELECT
	seller_id, seller_state, seller_city, seller_zip_code_prefix,
	SUM(price) as total_revenue,
	MAX(ordered_at) as most_recent_sale,
	AVG(review_score) as avg_review_score,
	COUNT(review_score) as num_of_reviews
FROM combined_review
GROUP BY seller_id, seller_state, seller_city, seller_zip_code_prefix
