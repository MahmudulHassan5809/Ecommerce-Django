from django.db import models
from django.utils.text import slugify
from smart_selects.db_fields import GroupedForeignKey
# Create your models here.


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


def generate_unique_slug(klass, field):
    slug = field
    numb = 1
    while klass.objects.filter(slug=slug).exists():
        slug = '%s-%d' % ("-".join(slug.split()), numb)
        numb += 1

    return slug


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
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = '2.Product'

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

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to="product")

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = '4. Product Images'

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
        verbose_name_plural = "3.Lead Sections"

    def __str__(self):
        return 'Lead Section'
