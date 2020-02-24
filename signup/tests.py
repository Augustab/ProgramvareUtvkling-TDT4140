from django.contrib.auth.models import User
from django.test import TestCase
from signup.forms import RegisterForm
from django.test import Client

class SetupClass(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@mail.com", password1="123", password2="123")


class UserFormTest(TestCase):
    def test_UserForm_valid(self):
        form = RegisterForm(
            data={'username': "testuser", 'email': "test@mail.com", 'password1': "123jenny", 'password2': "123jenny"})
        self.assertTrue(form.is_valid())

    def test_UserForm_invalid(self):
        form = RegisterForm(data={'username': "", 'email': "", 'password1': "", 'password2': ""})
        self.assertFalse(form.is_valid())


class UserViewsTest(SetupClass):
    def test_login_view(self):
        c = Client()
        user_login = c.login(email="test@mail.com", password="123jenny")
        self.assertTrue(user_login)
        response = c.get("/login/")
        self.assertEqual(response.status_code, 302) # 302 er Found

    def test_signup_view(self):
        c = Client()
        response = c.get("/signup/")
        self.assertEqual(response.status_code, 200) # 200 er HTTP OK
        self.assertTemplateUsed(response, "../templates/register.html")

