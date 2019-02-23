from django.db import models

# Create your models here.


class HiddenActIS (models.Model):
    act_number=models.CharField(max_length=20)
    act_date=models.CharField(max_length=50)
    presented_work=models.CharField(max_length=200)
    materials=models.CharField(max_length=200)
    permitted_work=models.CharField(max_length=200)
    begin_date=models.CharField(max_length=50)
    end_date=models.CharField(max_length=50)

    class Meta:
        ordering=['act_number']
        verbose_name='Акт скрытых инженерка '

    def __str__(self):
        return '{}'.format(self.act_number)


class ObjectActs (models.Model):
    address = models.CharField(max_length=100)
    system_type=models.CharField(max_length=100)
    designer=models.CharField(max_length=200)
    supervisor_engineer_full=models.CharField(max_length=200)
    contractor_engineer_full=models.CharField(max_length=200)
    project_number=models.CharField(max_length=100)
    exec_documents=models.CharField(max_length=100)
    supervisor_engineer_short=models.CharField(max_length=100)
    contractor_engineer_short=models.CharField(max_length=100)
    acts=models.ManyToManyField(HiddenActIS, blank=True)


    class Meta:
        verbose_name='Набор актов объекта '

    def __str__(self):
        return '{}'.format(", ".join([self.system_type, self.address]))



