from django.contrib.auth.models import User
from django.test import TestCase
from signup.forms import RegisterForm
from django.test import Client


class UserFormTest(TestCase):
    def test_UserForm_valid(self):  # tester om registreringsskjema fungerer
        form = RegisterForm(data={
                             'username': "testuser",
                             'email': "test@mail.com",
                             'password1': "123goodpassword",
                             'password2': "123goodpassword"})
        self.assertTrue(form.is_valid())

    def test_UserForm_noData(self):  # tester om hva som skjer uten
        form = RegisterForm(data={
                             'username': "",
                             'email': "",
                             'password1': "",
                             'password2': ""})
        self.assertFalse(form.is_valid())


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_view(self):  # tester om man blir sendt til riktig sted når man trykker på 'logg inn'-knapp
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)  # 200 er HTTP OK
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login(self):  # tester om man klarer å logge inn på 'logg inn'-side
        user = User.objects.create(username='testuser2')
        user.set_password('123password')
        user.save()
        logged_in = self.client.login(username="testuser2", password='123password')
        self.assertTrue(logged_in)

    def test_signup_view(self):  # tester om man blir sendt til riktig sted når man trykker 'lag bruker'-knapp
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)  # 200 er HTTP OK
        self.assertTemplateUsed(response, "register/register.html")
