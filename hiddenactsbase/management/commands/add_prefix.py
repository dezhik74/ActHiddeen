from django.core.management.base import BaseCommand

from ...models import ObjectActs, Certificate


class Command(BaseCommand):
    help = 'Во все наборы актов добавляет префиксы и удаляет префиксы из номеров актов'

    def handle(self, *args, **kwargs):

        obj_list = ObjectActs.objects.all()
        for obj in obj_list:
            print(obj)
            acts = obj.acts.all()
            if len(acts) > 0:
                if len(acts[0].act_number.split('-')) > 0:
                    prefix = acts[0].act_number.split('-')[0]
                    obj.acts_prefix = prefix
                    if len(obj.w_p_act_number) > 0:
                        obj.w_p_act_number = obj.w_p_act_number.replace(prefix+'-', '')
                    if len(obj.w_d_act_number) > 0:
                        obj.w_d_act_number = obj.w_d_act_number.replace(prefix+'-', '')
                    if len(obj.h_act_number) > 0:
                        obj.h_act_number = obj.h_act_number.replace(prefix+'-', '')
                    if len(obj.s_t_act_number) > 0:
                        obj.s_t_act_number = obj.s_t_act_number.replace(prefix+'-', '')
                    if len(obj.a_act_number) > 0:
                        obj.a_act_number = obj.a_act_number.replace(prefix+'-', '')
                    obj.save()
                    for act in acts:
                        act.act_number = act.act_number.replace(prefix+'-', '')
                        act.save()
                        print(f"act_number: {act.act_number}, prefix: {prefix}")




