import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from celery.utils.log import get_task_logger


from apps import app

logger = logging.getLogger(__name__)
logger_celery = get_task_logger(__name__)


@app.task
def send_templated_email(subject, to_email, template_name_txt, template_name_html, **kwargs):
    try:
        txt = get_template(template_name_txt).render(kwargs)
        html = get_template(template_name_html).render(kwargs)
        email = EmailMultiAlternatives(subject, txt, settings.DEFAULT_FROM_EMAIL, to=[to_email])
        email.attach_alternative(html, 'text/html')
        email.send()
        logger_celery.info(email)
    except Exception as e:
        logger_celery.error(e)
