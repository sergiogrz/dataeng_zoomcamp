{{
    config(
        materialized='view'
    )
}}

select
    dispatching_base_num,

    -- identifiers
    cast(pu_location_id as integer) as  pu_location_id,
    cast(do_location_id as integer) as do_location_id,

    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp) as dropoff_datetime,

    -- trip info
    sr_flag
from {{ source('staging', 'fhv_taxi_data') }}


-- dbt build --select <model.sql> --vars '{"is_test_run": false}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}