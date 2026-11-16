import os
import uuid


def unique_upload_path(instance, filename):
    extension = os.path.splitext(filename)[1].lower()
    return f"app/uploads/{uuid.uuid4().hex}{extension}"


def default_car_meta():
    return {"primary_image": "", "images": []}


def default_user_id():
    return {"images": []}


def _public_reference(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:10].upper()}"


def generate_user_reference():
    return _public_reference("USR")


def generate_car_reference():
    return _public_reference("CAR")

def generate_content_reference():
    return _public_reference("CNT")


def generate_booking_reference():
    return _public_reference("BKG")


def generate_review_reference():
    return _public_reference("REV")


def generate_log_reference():
    return _public_reference("LOG")
