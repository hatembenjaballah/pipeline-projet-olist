with orders as (
    select * from {{ ref('stg_olist_orders') }}
),

payments as (
    select
        order_id,
        sum(payment_value) as total_payment_value,
        count(distinct payment_type) as payment_methods_count
    from {{ ref('stg_olist_order_payments') }}
    group by order_id
),

reviews as (
    select
        order_id,
        avg(review_score) as avg_review_score,
        count(review_id) as reviews_count
    from {{ ref('stg_olist_order_reviews') }}
    group by order_id
),

final as (
    select
        o.order_id,
        o.customer_id,
        o.order_status,
        o.purchased_at,
        o.approved_at,
        o.delivered_to_carrier_at,
        o.delivered_to_customer_at,
        o.estimated_delivery_at,
        datediff('day', o.purchased_at, o.delivered_to_customer_at) as days_to_deliver,
        datediff('day', o.estimated_delivery_at, o.delivered_to_customer_at) as days_early_or_late,
        coalesce(p.total_payment_value, 0) as total_payment_value,
        coalesce(p.payment_methods_count, 0) as payment_methods_count,
        r.avg_review_score,
        coalesce(r.reviews_count, 0) as reviews_count
    from orders o
    left join payments p on o.order_id = p.order_id
    left join reviews r on o.order_id = r.order_id
)

select * from final