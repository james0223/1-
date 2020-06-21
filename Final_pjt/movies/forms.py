from django import forms
from .models import Movie, Article, ArticleComment, MovieComment

RANK_CHOICES= [
    ( 1, '1'),
    ( 2, '2'),
    ( 3, '3'),
    ( 4, '4'),
    ( 5, '5'),
    ( 6, '6'),
    ( 7, '7'),
    ( 8, '8'),
    ( 9, '9'),
    ( 10, '10'),
]

class MovieCommentForm(forms.ModelForm):
    content = forms.CharField(label='Your opinion?', widget=forms.Textarea(attrs={'rows': 1,}))
    rank = forms.IntegerField(
        # label='Select',
        widget=forms.RadioSelect(choices=RANK_CHOICES, attrs={
            'class': 'form-check-inline'}
            )
        )
    class Meta:
        model = MovieComment
        fields = ['rank','content']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','content']

class ArticleCommentForm(forms.ModelForm):
    content = forms.CharField(label='Leave a comment!', widget=forms.Textarea(attrs={'rows': 2,}))
    class Meta:
        model = ArticleComment
        fields = ['content']