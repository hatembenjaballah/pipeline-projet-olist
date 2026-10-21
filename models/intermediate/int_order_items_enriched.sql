with order_items as (
    select * from {{ ref('stg_olist_order_items') }}
),

products as (
    select * from {{ ref('stg_olist_products') }}
),

sellers as (
    select * from {{ ref('stg_olist_sellers') }}
),

final as (
    select
        oi.order_id,
        oi.order_item_id,
        oi.product_id,
        oi.seller_id,
        oi.item_price,
        oi.freight_value,
        oi.item_price + oi.freight_value as total_item_value,
        p.product_category_name,
        p.product_weight_g,
        s.city as seller_city,
        s.state as seller_state
    from order_items oi
    left join products p on oi.product_id = p.product_id
    left join sellers s on oi.seller_id = s.seller_id
)

select * from final