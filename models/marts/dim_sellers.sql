{{
    config(
        materialized='table',
        unique_key='seller_id'
    )
}}

with sellers as (
    select * from {{ ref('stg_olist_sellers') }}
)

select * from sellers