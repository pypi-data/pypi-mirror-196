from netbox.views import generic

from netbox_storage.forms import LVMSimpleForm, VolumeSimpleForm, LinuxVolumeSimpleForm
from netbox_storage.forms.template import LinuxVolumeTemplateForm, LVMTemplateForm
from netbox_storage.models import Drive, StorageConfigurationLinuxVolume


class LVMAddTemplateView(generic.ObjectEditView):
    """View for editing a Drive instance."""

    queryset = StorageConfigurationLinuxVolume.objects.all()
    form = LVMTemplateForm
#    default_return_url = "plugins:netbox_storage:drive_list"


class AddSimpleTemplateVolumeView(generic.ObjectEditView):
    """View for editing a Drive instance."""
    # template_name = "netbox_storage/inc/volume_add.html"
    queryset = StorageConfigurationLinuxVolume.objects.all()
    form = LinuxVolumeTemplateForm
#    default_return_url = "plugins:netbox_storage:drive_list"
    # default_return_url = "virtualization:virtualmachine"
