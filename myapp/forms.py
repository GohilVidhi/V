from django import forms
from .models import *

# class SCategoryForm(forms.ModelForm):
#     class Meta:
#         model = sub_category
#         fields = ['name', 'mcategory']

# class PersonCreationForm(forms.ModelForm):
#     class Meta:
#         model = expertise
#         fields = '__all__'
#     # mcategory = forms.ChoiceField(widget=forms.Select(attrs={'class': 'custom-select'}), label='Main Category')
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['scategory'].queryset = sub_category.objects.none()
        

#         if 'mcategory' in self.data:
#             try:
#                 country_id = int(self.data.get('mcategory'))
#                 print(country_id)
#                 self.fields['scategory'].queryset = sub_category.objects.filter(mcategory_id=country_id).order_by("id")
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty s_category queryset
#         elif self.instance.pk:
#             print("ok")
#             self.fields['scategory'].queryset = self.instance.mcategory.scategory_set.order_by('name')        