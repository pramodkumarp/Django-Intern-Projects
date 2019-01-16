from django.db import models


class ImageHandling(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True)

    class Meta:
        db_table = 'db_image'
