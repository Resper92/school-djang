from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from trainer.models import TraineDescription, TraineSchedule, Category, Service
from trainer.forms import TrainerForm, WeeklyWorkScheduleForm, ServiceForm_01
import datetime

class TrainerPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='trainer1', password='testpassword')
        self.trainer_group = Group.objects.create(name='Trainer')
        self.user.groups.add(self.trainer_group)
        self.description = TraineDescription.objects.create(trainer=self.user, text="Trainer description")

    def test_trainer_page_authenticated(self):
        self.client.login(username='trainer1', password='testpassword')
        response = self.client.get(reverse('trainer_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainer.html')

    def test_trainer_page_not_trainer(self):
        user2 = User.objects.create_user(username='client1', password='testpassword')
        self.client.login(username='client1', password='testpassword')
        response = self.client.get(reverse('trainer_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_trainers.html')

class TrainerScheduleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='trainer1', password='testpassword')
        self.trainer_group = Group.objects.create(name='Trainer')
        self.user.groups.add(self.trainer_group)
        self.schedule = TraineSchedule.objects.create(trainer=self.user, datatime_start=datetime.datetime.now(), datatime_end=datetime.datetime.now() + datetime.timedelta(hours=1))

    def test_specific_trainer_schedule(self):
        self.client.login(username='trainer1', password='testpassword')
        response = self.client.get(reverse('specific_trainer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'specific_trainer.html')

class TrainerServiceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='trainer1', password='testpassword')
        self.trainer_group = Group.objects.create(name='Trainer')
        self.user.groups.add(self.trainer_group)
        self.category = Category.objects.create(name='Fitness')
        self.service = Service.objects.create(category=self.category, trainer=self.user, price=50.0, level=1, duration=60)
    
    def test_trainer_service_page(self):
        response = self.client.get(reverse('trainer_service'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainer_service.html')

class TrainerRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_trainer_registration(self):
        response = self.client.get(reverse('trainer_registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainer_registration.html')
    def test_service_form_valid(self):
        category = Category.objects.create(name="Fitness")  # ✅ Crea una categoria valida
        trainer = User.objects.create(username="trainer1", email="trainer1@example.com")  # ✅ Crea un trainer fittizio
        form = ServiceForm_01(data={
            'category': category.id,
            'trainer': trainer.id,  # ✅ Aggiungi il trainer
            'price': 50.0,
            'level': 1,
            'duration': 60
        })
        self.assertTrue(form.is_valid(), form.errors)  # ✅ Se fallisce, stampa gli errori per debugging


class FormsTests(TestCase):
    def setUp(self):        
        Group.objects.create(name="Trainer")  
    def test_service_form_valid(self):
        category = Category.objects.create(name="Fitness")  # Aggiunta una categoria
        form = ServiceForm_01(data={'category': category.id, 'price': 50.0, 'level': 1, 'duration': 60})
        self.assertTrue(form.is_valid())

    def test_schedule_form_valid(self):
        form = WeeklyWorkScheduleForm(data={'start_time': '09:00', 'end_time': '18:00', 'days': ['Monday', 'Tuesday']})
        self.assertTrue(form.is_valid())


