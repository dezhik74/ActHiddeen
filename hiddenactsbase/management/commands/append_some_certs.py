from django.core.management.base import BaseCommand

from ...models import ObjectActs, Certificate


class Command(BaseCommand):
    help = 'В акты ХВС ГВС 2023 года добавляет сертификаты'

    def handle(self, *args, **kwargs):

        cert_02_1 = Certificate.objects.filter(description__contains='ГФ-021').first()
        cert_02_2 = Certificate.objects.filter(description__contains='ПФ-115').first()
        cert_03_1 = Certificate.objects.filter(description__contains='3262').first()
        cert_03_2 = Certificate.objects.filter(description__contains='10704').first()
        cert_04_1 = Certificate.objects.filter(description__contains='Ротбанд').first()
        cert_05_1 = Certificate.objects.filter(description__contains='ПП').first()

        obj_list = ObjectActs.objects.filter(pk__gt=247)
        for obj in obj_list:
            print(f'[{obj.pk}] {obj.address} {obj.system_type}')
            for act in obj.acts.all():
                if act.act_number.endswith('02'):
                    act.certificates.add(cert_02_1, cert_02_2)
                if act.act_number.endswith('03'):
                    act.certificates.add(cert_03_1, cert_03_2)
                if act.act_number.endswith('04'):
                    act.certificates.add(cert_04_1)
                if act.act_number.endswith('05'):
                    act.certificates.add(cert_05_1)



