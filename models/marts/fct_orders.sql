{{
    config(
        materialized='table',
        unique_key='order_id'
    )
}}

with orders as (
    select * from {{ ref('int_orders_enriched') }}
),

final as (
    select
        order_id,
        customer_id,
        order_status,
        purchased_at,
        approved_at,
        delivered_to_carrier_at,
        delivered_to_customer_at,
        estimated_delivery_at,
        days_to_deliver,
        days_early_or_late,
        total_payment_value,
        payment_methods_count,
        avg_review_score,
        reviews_count,
        case
            when delivered_to_customer_at is null then 'not_delivered'
            when days_early_or_late <= 0 then 'on_time'
            else 'late'
        end as delivery_status
    from orders
)

select * from final