from django import forms
from crm.models import Event
# from django.shortcuts import render


class EventAdminForm(forms.ModelForm):
    '''Define the Event form in admin dashboard.'''
    class Meta:
        model = Event
        exclude = ['date_created', 'date_updated']

    # Ne pas rendre possible le changement du contrat
    # Only use clean method to raise errors
    def clean(self):
        cleaned_data = self.cleaned_data
        # print("cleaned_data", cleaned_data)
        # get contract from field form
        contrat = cleaned_data.get('contract')
        # print("--------------------------contrat", contrat)
        # search if there is an event with this contract in database
        selected_event = Event.objects.filter(contract=contrat).first()
        # if event_date_end is past make impossible to change event
        if selected_event is not None and selected_event.is_past():
            raise forms.ValidationError(
                'Vous ne pouvez pas modifier un événement terminé.')

        return cleaned_data
