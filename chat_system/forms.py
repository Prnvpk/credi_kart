from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('recipient', 'subject', 'body')
        widgets = {'body': forms.Textarea(attrs={'rows': 4})}

    def __init__(self, *args, **kwargs):
        recipients = kwargs.pop('recipients', None)
        super().__init__(*args, **kwargs)
        if recipients is not None:
            self.fields['recipient'].queryset = recipients
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
