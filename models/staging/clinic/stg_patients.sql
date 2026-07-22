select
    patient_id,
    cast(dob as date) as dob,
    gender,
    cast(registration_date as date) as registration_date
from {{ ref('raw_patients') }}