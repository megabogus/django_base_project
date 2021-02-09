from django.utils.translation import gettext_lazy as _


NOT_DEFINED, MALE, FEMALE = range(3)
GENDER_CHOICES = (
    (NOT_DEFINED, _('не указан')),
    (MALE, _('мужской')),
    (FEMALE, _('женский'))
)

DELTA_DAYS = 30
