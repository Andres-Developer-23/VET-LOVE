"""
Script para poblar la base de datos con datos de prueba
Ejecutar con: python populate_db.py
"""

import os
import django
import sys
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings')
django.setup()

from django.contrib.auth.models import User
from clientes.models import Cliente
from mascotas.models import Mascota
from citas.models import Cita
from tienda.models import Categoria, Producto


def crear_usuarios_y_clientes():
    """Crear 10 usuarios con sus perfiles de cliente"""
    print("Creando usuarios y clientes...")
    
    usuarios_data = [
        {'username': 'juan.perez', 'first_name': 'Juan', 'last_name': 'Pérez', 'email': 'juan.perez@email.com'},
        {'username': 'maria.garcia', 'first_name': 'María', 'last_name': 'García', 'email': 'maria.garcia@email.com'},
        {'username': 'carlos.rodriguez', 'first_name': 'Carlos', 'last_name': 'Rodríguez', 'email': 'carlos.rodriguez@email.com'},
        {'username': 'ana.martinez', 'first_name': 'Ana', 'last_name': 'Martínez', 'email': 'ana.martinez@email.com'},
        {'username': 'luis.lopez', 'first_name': 'Luis', 'last_name': 'López', 'email': 'luis.lopez@email.com'},
        {'username': 'sofia.sanchez', 'first_name': 'Sofía', 'last_name': 'Sánchez', 'email': 'sofia.sanchez@email.com'},
        {'username': 'diego.gomez', 'first_name': 'Diego', 'last_name': 'Gómez', 'email': 'diego.gomez@email.com'},
        {'username': 'laura.torres', 'first_name': 'Laura', 'last_name': 'Torres', 'email': 'laura.torres@email.com'},
        {'username': 'andres.ramirez', 'first_name': 'Andrés', 'last_name': 'Ramírez', 'email': 'andres.ramirez@email.com'},
        {'username': 'valentina.castro', 'first_name': 'Valentina', 'last_name': 'Castro', 'email': 'valentina.castro@email.com'},
    ]
    
    direcciones = [
        'Calle 72 #10-34, Bogotá',
        'Carrera 15 #85-20, Bogotá',
        'Avenida 19 #120-45, Bogotá',
        'Calle 127 #54-12, Bogotá',
        'Carrera 7 #32-16, Bogotá',
        'Transversal 93 #47-28, Bogotá',
        'Diagonal 40 Bis #20-55, Bogotá',
        'Calle 100 #18A-30, Bogotá',
        'Carrera 50 #26-45, Bogotá',
        'Avenida 68 #75-80, Bogotá',
    ]
    
    preferencias = ['email', 'sms', 'whatsapp']
    
    clientes = []
    for i, user_data in enumerate(usuarios_data):
        # Crear usuario
        usuario = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password='password123',
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        
        # Crear cliente
        cliente = Cliente.objects.create(
            usuario=usuario,
            telefono=f'301{random.randint(1000000, 9999999)}',
            direccion=direcciones[i],
            preferencias_comunicacion=random.choice(preferencias)
        )
        clientes.append(cliente)
        print(f"  ✓ Cliente creado: {cliente}")
    
    return clientes


def crear_mascotas(clientes):
    """Crear 10 mascotas por cada cliente (100 mascotas en total)"""
    print("\nCreando mascotas...")
    
    nombres_perros = ['Max', 'Luna', 'Rocky', 'Bella', 'Zeus', 'Lola', 'Bruno', 'Coco', 'Toby', 'Mia']
    nombres_gatos = ['Michi', 'Garfield', 'Salem', 'Felix', 'Whiskers', 'Simba', 'Nala', 'Tiger', 'Shadow', 'Luna']
    
    razas_perros = ['Labrador', 'Golden Retriever', 'Pastor Alemán', 'Bulldog', 'Poodle', 'Chihuahua', 'Beagle', 'Husky', 'Pitbull', 'Mestizo']
    razas_gatos = ['Siamés', 'Persa', 'Maine Coon', 'Angora', 'Bengalí', 'Ragdoll', 'Británico', 'Esfinge', 'Mestizo', 'Común Europeo']
    
    colores = ['Negro', 'Blanco', 'Café', 'Gris', 'Dorado', 'Tricolor', 'Atigrado', 'Moteado']
    
    mascotas = []
    for cliente in clientes:
        for i in range(10):
            tipo = random.choice(['perro', 'gato'])
            
            if tipo == 'perro':
                nombre = nombres_perros[i]
                raza = random.choice(razas_perros)
            else:
                nombre = nombres_gatos[i]
                raza = random.choice(razas_gatos)
            
            # Fecha de nacimiento entre 1 mes y 15 años atrás
            dias_atras = random.randint(30, 5475)
            fecha_nacimiento = datetime.now().date() - timedelta(days=dias_atras)
            
            mascota = Mascota.objects.create(
                nombre=nombre,
                tipo=tipo,
                raza=raza,
                sexo=random.choice(['macho', 'hembra']),
                fecha_nacimiento=fecha_nacimiento,
                cliente=cliente,
                microchip=f'MX{random.randint(100000000000, 999999999999)}' if random.random() > 0.3 else '',
                alergias_conocidas='Ninguna' if random.random() > 0.2 else random.choice(['Polen', 'Polvo', 'Ciertos alimentos']),
                alergias_tipo='' if random.random() > 0.2 else random.choice(['Ambiental', 'Alimentaria', 'Medicamentos']),
                enfermedades_cronicas='' if random.random() > 0.15 else random.choice(['Diabetes', 'Artritis', 'Problemas cardíacos']),
                esterilizado=random.choice(['si', 'no', 'desconocido']),
                peso_actual=Decimal(str(round(random.uniform(2.0, 35.0), 2))),
                medicacion_actual='' if random.random() > 0.2 else 'Suplementos vitamínicos',
                comportamiento_consulta=random.choice(['tranquilo', 'nervioso', 'asustadizo']),
                veterinario_habitual='Dr. García' if random.random() > 0.5 else 'Dra. Rodríguez',
                telefono_emergencia=f'301{random.randint(1000000, 9999999)}',
                estado_vacunacion=random.choice(['completo', 'parcial', 'desconocido']),
                fecha_ultima_vacuna=datetime.now().date() - timedelta(days=random.randint(30, 365)) if random.random() > 0.2 else None,
                desparasitacion=random.choice(['actualizado', 'pendiente', 'desconocido']),
                fecha_ultima_desparasitacion=datetime.now().date() - timedelta(days=random.randint(30, 180)) if random.random() > 0.3 else None,
                cirugias_previas='' if random.random() > 0.2 else random.choice(['Esterilización', 'Fractura', 'Tumor']),
                tipo_alimentacion=random.choice(['Concentrado', 'BARF', 'Mixta', 'Casera']),
                frecuencia_alimentacion=random.choice(['2 veces al día', '3 veces al día', '1 vez al día']),
                comportamiento=random.choice(['Activo', 'Tranquilo', 'Juguetón', 'Tímido']),
                permite_manejo=random.choice(['Sí, sin problemas', 'Con precaución', 'Solo con el dueño']),
                caracteristicas=f'Mascota {tipo} de raza {raza}',
                color=random.choice(colores)
            )
            mascotas.append(mascota)
        
        print(f"  ✓ 10 mascotas creadas para {cliente}")
    
    return mascotas


def crear_citas(mascotas):
    """Crear 10 citas distribuidas entre las mascotas"""
    print("\nCreando citas...")
    
    tipos_cita = ['consulta_general', 'vacunacion', 'desparasitacion', 'control', 'urgencia']
    veterinarios = ['Dr. García Martínez', 'Dra. Rodríguez Silva', 'Dr. López Torres', 'Dra. Sánchez Ruiz']
    salas = ['Consultorio 1', 'Consultorio 2', 'Consultorio 3', 'Sala de Cirugía', 'Sala de Urgencias']
    
    motivos = [
        'Control de rutina y revisión general',
        'Aplicación de vacunas pendientes',
        'Desparasitación programada',
        'Consulta por vómito y diarrea',
        'Revisión de herida en pata',
        'Control de peso y nutrición',
        'Consulta dermatológica por picazón',
        'Chequeo post-cirugía',
        'Control de enfermedad crónica',
        'Vacunación antirrábica anual'
    ]
    
    sintomas = [
        'Sin síntomas aparentes',
        'Vómito ocasional',
        'Pérdida de apetito',
        'Picazón en la piel',
        'Cojera leve',
        'Tos seca',
        'Ojos llorosos',
        'Letargo',
        'Diarrea',
        'Secreción nasal'
    ]
    
    citas = []
    mascotas_seleccionadas = random.sample(mascotas, 10)
    
    for i, mascota in enumerate(mascotas_seleccionadas):
        # Fecha entre hoy y 30 días adelante
        dias_adelante = random.randint(1, 30)
        hora = random.randint(8, 17)
        minutos = random.choice([0, 30])
        fecha_cita = datetime.now() + timedelta(days=dias_adelante)
        fecha_cita = fecha_cita.replace(hour=hora, minute=minutos, second=0, microsecond=0)
        
        tipo_cita = random.choice(tipos_cita)
        
        cita = Cita.objects.create(
            mascota=mascota,
            fecha=fecha_cita,
            tipo=tipo_cita,
            prioridad='urgente' if tipo_cita == 'urgencia' else random.choice(['normal', 'normal', 'normal', 'urgente']),
            motivo=motivos[i],
            sintomas=sintomas[i] if random.random() > 0.3 else '',
            estado=random.choice(['programada', 'confirmada']),
            veterinario=random.choice(veterinarios),
            duracion_estimada=random.choice([30, 45, 60]),
            sala=random.choice(salas),
            notas=f'Cita programada para {tipo_cita.replace("_", " ")}',
            antecedentes=mascota.enfermedades_cronicas if mascota.enfermedades_cronicas else 'Sin antecedentes relevantes',
            medicamentos_actuales=mascota.medicacion_actual if mascota.medicacion_actual else 'Ninguno',
            alergias=mascota.alergias_conocidas if mascota.alergias_conocidas else 'Sin alergias conocidas',
            recordatorio_enviado=random.choice([True, False]),
            confirmada_por_cliente=random.choice([True, False])
        )
        citas.append(cita)
        print(f"  ✓ Cita creada: {cita}")
    
    return citas


def crear_categorias_y_productos():
    """Crear categorías y 20 productos"""
    print("\nCreando categorías...")
    
    categorias_data = [
        {'nombre': 'Alimentos para Perros', 'descripcion': 'Alimentos balanceados y premium para perros de todas las edades'},
        {'nombre': 'Alimentos para Gatos', 'descripcion': 'Alimentos especializados para gatos'},
        {'nombre': 'Medicamentos', 'descripcion': 'Medicamentos veterinarios y suplementos'},
        {'nombre': 'Accesorios', 'descripcion': 'Collares, correas, camas y más'},
        {'nombre': 'Higiene y Cuidado', 'descripcion': 'Productos de higiene y cuidado personal para mascotas'},
        {'nombre': 'Juguetes', 'descripcion': 'Juguetes para entretenimiento y ejercicio'},
    ]
    
    categorias = []
    for cat_data in categorias_data:
        categoria = Categoria.objects.create(**cat_data)
        categorias.append(categoria)
        print(f"  ✓ Categoría creada: {categoria.nombre}")
    
    print("\nCreando productos...")
    
    productos_data = [
        # Alimentos
        {'nombre': 'Dog Chow Adultos 15kg', 'tipo': 'alimento', 'categoria_idx': 0, 'precio': '125000', 'stock': 50, 'descripcion': 'Alimento balanceado para perros adultos de todas las razas'},
        {'nombre': 'Chunky Cachorro 10kg', 'tipo': 'alimento', 'categoria_idx': 0, 'precio': '98000', 'stock': 35, 'descripcion': 'Alimento premium para cachorros en crecimiento'},
        {'nombre': 'Royal Canin Adulto 7.5kg', 'tipo': 'alimento', 'categoria_idx': 0, 'precio': '185000', 'stock': 25, 'descripcion': 'Alimento premium para perros adultos'},
        {'nombre': 'Gatsy Adultos 10kg', 'tipo': 'alimento', 'categoria_idx': 1, 'precio': '95000', 'stock': 40, 'descripcion': 'Alimento completo para gatos adultos'},
        {'nombre': 'Whiskas Húmedo Pouch 85g', 'tipo': 'alimento', 'categoria_idx': 1, 'precio': '3500', 'stock': 200, 'descripcion': 'Alimento húmedo para gatos, sabor pescado'},
        
        # Medicamentos
        {'nombre': 'Bravecto 20-40kg', 'tipo': 'medicamento', 'categoria_idx': 2, 'precio': '89000', 'stock': 30, 'descripcion': 'Antipulgas y garrapatas de larga duración'},
        {'nombre': 'Nexgard Spectra M', 'tipo': 'medicamento', 'categoria_idx': 2, 'precio': '75000', 'stock': 45, 'descripcion': 'Protección contra pulgas, garrapatas y parásitos internos'},
        {'nombre': 'Vitalkan Multivitamínico', 'tipo': 'medicamento', 'categoria_idx': 2, 'precio': '35000', 'stock': 60, 'descripcion': 'Suplemento multivitamínico para mascotas'},
        {'nombre': 'Revolution Plus Gatos', 'tipo': 'medicamento', 'categoria_idx': 2, 'precio': '65000', 'stock': 38, 'descripcion': 'Protección integral para gatos'},
        
        # Accesorios
        {'nombre': 'Collar Ajustable Mediano', 'tipo': 'accesorio', 'categoria_idx': 3, 'precio': '25000', 'stock': 75, 'descripcion': 'Collar ajustable de nylon resistente'},
        {'nombre': 'Correa Retráctil 5m', 'tipo': 'accesorio', 'categoria_idx': 3, 'precio': '45000', 'stock': 50, 'descripcion': 'Correa retráctil para paseos cómodos'},
        {'nombre': 'Cama Acolchada Grande', 'tipo': 'accesorio', 'categoria_idx': 3, 'precio': '120000', 'stock': 20, 'descripcion': 'Cama acolchada lavable para perros grandes'},
        {'nombre': 'Plato Acero Inoxidable', 'tipo': 'accesorio', 'categoria_idx': 3, 'precio': '18000', 'stock': 100, 'descripcion': 'Plato antideslizante de acero inoxidable'},
        
        # Higiene
        {'nombre': 'Shampoo Antipulgas 500ml', 'tipo': 'higiene', 'categoria_idx': 4, 'precio': '28000', 'stock': 65, 'descripcion': 'Shampoo medicado antipulgas y garrapatas'},
        {'nombre': 'Cepillo Removedor de Pelo', 'tipo': 'higiene', 'categoria_idx': 4, 'precio': '32000', 'stock': 55, 'descripcion': 'Cepillo profesional para remoción de pelo muerto'},
        {'nombre': 'Toallas Húmedas Pack x30', 'tipo': 'higiene', 'categoria_idx': 4, 'precio': '15000', 'stock': 80, 'descripcion': 'Toallas húmedas hipoalergénicas'},
        
        # Juguetes
        {'nombre': 'Pelota Kong Mediana', 'tipo': 'juguete', 'categoria_idx': 5, 'precio': '35000', 'stock': 70, 'descripcion': 'Pelota resistente para perros medianos'},
        {'nombre': 'Ratón con Catnip', 'tipo': 'juguete', 'categoria_idx': 5, 'precio': '8000', 'stock': 150, 'descripcion': 'Juguete para gatos con hierba gatera'},
        {'nombre': 'Cuerda Dental 3 Nudos', 'tipo': 'juguete', 'categoria_idx': 5, 'precio': '22000', 'stock': 90, 'descripcion': 'Juguete de cuerda para limpieza dental'},
        {'nombre': 'Rascador Poste Gatos', 'tipo': 'juguete', 'categoria_idx': 5, 'precio': '85000', 'stock': 25, 'descripcion': 'Rascador vertical con juguetes colgantes'},
    ]
    
    productos = []
    for prod_data in productos_data:
        categoria = categorias[prod_data.pop('categoria_idx')]
        precio = Decimal(prod_data.pop('precio'))
        
        # Algunos productos con descuento
        precio_descuento = None
        if random.random() > 0.7:
            descuento = random.uniform(0.1, 0.3)
            precio_descuento = precio * Decimal(str(1 - descuento))
        
        producto = Producto.objects.create(
            categoria=categoria,
            precio=precio,
            precio_descuento=precio_descuento,
            stock_minimo=5,
            activo=True,
            destacado=random.choice([True, False]),
            **prod_data
        )
        productos.append(producto)
        descuento_info = f" (Oferta: ${precio_descuento})" if precio_descuento else ""
        print(f"  ✓ Producto creado: {producto.nombre}{descuento_info}")
    
    return productos


def crear_usuarios_adicionales():
    """Crear 5 cuentas de usuarios adicionales con toda su información"""
    print("\nCreando 5 usuarios adicionales con perfiles completos...")
    
    usuarios_extra = [
        {
            'username': 'pedro.morales',
            'first_name': 'Pedro',
            'last_name': 'Morales',
            'email': 'pedro.morales@email.com',
            'telefono': '3201234567',
            'direccion': 'Calle 45 #12-34, Bogotá',
            'preferencias': 'email'
        },
        {
            'username': 'carolina.diaz',
            'first_name': 'Carolina',
            'last_name': 'Díaz',
            'email': 'carolina.diaz@email.com',
            'telefono': '3109876543',
            'direccion': 'Carrera 30 #67-89, Bogotá',
            'preferencias': 'whatsapp'
        },
        {
            'username': 'ricardo.vera',
            'first_name': 'Ricardo',
            'last_name': 'Vera',
            'email': 'ricardo.vera@email.com',
            'telefono': '3155555555',
            'direccion': 'Avenida 68 #45-12, Bogotá',
            'preferencias': 'sms'
        },
        {
            'username': 'natalia.rojas',
            'first_name': 'Natalia',
            'last_name': 'Rojas',
            'email': 'natalia.rojas@email.com',
            'telefono': '3187654321',
            'direccion': 'Transversal 25 #34-56, Bogotá',
            'preferencias': 'email'
        },
        {
            'username': 'fernando.silva',
            'first_name': 'Fernando',
            'last_name': 'Silva',
            'email': 'fernando.silva@email.com',
            'telefono': '3143216789',
            'direccion': 'Diagonal 80 #90-12, Bogotá',
            'preferencias': 'whatsapp'
        }
    ]
    
    for user_data in usuarios_extra:
        usuario = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password='password123',
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        
        cliente = Cliente.objects.create(
            usuario=usuario,
            telefono=user_data['telefono'],
            direccion=user_data['direccion'],
            preferencias_comunicacion=user_data['preferencias']
        )
        
        print(f"  ✓ Usuario y cliente creado: {cliente} ({usuario.email})")


def main():
    """Función principal"""
    print("="*60)
    print("INICIANDO POBLACIÓN DE BASE DE DATOS")
    print("="*60)

    try:
        # Paso 1: Crear usuarios y clientes
        clientes = crear_usuarios_y_clientes()

        # Paso 2: Crear mascotas
        mascotas = crear_mascotas(clientes)

        # Paso 3: Crear citas
        citas = crear_citas(mascotas)

        # Paso 4: Crear categorías y productos
        productos = crear_categorias_y_productos()

        # Paso 5: Crear usuarios adicionales
        crear_usuarios_adicionales()

        print("\n" + "="*60)
        print("RESUMEN DE DATOS CREADOS:")
        print("="*60)
        print(f"✓ {User.objects.count()} usuarios")
        print(f"✓ {Cliente.objects.count()} clientes")
        print(f"✓ {Mascota.objects.count()} mascotas")
        print(f"✓ {Cita.objects.count()} citas")
        print(f"✓ {Categoria.objects.count()} categorías")
        print(f"✓ {Producto.objects.count()} productos")
        print("="*60)
        print("✅ BASE DE DATOS POBLADA EXITOSAMENTE")
        print("="*60)
        print("\nCredenciales de acceso:")
        print("  Usuario: juan.perez")
        print("  Contraseña: password123")
        print("\n  (Todos los usuarios tienen la contraseña: password123)")

    except Exception as e:
        print(f"\n❌ Error durante la población: {str(e)}")
        print("Continuando con la ejecución para asegurar que la aplicación funcione...")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()