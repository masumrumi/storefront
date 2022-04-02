from django.db import models
# poor implementation
#from store.models import Product
# better implementation
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)
    
class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # poor implementation
    # this is a poor way to implement. since tags app will be dependent on Product class from the store app and might also be used in many different apps, we should use a generic relation.
    #product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # better implementation(generic relation)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    # So, in order to define a generic relation, we need to define a content_type and object_id field and then we need to define a GenericForeignKey field.