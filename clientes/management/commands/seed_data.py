import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from clientes.models import Cliente, Direccion, Especie, Raza, Mascota
from tienda.models import (
    Categoria, Proveedor, Producto, Cupon, Carrito, CarritoItem,
    Pedido, DetallePedido, Pago, Resena
)
from veterinaria.models import (
    Veterinario, Servicio, Cita, HistorialMedico, Vacuna, Refugio, Adopcion
)

fake = Faker('es_MX')


class Command(BaseCommand):
    help = "Carga datos de prueba realistas para las 22 tablas del proyecto"

    def handle(self, *args, **options):
        self.stdout.write("Cargando datos...")

        especies = self.crear_especies()
        razas = self.crear_razas(especies)
        clientes = self.crear_clientes()
        direcciones = self.crear_direcciones(clientes)
        mascotas = self.crear_mascotas(clientes, especies, razas)

        categorias = self.crear_categorias()
        proveedores = self.crear_proveedores()
        productos = self.crear_productos(categorias, proveedores)
        cupones = self.crear_cupones()
        carritos = self.crear_carritos(clientes)
        self.crear_carrito_items(carritos, productos)
        pedidos = self.crear_pedidos(clientes, direcciones, cupones)
        self.crear_detalle_pedido(pedidos, productos)
        self.crear_pagos(pedidos)
        self.crear_resenas(clientes, productos)

        veterinarios = self.crear_veterinarios()
        servicios = self.crear_servicios()
        citas = self.crear_citas(mascotas, veterinarios, servicios)
        self.crear_historial_medico(mascotas, citas, veterinarios)
        self.crear_vacunas(mascotas, veterinarios)
        refugios = self.crear_refugios()
        self.crear_adopciones(mascotas, refugios, clientes)

        self.stdout.write(self.style.SUCCESS("¡Listo! Datos cargados en las 22 tablas."))

    # ---------------- clientes app ----------------

    def crear_especies(self):
        nombres = ["Perro", "Gato", "Ave", "Conejo", "Hámster", "Tortuga", "Pez",
                   "Cuyo", "Hurón", "Chinchilla", "Iguana", "Serpiente", "Loro",
                   "Erizo", "Tarántula"]
        especies = [Especie.objects.get_or_create(nombre=n)[0] for n in nombres]
        self.stdout.write(f"  {len(especies)} especies")
        return especies

    def crear_razas(self, especies):
        por_especie = {
            "Perro": ["Labrador Retriever", "Bulldog Francés", "Pastor Alemán", "Poodle", "Chihuahua"],
            "Gato": ["Siamés", "Persa", "Maine Coon", "Bengalí"],
            "Ave": ["Canario", "Periquito Australiano"],
            "Conejo": ["Holland Lop", "Rex"],
            "Hámster": ["Sirio", "Ruso"],
            "Tortuga": ["Orejas Rojas"],
            "Pez": ["Betta", "Goldfish"],
        }
        edict = {e.nombre: e for e in especies}
        razas = []
        for esp_nombre, lista in por_especie.items():
            for nombre in lista:
                raza, _ = Raza.objects.get_or_create(
                    especie=edict[esp_nombre], nombre=nombre,
                    defaults={"tamano_promedio": random.choice(["Pequeño", "Mediano", "Grande"]),
                              "esperanza_vida_anios": random.randint(2, 18)}
                )
                razas.append(raza)
        self.stdout.write(f"  {len(razas)} razas")
        return razas

    def crear_clientes(self):
        clientes = []
        for _ in range(15):
            c = Cliente.objects.create(
                nombre=fake.first_name(), apellido=fake.last_name(),
                email=fake.unique.email(), password_hash=fake.sha256(),
                telefono=fake.msisdn()[:15],
                dni=fake.unique.bothify(text='??######', letters='ABCDEFGHIJ'),
                fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=70),
                genero=random.choice(['M', 'F', 'O']), activo=True,
            )
            clientes.append(c)
        self.stdout.write(f"  {len(clientes)} clientes")
        return clientes

    def crear_direcciones(self, clientes):
        direcciones = []
        for cliente in clientes:
            for _ in range(random.choice([1, 1, 2])):
                d = Direccion.objects.create(
                    cliente=cliente, calle=fake.street_name(),
                    numero=str(fake.building_number()), colonia=fake.street_prefix(),
                    ciudad=fake.city(), estado=fake.state(), codigo_postal=fake.postcode(),
                    pais="México", tipo=random.choice(['envio', 'facturacion']),
                    principal=(len(direcciones) == 0),
                )
                direcciones.append(d)
        self.stdout.write(f"  {len(direcciones)} direcciones")
        return direcciones

    def crear_mascotas(self, clientes, especies, razas):
        nombres_mascotas = ["Max", "Luna", "Rocky", "Bella", "Simba", "Nala", "Toby",
                             "Coco", "Rex", "Mia", "Thor", "Kira", "Milo", "Lola", "Bruno",
                             "Nina", "Zeus", "Chispa", "Firulais", "Canela"]
        mascotas = []
        for cliente in clientes:
            for _ in range(random.choice([1, 1, 2])):
                especie = random.choice(especies)
                razas_especie = [r for r in razas if r.especie == especie]
                raza = random.choice(razas_especie) if razas_especie else None
                m = Mascota.objects.create(
                    cliente=cliente, especie=especie, raza=raza,
                    nombre=random.choice(nombres_mascotas),
                    fecha_nacimiento=fake.date_between(start_date='-10y', end_date='-1M'),
                    peso=round(random.uniform(0.5, 40), 2),
                    color=random.choice(["Café", "Negro", "Blanco", "Gris", "Dorado", "Manchado"]),
                    sexo=random.choice(['M', 'H']),
                    esterilizado=random.choice([True, False]),
                    notas=fake.sentence(nb_words=8),
                )
                mascotas.append(m)
        self.stdout.write(f"  {len(mascotas)} mascotas")
        return mascotas

    # ---------------- tienda app ----------------

    def crear_categorias(self):
        nombres = ["Alimento para Perros", "Alimento para Gatos", "Juguetes", "Accesorios",
                   "Higiene y Cuidado", "Camas y Descanso", "Correas y Collares",
                   "Transportadoras", "Snacks y Premios", "Vitaminas y Suplementos",
                   "Ropa para Mascotas", "Acuarios y Peceras", "Jaulas para Aves",
                   "Arena Sanitaria", "Medicamentos"]
        categorias = [Categoria.objects.get_or_create(nombre=n)[0] for n in nombres]
        self.stdout.write(f"  {len(categorias)} categorías")
        return categorias

    def crear_proveedores(self):
        proveedores = []
        for _ in range(15):
            p = Proveedor.objects.create(
                nombre=fake.company(), contacto=fake.name(),
                telefono=fake.msisdn()[:15], email=fake.company_email(),
                direccion=fake.address()[:200], activo=True,
            )
            proveedores.append(p)
        self.stdout.write(f"  {len(proveedores)} proveedores")
        return proveedores

    def crear_productos(self, categorias, proveedores):
        base_nombres = ["Croquetas Premium", "Juguete Interactivo", "Cama Ortopédica",
                         "Collar Ajustable", "Shampoo Antipulgas", "Snack Dental",
                         "Transportadora Mediana", "Arena Aglomerante", "Vitaminas Multi",
                         "Correa Retráctil", "Rascador para Gatos", "Pecera 20L",
                         "Jaula para Periquito", "Suéter para Perro", "Cepillo Deslanador",
                         "Comedero Automático", "Bebedero Fuente", "Antipulgas Pipeta",
                         "Peluche Resistente", "Bolsa de Arena Sanitaria"]
        productos = []
        for i, nombre in enumerate(base_nombres):
            p = Producto.objects.create(
                categoria=random.choice(categorias), proveedor=random.choice(proveedores),
                nombre=nombre, descripcion=fake.sentence(nb_words=10),
                sku=f"SKU-{1000 + i}", marca=fake.company(),
                precio=round(random.uniform(80, 1500), 2),
                costo=round(random.uniform(40, 900), 2),
                stock=random.randint(5, 200),
                peso=round(random.uniform(0.1, 15), 2), activo=True,
            )
            productos.append(p)
        self.stdout.write(f"  {len(productos)} productos")
        return productos

    def crear_cupones(self):
        cupones = []
        for i in range(15):
            inicio = fake.date_between(start_date='-60d', end_date='today')
            c = Cupon.objects.create(
                codigo=f"MASCOTA{i+1}{random.randint(10,99)}",
                descripcion=fake.sentence(nb_words=6),
                tipo_descuento=random.choice(['porcentaje', 'monto_fijo']),
                valor=round(random.uniform(5, 30), 2) if random.random() > 0.5 else round(random.uniform(50, 300), 2),
                fecha_inicio=inicio, fecha_fin=inicio + timedelta(days=random.randint(15, 90)),
                usos_maximos=random.randint(10, 100), usos_actuales=random.randint(0, 9),
                activo=True,
            )
            cupones.append(c)
        self.stdout.write(f"  {len(cupones)} cupones")
        return cupones

    def crear_carritos(self, clientes):
        carritos = [Carrito.objects.create(cliente=c, estado=random.choice(['activo', 'abandonado', 'convertido']))
                    for c in clientes]
        self.stdout.write(f"  {len(carritos)} carritos")
        return carritos

    def crear_carrito_items(self, carritos, productos):
        items = []
        for carrito in carritos:
            for _ in range(random.choice([1, 2])):
                producto = random.choice(productos)
                items.append(CarritoItem.objects.create(
                    carrito=carrito, producto=producto,
                    cantidad=random.randint(1, 4), precio_unitario=producto.precio,
                ))
        self.stdout.write(f"  {len(items)} items de carrito")
        return items

    def crear_pedidos(self, clientes, direcciones, cupones):
        pedidos = []
        for _ in range(18):
            cliente = random.choice(clientes)
            direccion = random.choice([d for d in direcciones if d.cliente == cliente])
            subtotal = round(random.uniform(200, 3000), 2)
            descuento = round(subtotal * 0.1, 2) if random.random() > 0.6 else 0
            impuestos = round(subtotal * 0.16, 2)
            p = Pedido.objects.create(
                cliente=cliente, direccion=direccion,
                cupon=random.choice(cupones) if random.random() > 0.5 else None,
                estado=random.choice(['pendiente', 'pagado', 'enviado', 'entregado', 'cancelado']),
                subtotal=subtotal, descuento=descuento, impuestos=impuestos,
                total=round(subtotal - descuento + impuestos, 2),
                metodo_pago=random.choice(['Tarjeta de crédito', 'PayPal', 'Transferencia', 'Efectivo']),
                fecha_entrega_estimada=fake.date_between(start_date='today', end_date='+15d'),
            )
            pedidos.append(p)
        self.stdout.write(f"  {len(pedidos)} pedidos")
        return pedidos

    def crear_detalle_pedido(self, pedidos, productos):
        detalles = []
        for pedido in pedidos:
            for _ in range(random.choice([1, 2, 3])):
                producto = random.choice(productos)
                cantidad = random.randint(1, 5)
                detalles.append(DetallePedido.objects.create(
                    pedido=pedido, producto=producto, cantidad=cantidad,
                    precio_unitario=producto.precio,
                    subtotal=round(producto.precio * cantidad, 2),
                ))
        self.stdout.write(f"  {len(detalles)} detalles de pedido")
        return detalles

    def crear_pagos(self, pedidos):
        pagos = []
        for pedido in pedidos:
            pagos.append(Pago.objects.create(
                pedido=pedido, monto=pedido.total,
                metodo=pedido.metodo_pago,
                estado=random.choice(['pendiente', 'completado', 'rechazado', 'reembolsado']),
                referencia_transaccion=fake.uuid4()[:20],
                hash_seguridad=fake.sha256(),
            ))
        self.stdout.write(f"  {len(pagos)} pagos")
        return pagos

    def crear_resenas(self, clientes, productos):
        resenas = []
        for _ in range(20):
            resenas.append(Resena.objects.create(
                cliente=random.choice(clientes), producto=random.choice(productos),
                calificacion=random.randint(1, 5), comentario=fake.sentence(nb_words=12),
            ))
        self.stdout.write(f"  {len(resenas)} reseñas")
        return resenas

    # ---------------- veterinaria app ----------------

    def crear_veterinarios(self):
        especialidades = ["Medicina General", "Cirugía", "Dermatología", "Cardiología",
                           "Odontología", "Oftalmología", "Nutrición Animal"]
        veterinarios = []
        for i in range(15):
            v = Veterinario.objects.create(
                nombre=fake.first_name(), apellido=fake.last_name(),
                cedula_profesional=f"VET-{100000 + i}",
                especialidad=random.choice(especialidades),
                telefono=fake.msisdn()[:15], email=fake.email(),
                fecha_contratacion=fake.date_between(start_date='-8y', end_date='-1M'),
            )
            veterinarios.append(v)
        self.stdout.write(f"  {len(veterinarios)} veterinarios")
        return veterinarios

    def crear_servicios(self):
        nombres_precios = [
            ("Consulta General", 350, 30), ("Vacunación", 250, 15),
            ("Desparasitación", 200, 15), ("Baño y Corte", 300, 60),
            ("Cirugía Menor", 1800, 90), ("Radiografía", 600, 20),
            ("Análisis de Sangre", 450, 15), ("Limpieza Dental", 900, 45),
            ("Aplicación de Microchip", 400, 15), ("Esterilización", 1500, 60),
            ("Consulta Dermatológica", 500, 30), ("Urgencias", 700, 45),
            ("Chequeo Geriátrico", 400, 30), ("Terapia Física", 350, 30),
            ("Extracción Dental", 800, 45),
        ]
        servicios = []
        for nombre, precio, duracion in nombres_precios:
            s = Servicio.objects.create(
                nombre=nombre, descripcion=fake.sentence(nb_words=8),
                precio=precio, duracion_minutos=duracion,
                categoria=random.choice(["Preventivo", "Diagnóstico", "Estética", "Cirugía"]),
            )
            servicios.append(s)
        self.stdout.write(f"  {len(servicios)} servicios")
        return servicios

    def crear_citas(self, mascotas, veterinarios, servicios):
        citas = []
        for _ in range(20):
            c = Cita.objects.create(
                mascota=random.choice(mascotas), veterinario=random.choice(veterinarios),
                servicio=random.choice(servicios),
                fecha_hora=timezone.now() + timedelta(days=random.randint(-60, 30), hours=random.randint(8, 17)),
                estado=random.choice(['agendada', 'confirmada', 'completada', 'cancelada']),
                motivo=fake.sentence(nb_words=6),
                costo=round(random.uniform(200, 1800), 2),
            )
            citas.append(c)
        self.stdout.write(f"  {len(citas)} citas")
        return citas

    def crear_historial_medico(self, mascotas, citas, veterinarios):
        historiales = []
        for _ in range(20):
            historiales.append(HistorialMedico.objects.create(
                mascota=random.choice(mascotas),
                cita=random.choice(citas) if random.random() > 0.4 else None,
                veterinario=random.choice(veterinarios),
                diagnostico=fake.sentence(nb_words=10),
                tratamiento=fake.sentence(nb_words=10),
                peso_registrado=round(random.uniform(0.5, 40), 2),
                temperatura=round(random.uniform(37.5, 39.5), 1),
                observaciones=fake.sentence(nb_words=8),
                proxima_revision=fake.date_between(start_date='today', end_date='+90d'),
            ))
        self.stdout.write(f"  {len(historiales)} historiales médicos")
        return historiales

    def crear_vacunas(self, mascotas, veterinarios):
        nombres_vacunas = ["Rabia", "Parvovirus", "Moquillo", "Triple Felina", "Leptospirosis",
                            "Hepatitis Infecciosa", "Bordetella", "Leucemia Felina"]
        vacunas = []
        for _ in range(20):
            fecha_aplicacion = fake.date_between(start_date='-2y', end_date='today')
            vacunas.append(Vacuna.objects.create(
                mascota=random.choice(mascotas), veterinario=random.choice(veterinarios),
                nombre_vacuna=random.choice(nombres_vacunas),
                fecha_aplicacion=fecha_aplicacion,
                lote=f"L-{random.randint(1000,9999)}",
                fecha_proxima_dosis=fecha_aplicacion + timedelta(days=365),
            ))
        self.stdout.write(f"  {len(vacunas)} vacunas")
        return vacunas

    def crear_refugios(self):
        refugios = []
        for _ in range(15):
            refugios.append(Refugio.objects.create(
                nombre=f"Refugio {fake.city()}", direccion=fake.address()[:200],
                telefono=fake.msisdn()[:15], email=fake.company_email(),
                capacidad=random.randint(20, 150),
            ))
        self.stdout.write(f"  {len(refugios)} refugios")
        return refugios

    def crear_adopciones(self, mascotas, refugios, clientes):
        adopciones = []
        for _ in range(15):
            adopciones.append(Adopcion.objects.create(
                mascota=random.choice(mascotas),
                refugio=random.choice(refugios) if random.random() > 0.3 else None,
                cliente=random.choice(clientes),
                estado=random.choice(['en_proceso', 'completada', 'cancelada']),
                costo_adopcion=round(random.uniform(0, 800), 2),
                contrato_firmado=random.choice([True, False]),
            ))
        self.stdout.write(f"  {len(adopciones)} adopciones")
        return adopciones