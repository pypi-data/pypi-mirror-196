import logging

from extras.plugins import PluginTemplateExtension
from netbox_storage.models import PhysicalVolume, LogicalVolume, MountedVolume, StorageConfigurationLinuxVolume


class RelatedDrives(PluginTemplateExtension):
    model = "virtualization.virtualmachine"

    def left_page(self):
        obj = self.context.get("object")

        lv = LogicalVolume.objects.all()

        storage_configuration = StorageConfigurationLinuxVolume.objects.filter(virtual_machine=obj)

        platform = obj.platform
        if platform is not None:
            if platform.name.lower().__contains__('windows'):
                return self.render(
                    "netbox_storage/inc/windowsvolume_box.html",
                    extra_context={
                        # "volumes": volumes,
                        # "unmapped_drives": unmapped_drives,
                        "type": type(obj.platform),
                    },
                )
            elif platform.name.lower().__contains__('linux'):
                return self.render(
                    "netbox_storage/inc/linuxvolume_box.html"
                )
        else:
            return self.render(
                "netbox_storage/inc/unknown_os_box.html",
                extra_context={
                    "lv": lv,
                    "storage_configuration": storage_configuration
                }
            )


class TemplateVolumeConfig(PluginTemplateExtension):
    model = "dcim.Platform"

    def right_page(self):
        obj = self.context.get("object")

        lv = LogicalVolume.objects.all()

        # storage_configuration = StorageConfigurationLinuxVolume.objects.filter(virtual_machine=obj)

        return self.render(
            "netbox_storage/inc/template_box.html",
            extra_context={
                "lv": lv,
            }
        )


template_extensions = [RelatedDrives, TemplateVolumeConfig]
