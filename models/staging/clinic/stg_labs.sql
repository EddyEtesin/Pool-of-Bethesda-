select
    visit_id,
    patient_id,
    diagnosis_id,
    conducted_by_staff_id,
    lower(test_type) as test_type,
    cast(test_cost as decimal(10,2)) as test_cost,
    cast(test_date as date) as test_date,
    lower(result) as result
from {{ ref('raw_labs') }}