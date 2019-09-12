import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

# Create your models here.


__all__ = [
    'Images', 'Cluster', 'Master', 'Label', 'Node'
]


# 镜像
class Images(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Name"))
    tag = models.CharField(max_length=64, default='latest', verbose_name=_("Tags"))
    project = models.CharField(max_length=64, verbose_name=_("Project"))
    app = models.CharField(max_length=64, verbose_name=_("Application"))
    url = models.URLField(max_length=64, null=True, blank=True, verbose_name=_("Pull URL"))

    class Meta:
        verbose_name = "Images"
        verbose_name_plural = verbose_name
        unique_together = ('name', 'project')
        db_table = "cms_images"

    def __str__(self):
        return self.name


# 集群
class Cluster(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=64, unique=True, verbose_name=_("Name"))
    type = models.IntegerField(choices=((0, _("kubernetes")), (1, _("swarm")), (2, _("mesos"))), verbose_name=_("Type"))
    idc = models.CharField(max_length=64, verbose_name=_("DataCenter"))
    api = models.URLField(max_length=64, verbose_name=_("Api"))
    token = models.CharField(max_length=1024, verbose_name=_("Token"))
    cidr = models.CharField(max_length=32, verbose_name=_("CIDR"))
    comment = models.TextField(max_length=128, null=True, blank=True, verbose_name=_("Cluster Desc"))
    add_time = models.DateTimeField(default=datetime.now, verbose_name=_("Add Time"))

    @property
    def get_type(self):
        return self.get_type_display

    class Meta:
        verbose_name = "集群"
        verbose_name_plural = verbose_name
        db_table = "cms_cluster"

    def __str__(self):
        return self.name


# 主节点
class Master(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    ip = models.GenericIPAddressField(max_length=32, verbose_name=_("IP"))
    unschedulable = models.BooleanField(default=False, verbose_name=_("unschedulable"))
    cluster = models.ForeignKey(Cluster, verbose_name=_("Cluster"))
    os_image = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("OS Image"))
    kernel_version = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Kernel Version"))
    kube_version = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Kubernetes Version"))
    creation_timestamp = models.DateTimeField(null=True, blank=True, verbose_name=_("Create Time"))

    @property
    def get_cluster(self):
        return self.cluster.name

    class Meta:
        verbose_name = "主节点"
        verbose_name_plural = verbose_name
        unique_together = ('name', 'cluster')
        db_table = "cms_master"

    def __str__(self):
        return self.name


# 节点
class Node(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    ip = models.GenericIPAddressField(max_length=32, verbose_name=_("IP"))
    cluster = models.ForeignKey(Cluster, verbose_name=_("Cluster"))
    pod_cidr = models.CharField(max_length=32, verbose_name=_("CIDR"))
    unschedulable = models.BooleanField(default=False, verbose_name=_("unschedulable"))
    daemon_endpoints = models.TextField(max_length=64, null=True, blank=True, verbose_name=_("Endpoints"))
    architecture = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Architecture"))
    container_runtime_version = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Docker Version"))
    kernel_version = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Kernel Version"))
    kube_version = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Kubelet Version"))
    os_image = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("OS Image"))
    creation_timestamp = models.DateTimeField(null=True, blank=True, verbose_name=_("Create Time"))

    @property
    def get_cluster(self):
        return self.cluster.name

    class Meta:
        verbose_name = "节点"
        verbose_name_plural = verbose_name
        unique_together = ('name', 'cluster')
        db_table = "cms_node"

    def __str__(self):
        return self.name


# 节点标签
class Label(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    node = models.ForeignKey(Node, related_name='labels', verbose_name=_("Node"))
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    value = models.CharField(max_length=64, verbose_name=_("Value"))

    @property
    def get_node(self):
        return self.node.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name
        db_table = "cms_label"

    def __str__(self):
        return "{0}:{1}:{2}".format(self.node.name, self.name, self.value)
