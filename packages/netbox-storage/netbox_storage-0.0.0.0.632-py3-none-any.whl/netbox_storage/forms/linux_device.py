from django.forms import (
    CharField
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)

from netbox_storage.models import LinuxDevice


class LinuxDeviceForm(NetBoxModelForm):
    device = CharField(
        label="Device Name",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )

    class Meta:
        model = LinuxDevice

        fields = (
            "device",
            "type",
            "description",
        )


class LinuxDeviceFilterForm(NetBoxModelFilterSetForm):

    model = LinuxDevice

    device = CharField(
        label="Device",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )


class LinuxDeviceImportForm(NetBoxModelImportForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = LinuxDevice

        fields = (
            "device",
            "type",
            "description",
        )


class LinuxDeviceBulkEditForm(NetBoxModelBulkEditForm):
    model = LinuxDevice

    device = CharField(
        required=False,
        label="Device",
    )
    type = CharField(
        required=False,
        label="Type",
    )
    description = CharField(max_length=255, required=False)

    fieldsets = (
        (
            None,
            ("device", "type", "description"),
        ),
    )
    nullable_fields = ["description"]
