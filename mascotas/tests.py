from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from clientes.models import Cliente
from .models import Mascota

class MascotasTestCase(TestCase):
    def setUp(self):
        # Crear usuario y cliente
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.cliente = Cliente.objects.create(
            usuario=self.user,
            telefono='+34123456789',
            direccion='Calle Test 123'
        )
        
        # Crear mascota
        self.mascota = Mascota.objects.create(
            nombre='Firulais',
            tipo='perro',
            raza='Labrador',
            sexo='macho',
            cliente=self.cliente
        )
        
        self.client = Client()
    
    def test_creacion_mascota(self):
        self.assertEqual(self.mascota.nombre, 'Firulais')
        self.assertEqual(self.mascota.tipo, 'perro')
        self.assertEqual(self.mascota.cliente, self.cliente)
    
    def test_vista_lista_mascotas(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('mascotas:lista_mascotas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Firulais')
    
    def test_vista_detalle_mascota(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('mascotas:detalle_mascota', args=[self.mascota.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Firulais')
    
    def test_acceso_no_autorizado(self):
        # Crear otro usuario
        user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        cliente2 = Cliente.objects.create(
            usuario=user2,
            telefono='+34987654321',
            direccion='Otra dirección'
        )
        
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(reverse('mascotas:detalle_mascota', args=[self.mascota.id]))
        self.assertEqual(response.status_code, 403)  # Debería ser prohibido