from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from .validators import validate_icon_image_size, validate_image_file_extension


def room_icon_upload_path(instance, filename):
    return f"room/{instance.id}/room_icon/{filename}"


def room_banner_upload_path(instance, filename):
    return f"room/{instance.id}/room_banner/{filename}"


#  function to generate a path for uploading category icons. 
# It uses the `filename` parameter to construct the path string.
def category_icon_upload_path(instance, filename):
    return f"category/{instance.id}/category_icon/{filename}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(null=True, upload_to=category_icon_upload_path, blank=True)

    # responsible for handling the saving logic of a model instance.
    # If the instance being saved is an update to an existing record and 
    # the icon attribute has changed, the old icon file associated with 
    # the existing record is deleted before saving the updated instance.
    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    # This code ensures that when a Category object is deleted, 
    # any associated file (in the "icon" field) is also removed.
    @receiver(models.signals.pre_delete, sender="room.Category")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)


    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="room_owner")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='room_category')
    description = models.CharField(max_length=250, blank=True, null=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    # def save(self, *args, **kwargs):
    #     self.name = self.name.lower()
    #     super(Room, self).save(*args,**kwargs)

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner")
    topic = models.CharField(max_length=100)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="channel_room")
    banner = models.ImageField(upload_to=room_banner_upload_path, null=True, blank=True, validators=[validate_image_file_extension])
    icon = models.ImageField(upload_to=room_icon_upload_path, null=True, blank=True, validators=[validate_icon_image_size, validate_image_file_extension])

    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Channel, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)
        super(Channel, self).save(*args, **kwargs)

    # This code ensures that when a Category object is deleted, 
    # any associated file (in the "icon" field) is also removed.
    @receiver(models.signals.pre_delete, sender="room.Channel")
    def channel_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)



    def __str__(self):
        return self.name