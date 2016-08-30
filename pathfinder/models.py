from django.db import models


# Create your models here.
class Node(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    able_to = models.TextField()
    resources = models.ManyToManyField('Resource', through='NodeResources')


class Edge(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.ForeignKey(Node, related_name='source_edge')
    dest = models.ForeignKey(Node, related_name='dest_edge')
    weight = models.IntegerField(default=1)


class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    description = models.TextField()
    link = models.TextField()
    how_to = models.TextField()


class NodeResources(models.Model):
    id = models.AutoField(primary_key=True)
    node = models.ForeignKey(Node)
    resource = models.ForeignKey(Resource)

