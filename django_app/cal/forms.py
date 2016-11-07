from django import forms


class MemoForm(forms.Form):
    memo = forms.CharField(max_length=200,
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'memoText',
                'rows': 5,
                })
            )
