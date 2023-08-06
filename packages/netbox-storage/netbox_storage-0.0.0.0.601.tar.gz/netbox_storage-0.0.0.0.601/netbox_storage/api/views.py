from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet
from netbox_storage.api.serializers import (
    DriveSerializer,
    FilesystemSerializer, PartitionSerializer, MountedVolumeSerializer, LinuxDeviceSerializer
)
from netbox_storage.filters import DriveFilter, FilesystemFilter, \
    PartitionFilter, MountedVolumeFilter, LinuxDeviceFilter
from netbox_storage.models import Drive, Filesystem, Partition, MountedVolume, LinuxDevice


class NetboxStorageRootView(APIRootView):
    """
    NetboxDNS API root view
    """

    def get_view_name(self):
        return "NetboxStorage"


class DriveViewSet(NetBoxModelViewSet):
    queryset = Drive.objects.all()
    serializer_class = DriveSerializer
    filterset_class = DriveFilter

    @action(detail=True, methods=["get"])
    def drive(self, request, pk=None):
        drives = Drive.objects.filter(drive__id=pk)
        serializer = DriveSerializer(drives, many=True, context={"request": request})
        return Response(serializer.data)


class FilesystemViewSet(NetBoxModelViewSet):
    queryset = Filesystem.objects.all()
    serializer_class = FilesystemSerializer
    filterset_class = FilesystemFilter

    @action(detail=True, methods=["get"])
    def filesystem(self, request, pk=None):
        filesystem = Filesystem.objects.filter(filesystem__id=pk)
        serializer = FilesystemSerializer(filesystem, many=True, context={"request": request})
        return Response(serializer.data)


class PartitionViewSet(NetBoxModelViewSet):
    queryset = Partition.objects.all()
    serializer_class = PartitionSerializer
    filterset_class = PartitionFilter

    @action(detail=True, methods=["get"])
    def partition(self, request, pk=None):
        partition = Partition.objects.filter(partition__id=pk)
        serializer = PartitionSerializer(partition, many=True, context={"request": request})
        return Response(serializer.data)


class MountedVolumeViewSet(NetBoxModelViewSet):
    queryset = MountedVolume.objects.all()
    serializer_class = MountedVolumeSerializer
    filterset_class = MountedVolumeFilter

    @action(detail=True, methods=["get"])
    def mountedvolume(self, request, pk=None):
        mountedvolume = MountedVolume.objects.filter(mountedvolume__id=pk)
        serializer = MountedVolumeSerializer(mountedvolume, many=True, context={"request": request})
        return Response(serializer.data)


class LinuxDeviceViewSet(NetBoxModelViewSet):
    queryset = LinuxDevice.objects.all()
    serializer_class = LinuxDeviceSerializer
    filterset_class = LinuxDeviceFilter

    @action(detail=True, methods=["get"])
    def linuxdevice(self, request, pk=None):
        linuxdevice = LinuxDevice.objects.filter(linuxdevice__id=pk)
        serializer = LinuxDeviceSerializer(linuxdevice, many=True, context={"request": request})
        return Response(serializer.data)
