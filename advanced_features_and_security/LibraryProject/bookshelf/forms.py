from django import forms

class ExampleForm(forms.Form):
  title = forms.CharField(max_length=100, required=True)
  author = forms.CharField(max_length=100, required=True)
  published_date = forms.DateField(widget=forms.SelectDateWidget)

  def clean_title(self):
    data = self.cleaned_data["title"]
    # Add custom validation for title here if necessary
    return data

  def clean_author(self):
    data = self.cleaned_data["author"]
    # Add custom validation for author here if necessary
    return data
