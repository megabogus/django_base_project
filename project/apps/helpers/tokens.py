# -*- coding: utf-8 -*-
import re
from random import choice, randint

__version__ = '1.0.1'

DEFAULT_LOCALE = 'en'
LOCALES = ('en', 'ru')
MIN_LENGTH = 10
MAX_LENGTH = 10

en_vowels = ('a', 'e', 'i', 'o', 'u', 'y',)
en_consonants = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z',
                 'sh', 'zh', 'ch', 'kh', 'th', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
# ru_vowels = ('а', 'е', 'и', 'о', 'у', 'э', 'ю', 'я')
# ru_consonants = ('б', 'в', 'г', 'д', 'ж', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ')
ru_vowels = ('а', 'аг', 'ас', 'ад', 'да', 'ол', 'еа', 'ед')
ru_consonants = ('бу', 'ву', 'га', 'та', 'ри', 'де' 'дес', 'ли', 'нз', 'лл', 'рс', 'пи')


def generate(locale=None):
    """
    Generates nickname

    from nickname import generate

    print generate('ru')
    print generate('en')
    """
    if locale is None or locale not in LOCALES:
        locale = DEFAULT_LOCALE

    vowels = globals()['{}_vowels'.format(locale)]
    consonants = globals()['{}_consonants'.format(locale)]

    is_vowels_first = bool(randint(0, 1))
    result = ''
    for i in range(0, randint(MIN_LENGTH, MAX_LENGTH)):
        is_even = i % 2 is 0
        if (is_vowels_first and is_even) or (not is_vowels_first and not is_even):
            result += choice(vowels)
        else:
            result += choice(consonants)
    if not re.search('\d+', result.title()):
        return generate(locale)

    return result.title()
