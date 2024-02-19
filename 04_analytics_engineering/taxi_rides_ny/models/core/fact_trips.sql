{{
    config(
        materialized='table'
    )
}}

with green_data as (
    select *,
            'Green' as service_type
    from {{ ref('stg_green_taxi_data') }}
),

yellow_data as (
    select *,
            'Yellow' as service_type
    from {{ ref('stg_yellow_taxi_data') }}
),
trips_union as (
    select * from green_data
    union all
    select * from yellow_data
),
dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)

select
    trips_union.trip_id, 
    trips_union.vendor_id, 
    trips_union.service_type,
    trips_union.ratecode_id, 
    trips_union.pu_location_id, 
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone, 
    trips_union.do_location_id,
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,  
    trips_union.pickup_datetime, 
    trips_union.dropoff_datetime, 
    trips_union.store_and_fwd_flag, 
    trips_union.passenger_count, 
    trips_union.trip_distance, 
    trips_union.trip_type, 
    trips_union.fare_amount, 
    trips_union.extra, 
    trips_union.mta_tax, 
    trips_union.tip_amount, 
    trips_union.tolls_amount, 
    trips_union.ehail_fee, 
    trips_union.improvement_surcharge, 
    trips_union.total_amount, 
    trips_union.payment_type, 
    trips_union.payment_type_description, 
    trips_union.congestion_surcharge
from trips_union
inner join dim_zones as pickup_zone
on trips_union.pu_location_id = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on trips_union.do_location_id = dropoff_zone.locationid