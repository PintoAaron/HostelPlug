from django.dispatch import receiver
from core.signals import hostel_booked_signal
from core.tasks import hostel_booked_task
import logging

logger = logging.getLogger(__name__)


@receiver(hostel_booked_signal)
def send_hostel_booked_mail(sender,**kwargs):
    logger.info("Received hostel_booked_signal")
    booking_id = kwargs['booking_id']
    print("finally................................IM HERE")
    hostel_booked_task.delay(booking_id)