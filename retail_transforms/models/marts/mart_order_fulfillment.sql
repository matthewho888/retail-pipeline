SELECT DISTINCT
    order_id,
    order_status,
    ordered_at,
    delivered_at,
    estimated_delivery_at,
    CASE 
        WHEN order_status = 'delivered' AND delivered_at <= estimated_delivery_at THEN 'on_time'
        WHEN order_status = 'delivered' AND delivered_at > estimated_delivery_at THEN 'late'
        ELSE NULL
    END AS delivery_status,
    delivered_at - estimated_delivery_at AS days_difference
FROM retail_transforms.int_orders_enriched