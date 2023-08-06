from netbox.views import generic

from netbox_storage.forms.template import LinuxVolumeTemplateForm, LVMTemplateForm, DriveTemplateForm, \
    PartitionTemplateForm
from netbox_storage.models import TemplateConfigurationDrive, Partition


class LVMAddTemplateView(generic.ObjectEditView):
    """View for editing a Drive instance."""

    queryset = TemplateConfigurationDrive.objects.all()
    form = LVMTemplateForm
#    default_return_url = "plugins:netbox_storage:drive_list"


class AddTemplateVolumeView(generic.ObjectEditView):
    """View for editing a Drive instance."""
    # template_name = "netbox_storage/inc/volume_add.html"
    queryset = TemplateConfigurationDrive.objects.all()
    form = LinuxVolumeTemplateForm
#    default_return_url = "plugins:netbox_storage:drive_list"
    # default_return_url = "virtualization:virtualmachine"


class AddTemplateDriveView(generic.ObjectEditView):
    queryset = TemplateConfigurationDrive.objects.all()
    form = DriveTemplateForm


class AddTemplatePartitionView(generic.ObjectEditView):
    queryset = Partition.objects.all()
    form = PartitionTemplateForm
