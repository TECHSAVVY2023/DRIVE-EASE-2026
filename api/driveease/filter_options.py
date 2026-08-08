from django.db.models import Count

from .models import Cars


def get_filter_options():
    categories = (
        Cars.objects
        .values("car_type")
        .annotate(count=Count("car_id"))
        .order_by("car_type")
    )

    transmissions = (
        Cars.objects
        .values("transmission")
        .annotate(count=Count("car_id"))
        .order_by("transmission")
    )

    seats = (
        Cars.objects
        .values("seats")
        .annotate(count=Count("car_id"))
        .order_by("seats")
    )

    return {
        "categories": [
            {
                "label": item["car_type"],
                "count": item["count"],
            }
            for item in categories
        ],

        "transmissions": [
            {
                "label": item["transmission"],
                "count": item["count"],
            }
            for item in transmissions
        ],

        "seats": [
            {
                "label": item["seats"],
                "count": item["count"],
            }
            for item in seats
        ]
    }

    