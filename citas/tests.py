from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from mascotas.models import Mascota, Cliente
from .models import Cita
from django.urls import reverse

class CitasTestCase(TestCase):
    def setUp(self):
        # Crear usuario y cliente
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.cliente = Cliente.objects.create(
            usuario=self.user,
            telefono='+34123456789',
            direccion='Calle Test 123'
        )
        
        # Crear mascota
        self.mascota = Mascota.objects.create(
            nombre='Firulais',
            especie='perro',
            raza='Labrador',
            cliente=self.cliente
        )
        
        # Crear cita
        self.cita = Cita.objects.create(
            mascota=self.mascota,
            fecha=timezone.now() + timedelta(days=1),
            tipo='consulta_general',
            prioridad='normal',
            motivo='Consulta de rutina',
            sintomas='Ninguno en particular',
            estado='programada'
        )
        
        self.client = Client()
    
    def test_creacion_cita(self):
        self.assertEqual(self.cita.mascota.nombre, 'Firulais')
        self.assertEqual(self.cita.estado, 'programada')
        self.assertEqual(self.cita.prioridad, 'normal')
        self.assertEqual(self.cita.tipo, 'consulta_general')
    
    def test_vista_solicitar_cita(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('citas:solicitar_cita'))
        self.assertEqual(response.status_code, 200)
    
    def test_vista_mis_citas(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('citas:mis_citas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Firulais')
    
    def test_cancelar_cita(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('citas:cancelar_cita', args=[self.cita.id]))
        self.cita.refresh_from_db()
        self.assertEqual(self.cita.estado, 'cancelada')
        self.assertRedirects(response, reverse('citas:mis_citas'))
    
    def test_confirmar_cita(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('citas:confirmar_cita', args=[self.cita.id]))
        self.cita.refresh_from_db()
        self.assertEqual(self.cita.estado, 'confirmada')
        self.assertTrue(self.cita.confirmada_por_cliente)
        self.assertRedirects(response, reverse('citas:mis_citas'))
    
    def test_puede_ser_cancelada(self):
        self.assertTrue(self.cita.puede_ser_cancelada())
        
        # Probar con cita completada
        cita_completada = Cita.objects.create(
            mascota=self.mascota,
            fecha=timezone.now() + timedelta(days=1),
            tipo='vacunacion',
            estado='completada'
        )
        self.assertFalse(cita_completada.puede_ser_cancelada())