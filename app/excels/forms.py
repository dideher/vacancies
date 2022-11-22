from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Αρχείο')
    purge_existing_schools = forms.BooleanField(initial=False, label='Λειτουργία Αρχικοποίησης', required=False,
                                                help_text='Αν επιλέξετε αρχικοποίηση, τότε τυχόν υπαρκτά σχολεία '
                                                          'στην βάση θα διαγραφούν αμετάκλειτα')
