select
	customer_unique_id,
	MAX(ordered_at) as most_recent_purchase,
	COUNT(DISTINCT order_id) as num_of_orders,
	SUM(price) as total_sum
from retail_transforms.int_orders_enriched
group by customer_unique_id

