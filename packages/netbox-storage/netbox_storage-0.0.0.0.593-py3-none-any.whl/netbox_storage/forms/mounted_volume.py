from django.core.validators import MinValueValidator
from django.forms import (
    CharField, FloatField,
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from utilities.forms import (
    DynamicModelChoiceField,
    APISelect,
)

from django.urls import reverse_lazy

from netbox_storage.models import Filesystem, MountedVolume, Drive, Partition, LinuxDevice
from virtualization.models import VirtualMachine


class MountedVolumeForm(NetBoxModelForm):
    device = DynamicModelChoiceField(
        queryset=LinuxDevice.objects.all(),
        help_text="The Storage Cluster of the drive",
    )
    mount_point = CharField(
        label="Mountpoint",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )
    fs_type = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )
    options = CharField(
        label="Options",
        help_text="The size of the logical volume e.g. 25",
    )

    class Meta:
        model = MountedVolume

        fields = (
            "device",
            "mount_point",
            "fs_type",
            "options",
            "description",
        )


class MountedVolumeFilterForm(NetBoxModelFilterSetForm):

    model = MountedVolume

    drive = DynamicModelChoiceField(
        queryset=Drive.objects.all(),
        help_text="The Storage Cluster of the drive",
    )
    partition = DynamicModelChoiceField(
        queryset=Partition.objects.all(),
        label="Partition",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:partition-list")}
        ),
        query_params={
            'drive_id': '$drive',
        },
        help_text="The Partition for the LinuxVolume e.g. /dev/sda1",
    )
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.0)],
    )
    path = CharField(
        label="Path",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )


class MountedVolumeImportForm(NetBoxModelImportForm):
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = MountedVolume

        fields = (
            "device",
            "mount_point",
            "fs_type",
            "options",
            "description",
        )


class MountedVolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = MountedVolume

    path = CharField(
        required=False,
        label="Path",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        required=False,
        label="Filesystem Name",
    )
    description = CharField(max_length=255, required=False)

    fieldsets = (
        (
            None,
            ("device", "mount_point", "fs_type", "options", "description",),
        ),
    )
    nullable_fields = ["description"]
