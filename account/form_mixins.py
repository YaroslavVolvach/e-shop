from django import forms


class ChangeWigetsMixins:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            value.widget.attrs = {'class': 'form-control'}

            if key == 'birth_date':
                value.widget = forms.widgets.DateInput(attrs={'type': 'date'})
