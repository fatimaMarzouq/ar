from django.db import models
import uuid
# from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
User = get_user_model()


class Asset(models.Model):
    id = models.UUIDField(
        primary_key=True,
        # db_index=True,  # new
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(
        User,
        default=1,
        on_delete=models.CASCADE,
    )
    code = models.CharField(max_length=400)
    featured_image = models.ImageField(upload_to='covers/', blank=True)
    Google_maps_link = models.CharField(max_length=200)
    ASSETS_TYPE = [("IOS", 'IOS'), ("ANDROID", 'Android'), ]
    ASSETS_TYPE = models.CharField(
        max_length=8,
        choices=ASSETS_TYPE,
        default="IOS",
    )
    Expiry_date = models.DateField(null=True)
    Expiry_time = models.TimeField(null=True)
    # Locations = models.ForeignKey(
    #     Location,
    #     on_delete=models.CASCADE,
    #     related_name='Asset_Locations',
    #     null=True
    # )

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('Assets_list')


class Location(models.Model):
    id = models.UUIDField(
        primary_key=True,
        # db_index=True,  # new
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(
        User,
        default=1,
        on_delete=models.CASCADE,
    )
    Name = models.CharField(max_length=200)
    Longitude = models.DecimalField(null=True, max_digits=10, decimal_places=5)
    Latitude = models.DecimalField(null=True, max_digits=10, decimal_places=5)
    Google_maps_link = models.CharField(max_length=200)
    Plus_code = models.CharField(max_length=200)
    Radius = models.DecimalField(null=True, max_digits=10, decimal_places=5)
    # Events = models.ForeignKey(
    #     Event,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     related_name='Events',
    # )
    Assets = models.ManyToManyField(Asset)

    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('location_list')


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        # db_index=True,  # new
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=200)
    Photo = models.ImageField(upload_to='covers/', blank=True,null=True)
    starting_date = models.DateField(null=True)
    ending_date = models.DateField(null=True)
    user = models.ForeignKey(
        User,
        default=1,
        on_delete=models.CASCADE,
    )
    Locations = models.ManyToManyField(Location)
    Assets = models.ManyToManyField(Asset)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True,null=True)

    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('events')

    def save(self, *args,**kwargs):
        qrcode_img = qrcode.make(self.id)
        canvas = Image.new('RGB',(290,290),'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.id}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'png')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)








