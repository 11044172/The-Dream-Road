from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE_CHOICES = [
        ('normal', 'ノーマル'),
        ('large', '大'),
        ('extra_large', '特大'),
    ]
    title = models.CharField(max_length=200,)
    price = models.CharField(max_length=20)
    image = models.URLField()
    description = models.TextField()
    category = models.CharField(max_length=50, blank=True, null=True)
    url = models.URLField(default="1234")
    shipping_size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='normal')

    def __str__(self):
        return self.title
    
class Attribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.product.title} - {self.attribute.name}: {self.value.value}"

class ColorImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='color_images')
    color = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"{self.product.title} - {self.color.value} Image"