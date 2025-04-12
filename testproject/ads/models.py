from django.db import models
from django.contrib.auth.models import User
import random

class Ad(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/у'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL изображения")
    category = models.CharField(max_length=100, verbose_name="Категория")
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, verbose_name="Состояние")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    def __str__(self):
        return self.title

class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]
    
    id = models.AutoField(primary_key=True)
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals', verbose_name="Отправитель")
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals', verbose_name="Получатель")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата предложения")

    def __str__(self):
        return f"{self.ad_sender.title} → {self.ad_receiver.title} ({self.get_status_display()})"

'''
user = User.objects.create_user(username='user1', password='pass')
categories = ['Электроника', 'Книги', 'Одежда', 'Игрушки', 'Спорт', 'Бытовая техника']
conditions = ['new', 'used']
        
for i in (range10):
    cat = random.choice(categories)
    ad = Ad.objects.create(
         category=cat,
         user=user,
         title=cat+str(i),
         description="Описание"+cat+str(i),
         condition=random.choice(conditions),
         )
    print(f"Создано объявление: {ad.title}")
'''