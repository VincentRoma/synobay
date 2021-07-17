from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)

class DownloadForm(forms.Form):
    magnet = forms.CharField(label='Magnet', max_length=1000)
    genre = forms.CharField(label='Genre', max_length=20)