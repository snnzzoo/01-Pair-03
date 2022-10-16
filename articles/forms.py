from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    grade = forms.FloatField(
        required=True,
        max_value=5,
        min_value=1,
        widget=forms.NumberInput(attrs={"step": "0.5"}),
    )
    class Meta:
        model = Article
        fields = "__all__"
