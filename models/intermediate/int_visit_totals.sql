with diagnosis_costs as (
    select
        visit_id,
        patient_id,
        sum(total_diagnosis_cost) as total_diagnoses_cost
    from {{ ref('int_visit_diagnosis_costs') }}
    group by visit_id, patient_id
),

consultations as (
    select * from {{ ref('stg_consultations') }}
),

payments as (
    select * from {{ ref('stg_payments') }}
)

select
    c.visit_id,
    c.patient_id,
    c.visit_date,
    c.consultation_fee,
    coalesce(dc.total_diagnoses_cost, 0) as total_diagnoses_cost,
    c.consultation_fee + coalesce(dc.total_diagnoses_cost, 0) as total_visit_cost,
    p.payment_method,
    p.insurance_status,
    p.insurance_coverage_pct,
    p.amount_paid,
    p.amount_owed
from consultations c
left join diagnosis_costs dc
    on c.visit_id = dc.visit_id and c.patient_id = dc.patient_id
left join payments p
    on c.visit_id = p.visit_id