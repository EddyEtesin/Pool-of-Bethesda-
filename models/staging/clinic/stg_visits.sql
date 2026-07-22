select
    visit_id,
    patient_id,
    diagnosis_id,
    attending_staff_id,
    cast(visit_date as date) as visit_date
from {{ ref('raw_visits') }}