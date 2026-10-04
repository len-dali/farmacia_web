from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-por-una-propia"  # necesaria para los mensajes flash

NOMBRE_FARMACIA = "Farmacias Similares"

CATEGORIAS = [
    {
        "id": "medicamentos",
        "nombre": "Medicamentos",
        "detalle": "Analgésicos, antigripales, antialérgicos y digestivos, con orientación de nuestros farmacéuticos.",
        "tam": "grande",
        "imagen": "medicamentos.avif",
    },
    {
        "id": "vitaminas",
        "nombre": "Vitaminas y suplementos",
        "detalle": "Para cada etapa de la vida.",
        "tam": "mediano",
        "imagen": "vitaminas.webp",
    },
    {
        "id": "cuidado",
        "nombre": "Cuidado personal",
        "detalle": "Piel, cabello e higiene diaria.",
        "tam": "mediano",
        "imagen": "cuidado_personal.avif"
    },
    {
        "id": "bebes",
        "nombre": "Mamá y bebé",
        "detalle": "Cuidado del recién nacido.",
        "tam": "pequeno",
        "imagen": "bebes.avif",
    },
    {
        "id": "equipos",
        "nombre": "Equipos médicos",
        "detalle": "Mide tu salud en casa.",
        "tam": "pequeno",
        "imagen": "equipos.avif"
    },
]

# Productos de ejemplo: 
PRODUCTOS = [
    {"nombre": "Paracetamol 500 mg", "categoria": "medicamentos", "presentacion": "Caja con 20 tabletas",
     "descripcion": "Alivia el dolor leve y baja la fiebre.", "imagen":"paracetamol.webp" },

    {"nombre": "Ibuprofeno 400 mg", "categoria": "medicamentos", "presentacion": "Caja con 10 cápsulas",
     "descripcion": "Para dolor muscular, de cabeza y malestar con inflamación.", "imagen":"ibuprofeno.webp" },

    {"nombre": "Loratadina 10 mg", "categoria": "medicamentos", "presentacion": "Caja con 10 tabletas",
     "descripcion": "Antialérgico de uso diario, no produce mucho sueño.", "imagen":"loratadina.webp" },

    {"nombre": "Suero oral", "categoria": "medicamentos", "presentacion": "Botella de 500 ml",
     "descripcion": "Ayuda a reponer líquidos y sales en caso de deshidratación.", "imagen":"suerox.avif" },

    {"nombre": "Vitamina C 1 g", "categoria": "vitaminas", "presentacion": "Tubo con 10 efervescentes",
     "descripcion": "Apoyo para tus defensas en temporada de frío.", "imagen":"vitaminac.jpg" },

    {"nombre": "Multivitamínico adultos", "categoria": "vitaminas", "presentacion": "Frasco con 60 tabletas",
     "descripcion": "Complemento diario de vitaminas y minerales.", "imagen":"multivitaminico.webp" },

    {"nombre": "Protector solar FPS 50", "categoria": "cuidado", "presentacion": "Tubo de 120 ml",
     "descripcion": "Protección alta contra rayos UVA y UVB, resistente al agua.", "imagen":"protector_solar.avif" },

    {"nombre": "Crema hidratante", "categoria": "cuidado", "presentacion": "Frasco de 250 ml",
     "descripcion": "Hidratación profunda para piel seca o sensible.", "imagen":"crema.jpg" },

    {"nombre": "Pañales etapa 3", "categoria": "bebes", "presentacion": "Paquete con 40 piezas",
     "descripcion": "Alta absorción y ajuste suave para tu bebé.", "imagen":"panales.webp" },

    {"nombre": "Termómetro digital", "categoria": "equipos", "presentacion": "Lectura en 10 segundos",
     "descripcion": "Medición oral, axilar o rectal con alarma de fiebre.", "imagen":"termometro.webp" },

    {"nombre": "Tensiómetro de brazo", "categoria": "equipos", "presentacion": "Pantalla digital",
     "descripcion": "Controla tu presión arterial desde casa.", "imagen":"tensiometro.webp" },

    {"nombre": "Glucómetro con tiras", "categoria": "equipos", "presentacion": "Kit con 25 tiras",
     "descripcion": "Medición rápida de glucosa en una gota de sangre.", "imagen":"glucometro.webp" },
]


@app.route("/")
def inicio():
    q = request.args.get("q", "").strip()
    categoria = request.args.get("categoria", "").strip()
    pedido = request.args.get("pedido", "").strip()

    productos = PRODUCTOS
    if categoria:
        productos = [p for p in productos if p["categoria"] == categoria]
    if q:
        ql = q.lower()
        productos = [
            p for p in productos
            if ql in p["nombre"].lower() or ql in p["descripcion"].lower()
        ]

    conteo = {
        c["id"]: sum(1 for p in PRODUCTOS if p["categoria"] == c["id"])
        for c in CATEGORIAS
    }
    nombres_categoria = {c["id"]: c["nombre"] for c in CATEGORIAS}

    return render_template(
        "index.html",
        nombre=NOMBRE_FARMACIA,
        categorias=CATEGORIAS,
        productos=productos,
        conteo=conteo,
        nombres_categoria=nombres_categoria,
        q=q,
        categoria=categoria,
        pedido=pedido,
    )


@app.route("/contacto", methods=["POST"])
def contacto():
    nombre = request.form.get("nombre", "").strip()
    telefono = request.form.get("telefono", "").strip()
    mensaje = request.form.get("mensaje", "").strip()

    if not nombre or not telefono or not mensaje:
        flash("Completa tu nombre, teléfono y mensaje para poder atenderte.", "error")
    else:
        # Aquí podrías guardar el pedido en una base de datos o enviar un correo.
        print(f"Nuevo mensaje de {nombre} ({telefono}): {mensaje}")
        flash(f"Gracias, {nombre}. Te llamaremos al {telefono} en unos minutos.", "ok")

    return redirect(url_for("inicio", _anchor="contacto"))


if __name__ == "__main__":
    app.run(debug=True)