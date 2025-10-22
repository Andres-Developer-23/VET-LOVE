from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import date, datetime, timedelta
import random
from decimal import Decimal

from clientes.models import Cliente
from mascotas.models import Mascota, HistorialMedico, Vacuna
from citas.models import Cita
from tienda.models import Categoria, Producto


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Starting database population...')

        # Create groups if they don't exist
        clientes_group, created = Group.objects.get_or_create(name='Clientes')
        if created:
            self.stdout.write('Created Clientes group')

        # Create sample clients
        self.create_clients()

        # Create sample pets
        self.create_pets()

        # Create sample appointments
        self.create_appointments()

        # Create sample products
        self.create_products()

        self.stdout.write(self.style.SUCCESS('Database population completed!'))

    def create_clients(self):
        clients_data = [
            {
                'username': 'cliente1',
                'email': 'cliente1@example.com',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'telefono': '+573101234567',
                'direccion': 'Calle 123 #45-67, Bogotá',
                'preferencias_comunicacion': 'email'
            },
            {
                'username': 'cliente2',
                'email': 'cliente2@example.com',
                'first_name': 'María',
                'last_name': 'García',
                'telefono': '+573102345678',
                'direccion': 'Carrera 89 #12-34, Medellín',
                'preferencias_comunicacion': 'whatsapp'
            },
            {
                'username': 'cliente3',
                'email': 'cliente3@example.com',
                'first_name': 'Carlos',
                'last_name': 'Rodríguez',
                'telefono': '+573103456789',
                'direccion': 'Avenida 56 #78-90, Cali',
                'preferencias_comunicacion': 'email'
            },
            {
                'username': 'cliente4',
                'email': 'cliente4@example.com',
                'first_name': 'Ana',
                'last_name': 'Martínez',
                'telefono': '+573104567890',
                'direccion': 'Diagonal 23 #45-67, Barranquilla',
                'preferencias_comunicacion': 'sms'
            },
            {
                'username': 'cliente5',
                'email': 'cliente5@example.com',
                'first_name': 'Luis',
                'last_name': 'Hernández',
                'telefono': '+573105678901',
                'direccion': 'Transversal 78 #90-12, Cartagena',
                'preferencias_comunicacion': 'email'
            }
        ]

        for client_data in clients_data:
            user, created = User.objects.get_or_create(
                username=client_data['username'],
                defaults={
                    'email': client_data['email'],
                    'first_name': client_data['first_name'],
                    'last_name': client_data['last_name'],
                    'is_active': True
                }
            )

            if created:
                user.set_password('password123')
                user.save()
                user.groups.add(Group.objects.get(name='Clientes'))

                Cliente.objects.create(
                    usuario=user,
                    telefono=client_data['telefono'],
                    direccion=client_data['direccion'],
                    preferencias_comunicacion=client_data['preferencias_comunicacion']
                )
                self.stdout.write(f'Created client: {user.username}')

    def create_pets(self):
        clients = list(Cliente.objects.all())
        if not clients:
            self.stdout.write(self.style.WARNING('No clients found, skipping pet creation'))
            return

        pets_data = [
            {
                'nombre': 'Max',
                'tipo': 'perro',
                'raza': 'Labrador Retriever',
                'sexo': 'macho',
                'fecha_nacimiento': date(2020, 5, 15),
                'peso_actual': Decimal('25.5'),
                'esterilizado': 'si',
                'estado_vacunacion': 'completo',
                'desparasitacion': 'actualizado',
                'comportamiento_consulta': 'tranquilo'
            },
            {
                'nombre': 'Luna',
                'tipo': 'gato',
                'raza': 'Siamés',
                'sexo': 'hembra',
                'fecha_nacimiento': date(2019, 8, 22),
                'peso_actual': Decimal('4.2'),
                'esterilizado': 'si',
                'estado_vacunacion': 'completo',
                'desparasitacion': 'actualizado',
                'comportamiento_consulta': 'tranquilo'
            },
            {
                'nombre': 'Rocky',
                'tipo': 'perro',
                'raza': 'Bulldog Francés',
                'sexo': 'macho',
                'fecha_nacimiento': date(2021, 3, 10),
                'peso_actual': Decimal('12.8'),
                'esterilizado': 'no',
                'estado_vacunacion': 'parcial',
                'desparasitacion': 'pendiente',
                'comportamiento_consulta': 'nervioso'
            },
            {
                'nombre': 'Bella',
                'tipo': 'perro',
                'raza': 'Golden Retriever',
                'sexo': 'hembra',
                'fecha_nacimiento': date(2018, 12, 5),
                'peso_actual': Decimal('28.3'),
                'esterilizado': 'si',
                'estado_vacunacion': 'completo',
                'desparasitacion': 'actualizado',
                'comportamiento_consulta': 'tranquilo'
            },
            {
                'nombre': 'Milo',
                'tipo': 'gato',
                'raza': 'Persa',
                'sexo': 'macho',
                'fecha_nacimiento': date(2022, 1, 18),
                'peso_actual': Decimal('5.1'),
                'esterilizado': 'no',
                'estado_vacunacion': 'ninguna',
                'desparasitacion': 'desconocido',
                'comportamiento_consulta': 'asustadizo'
            },
            {
                'nombre': 'Coco',
                'tipo': 'ave',
                'raza': 'Loro Amazónico',
                'sexo': 'macho',
                'fecha_nacimiento': date(2017, 6, 30),
                'peso_actual': Decimal('0.8'),
                'esterilizado': 'desconocido',
                'estado_vacunacion': 'desconocido',
                'desparasitacion': 'desconocido',
                'comportamiento_consulta': 'nervioso'
            },
            {
                'nombre': 'Toby',
                'tipo': 'perro',
                'raza': 'Beagle',
                'sexo': 'macho',
                'fecha_nacimiento': date(2020, 9, 14),
                'peso_actual': Decimal('11.5'),
                'esterilizado': 'si',
                'estado_vacunacion': 'completo',
                'desparasitacion': 'actualizado',
                'comportamiento_consulta': 'tranquilo'
            },
            {
                'nombre': 'Nina',
                'tipo': 'gato',
                'raza': 'Maine Coon',
                'sexo': 'hembra',
                'fecha_nacimiento': date(2019, 11, 8),
                'peso_actual': Decimal('6.2'),
                'esterilizado': 'si',
                'estado_vacunacion': 'completo',
                'desparasitacion': 'actualizado',
                'comportamiento_consulta': 'tranquilo'
            },
            {
                'nombre': 'Bruno',
                'tipo': 'perro',
                'raza': 'Pastor Alemán',
                'sexo': 'macho',
                'fecha_nacimiento': date(2021, 7, 25),
                'peso_actual': Decimal('32.1'),
                'esterilizado': 'no',
                'estado_vacunacion': 'parcial',
                'desparasitacion': 'pendiente',
                'comportamiento_consulta': 'agresivo'
            },
            {
                'nombre': 'Lola',
                'tipo': 'roedor',
                'raza': 'Cobaya',
                'sexo': 'hembra',
                'fecha_nacimiento': date(2023, 4, 12),
                'peso_actual': Decimal('0.9'),
                'esterilizado': 'desconocido',
                'estado_vacunacion': 'desconocido',
                'desparasitacion': 'desconocido',
                'comportamiento_consulta': 'asustadizo'
            }
        ]

        for i, pet_data in enumerate(pets_data):
            client = clients[i % len(clients)]
            pet, created = Mascota.objects.get_or_create(
                nombre=pet_data['nombre'],
                cliente=client,
                defaults=pet_data
            )
            if created:
                self.stdout.write(f'Created pet: {pet.nombre} for {client.usuario.username}')

    def create_appointments(self):
        pets = list(Mascota.objects.all())
        if not pets:
            self.stdout.write(self.style.WARNING('No pets found, skipping appointment creation'))
            return

        appointments_data = [
            {
                'tipo': 'consulta_general',
                'motivo': 'Revisión anual',
                'prioridad': 'normal',
                'estado': 'completada',
                'duracion_estimada': 30
            },
            {
                'tipo': 'vacunacion',
                'motivo': 'Vacuna antirrábica',
                'prioridad': 'normal',
                'estado': 'programada',
                'duracion_estimada': 15
            },
            {
                'tipo': 'desparasitacion',
                'motivo': 'Desparasitación interna',
                'prioridad': 'normal',
                'estado': 'confirmada',
                'duracion_estimada': 20
            },
            {
                'tipo': 'urgencia',
                'motivo': 'Vómitos y diarrea',
                'prioridad': 'urgente',
                'estado': 'completada',
                'duracion_estimada': 45
            },
            {
                'tipo': 'odontologia',
                'motivo': 'Limpieza dental',
                'prioridad': 'normal',
                'estado': 'programada',
                'duracion_estimada': 60
            },
            {
                'tipo': 'cirugia',
                'motivo': 'Esterilización',
                'prioridad': 'normal',
                'estado': 'confirmada',
                'duracion_estimada': 90
            },
            {
                'tipo': 'analisis',
                'motivo': 'Análisis de sangre rutinario',
                'prioridad': 'normal',
                'estado': 'completada',
                'duracion_estimada': 30
            },
            {
                'tipo': 'control',
                'motivo': 'Control de peso post-dieta',
                'prioridad': 'normal',
                'estado': 'programada',
                'duracion_estimada': 20
            },
            {
                'tipo': 'estetica',
                'motivo': 'Baño y corte de uñas',
                'prioridad': 'normal',
                'estado': 'confirmada',
                'duracion_estimada': 45
            },
            {
                'tipo': 'comportamiento',
                'motivo': 'Problemas de ansiedad',
                'prioridad': 'normal',
                'estado': 'programada',
                'duracion_estimada': 45
            }
        ]

        for i, appointment_data in enumerate(appointments_data):
            pet = pets[i % len(pets)]
            # Create appointment date (some in past, some in future)
            if appointment_data['estado'] == 'completada':
                fecha = timezone.now() - timedelta(days=random.randint(1, 30))
            else:
                fecha = timezone.now() + timedelta(days=random.randint(1, 14))

            appointment, created = Cita.objects.get_or_create(
                mascota=pet,
                fecha=fecha,
                defaults={
                    **appointment_data,
                    'veterinario': f'Dr. {random.choice(["Rodríguez", "Martínez", "García", "López", "Hernández"])}',
                    'sala': f'Sala {random.randint(1, 5)}'
                }
            )
            if created:
                self.stdout.write(f'Created appointment for {pet.nombre}: {appointment.get_tipo_display()}')

    def create_products(self):
        # Create categories
        categories_data = [
            {'nombre': 'Alimentos', 'descripcion': 'Alimentos para mascotas'},
            {'nombre': 'Medicamentos', 'descripcion': 'Medicamentos veterinarios'},
            {'nombre': 'Accesorios', 'descripcion': 'Accesorios y juguetes'},
            {'nombre': 'Higiene', 'descripcion': 'Productos de higiene y cuidado'}
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.nombre}')

        # Create products
        products_data = [
            {
                'nombre': 'Royal Canin Medium Adult',
                'descripcion': 'Alimento premium para perros adultos de tamaño mediano',
                'precio': Decimal('85.000'),
                'categoria': categories[0],
                'tipo': 'alimento',
                'stock': 50
            },
            {
                'nombre': 'Purina Pro Plan Urinary',
                'descripcion': 'Alimento especializado para problemas urinarios en gatos',
                'precio': Decimal('95.000'),
                'categoria': categories[0],
                'tipo': 'alimento',
                'stock': 30
            },
            {
                'nombre': 'Hills Science Diet Puppy',
                'descripcion': 'Alimento para cachorros de todas las razas',
                'precio': Decimal('78.000'),
                'categoria': categories[0],
                'tipo': 'alimento',
                'stock': 40
            },
            {
                'nombre': 'Vitapet Multivitamínico',
                'descripcion': 'Suplemento vitamínico completo para perros y gatos',
                'precio': Decimal('45.000'),
                'categoria': categories[1],
                'tipo': 'medicamento',
                'stock': 100
            },
            {
                'nombre': 'Collar Antipulgas',
                'descripcion': 'Collar repelente de pulgas y garrapatas',
                'precio': Decimal('25.000'),
                'categoria': categories[1],
                'tipo': 'medicamento',
                'stock': 75
            },
            {
                'nombre': 'Champú Hidratante para Perros',
                'descripcion': 'Champú suave para piel sensible',
                'precio': Decimal('18.000'),
                'categoria': categories[3],
                'tipo': 'higiene',
                'stock': 60
            },
            {
                'nombre': 'Correa Extensible 5m',
                'descripcion': 'Correa retráctil de alta calidad',
                'precio': Decimal('35.000'),
                'categoria': categories[2],
                'tipo': 'accesorio',
                'stock': 25
            },
            {
                'nombre': 'Comedero Doble Acero Inoxidable',
                'descripcion': 'Comedero doble resistente y fácil de limpiar',
                'precio': Decimal('28.000'),
                'categoria': categories[2],
                'tipo': 'accesorio',
                'stock': 40
            },
            {
                'nombre': 'Juguete Interactivo Dispensador',
                'descripcion': 'Juguete que libera premios para mantener entretenido a tu perro',
                'precio': Decimal('22.000'),
                'categoria': categories[2],
                'tipo': 'juguete',
                'stock': 35
            },
            {
                'nombre': 'Pelota con Sonido para Perros',
                'descripcion': 'Pelota que hace ruido para atraer la atención',
                'precio': Decimal('12.000'),
                'categoria': categories[2],
                'tipo': 'juguete',
                'stock': 80
            },
            {
                'nombre': 'Arenero Cubierto para Gatos',
                'descripcion': 'Arenero con tapa para mayor higiene',
                'precio': Decimal('45.000'),
                'categoria': categories[2],
                'tipo': 'accesorio',
                'stock': 20
            },
            {
                'nombre': 'Snacks Dentales para Perros',
                'descripcion': 'Premios que ayudan a limpiar los dientes',
                'precio': Decimal('15.000'),
                'categoria': categories[0],
                'tipo': 'alimento',
                'stock': 90
            },
            {
                'nombre': 'Transportín para Gatos',
                'descripcion': 'Jaula de transporte segura y cómoda',
                'precio': Decimal('85.000'),
                'categoria': categories[2],
                'tipo': 'accesorio',
                'stock': 15
            },
            {
                'nombre': 'Rascador para Gatos 3 Niveles',
                'descripcion': 'Rascador con múltiples plataformas',
                'precio': Decimal('65.000'),
                'categoria': categories[2],
                'tipo': 'accesorio',
                'stock': 12
            },
            {
                'nombre': 'Cepillo para Pelo de Perros',
                'descripcion': 'Cepillo deslanador profesional',
                'precio': Decimal('20.000'),
                'categoria': categories[3],
                'tipo': 'higiene',
                'stock': 55
            },
            {
                'nombre': 'Shampoo Antipulgas para Perros',
                'descripcion': 'Shampoo que elimina pulgas y garrapatas',
                'precio': Decimal('28.000'),
                'categoria': categories[1],
                'tipo': 'medicamento',
                'stock': 45
            },
            {
                'nombre': 'Cama Ortodédica para Perros',
                'descripcion': 'Cama ergonómica para perros mayores',
                'precio': Decimal('120.000'),
                'categoria': categories[2],
                'tipo': 'accesorio',
                'stock': 8
            },
            {
                'nombre': 'Pienso para Gatos Esterilizados',
                'descripcion': 'Alimento específico para gatos castrados',
                'precio': Decimal('72.000'),
                'categoria': categories[0],
                'tipo': 'alimento',
                'stock': 35
            },
            {
                'nombre': 'Juguete Láser para Gatos',
                'descripcion': 'Puntero láser para ejercicio y diversión',
                'precio': Decimal('8.000'),
                'categoria': categories[2],
                'tipo': 'juguete',
                'stock': 70
            },
            {
                'nombre': 'Bolsas Higiénicas para Perros',
                'descripcion': 'Paquete de 100 bolsas biodegradables',
                'precio': Decimal('5.000'),
                'categoria': categories[3],
                'tipo': 'higiene',
                'stock': 150
            }
        ]

        for product_data in products_data:
            product, created = Producto.objects.get_or_create(
                nombre=product_data['nombre'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'Created product: {product.nombre}')