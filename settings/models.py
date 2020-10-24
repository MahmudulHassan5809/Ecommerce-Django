from django.db import models

# Create your models here.


class SiteInfo(models.Model):
    site_name = models.CharField(max_length=255)
    site_phone = models.CharField(max_length=20)
    site_email = models.EmailField()
    site_address = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='settings')

    class Meta:
        verbose_name = 'SiteInfo'
        verbose_name_plural = '1.SiteInfo'

    def __str__(self):
        return self.site_name


class ContactUs(models.Model):
    name = models.CharField(max_length=150)
    subject = models.CharField(max_length=150)
    problem = models.TextField()
    phone_number = models.CharField(max_length=50)
    solved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = '2.Contact Us'

    def __str__(self):
        return self.subject


class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banner')
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = '3.Banner'

    def __str__(self):
        return self.title


class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='about_us')
    description = models.TextField()

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = '4.About Us'

    def __str__(self):
        return self.title


class SiteAd(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    image = models.ImageField(upload_to='site_ad')
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Site Ad'
        verbose_name_plural = '5.Site Ad'

    def __str__(self):
        return self.title
