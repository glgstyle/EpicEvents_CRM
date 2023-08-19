from django import forms
from crm.models import Event


class EventAdminForm(forms.ModelForm):
    '''Define the Event form in admin dashboard.'''
    class Meta:
        model = Event
        exclude = ['date_created', 'date_updated']

    def clean(self):
        cleaned_data = self.cleaned_data
        # get contract from field form
        contrat = cleaned_data.get('contract')
        # search if there is an event with this contract in database
        selected_event = Event.objects.filter(contract=contrat).exists()
        # if an event already exists with this contract
        if selected_event:
            raise forms.ValidationError(
                'Il y a déjà un événement avec ce contrat. '
                'Veuillez signer un autre contrat pour '
                'créer un nouvel événement')
        return cleaned_data
