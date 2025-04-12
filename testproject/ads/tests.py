from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ads.models import Ad, ExchangeProposal
import random

class AdModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.categories = ['Электроника', 'Книги', 'Одежда', 'Игрушки', 'Спорт', 'Бытовая техника']
        self.conditions = ['new', 'used']

        cat = random.choice(self.categories)
        num = str(random.randint(10, 1000))
        self.ad1 = Ad.objects.create(
            category=cat,
            title=cat+num,
            description='Описание '+cat+num,
            condition=random.choice(self.conditions),
            user=self.user1)
        self.ad2 = Ad.objects.create(
            category=cat,
            title=cat+num,
            description='Описание '+cat+num,
            condition=random.choice(self.conditions),
            user=self.user2)
    
    def test_create_ad(self):
        self.client.login(username='user1', password='pass')
        cat = random.choice(self.categories)
        num = str(random.randint(10, 1000))
        response = self.client.post(reverse('create_ad'), {
            'category': cat,
            'title': cat+num,
            'description': 'Описание '+cat+num,
            'condition': random.choice(self.conditions)
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title=cat+num).exists())

    def test_edit_ad(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('edit_ad', args=[self.ad1.id]), {
            'title': 'Изменённый заголовок',
            'description': self.ad1.description,
            'category': self.ad1.category,
            'condition': self.ad1.condition
        })
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Изменённый заголовок')

    # Запрет на редактирование чужих объявлений
    def test_edit_ad_forbidden(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('edit_ad', args=[self.ad2.id]), {
            'title': 'Теперь это моё объявление',
            'description': self.ad2.description,
            'category': self.ad2.category,
            'condition': self.ad2.condition
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_ad(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('delete_ad', args=[self.ad1.id]))
        self.assertFalse(Ad.objects.filter(id=self.ad1.id).exists())
        self.assertRedirects(response, reverse('ad_list'))

    # Запрет на удаление чужих объявлений
    def test_delete_ad_forbidden(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('delete_ad', args=[self.ad2.id]))
        self.assertEqual(response.status_code, 403)

    def test_create_proposal(self):
        self.client.login(username='user1', password='pass')
        user1_ad = Ad.objects.create(
            category='Бытовая техника',
            title='Стиральная машина',
            description='Описание',
            condition='used',
            user=self.user1)
        response = self.client.post(reverse('create_proposal', args=[self.ad2.id]), {
            'ad_sender': user1_ad.id,
            'comment': 'Обмен?'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ExchangeProposal.objects.filter(ad_sender=user1_ad.id, ad_receiver=self.ad2).exists())

    # Предложение обмена самому себе
    def test_self_proposal_forbidden(self):
        self.client.login(username='user1', password='pass')
        user1_ad = Ad.objects.create(
            category='Бытовая техника',
            title='Холодильник',
            description='Описание',
            condition='used',
            user=self.user1)
        response = self.client.post(reverse('create_proposal', args=[user1_ad.id]), {
            'ad_sender': user1_ad.id,
            'comment': 'Самообмен'
        })
        self.assertEqual(response.status_code, 403)
        self.assertFalse(ExchangeProposal.objects.filter(ad_receiver=user1_ad).exists())
