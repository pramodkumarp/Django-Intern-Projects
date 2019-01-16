from django.db import models



class User(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100)
    user_pass = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name
    
    class Meta:
        db_table = 'user_table'
