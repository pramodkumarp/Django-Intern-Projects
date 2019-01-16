from django.db import models
import random
from django.db.models.signals import pre_save
from django.utils.text import slugify


class NameTable(models.Model):
    fname = models.CharField(max_length=30, null=False)
    lname = models.CharField(max_length=30, null=False)
    slug_name = models.SlugField(max_length=200, null=False)

    def __str__(self):
        return self.fname+" "+self.lname

    class Meta:
        db_table = "NameTable"


def create_slug(instance, new_slug=None):
    slug = slugify(instance.fname)
    if new_slug is not None:
        slug = new_slug
    qs = NameTable.objects.filter(slug_name=slug)
    exists = qs.exists()
    if exists:
        new_slug = f"{slug}-{qs.last().id}"
        return create_slug(instance, new_slug=new_slug)
    else:
        return slug

def pre_save_name_slug(sender, instance, *args, **kwargs):
    if not instance.slug_name:
        instance.slug_name = create_slug(instance)

pre_save.connect(pre_save_name_slug, sender=NameTable)


class GenderTable(models.Model):
    gender = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = "GenderTable"

class BirthdayTable(models.Model):
    birthday = models.CharField(max_length=2, null=False)
    birthmonth = models.CharField(max_length=2, null=False)
    birthyear = models.CharField(max_length=4, null=False)

    class Meta:
        db_table = "BirthdayTable"


class ProfilePhotoTable(models.Model):
    profile_photo = models.ImageField()

    def __str__(self):
        return self.profile_photo

    class Meta:
        db_table = "ProfilePhotoTable"


class AddressTable(models.Model):
    village = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    zip = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.country

    class Meta:
        db_table = "AddressTable"


class DeviceDetailsTable(models.Model):
    device_name = models.CharField(max_length=100, null=False)
    ip_address = models.GenericIPAddressField(null=False)
    current_os = models.CharField(max_length=200, null=False)
    os_quality = models.CharField(max_length=100, null=False)
    machine_type = models.CharField(max_length=100, null=False)
    device_details = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table ="DeviceDetailsTable"

class MessageTable(models.Model):
    message = models.TextField(max_length=3000, null=True)

    def __str__(self):
        return self.message

    class Meta:
        db_table = "MessageTable"


class UserTable(models.Model):
    email_address = models.EmailField(max_length=50, null=True)
    email_verification_code = models.CharField(max_length=10, null=False)
    email_validity = models.IntegerField(default=0)
    password = models.CharField(max_length=30, null=False)
    password_reset_code = models.IntegerField(null=True)
    registered_on = models.DateField(auto_now_add=True)
    user_activity = models.IntegerField(default=0)
    profile_completion = models.IntegerField(null=False)

    name_table = models.ForeignKey(NameTable, on_delete=models.CASCADE, null=False)
    gender_table = models.ForeignKey(GenderTable, on_delete=models.CASCADE, null=False)
    birthday_table = models.ForeignKey(BirthdayTable, on_delete=models.CASCADE, null=False)
    device_table = models.ForeignKey(DeviceDetailsTable, on_delete=models.CASCADE, null=False)
    pp_table = models.ForeignKey(ProfilePhotoTable, on_delete=models.CASCADE, null=True)
    address_table = models.ForeignKey(AddressTable, on_delete=models.CASCADE, null=True)
    msg_tabl = models.ForeignKey(MessageTable, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "UserTable"


class PostTable(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=1000, null=True)
    post_image = models.ImageField(null=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    slug_post = models.SlugField(max_length=200, null=True)
    post_table = models.ForeignKey(UserTable, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "PostTable"


class ReactionTable(models.Model):
    like = models.IntegerField(default=0)
    comment = models.TextField(null=True)
    post_tbl = models.ForeignKey(PostTable, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = "ReactionTable"
