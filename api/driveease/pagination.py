# api/pagination.py
from rest_framework.pagination import PageNumberPagination

class ReviewPagination(PageNumberPagination):
    page_size = 3

class FleetPagination(PageNumberPagination):
    page_size = 9

class TransactionPagination(PageNumberPagination):
    page_size = 5