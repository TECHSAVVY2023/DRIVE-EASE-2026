from django.forms import ModelForm
from .models import ContactListModel

class ContactListForm(ModelForm):
  class Meta:
    model = ContactListModel
    fields = '__all__'
