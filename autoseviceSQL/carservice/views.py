import datetime
import json

import pytz

from django.db.models import Avg, Sum, Subquery, F, OuterRef
from django.http import HttpResponse
from django.core.cache import cache
from .models import *


def index(request):
    if "cs1" in cache and "cs2" in cache and "cs3" in cache and "cs4" in cache :
        client_service1 = cache.get("cs1")
        client_service2 = cache.get("cs2")
        client_service3 = cache.get("cs3")
        client_service4 = cache.get("cs4")
        load = "Cache"
    else:
        client_service1 = Client.objects.filter(clientcity="Гродно") \
            .values("clientcity", "clientname") \
            .annotate(sum_price=Sum("serviceclient__service__price")) \
            .filter(sum_price__lt=(5000 - 1000))
        cache.set("cs1", client_service1)

        client_service2 = Client.objects \
            .filter(serviceclient__date_service__date=datetime.datetime(2023, 6, 3, tzinfo=pytz.UTC)) \
            .values("serviceclient__date_service", "clientcity") \
            .annotate(sum_price=Sum("serviceclient__service__price")).order_by("-sum_price")


        client_service3 = Client.objects \
            .values("clientname", "clientcity") \
            .annotate(sum_price=Sum("serviceclient__service__price"),
                      average_price_city=Subquery(Client.objects
                                                  .values("clientcity")
                                                  .annotate(average_price=Avg("serviceclient__service__price"))
                                                  .filter(clientcity=OuterRef("clientcity"))
                                                  .values("average_price")[:1]
                                                  )
                      ) \
            .filter(sum_price__gt=F("average_price_city") * 1.20)


        client_service4 = Client.objects \
            .values("serviceclient__id", "clientname", "clientcity") \
            .annotate(average_price_client_service=Avg("serviceclient__service__price"),
                      average_price_city=Subquery(Client.objects
                                                  .values("clientcity")
                                                  .annotate(average_price=Avg("serviceclient__service__price"))
                                                  .filter(clientcity=OuterRef("clientcity"))
                                                  .values("average_price")[:1]
                                                  )
                      ) \
            .filter(average_price_client_service__gt=F("average_price_city") * 1.10)
        load = "DataBase"
        cache.set_many({"cs1": client_service1, "cs2": client_service2, "cs3": client_service3, "cs4": client_service4})

    cs1 = "<h4>Найти все клиентов из указанного города с суммой чека меньше указанного на 1000</h4>"
    for ind, key in enumerate(client_service1):
        cs1 += f"""
            <p>{ind+1}</p>
            <p>Город - {key['clientcity']}</p>
            <p>Имя клиента - {key['clientname']}</p>
            <p>Сумма заказа - {key['sum_price']} руб</p>
            """

    cs2 = "<h4>Вывести по порядку убывания выручки всех городов за указанный период времени</h4>"
    for ind, key in enumerate(client_service2):
        cs2 += f"""
            <p>{ind+1}</p>
            <p>Город - {key['clientcity']}</p>
            <p>Дата - {key['serviceclient__date_service']}</p>
            <p>Сумма заказа - {key['sum_price']} руб</p>
            """

    cs3 = "<h4>Найти все заказы, сумма которых выше на 20% BYN среднего заказа по данному городу</h4>"
    for ind, key in enumerate(client_service3):
        cs3 += f"""
            <p>{ind+1}</p>
            <p>Город - {key['clientcity']}</p>
            <p>Имя клиента - {key['clientname']}</p>
            <p>Сумма заказа - {key['sum_price']} руб</p>
            <p>Средний заказ по городу - {key["average_price_city"]:.2f} руб</p>
            """
    cs4 = "<h4>Найти всех клиентов средний чек у которых на 10% выше чем средний чек по их городу</h4>"
    for ind, key in enumerate(client_service4):
        cs4 += f"""
            <p>{ind+1}</p>
            <p>Город - {key['clientcity']}</p>
            <p>Имя клиента - {key['clientname']}</p>
            <p>Средний заказ клиента - {key['average_price_client_service']:.2f} руб</p>
            <p>Средний заказ по городу - {key["average_price_city"]:.2f} руб</p>
            """

    return HttpResponse(f"""
        <h2>{load}</h2>
        <p>{cs1}</p>
        <p>{cs2}</p>
        <p>{cs3}</p>
        <p>{cs4}</p>
        """)
