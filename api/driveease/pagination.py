# api/pagination.py
from rest_framework.pagination import PageNumberPagination

class ReviewPagination(PageNumberPagination):
    page_size = 3

class AdminReviewPagination(PageNumberPagination):
    page_size = 5

class FleetPagination(PageNumberPagination):
    page_size = 9

class TransactionPagination(PageNumberPagination):
    page_size = 5

class NotificationPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100

class AccountsPagination(PageNumberPagination):
    page_size = 5

class AdminActivityLogPagination(PageNumberPagination):
    page_size = 5
