select
    visit_id,
    patient_id,
    diagnosis_id,
    drug_id,
    dispensed_by_staff_id,
    cast(quantity as integer) as quantity,
    cast(unit_price as decimal(10,2)) as unit_price,
    cast(quantity as decimal(10,2)) * cast(unit_price as decimal(10,2)) as line_total,
    cast(dispense_date as date) as dispense_date
from {{ ref('raw_dispensing') }}