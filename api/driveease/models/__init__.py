from . import common


# Keep these callables at driveease.models.* for existing migration compatibility.
def unique_upload_path(instance, filename):
    return common.unique_upload_path(instance, filename)


def default_car_meta():
    return common.default_car_meta()


def default_user_id():
    return common.default_user_id()


def generate_user_reference():
    return common.generate_user_reference()


def generate_car_reference():
    return common.generate_car_reference()

def generate_content_reference():
    return common.generate_content_reference()


def generate_booking_reference():
    return common.generate_booking_reference()


def generate_review_reference():
    return common.generate_review_reference()


def generate_log_reference():
    return common.generate_log_reference()


from .accounts import Accounts
from .fleet import CarType, Cars, Feature
from .reviews import ReviewHelpful, Reviews
from .bookings import Booking, Payment, Refund
from .notifications import CarAvailabilityAlert, Notification
from .logs import AdminActivityLog
from .misc import ContactListModel, FileUploadModel
from .content import (
    HomePageContent,
    HomePageFAQ,
    HomePageFeaturedCar,
    HomePageTrustItem,
    AboutUs,
    AboutUsWwrStats,
    AboutUsTeam,
    AboutUsJourney,
    ContactPageContent,
    ContactOpeningHour,
)

__all__ = [
    "Accounts",
    "AdminActivityLog",
    "Booking",
    "Cars",
    "CarType",
    "CarAvailabilityAlert",
    "ContactListModel",
    "Feature",
    "FileUploadModel",
    "HomePageContent",
    "HomePageFAQ",
    "HomePageFeaturedCar",
    "HomePageTrustItem",
    "AboutUs",
    "AboutUsWwrStats",
    "AboutUsTeam",
    "AboutUsJourney",
    "ContactPageContent",
    "ContactOpeningHour",
    "Notification",
    "Payment",
    "Refund",
    "ReviewHelpful",
    "Reviews",
    "default_car_meta",
    "default_user_id",
    "generate_booking_reference",
    "generate_car_reference",
    "generate_content_reference",
    "generate_log_reference",
    "generate_review_reference",
    "generate_user_reference",
    "unique_upload_path",
]
