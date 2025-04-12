from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']

class ProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']
        labels = {
            'ad_sender': 'Объявление отправителя',
            'comment': 'Комментарий',
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # извлекаем текущего пользователя
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)