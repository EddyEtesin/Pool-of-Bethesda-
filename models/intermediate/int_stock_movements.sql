with stock_out as (
    select
        drug_id,
        dispense_date as movement_date,
        -quantity as quantity_change,
        'dispensing' as movement_type
    from {{ ref('stg_dispensing') }}
),

stock_in as (
    select
        drug_id,
        restock_date as movement_date,
        quantity as quantity_change,
        'restock' as movement_type
    from {{ ref('stg_restocks') }}
)

select * from stock_out
union all
select * from stock_in