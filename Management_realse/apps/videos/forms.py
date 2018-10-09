from django import forms

class UploadFileForm(forms.Form):
    type = forms.CharField()
    name = forms.CharField()
    year = forms.IntegerField()
    info = forms.CharField(max_length=200)
    img = forms.ImageField()
    src_video = forms.FileField()
