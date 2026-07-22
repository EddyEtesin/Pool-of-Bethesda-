select
    visit_id,
    patient_id,
    cast(consultation_fee as decimal(10,2)) as consultation_fee,
    cast(visit_date as date) as visit_date
from {{ ref('raw_consultations') }}