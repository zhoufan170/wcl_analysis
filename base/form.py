from django import forms


class LoadReportForm(forms.Form):
    code = forms.CharField(label="WCL report code", max_length=30,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
