from ..models import Refund


ACTIVE_REFUND_STATUSES = {"pending_review", "processing", "succeeded"}


def create_pending_refund(*, payment, requested_by=None, customer_reason=""):
    """Create one full-refund review request without duplicating active attempts."""
    if payment.status != "paid" or not payment.paymongo_payment_id:
        return None, False

    existing = payment.refunds.filter(
        status__in=ACTIVE_REFUND_STATUSES,
    ).order_by("-requested_at").first()
    if existing:
        return existing, False

    return Refund.objects.create(
        payment=payment,
        amount=payment.amount,
        reason="customer_cancellation",
        customer_reason=customer_reason,
        requested_by=requested_by,
    ), True
