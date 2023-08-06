from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_storage.models import MountedVolume, LinuxDevice


class MountedVolumeFilter(NetBoxModelFilterSet):

    class Meta:
        model = MountedVolume
        fields = [
            "size",
            "path",
            "description",
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(size__icontains=value)
            | Q(path__icontains=value)
        )
        return queryset.filter(qs_filter)


class LinuxDeviceFilter(NetBoxModelFilterSet):

    class Meta:
        model = LinuxDevice
        fields = [
            "device",
            "type",
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(device__icontains=value)
            | Q(type__icontains=value)
        )
        return queryset.filter(qs_filter)
