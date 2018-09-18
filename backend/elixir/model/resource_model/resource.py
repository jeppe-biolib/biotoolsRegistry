from django.db import models
from elixir.model.resource_model.elixirInfo import * 
from elixir.model.resource_model.editPermission import *
from django.contrib.auth.models import User

class Resource(models.Model):
    
    YES_NO_CHOICES = (
        (0, 'NO'),
        (1, 'YES'),
    )

    WAS_ID_VALIDATED_CHOICES = (
        (0, 'NO'),
        (1, 'YES'),
    )

    HOMEPAGE_STATUS_CHOICES = (
        (0, 'UP'),
        (1, 'DOWN'),
        (2, 'DEAD')
    )


    # CharField doesn't $have a min_length
    #biotoolsID = models.CharField(min_length=1)
    #biotoolsCURIE = models.CharField(min_length=1)

    # so instead use blank=False, null=False
    # a lot of textId in views.py and urls.py, perhaps we should keep textId, in the JSON representation it's "id" anyway
    #   unless a simple replace of textId with biotoolsID can be done
    biotoolsID = models.CharField(blank=False, null=False, max_length=100)
    biotoolsCURIE = models.CharField(blank=False, null=False, max_length=109) #because of biotools: prefix

    name = models.TextField()
    # Version is it's own model now
    #version = models.TextField(blank=True, null=True)
    
    # Keep versionId for now, will probably remove later, there is no real data one can use from it anyway...
    # but don't serialize
    versionId = models.CharField(max_length=100, null=True, default='none')

    homepage = models.TextField()
    description = models.TextField()
    short_description = models.TextField(blank=True, null=True)

    canonicalID = models.TextField(blank=True, null=True)

    issue_score = models.FloatField(blank=True, null=True)

    version_hash = models.TextField(blank=True, null=True)
    visibility = models.IntegerField(choices=YES_NO_CHOICES, default=1)
    latest = models.IntegerField(choices=YES_NO_CHOICES, default=1)
    was_id_validated = models.IntegerField(choices=WAS_ID_VALIDATED_CHOICES, default=0)
    homepage_status = models.IntegerField(choices=HOMEPAGE_STATUS_CHOICES, default=0)

    # things that used to be in separate tables
    cost = models.TextField(blank=True, null=True)
    maturity = models.TextField(blank=True, null=True)
    license = models.TextField(blank=True, null=True)

    elixirInfo = models.ForeignKey(ElixirInfo, null=True, blank=True, on_delete=models.CASCADE)
    editPermission = models.ForeignKey(EditPermission, null=False, blank=True, on_delete=models.CASCADE)

    # metadata
    additionDate = models.DateTimeField(blank=True, null=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='resource', blank=False, null=False)

    # additional information that we don't have in the xsd model
    availability = models.TextField(blank=True, null=True)
    downtime = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.name) or u''


class OtherID(models.Model):
    value = models.CharField(blank=False, null=False, max_length=1000, unique=False)
    # TODO: make sure type is inferred from value, but still appears in the iterface
    type = models.TextField(blank=True, null=True)
    version = models.TextField(blank=True, null=True)
    resource = models.ForeignKey(Resource, null=True, blank=True, related_name='otherID', on_delete=models.CASCADE)
    additionDate = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return unicode(self.value) or u''


class ElixirPlatform(models.Model):
    elixirPlatform = models.TextField(blank=False, null=True)
    resource = models.ForeignKey(Resource, null=True, blank=True, related_name='elixirPlatform', on_delete=models.CASCADE)

    # metadata
    additionDate = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.name) or u''


class ElixirNode(models.Model):
    elixirNode = models.TextField(blank=False, null=True)
    resource = models.ForeignKey(Resource, null=True, blank=True, related_name='elixirNode', on_delete=models.CASCADE)

    # metadata
    additionDate = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.name) or u''



# table to keep user requests
class ResourceRequest(models.Model):
    requestId = models.CharField(max_length=50)
    resource = models.ForeignKey(Resource, null=True, blank=True, related_name='requests', on_delete=models.CASCADE)
    type = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, related_name='requests', blank=True, null=True, on_delete=models.CASCADE)
    completedBy = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
