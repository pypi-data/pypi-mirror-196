from django.core.validators import MinValueValidator
from django.forms import (
    CharField,
    FloatField, BooleanField
)
from django.urls import reverse_lazy

from dcim.models import Platform
from netbox.forms import (
    NetBoxModelForm,
)
from netbox_storage.models import Drive, Filesystem, Partition, PhysicalVolume, VolumeGroup, LogicalVolume, \
    StorageConfigurationDrive, MountedVolume, LinuxDevice, TemplateConfigurationDrive
from utilities.forms import (
    DynamicModelChoiceField, APISelect,
)
from virtualization.models import Cluster, ClusterType, VirtualMachine


class LVMTemplateForm(NetBoxModelForm):
    """Form for creating a new Drive object."""
    # ct = ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
    lv_name = CharField(
        label="LV Name",
        help_text="Logical Volume Name e.g. lv_docker",
    )
    vg_name = CharField(
        label="VG Name",
        help_text="Volume Group Name e.g. vg_docker",
    )
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
    )
    mount_point = CharField(
        label="mount_point",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
    )
    fs_type = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )
    fs_options = CharField(
        required=False,
        label="FS Options",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
    )
    cluster_type = DynamicModelChoiceField(
        queryset=ClusterType.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        query_params={
            'type_id': '$cluster_type'  # ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        },
        help_text="The Storage Cluster of the drive",
    )
    platform = DynamicModelChoiceField(
        queryset=Platform.objects.all(),
        help_text="Mapping between drive and platform  e.g. Rocky Linux 9",
    )
    drive = DynamicModelChoiceField(
        queryset=Drive.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Hard Drive 1 on SSD Cluster",
    )
    checkbox_partition = BooleanField(
        label="Create extra partition",
        help_text="Create an extra partition e.g. /dev/sdb1",
    )

    fieldsets = (
        (
            "Drive Cluster Config",
            (
                "drive",
                "platform",
                "checkbox_partition"
            ),
        ),
        (
            "LVM Configuration",
            (
                "lv_name",
                "vg_name",
                "size",
                "mount_point",
                "fs_type",
                "fs_options",
                "description",
            ),
        ),
    )

    class Meta:
        model = LogicalVolume
        fields = [
            "lv_name"
        ]

    def save(self, *args, **kwargs):
        print(f"drive: {self.cleaned_data['drive']}")
        print(f"ID OF drive: {self.cleaned_data['drive'].id}")
        print(f"ID OF drive: {self.cleaned_data['drive'].cluster}")
        new_partition_count = Partition.objects.filter(drive_id=self.cleaned_data['drive'].id).count() + 1
        device_name_prefix = Drive.objects.get(pk=self.cleaned_data['drive'].id).device_name()
        print(f"Partition Count: {new_partition_count}")
        print(f"Device Name: {device_name_prefix}")
        device_name = device_name_prefix + str(new_partition_count)

        mounted_volume = MountedVolume.objects.create(mount_point=self.cleaned_data['mount_point'],
                                                      fs_type=self.cleaned_data['fs_type'],
                                                      options=self.cleaned_data['fs_options'])

        linux_device = LinuxDevice.objects.create(device=device_name, type='efi')
        partition = Partition.objects.create(drive=self.cleaned_data['drive'], device=linux_device, size=self.cleaned_data['drive'], type='Linux LVM')

        volume_group = VolumeGroup.objects.create(vg_name=self.cleaned_data['vg_name'])
        PhysicalVolume.objects.create(device=linux_device, vg=volume_group)

        print(f"Checkbox Partition: {self.cleaned_data['checkbox_partition']}")
        print(f"{self.cleaned_data['lv_name']}")
        print(f"{self.cleaned_data['vg_name']}")
        print(f"{self.cleaned_data['size']}")
        print(f"{self.cleaned_data['mount_point']}")
        print(f"{self.cleaned_data['fs_type']}")

        linux_device_mapper = LinuxDevice.objects.create(device='/dev/mapper/vg_system-lv_home', type='ext4')

        self.instance.vg = self.cleaned_data['drive']
        self.instance.size = linux_device
        self.instance.device = linux_device_mapper
        logical_volume = super().save(*args, **kwargs)

        return logical_volume


class DriveTemplateForm(NetBoxModelForm):
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
    )
    cluster_type = DynamicModelChoiceField(
        queryset=ClusterType.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        query_params={
            'type_id': '$cluster_type'  # ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        },
        help_text="The Storage Cluster of the drive",
    )
    platform = DynamicModelChoiceField(
        queryset=Platform.objects.all(),
        help_text="Mapping between Volume and platform e.g. Rocky Linux 8",
    )

    fieldsets = (
        (
            "Drive Config",
            (
                "cluster_type",
                "cluster",
                "size",
                "platform",
            ),
        ),
    )

    class Meta:
        model = TemplateConfigurationDrive
        fields = [
            "platform",
        ]

    def save(self, *args, **kwargs):
        drive = Drive.objects.create(cluster=self.cleaned_data['cluster'], size=self.cleaned_data['size'])
        self.instance.drive = drive
        template_configuration = super().save(*args, **kwargs)

        print(f"{self.cleaned_data['size']}")

        print("Instances")
        print(drive)
        print(template_configuration)

        return template_configuration


class PartitionTemplateForm(NetBoxModelForm):
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
    )
    drive = DynamicModelChoiceField(
        queryset=Drive.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    platform = DynamicModelChoiceField(
        queryset=Platform.objects.all(),
        help_text="Mapping between Volume and platform e.g. Rocky Linux 8",
    )
    mount_point = CharField(
        label="mount_point",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
    )
    fs_type = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )
    fs_options = CharField(
        required=False,
        label="FS Options",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
    )
    label = CharField(
        required=False,
        label="Partition Label",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
    )

    fieldsets = (
        (
            "Select drive",
            (
                "drive",
                "platform",
            ),
        ),
        (
            "Select drive",
            (
                "mount_point",
                "size",
                "fs_type",
                "fs_options",
                "label",
            ),
        ),
    )

# /boot/efi --fstype="efi" --ondisk=sda --size=126 --fsoptions="umask=0077,shortname=winnt" --label=boot_efi
    class Meta:
        model = Partition
        fields = [
            "size"
        ]

    def save(self, *args, **kwargs):
        print(f"drive: {self.cleaned_data['drive']}")
        print(f"ID OF drive: {self.cleaned_data['drive'].id}")
        print(f"ID OF drive: {self.cleaned_data['drive'].cluster}")
        new_partition_count = Partition.objects.filter(drive_id=self.cleaned_data['drive'].id).count() + 1
        device_name_prefix = Drive.objects.get(pk=self.cleaned_data['drive'].id).device_name()
        print(f"Partition Count: {new_partition_count}")
        print(f"Device Name: {device_name_prefix}")
        device_name = device_name_prefix + str(new_partition_count)

        mounted_volume = MountedVolume.objects.create(mount_point=self.cleaned_data['mount_point'],
                                                      fs_type=self.cleaned_data['fs_type'],
                                                      options=self.cleaned_data['fs_options'])

        linux_device = LinuxDevice.objects.create(device=device_name, type='efi', mounted_volume=mounted_volume)

        self.instance.drive = self.cleaned_data['drive']
        self.instance.device = linux_device
        self.instance.type = 'vfat'
        partition = super().save(*args, **kwargs)

        # print(f"{self.cleaned_data['size']}")
        return partition


class VolumeSimpleForm(NetBoxModelForm):
    """Form for creating a new Drive object."""
    # ct = ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
        required=False
    )
    lv_name = CharField(
        label="LV Name",
        help_text="The logical volume name e.g. lv_data",
        required=False
    )
    vg_name = CharField(
        label="VG Name",
        help_text="The volume group name e.g. vg_data",
        required=False
    )
    mount_point = CharField(
        label="mount_point",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
        required=False
    )
    hard_drive_label = CharField(
        label="Hard Drive Label",
        help_text="The label of the hard drive e.g. D",
        required=False
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
        required=False
    )
    cluster_type = DynamicModelChoiceField(
        queryset=ClusterType.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        query_params={
            'type_id': '$cluster_type'  # ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        },
        help_text="The Storage Cluster of the drive",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Hard Drive 1 on SSD Cluster",
    )

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "description",
        )

    def save(self, *args, **kwargs):
        drive = super().save(*args, **kwargs)

        # Assign/clear this IPAddress as the primary for the associated Device/VirtualMachine.
        # print(f"{self.instance}")
        print(f"{self.cleaned_data['lv_data']}")
        print(f"{self.cleaned_data['vg_data']}")
        print(f"{self.cleaned_data['size']}")
        print(f"{self.cleaned_data['mount_point']}")
        print(f"{self.cleaned_data['fs']}")

        return drive
