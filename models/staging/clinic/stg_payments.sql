select
    visit_id,
    patient_id,
    payment_method,
    insurance_status,
    cast(insurance_coverage_pct as integer) as insurance_coverage_pct,
    cast(amount_paid as decimal(10,2)) as amount_paid,
    cast(amount_owed as decimal(10,2)) as amount_owed,
    cast(payment_date as date) as payment_date
from {{ ref('raw_payments') }}