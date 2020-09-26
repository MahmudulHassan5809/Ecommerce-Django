from django.db import models
from django.utils.text import slugify
from smart_selects.db_fields import GroupedForeignKey
from django.db.models import Q, Avg

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta
# Create your models here.


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    icon = models.CharField(max_length=150)
    slug = models.CharField(max_length=150, unique=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Category'
        verbose_name_plural = '1.Categories'

    def save(self, *args, **kwargs):
        self.slug = "-".join(self.name.split())
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=150, unique=True)
    slug = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = '2.SubCategories'

    def save(self, *args, **kwargs):
        self.slug = "-".join(self.name.split())
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = '3.Brand'

    def save(self, *args, **kwargs):
        self.slug = "-".join(self.name.split())
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def generate_unique_slug(klass, field):
    slug = field
    numb = 1
    while klass.objects.filter(slug=slug).exists():
        slug = '%s-%d' % ("-".join(slug.split()), numb)
        numb += 1

    return slug


class ProductQuerySet(models.QuerySet):
    def price_filter(self, price, last_price=None):
        print(price, last_price)
        if last_price:
            print(last_price)
            return self.filter(price__gte=last_price)
        return self.filter(price__range=(0, price))

    def brand_filter(self, brand_id):
        return self.filter(brand_id=brand_id)

    def size_filter(self, size):
        return self.filter(size__icontains=size)

    def newest_filter(self):
        return self.filter(created_at__gte=datetime.now() - timedelta(days=7))

    def subcat_filter(self, subcat_id):
        return self.filter(sub_category_id=subcat_id)

    def title_desc_filter(self, query):
        return self.filter(Q(title__icontains=query) | Q(description__icontains=query))

    def active_filter(self):
        return self.filter(active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self.db)

    def price_filter(self, price, last_price):
        return self.get_queryset().price_filter(price, last_price)

    def brand_filter(self, brand_id):
        return self.get_queryset().brand_filter(brand_id)

    def brand_filter(self, size):
        return self.get_queryset().size_filter(size)

    def newest_filter(self):
        return self.get_queryset().newest_filter()

    def subcat_filter(self, subcat_id):
        return self.get_queryset().subcat_filter(subcat_id)

    def title_desc_filter(self, subcat_id):
        return self.get_queryset().title_desc_filter(query)

    def active_filter(self):
        return self.get_queryset().active_filter()


class Product(models.Model):
    AVAILIBILITY_CHOICES = (
        ('0', 'In Stock'),
        ('1', 'Out Of Stock'),
        ('2', 'Comming Soon'),
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='cat_products')
    sub_category = GroupedForeignKey(
        SubCategory, "category", on_delete=models.CASCADE, related_name='subcat_products', null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='brand_products', null=True, blank=True)
    title = models.CharField(max_length=220)
    slug = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=255)
    availibility = models.CharField(
        max_length=20, choices=AVAILIBILITY_CHOICES)
    price = models.FloatField()
    color = models.CharField(max_length=150, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    discount = models.FloatField(default=0.0)
    description = models.TextField()
    warranty = models.CharField(max_length=150)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField()

    objects = ProductManager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = '3.Product'

    @property
    def discount_price(self):
        if self.discount > 0:
            discount = self.price * self.discount / 100
            return self.price - discount
        else:
            return False

    def save(self, *args, **kwargs):
        if self.slug:
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Product, self.title)
        else:
            self.slug = generate_unique_slug(Product, self.title)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product:edit_product', args=[str(self.id)])

    def get_detail_url(self):
        return reverse('ecom:product_detail', args=[str(self.slug), str(self.id)])

    @property
    def average_rating(self):
        value = list(self.product_reviews.aggregate(Avg('rating')).values())[0]
        if value:
            return round(value)
        else:
            return 0

    @property
    def total_review(self):
        return self.product_reviews.count()

    @property
    def five_star_percentage(self):
        try:
            value = 100 * \
                float(self.product_reviews.filter(rating=5).count()) / \
                float(self.total_review)
            return "{:.2f}".format(value)
        except Exception as e:
            return "{:.2f}".format(0)

    @property
    def four_star_percentage(self):
        try:
            value = 100 * \
                float(self.product_reviews.filter(rating=4).count()) / \
                float(self.total_review)
            return "{:.2f}".format(value)
        except:
            return "{:.2f}".format(0)

    @property
    def three_star_percentage(self):
        try:
            value = 100 * \
                float(self.product_reviews.filter(rating=3).count()) / \
                float(self.total_review)
            return "{:.2f}".format(value)
        except:
            return "{:.2f}".format(0)

    @property
    def two_star_percentage(self):
        try:
            value = 100 * \
                float(self.product_reviews.filter(rating=2).count()) / \
                float(self.total_review)
            return "{:.2f}".format(value)
        except:
            return "{:.2f}".format(0)

    @property
    def one_star_percentage(self):
        try:
            value = 100 * \
                float(self.product_reviews.filter(rating=1).count()) / \
                float(self.total_review)
            return "{:.2f}".format(value)
        except:
            return "{:.2f}".format(0)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to="product")

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = '5. Product Images'

    def __str__(self):
        return self.product.title


class LeadSection(models.Model):
    first_lead = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name='category_first_lead')
    second_lead = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name='category_second_lead')
    third_lead = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name='category_third_lead')

    class Meta:
        verbose_name_plural = "4.Lead Sections"

    def __str__(self):
        return 'Lead Section'


class WishList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "4.Wish List"

    def __str__(self):
        return f"{self.user.username} added {self.product.title} to wishlist"


class CompareProduct(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_comparelist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "5.Compare Product"

    def __str__(self):
        return f"{self.user.username} added {self.product.title} to compare"


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_reviews')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_reviews')
    review = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = "5.Product Review"

    def __str__(self):
        return f"{self.user.username} review to {self.product.title}"
