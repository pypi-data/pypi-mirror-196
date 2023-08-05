from django.db import migrations, models
import utilities.json


class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.CreateModel(
            name="Drive",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("cluster",
                 models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="cluster_drive",
                                   to="virtualization.cluster")),
                ("size", models.FloatField()),
                ("identifier", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("size", "id"),
            },
        ),
        migrations.CreateModel(
            name="LinuxDevice",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("drive",
                 models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="drive_device",
                                   to="netbox_storage.drive")),
                ("device", models.CharField(max_length=255)),
                ("size", models.FloatField()),
                ("type", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Partition",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("drive",
                 models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="drive_partition",
                                   to="netbox_storage.drive")),
                ("device", models.CharField(max_length=255)),
                ("size", models.FloatField()),
                ("type", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("size", "id"),
            },
        ),
        migrations.CreateModel(
            name="VolumeGroup",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("vg_name", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("lv_name", "id"),
            },
        ),
        migrations.CreateModel(
            name="PhysicalVolume",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("partition",
                 models.OneToOneField(on_delete=models.deletion.CASCADE, related_name="partition_physicalvolume",
                                      to="netbox_storage.partition")),
                ("vg",
                 models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="volumegroup_physicalvolume",
                                   to="netbox_storage.volumegroup", null=True)),
                ("pv_name", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("pv_name", "id"),
            },
        ),
        migrations.CreateModel(
            name="Filesystem",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("filesystem", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("filesystem", "id"),
            },
        ),
        migrations.CreateModel(
            name="LogicalVolume",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("vg", models.ForeignKey(on_delete=models.deletion.CASCADE,
                                         related_name="volumegroup_logicalvolume",
                                         to="netbox_storage.volumegroup")),
                ("lv_name", models.CharField(max_length=255)),
                ("path", models.CharField(max_length=255)),
                ("fs",
                 models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, related_name='fs_lvm',
                                   to='netbox_storage.filesystem')),
                ("size", models.FloatField()),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("lv_name", "id"),
            },
        ),
        migrations.CreateModel(
            name="MountedVolume",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("device",
                 models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="device_mounted_volume",
                                   to="netbox_storage.LinuxDevice")),
                ("path", models.CharField(max_length=255)),
                ("fs",
                 models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, related_name='fs_linux',
                                   to='netbox_storage.filesystem')),
                ("size", models.FloatField()),
                ("description", models.CharField(max_length=255)),
                ("label", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("path", "fs", "id"),
            },
        ),
        migrations.CreateModel(
            name="StorageConfigurationLinuxVolume",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("virtual_machine",
                 models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE,
                                   related_name="virtual_machine_storage_configuration",
                                   to="virtualization.virtualmachine")),
                ("linux_volume",
                 models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE,
                                   related_name='linux_volume_storage_configuration',
                                   to='netbox_storage.mountedvolume')),
            ],
        ),
        migrations.CreateModel(
            name="TemplateConfigurationLinuxVolume",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("platform",
                 models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE,
                                   related_name="platform_template_configuration",
                                   to="dcim.platform")),
                ("linux_volume",
                 models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE,
                                   related_name='linux_volume_template_configuration',
                                   to='netbox_storage.mountedvolume')),
            ],
        ),
    ]
