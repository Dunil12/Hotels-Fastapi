import logging
import io
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from openpyxl.workbook import Workbook

from src.tasks.celery_app import celery_instance
from src.config import settings
from src.schemas.emails import BookingEmailData # !!!
from src.tasks.emails.utils import render_html, generate_excel


#BookingEmailData # !!!



@celery_instance.task(max_retries=1, time_limit=60)
def send_booking_confirmation_email(email_data: dict):
    logging.info(f"Отправка письма для бронирования ID={email_data['booking_id']}")

    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_SENDER
    msg['To'] = email_data['user_email']
    msg['Subject'] = f"Подтверждение бронирования #{email_data['booking_id']}"

    html_body = render_html("/app/src/tasks/emails/templates/booking_confirmation2.html", email_data)
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))

    excel_file = generate_excel(email_data)

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(excel_file.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename=Booking_{email_data["booking_id"]}.xlsx'
    )
    msg.attach(part)

    try:
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            # server.starttls()
            server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
            server.send_message(msg)
        logging.info(f"Письмо успешно отправлено на {email_data['user_email']}")
    except Exception as e:
        logging.error(f"Ошибка при отправке письма на {email_data['user_email']}: {str(e)}")
        raise send_booking_confirmation_email(exc=e)

