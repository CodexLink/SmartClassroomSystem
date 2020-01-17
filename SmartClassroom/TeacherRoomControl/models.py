from django.db import models

# Create your models here.


class StaffDataSet(models.Model):
    sds_FN = models.CharField(max_length=20,null=False,blank=False)
    sds_MN = models.CharField(max_length=20,null=True,blank=True)
    sds_LN = models.CharField(max_length=50,null=False,blank=False)
    #sds_UN = models.CharField()
    #sds_PW = models.CharField()
    sds_Created = models.DateTimeField(auto_now_add=True)