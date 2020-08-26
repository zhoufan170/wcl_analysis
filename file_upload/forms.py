from django import forms
from .models import File


# Regular form
class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    wcl_link = forms.CharField(label="WCL Link", max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["csv", "pdf", "txt"]:
            raise forms.ValidationError("Only csv, pdf and txt files are allowed.")
        # return cleaned data is very important.
        return file


# Model form
class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', 'wcl_link',)

        widgets = {
            'wcl_link': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["csv", "pdf", "txt"]:
            raise forms.ValidationError("Only csv, pdf and txt files are allowed.")
        # return cleaned data is very important.
        return file

