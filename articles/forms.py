from django import forms
from articles.models import Article 

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
    
    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        qs = Article.objects.all().filter(title__icontains=title) 
        if qs.exists():
            self.add_error('title', f'\"{title}\" is already in use!')
        return data


class ArticleFormOld(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    # def clean_title(self):
    #     cleaned_data = self.cleaned_data # Dictionary
    #     title = cleaned_data.get('title')
    #     if title.lower().strip() == 'new article':
    #         raise forms.ValidationError('This title is taken.')
    #     return title

    def clean(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title.lower().strip() == 'new article':
            self.add_error('title', 'This title is taken.')
            # raise forms.ValidationError('This title is taken.')
        if 'office' in content.lower() or 'office' in title.lower():
            self.add_error('content', 'Office can not be in content.')
        return cleaned_data
