from django.db import models
from django.urls import reverse, reverse_lazy
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = '1.Categories'

    def save(self, *args, **kwargs):
        self.slug = "-".join(self.name.split())
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def generate_unique_slug(klass, field):
    slug = field
    numb = 1
    while klass.objects.filter(slug=slug).exists():
        slug = '%s-%d' % ("-".join(slug.split()), numb)
        numb += 1

    return slug


class Post(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category_posts')
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=150)
    image = models.ImageField(upload_to='blog')
    description = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateField()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = '2.Posts'

    def save(self, *args, **kwargs):
        self.slug = "-".join(self.name.split())
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_detail_url(self):
        return reverse('blog:single_post', args=[str(self.slug), str(self.pk)])

    def save(self, *args, **kwargs):
        if self.slug:
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Post, self.title)
        else:
            self.slug = generate_unique_slug(Post, self.title)
        super(Post, self).save(*args, **kwargs)
