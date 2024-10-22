from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_invite_email(user_first_name, email, invite_url):
    send_mail(
        subject='You are invited!',
        message=f'''
        Hello {user_first_name},\n\nYou have been invited to join our platform.
        Please click the following link to accept the invitation:\n{invite_url}
        ''',
        from_email='noreply@yourdomain.com',
        recipient_list=[email],
        fail_silently=False,
    )
