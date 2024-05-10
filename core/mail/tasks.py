from django.core.mail import EmailMessage,BadHeaderError
from core.models import User
from celery import shared_task
from core.models import User , Hostel
import logging


logger = logging.getLogger(__name__)




@shared_task
def hostel_booked_task(**kwargs):
    print("Inside hostel_booked_task..................")
    print(kwargs)
    if kwargs['booking']:
        booking = kwargs['booking']
        username, email = User.objects.filter(pk=booking['user']).values_list('username', 'email').first()
        items = booking['bookingitems']
        msg = ""
        
        for item in items:
            hostel_id = item['room']['hostel_id']
            capacity = item['room']['capacity']
            quantity = item['quantity']
            hostel_name = Hostel.objects.filter(pk=hostel_id).values_list('name', flat=True).first()
            msg += f"Hostel Name: {hostel_name}, Capacity: {capacity}, Quantity Booked: {quantity}\n"
            
        message = f"Hello {username},\n\nYou have booked the following:\n{msg}\nThank you for your booking."
        
        
        try:
            mail = EmailMessage(
                'Booking Confirmation',
                message,
                'aaronpinto111@gmail.com',
                [email],
            )
            mail.send()
            print("Mail sent successfully")
        except BadHeaderError:
            logger.error(f"Error - failed to send mail to {email}")
            
            


@shared_task
def mail_clients_every_friday():
    print("Inside mail_clients_every_friday..................")
    users_info = User.objects.values_list('username', 'email')
    for username, email in users_info:
        message = f"Hello {username},\n\nThis is a reminder to book your hostel for the weekend.\nThank you."
        try:
            mail = EmailMessage(
                'HostelPlug - Hostel Booking Reminder',
                message,
                'aaronpinto111@gmail.com',
                [email],
            )
            mail.send()
            print("Mail sent successfully")
        except BadHeaderError:
            logger.error(f"Error - failed to send mail to {email}")