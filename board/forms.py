from typing import Any
from django import forms
from .models import Thread, Post
from .utils import create_id

class ThreadForm(forms.Form):
    title = forms.CharField(max_length=100)
    author = forms.CharField(max_length=100, required=False)
    mail = forms.EmailField(required=False)
    content = forms.CharField(widget=forms.Textarea)


    def save(self, ip_address: str = None, commit: bool = ...) -> Any:
        userid = create_id(ip_address)
        thread = Thread(
            title=self.cleaned_data['title'],
            user_id=userid,
            ip_address=ip_address
        )
        if commit:
            thread.save()

        post = Post(
            author=self.cleaned_data['author'],
            mail=self.cleaned_data['mail'],
            content=self.cleaned_data['content'],
            ip_address=ip_address,
            thread=thread,
            user_id=userid
        )
        if commit:
            post.save()
        return thread, post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'mail', 'content']
    def save(self, commit: bool = ...) -> Any:
        post = super().save(commit=False)
        if commit:
            post.save()
        return post