from django import forms
from .models import weightlist





class weightchart(forms.ModelForm)   :
    class Meta:
        model = weightlist
        fields = ['name','weight']  

        widgets ={
            'timeOfmarking': forms.TimeInput(attrs={'type':'time'})
        }  