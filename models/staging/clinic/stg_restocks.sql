select
    drug_id,
    cast(quantity as integer) as quantity,
    supplier,
    cast(unit_cost as decimal(10,2)) as unit_cost,
    cast(restock_date as date) as restock_date
from {{ ref('raw_restocks') }}