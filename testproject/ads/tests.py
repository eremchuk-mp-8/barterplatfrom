from django.test import TestCase
from django.contrib.auth.models import User
from ads.models import Ad
import random

class AdModelTest(TestCase):
    def test_ad_creation(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        categories = ['Электроника', 'Книги', 'Одежда', 'Игрушки', 'Спорт', 'Бытовая техника']
        conditions = ['new', 'used']
        
        for i in range(10):
            cat = random.choice(categories)
            ad = Ad.objects.create(
                category=cat,
                user=self.user,
                title=cat+str(i),
                description="Описание"+cat+str(i),
                condition=random.choice(conditions),
            )
            print(f"Создано объявление: {ad.title}")
'''
    def test_ads_count(self):
        self.assertEqual(Ad.objects.count(), 10)

    def test_first_ad_content(self):
        # Получение первого объявления
        ad = Ad.objects.first()

        # Проверка, что первое объявление существует
        self.assertIsNotNone(ad, "Первое объявление не найдено")

        # Проверка, что у объявления есть название и описание
        self.assertTrue(ad.title, "У объявления нет названия")
        self.assertTrue(ad.description, "У объявления нет описания")
'''