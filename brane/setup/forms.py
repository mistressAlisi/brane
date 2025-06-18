from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from django.core.exceptions import ValidationError
from django.forms import Form, CharField
from django.forms.fields import IntegerField
from django.forms.models import ModelChoiceField
from django.utils.timezone import now
from django.utils.translation import gettext as _

from brane.toolkit.validators.network import validate_network_block


class CreateBraneDBForm(Form):
    cidr = CharField(label=_("Virtual Network CIDR"),help_text=_("This is the /24 subnet that will be used to create the Podman network for this Multiverse."),required=True,initial="10.31.159.0/24")
    pgpasswd = CharField(label=_("PostgreSQL Admin Password"),help_text=_("This is the password that will be set for the postgres user."),required=True,initial="postgres")
    pgdata = CharField(label=_("PostgreSQL DB Path"),help_text=_("This the directory (on the host) where the Postgres database will be created and persisted."),required=True,initial="/opt/brane/postgres/")
    ctrlport = CharField(label=_("Brane Control Plane Port"),help_text=_("This is the Port on the host the Brane Control Plane (this app) will be exposed on."),initial=13145)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'row'
        self.helper.layout = Layout(
            Div(
                Div(FloatingField("ctrlport"), css_class="col"),
            ),
            Div(
                Div(FloatingField("cidr"), css_class="col"),
            ),
            Div(
                Div(FloatingField("pgpasswd"), css_class="col"),
            ),
            Div(
                Div(FloatingField("pgdata"), css_class="col"),
            ),
            Div(
                HTML(f'<div class="d-flex justify-content-end"><input type="submit" class="btn btn-bd-primary mt-3" value="{_("Create Multiverse!")}"/></div>'),
                css_class="col py-2"
            )

        )

    def clean(self):
        cdata = super().clean()
        port = int(cdata.get("ctrlport"))
        if port < 0 or port > 65535:
            raise ValidationError(_("Port number must be between 0 and 65535"))
        if not validate_network_block(cdata.get('cidr')):

            raise ValidationError(_("Invalid Network Block Specified"),code="invalid",params={"value":cdata.get('cidr')})


