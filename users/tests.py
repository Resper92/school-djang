from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponse


class UserViewsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Creiamo un utente di prova e lo aggiungiamo a un gruppo "user"
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.client_group = Group.objects.create(name="user")
        cls.user.groups.add(cls.client_group)
        cls.user.save()

    def test_login_page_get(self):
        """Verifica che la pagina di login venga caricata correttamente"""
        response = self.client.get(reverse('login_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_page_post_valid(self):
        """Verifica il login con credenziali valide"""
        response = self.client.post(reverse('login_page'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('home_page'))
        user = authenticate(username='testuser', password='testpassword')
        self.assertTrue(user is not None and user.is_authenticated)

    def test_login_page_post_invalid(self):
        response = self.client.post(reverse('login_page'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 302)  # 302 per il redirect
        self.assertRedirects(response, reverse('login_page'))  # Se è un redirect, torna alla pagina di login



    def test_logout_page(self):
        """Verifica che l'utente venga disconnesso correttamente"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout_page'))
        self.assertRedirects(response, '/login/')

    def test_register_page_get(self):
        """Verifica che la pagina di registrazione venga caricata correttamente"""
        response = self.client.get(reverse('register_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_page_post_valid(self):
        """Verifica la registrazione con dati validi"""
        response = self.client.post(reverse('register_page'), {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
        })
        self.assertRedirects(response, reverse('login_page'))
        new_user = User.objects.get(username='newuser')
        self.assertTrue(new_user.check_password('newpassword'))
    def test_register_page_post_invalid(self):
        response = self.client.post(reverse('register_page'), {
            'username': 'testuser',
            'email': 'test@example.com',
            # Manca la password
        })

        # ✅ Controlla che la risposta restituisca il form con errori
        self.assertEqual(response.status_code, 400)

        # ✅ Assicura che il form sia nel contesto della risposta
        self.assertIn('form', response.context)

        # ✅ Verifica che il form contenga errori nel campo 'password'
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('password', form.errors)


    def test_user_page_authenticated(self):
        """Verifica che la pagina utente sia visibile solo se l'utente è autenticato"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user_specific', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_detail.html')


    def test_update_user_profile(self):
        """Verifica che un utente possa aggiornare il proprio profilo"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user_specific', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)

        # Verifica che possiamo aggiornare i dati dell'utente
        response = self.client.post(reverse('user_specific', kwargs={'user_id': self.user.id}), {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updateduser@example.com',
        })
        self.assertRedirects(response, reverse('user_specific', kwargs={'user_id': self.user.id}))

        # Verifica che i dati dell'utente siano stati aggiornati
        updated_user = User.objects.get(username='updateduser')
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.email, 'updateduser@example.com')
