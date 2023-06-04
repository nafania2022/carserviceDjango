-- 1
select
    clientname,
    clientcity,
    sum(c.price) sum_price
from carservice_client
join carservice_serviceclient cs on carservice_client.id = cs.client_id
join carservice_serviceclient_service css on cs.id = css.serviceclient_id
join carservice_service c on c.id = css.service_id
group by clientname, clientcity
having sum(c.price) < 3000 - 1000;

-- 2
select
    clientcity,
    DATE (data),
    sum(c.price) sum_price
from carservice_client
join carservice_serviceclient cs on carservice_client.id = cs.client_id
join carservice_serviceclient_service css on cs.id = css.serviceclient_id
join carservice_service c on c.id = css.service_id
where DATE (data) = '2023-05-13'
group by clientcity, data
order by sum_price desc;
-- 3
select
    carservice_client.clientcity,
    clientname,
    average_price_sity,
    sum(c.price) sum_price_client
from carservice_client
join carservice_serviceclient cs on carservice_client.id = cs.client_id
join carservice_serviceclient_service css on cs.id = css.serviceclient_id
join carservice_service c on c.id = css.service_id
         INNER JOIN (select distinct
                        clientcity,
                        round(avg(c.price) over (partition by clientcity), 2)  average_price_sity
                    from carservice_client
                    join carservice_serviceclient cs on carservice_client.id = cs.client_id
                    join carservice_serviceclient_service css on cs.id = css.serviceclient_id
                    join carservice_service c on c.id = css.service_id
                    group by clientcity, c.price, clientname) sity_price on sity_price.clientcity = carservice_client.clientcity
group by carservice_client.clientcity, clientname, average_price_sity
having average_price_sity * 1.2 < sum(c.price);
-- 4
select
        carservice_client.clientcity,
        clientname,
        average_price_sity,
        average_price_client_service
from carservice_client
        INNER JOIN (select clientcity,
                            round(avg(c.price) over (partition by clientcity), 2) average_price_sity,
                            round(avg(c.price) over (partition by cs.id), 2)      average_price_client_service
                     from carservice_client
                              join carservice_serviceclient cs on carservice_client.id = cs.client_id
                              join carservice_serviceclient_service css on cs.id = css.serviceclient_id
                              join carservice_service c on c.id = css.service_id
                     group by clientcity, c.price, cs.id) sity_price
                    on sity_price.clientcity = carservice_client.clientcity
where average_price_sity * 1.1 < average_price_client_service
group by carservice_client.clientcity, clientname, average_price_sity, average_price_client_service
-- 5
select
    clientname,
    clientcity,
    c.price,
    row_number()  over (
        partition by cs.client_id
        ORDER BY price) row
from carservice_client
join carservice_serviceclient cs on carservice_client.id = cs.client_id
join carservice_serviceclient_service css on cs.id = css.serviceclient_id
join carservice_service c on c.id = css.service_id
order by clientname, price;

select
    clientname,
    clientcity,
    c.price,
    rank()  over (
        partition by cs.client_id
        ORDER BY price) row
from carservice_client
join carservice_serviceclient cs on carservice_client.id = cs.client_id
join carservice_serviceclient_service css on cs.id = css.serviceclient_id
join carservice_service c on c.id = css.service_id
order by clientname, price;

select
    clientname,
    clientcity,
    c.price,
    dense_rank()  over (
        partition by cs.client_id
        ORDER BY price) row
from carservice_client
join carservice_serviceclient cs on carservice_client.id = cs.client_id
join carservice_serviceclient_service css on cs.id = css.serviceclient_id
join carservice_service c on c.id = css.service_id
order by clientname, price

