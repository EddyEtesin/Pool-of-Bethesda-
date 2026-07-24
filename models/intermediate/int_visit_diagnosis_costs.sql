with visits as (
    select * from {{ ref('stg_visits') }}
),

dispensing_costs as (
    select
        visit_id,
        diagnosis_id,
        sum(line_total) as total_drug_cost
    from {{ ref('stg_dispensing') }}
    group by visit_id, diagnosis_id
),

lab_costs as (
    select
        visit_id,
        diagnosis_id,
        sum(test_cost) as total_lab_cost
    from {{ ref('stg_labs') }}
    group by visit_id, diagnosis_id
)

select
    v.visit_id,
    v.patient_id,
    v.diagnosis_id,
    v.attending_staff_id,
    v.visit_date,
    coalesce(d.total_drug_cost, 0) as total_drug_cost,
    coalesce(l.total_lab_cost, 0) as total_lab_cost,
    coalesce(d.total_drug_cost, 0) + coalesce(l.total_lab_cost, 0) as total_diagnosis_cost
from visits v
left join dispensing_costs d
    on v.visit_id = d.visit_id and v.diagnosis_id = d.diagnosis_id
left join lab_costs l
    on v.visit_id = l.visit_id and v.diagnosis_id = l.diagnosis_id