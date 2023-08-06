# -*- coding: utf-8 -*-
import os
from typing import Union
from faker import Faker
from faker.providers.address import Provider as TypeAddressFaker
from faker.providers.automotive import Provider as TypeAutomotiveFaker
from faker.providers.bank import Provider as TypeBankFaker
from faker.providers.barcode import Provider as TypeBarcodeFaker
from faker.providers.color import Provider as TypeColorFaker
from faker.providers.company import Provider as TypeCompanyFaker
from faker.providers.credit_card import Provider as TypeCreditCardFaker
from faker.providers.currency import Provider as TypeCurrencyFaker
from faker.providers.date_time import Provider as TypeDateTimeFaker
from faker.providers.emoji import Provider as TypeEmojiFaker
from faker.providers.file import Provider as TypeFileFaker
from faker.providers.geo import Provider as TypeGeoFaker
from faker.providers.internet import Provider as TypeInternetFaker
from faker.providers.isbn import Provider as TypeIsbnFaker
from faker.providers.job import Provider as TypeJobFaker
from faker.providers.lorem import Provider as TypeLoremFaker
from faker.providers.misc import Provider as TypeMiscFaker
from faker.providers.person import Provider as TypePersonFaker
from faker.providers.phone_number import Provider as TypePhoneNumberFaker
from faker.providers.profile import Provider as TypeProfileFaker
from faker.providers.python import Provider as TypePythonFaker
from faker.providers.sbn import Provider as TypeSbnFaker
from faker.providers.ssn import Provider as TypeSsnFaker
from faker.providers.user_agent import Provider as TypeUserAgentFaker


TypeAllFakers = Union[
    Faker,
    TypeAddressFaker, TypeAutomotiveFaker, TypeBankFaker, TypeBarcodeFaker,
    TypeColorFaker, TypeCompanyFaker, TypeCreditCardFaker, TypeCurrencyFaker,
    TypeDateTimeFaker, TypeEmojiFaker, TypeFileFaker, TypeGeoFaker, TypeInternetFaker,
    TypeIsbnFaker, TypeJobFaker, TypeLoremFaker, TypeMiscFaker, TypePersonFaker,
    TypePhoneNumberFaker, TypeProfileFaker, TypePythonFaker, TypeSbnFaker, TypeSsnFaker,
    TypeUserAgentFaker
]


class FakerProxy:
    _FAKER_LOCALE_ENV_NAME = 'FAKER_LOCALE'
    _DEFAULT_LOCALE = None
    _FAKER_REGISTRY = None

    @classmethod
    def get_faker(cls, locale: str = None) -> TypeAllFakers:
        if cls._FAKER_REGISTRY is None:
            cls._FAKER_REGISTRY = dict()
            cls._DEFAULT_LOCALE = os.getenv(cls._FAKER_LOCALE_ENV_NAME)

        if locale is None:
            locale = cls._DEFAULT_LOCALE

        f = cls._FAKER_REGISTRY.get(locale)
        if f is None:
            f = Faker(locale=locale)
            cls._FAKER_REGISTRY[locale] = f

        return f
