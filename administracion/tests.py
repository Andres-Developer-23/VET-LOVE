from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AdministracionTestCase(TestCase):
    def setUp(self):
        # Crear usuario staff
        self.staff_user = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True
        )
        
        # Crear usuario normal
        self.normal_user = User.objects.create_user(
            username='usuario',
            password='user123',
            is_staff=False
        )
        
        self.client = Client()
    
    def test_dashboard_acceso_staff(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('administracion:dashboard_admin'))
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_acceso_no_staff(self):
        self.client.login(username='usuario', password='user123')
        response = self.client.get(reverse('administracion:dashboard_admin'))
        self.assertEqual(response.status_code, 302)  # Redirección a login
        self.assertRedirects(response, '/admin/login/')
    
    def test_dashboard_sin_autenticar(self):
        response = self.client.get(reverse('administracion:dashboard_admin'))
        self.assertEqual(response.status_code, 302)  # Redirección a login  