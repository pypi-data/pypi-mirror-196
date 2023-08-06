from rest_framework import serializers

from dcim.api.nested_serializers import NestedPlatformSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox_storage.api.nested_serializers import NestedFilesystemSerializer, NestedDriveSerializer, \
    NestedPartitionSerializer, NestedMountedVolumeSerializer, NestedDeviceSerializer
from netbox_storage.models import Drive, Filesystem, Partition, MountedVolume, StorageConfigurationLinuxVolume, \
    LinuxDevice, TemplateConfigurationLinuxVolume
from virtualization.api.nested_serializers import NestedClusterSerializer, NestedVirtualMachineSerializer


class FilesystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filesystem
        fields = (
            "id",
            "filesystem",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class DriveSerializer(NetBoxModelSerializer):
    cluster = NestedClusterSerializer(required=False, allow_null=True)
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_storage-api:drive-detail")

    class Meta:
        model = Drive
        fields = (
            "id",
            "url",
            "display",
            "size",
            "cluster",
            "identifier",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class PartitionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_storage-api:partition-detail')
    drive = NestedDriveSerializer(required=False, allow_null=True)
    device = NestedDeviceSerializer(required=False, allow_null=True)

    class Meta:
        model = Partition
        fields = (
            "id",
            "url",
            "drive",
            "device",
            "size",
            "type",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class MountedVolumeSerializer(serializers.ModelSerializer):
    fs = NestedFilesystemSerializer(required=False, allow_null=True)
    partition = NestedPartitionSerializer(required=False, allow_null=True)

    class Meta:
        model = MountedVolume
        fields = (
            "id",
            "partition",
            "fs",
            "size",
            "path",
            "label",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class LinuxDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinuxDevice
        fields = (
            "id",
            "device",
            "type",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class StorageConfigurationLinuxVolumeSerializer(serializers.ModelSerializer):
    linux_volume = NestedMountedVolumeSerializer(required=False, allow_null=True)
    virtual_machine = NestedVirtualMachineSerializer(required=False, allow_null=True)

    class Meta:
        model = StorageConfigurationLinuxVolume
        fields = (
            "id",
            "device",
            "linux_volume",
            "created",
            "last_updated",
            "custom_fields",
        )


class TemplateConfigurationLinuxVolumeSerializer(serializers.ModelSerializer):
    drive = NestedDriveSerializer(required=False, allow_null=True)
    platform = NestedPlatformSerializer(required=False, allow_null=True)

    class Meta:
        model = TemplateConfigurationLinuxVolume
        fields = (
            "id",
            "platform",
            "drive",
            "created",
            "last_updated",
            "custom_fields",
        )
