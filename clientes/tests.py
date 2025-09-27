from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Cliente
from django.urls import reverse

class ClienteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.cliente = Cliente.objects.create(
            usuario=self.user,
            telefono='+34123456789',
            direccion='Calle Test 123',
            preferencias_comunicacion='email'
        )
        self.client = Client()
    
    def test_creacion_cliente(self):
        self.assertEqual(self.cliente.usuario.username, 'testuser')
        self.assertEqual(self.cliente.telefono, '+34123456789')
    
    def test_vista_perfil_cliente(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('clientes:perfil_cliente'))
        self.assertEqual(response.status_code, 200)from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Cliente
from django.urls import reverse

class ClienteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.cliente = Cliente.objects.create(
            usuario=self.user,
            telefono='+34123456789',
            direccion='Calle Test 123',
            preferencias_comunicacion='email'
        )
        self.client = Client()
    
    def test_creacion_cliente(self):
        self.assertEqual(self.cliente.usuario.username, 'testuser')
        self.assertEqual(self.cliente.telefono, '+34123456789')
    
    def test_vista_perfil_cliente(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('clientes:perfil_cliente'))
        self.assertEqual(response.status_code, 200)
    
    def test_vista_crear_perfil(self):
        # Crear un usuario sin perfil
        user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(reverse('clientes:crear_perfil_cliente'))
        self.assertEqual(response.status_code, 200)
    
    def test_vista_crear_perfil(self):
        # Crear un usuario sin perfil
        user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(reverse('clientes:crear_perfil_cliente'))
        self.assertEqual(response.status_code, 200)