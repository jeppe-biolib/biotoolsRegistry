from django.db import models
from elixir.model.resource_model.resource import * 

class CollectionID(models.Model):
    name = models.TextField(blank=True, null=True)
    resource = models.ForeignKey(Resource, null=True, blank=True, related_name='collectionID', on_delete=models.CASCADE)

    # metadata
    additionDate = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.name) or u''
