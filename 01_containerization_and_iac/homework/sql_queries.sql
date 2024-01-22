-- How many taxi trips were totally made on September 18th 2019?
select count(*)
from green_taxi_data
where date(lpep_pickup_datetime) = '2019-09-18'
and date(lpep_dropoff_datetime) = '2019-09-18';


-- Which was the pick up day with the largest trip distance?
select 
	date(lpep_pickup_datetime) as pickup_date,
	max(trip_distance) as max_trip_distance
from green_taxi_data
where date(lpep_pickup_datetime) between '2019-09-01' and '2019-09-30'
group by pickup_date
order by max_trip_distance desc;


-- Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown
-- Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
select
	z."Borough" as borough,
	sum(gt.total_amount) as sum_total_amount
from green_taxi_data as gt
inner join taxi_zones as z
on gt."PULocationID" = z."LocationID"
where date(lpep_pickup_datetime) = '2019-09-18'
and z."Borough" != 'Unknown'
group by borough
having sum(gt.total_amount) > 50000
order by sum_total_amount desc;


-- For the passengers picked up in September 2019 in the zone name Astoria which was the 
-- drop off zone that had the largest tip?
select
	zpu."Zone" as pickup_zone,
	zdo."Zone" as dropoff_zone,
	max(gt.tip_amount) as max_tip
from green_taxi_data as gt
inner join taxi_zones as zpu
on gt."PULocationID" = zpu."LocationID"
left join taxi_zones as zdo
on gt."DOLocationID" = zdo."LocationID"
where date(gt.lpep_pickup_datetime) between '2019-09-01' and '2019-09-30'
and zpu."Zone" = 'Astoria'
group by pickup_zone, dropoff_zone
order by max_tip desc;