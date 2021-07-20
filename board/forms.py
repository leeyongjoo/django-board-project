from django import forms
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']

        labels = {
            'subject': '제목',
            'content': '내용',
        }

        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

        labels = {
            'content': '답변 내용',
        }
