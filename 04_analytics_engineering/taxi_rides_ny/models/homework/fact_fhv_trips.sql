{{
    config(
        materialized='table'
    )
}}

with fhv_data as (
    select *,
            'Fhv' as service_type
    from {{ ref('stg_fhv_data') }}
),

dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)

select
    fhv_data.dispatching_base_num,
    fhv_data.service_type,
    fhv_data.pu_location_id,
    pickup_zone.borough as pickup_borough,
    pickup_zone.zone as pickup_zone,
    dropoff_zone.borough as dropoff_borough,
    dropoff_zone.zone as dropoff_zone,
    fhv_data.pickup_datetime,
    fhv_data.dropoff_datetime,
    fhv_data.sr_flag
from fhv_data
inner join dim_zones as pickup_zone
on fhv_data.pu_location_id = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhv_data.do_location_id = dropoff_zone.locationid

