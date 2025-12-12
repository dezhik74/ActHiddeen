import hashlib
from datetime import timedelta
from django.utils import timezone

from water.digit_hashes import generate_5digit_hash, generate_4digit_hash


def working_days_before(date, days: int):
    """
    Возвращает дату, отстоящую на `days` рабочих дней НАЗАД от `date`.
    Учитывает только ПН-ПТ.
    """
    if not date:
        return None
    current = date
    while days > 0:
        current -= timedelta(days=1)
        if current.weekday() < 5:  # 0-4 = Пн-Пт
            days -= 1
    return current


def autofill_water_assay_data(conclusion_date, customer, address):
    """
    Возвращает словарь с автозаполняемыми полями.
    Не сохраняет в БД — только возвращает данные для initial.
    """
    if not all([conclusion_date, customer, address]):
        return {}

    # Базовые данные
    act_date = working_days_before(conclusion_date, 15)
    base_hash = generate_5digit_hash(customer, act_date, address)

    # Акт приёма проб
    act_number = f"{base_hash}-3"

    # Протоколы
    chemistry_date = working_days_before(conclusion_date, 4)
    bio_date = working_days_before(conclusion_date, 3)
    bio_begin_date = working_days_before(conclusion_date, 10)
    bio_end_date = working_days_before(conclusion_date, 8)

    # Био-коды
    hvs_bio_code = generate_4digit_hash(act_date, customer, address)
    gvs_bio_code_num = int(hvs_bio_code) + 1
    gvs_bio_code = f"{gvs_bio_code_num:04d}"

    return {
        # Акт приёма проб воды
        'act_number': act_number,
        'act_date': act_date,
        'probe_date': act_date,
        'hvs_probe_number': f"{base_hash}12-3-1",
        'gvs_probe_number': f"{base_hash}12-3-2",

        # Химия
        'chemistry_number': f"{base_hash}.12-3",
        'chemistry_date': chemistry_date,
        'chemistry_order_number': act_number,
        'chemistry_order_date': act_date,

        # Биология
        'bio_number': generate_5digit_hash(address, customer, act_date) + ".2026",
        'bio_date': bio_date,
        'hvs_bio_code': hvs_bio_code,
        'gvs_bio_code': gvs_bio_code,
        'hvs_bio_referral': f"{base_hash}-3",
        'gvs_bio_referral': f"{base_hash}-3",
        'bio_begin_date': bio_begin_date,
        'bio_end_date': bio_end_date,
    }