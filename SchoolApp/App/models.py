from django.db import models




class Employee(models.Model):

    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=15)
    user_country = models.CharField(max_length=20)
    user_city = models.CharField(max_length=20)
    user_state = models.CharField(max_length=50)
    user_zip = models.CharField(max_length=10)
    user_gender = models.CharField(max_length=8)
    user_about = models.CharField(max_length=500)
    user_image = models.ImageField()
    user_creation_date = models.CharField(max_length=100)
    user_info_last_update = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "tb_employee"
