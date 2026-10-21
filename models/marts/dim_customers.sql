{{
    config(
        materialized='table',
        unique_key='customer_id'
    )
}}

with customers as (
    select * from {{ ref('int_customers_with_geolocation') }}
)

select * from customers