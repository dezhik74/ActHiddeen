from django.db import models

# Create your models here.


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

    class Meta:
        verbose_name='Набор актов объекта '

    def __str__(self):
        return '{}'.format(", ".join([self.system_type, self.address]))


class Act (models.Model):
    object_acts = models.ForeignKey(ObjectActs, on_delete=models.CASCADE)
    act_number=models.CharField(max_length=20)
    act_date=models.CharField(max_length=50)

    class Meta:
        abstract = True
        ordering=['act_number']

    def __str__(self):
        return '{}'.format(self.act_number)


class HiddenActIS (Act):
    presented_work=models.CharField(max_length=200)
    materials=models.CharField(max_length=200)
    permitted_work=models.CharField(max_length=200)
    begin_date=models.CharField(max_length=50)
    end_date=models.CharField(max_length=50)

    class Meta:
        verbose_name='Акт скрытых инженерка '


