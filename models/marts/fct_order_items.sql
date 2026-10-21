{{
    config(
        materialized='table',
        unique_key='order_item_id'
    )
}}

with order_items as (
    select * from {{ ref('int_order_items_enriched') }}
)

select * from order_items