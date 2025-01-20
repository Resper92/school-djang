from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from trainer.models import TraineDescription, TraineSchedule, Category, Service
import datetime

class TrainerTests(TestCase):

    def setUp(self):
        # Crea un gruppo "Trainer"
        self.trainer_group = Group.objects.create(name="Trainer")

        # Crea un utente Trainer
        self.trainer_user = User.objects.create_user(
            username="trainer_user", password="password123"
        )
        self.trainer_user.groups.add(self.trainer_group)

        # Crea un utente generico
        self.generic_user = User.objects.create_user(
            username="generic_user", password="password123"
        )

        # Crea una descrizione del trainer
        self.trainer_description = TraineDescription.objects.create(
            trainer=self.trainer_user,
            text="Trainer Test Bio"
        )

        # Crea un orario per il trainer
        start_time = datetime.datetime.now() + datetime.timedelta(days=1, hours=9)
        end_time = start_time + datetime.timedelta(hours=1)
        self.trainer_schedule = TraineSchedule.objects.create(
            trainer=self.trainer_user,
            datatime_start=start_time,
            datatime_end=end_time,
        )

        # Crea una categoria e un servizio
        self.category = Category.objects.create(name="Fitness")
        self.service = Service.objects.create(
            trainer=self.trainer_user,
            category=self.category,
            price=50.0,
            level=1,
            duration=60
        )

    def test_trainer_page_as_trainer(self):
        # Esegui il login come trainer
        self.client.login(username="trainer_user", password="password123")

        response = self.client.get(reverse("trainer_page"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,TraineSchedule.objects.get(trainer=self.trainer_user).datatime_start.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertTemplateUsed(response, "trainer.html")

    def test_trainer_page_as_generic_user(self):
        # Esegui il login come utente generico
        self.client.login(username="generic_user", password="password123")

        response = self.client.get(reverse("trainer_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "all_trainers.html")
        self.assertContains(response, "Trainer Test Bio")

    def test_category_page(self):
        # Test della pagina della categoria
        self.client.login(username="trainer_user", password="password123")
        response = self.client.get(reverse("category_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "category.html")

    def test_trainer_details(self):
        # Test della pagina dei dettagli del trainer
        response = self.client.get(reverse("trainer_details", args=[self.trainer_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Trainer Test Bio")
        self.assertContains(response, self.trainer_schedule.datatime_start.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertContains(response, self.service.name)

    def test_trainer_service_page(self):
        # Test della pagina del servizio del trainer
        response = self.client.get(reverse("trainer_service_page", args=[self.trainer_user.id, self.service.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service.category)
        self.assertTemplateUsed(response, "trainer_service_page.html")

    def test_trainer_service_page_booking(self):
        # Test la creazione di una prenotazione per un servizio
        self.client.login(username="generic_user", password="password123")
        start_time = datetime.datetime.now() + datetime.timedelta(hours=1)
        response = self.client.post(reverse("trainer_service_page", args=[self.trainer_user.id, self.service.id]), {
            "training-start": start_time.strftime("%Y-%m-%d %H:%M:%S")
        })
        self.assertEqual(response.status_code, 302)  # Redirige dopo la prenotazione
        self.assertRedirects(response, reverse("trainer_service_page", args=[self.trainer_user.id, self.service.id]))

    def test_trainer_registration(self):
        # Test della registrazione di un nuovo trainer
        response = self.client.post(reverse("trainer/registratione/"), {
            "username": "new_trainer",
            "password1": "password123",
            "password2": "password123",
            "email": "new_trainer@example.com"
        })
        self.assertEqual(response.status_code, 302)  # Redirige dopo la registrazione
        self.assertRedirects(response, reverse("login_page"))  # Modifica con il percorso giusto

    def test_trainer_schedule_creation(self):
        # Test la creazione di un orario per il trainer
        schedule_data = {
            "start_time": "09:00",
            "end_time": "10:00",
            "days": ["Monday", "Tuesday"]
        }
        self.client.login(username="trainer_user", password="password123")
        response = self.client.post(reverse("specific_trainer"), schedule_data)
        self.assertEqual(response.status_code, 302)  # Redirige alla pagina specific_trainer
        self.assertRedirects(response, reverse("specific_trainer"))
        # Verifica che gli orari siano stati creati
        schedule = TraineSchedule.objects.filter(trainer=self.trainer_user)
        self.assertEqual(schedule.count(), 2)  # Dovrebbero esserci 2 orari per i giorni selezionati

    def test_trainer_service_creation(self):
        # Test per la creazione di un servizio
        self.client.login(username="trainer_user", password="password123")
        response = self.client.post(reverse("trainer_service"), {
            "category": self.category.id,
            "price": 60.0,
            "level": 1,
            "duration": 90
        })
        self.assertEqual(response.status_code, 302)  # Redirige alla pagina trainer_page
        self.assertRedirects(response, reverse("trainer_page"))
        # Verifica che il servizio sia stato creato
        service = Service.objects.get(trainer=self.trainer_user)
        self.assertEqual(service.price, 60.0)

