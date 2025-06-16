import os
from io import BytesIO
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from PIL import Image
import qrcode

LOGO_PATH = os.path.join(settings.MEDIA_ROOT, 'img', 'logo.png')


# ✅ QR para el CLIENTE (número del local)
def generar_qr_local(servicio):
    mensaje = (
        f"Hola, soy {servicio.cliente.nombre}. "
        f"Quisiera saber el estado del servicio {servicio.codigo} que dejé en COMPUSERV."
    )
    link = f"https://wa.me/5930962735727?text={mensaje.replace(' ', '%20')}"
    qr = qrcode.make(link)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return Image.open(buffer)



# ✅ QR para el LOCAL (número del cliente)
def generar_qr_cliente(servicio):
    telefono = servicio.cliente.telefono.replace(" ", "").strip()
    estado_mensaje = (
        "Su equipo está listo para ser retirado."
        if servicio.estado == "listo_para_entregar" else
        "Le compartimos información del proceso de reparación."
    )
    mensaje = (
        f"Hola {servicio.cliente.nombre}, le saludamos de COMPUSERV. "
        f"Nos comunicamos respecto al servicio {servicio.codigo}. "
        f"{estado_mensaje}"
    )
    link = f"https://wa.me/593{telefono}?text={mensaje.replace(' ', '%20')}"
    qr = qrcode.make(link)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return Image.open(buffer)



def _dibuja_comprobante_cliente(c, servicio, y_offset):
    margen_x = 40
    ancho_contenido = 515

    c.setFillColor(colors.HexColor("#003366"))
    c.rect(margen_x - 15, y_offset + 230, ancho_contenido + 30, 65, fill=1, stroke=0)

    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH, margen_x, y_offset + 242, width=50, height=50, preserveAspectRatio=True, mask='auto')

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margen_x + 60, y_offset + 270, "COMPUSERV")
    c.setFont("Helvetica", 9)
    c.drawString(margen_x + 60, y_offset + 258, "Email: compuservecuador@gmail.com")
    c.drawString(margen_x + 60, y_offset + 246, "Dirección: Av. General José Gallardo y S44-217, Quito")
    c.drawString(margen_x + 60, y_offset + 234, "Celular: 0962735727 / 0999281169")

    c.setStrokeColor(colors.lightgrey)
    c.rect(margen_x - 15, y_offset - 20, ancho_contenido + 30, 340, stroke=1, fill=0)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen_x, y_offset + 205, f"Comprobante de Servicio: {servicio.codigo}")

    labels = [
        ("Cliente:", servicio.cliente.nombre),
        ("Teléfono:", servicio.cliente.telefono or "N/A"),
        ("Descripción:", servicio.descripcion),
        ("Accesorios:", servicio.accesorios),
        ("Observaciones:", servicio.observaciones),
    ]
    if servicio.fecha_entrega:
        labels.append(("Fecha de recepción:", servicio.fecha_entrega.strftime('%d/%m/%Y')))

    for i, (label, value) in enumerate(labels):
        y = y_offset + 185 - (i * 15)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margen_x, y, label)
        c.setFont("Helvetica", 10)
        c.drawString(margen_x + 100, y, value)

    # QRs
    qr_img1 = generar_qr_local(servicio)
    qr_path1 = os.path.join(settings.MEDIA_ROOT, f"comprobantes/tempqr_whatsapp_{servicio.codigo}.png")
    qr_img1.save(qr_path1)
    qr_img2 = qrcode.make("https://maps.app.goo.gl/N6wopQ15Bp6NhNaZA")
    qr_path2 = os.path.join(settings.MEDIA_ROOT, f"comprobantes/tempqr_maps_{servicio.codigo}.png")
    qr_img2.save(qr_path2)

    qr1_x = margen_x + 330
    qr2_x = margen_x + 420
    qr_y = y_offset + 105

    c.drawImage(qr_path1, qr1_x, qr_y, width=90, height=90)
    c.drawImage(qr_path2, qr2_x, qr_y, width=90, height=90)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(qr1_x + 45, qr_y - 12, "WhatsApp")
    c.drawCentredString(qr2_x + 45, qr_y - 12, "Ubicación (Maps)")

    base_responsabilidad = y_offset + 85 - (len(labels) - 6) * 2
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margen_x, base_responsabilidad, "Responsabilidad del cliente:")
    c.setFont("Helvetica", 9)
    texto = [
        "El cliente declara haber entregado el equipo con los accesorios indicados y acepta las condiciones del servicio.",
        "Es su responsabilidad contar con respaldo de su información, ya que no se garantiza la integridad de datos o software.",
        "COMPUSERV no se hace responsable por pérdida de información, configuraciones, virus o daños no reportados al ingreso.",
        "El servicio no incluye garantía sobre el software instalado ni reclamos posteriores a la entrega del equipo reparado."
    ]
    for i, linea in enumerate(texto):
        c.drawString(margen_x + 10, base_responsabilidad - 15 - (i * 12), linea)


    firma_y = y_offset - 5
    c.setStrokeColor(colors.black)
    c.line(margen_x, firma_y, margen_x + 150, firma_y)
    c.drawString(margen_x, firma_y - 10, "Firma Cliente")
    c.line(margen_x + 310, firma_y, margen_x + 460, firma_y)
    c.drawString(margen_x + 310, firma_y - 10, "Departamento Técnico")

    try:
        os.remove(qr_path1)
        os.remove(qr_path2)
    except Exception as e:
        print(f"Advertencia: No se pudo eliminar QR temporal: {e}")


def _dibuja_comprobante_interno(c, servicio, y_offset):
    margen_x = 40  # centrado en A4
    ancho_comprobante = 230
    altura_total = 300

    # Marco del comprobante
    c.setStrokeColor(colors.lightgrey)
    c.rect(margen_x, y_offset - 20, ancho_comprobante, altura_total, stroke=1, fill=0)

    # Título
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(margen_x + ancho_comprobante / 2, y_offset + 245, "Copia Interna")
    c.setFont("Helvetica", 9)
    c.drawCentredString(margen_x + ancho_comprobante / 2, y_offset + 232, f"Servicio: {servicio.codigo}")

    # Datos alineados verticalmente
    labels = [
        ("Cliente", servicio.cliente.nombre),
        ("Teléfono", servicio.cliente.telefono or "N/A"),
        ("Tipo", dict(servicio.TIPO_CHOICES).get(servicio.tipo, servicio.tipo)),
        ("Estado", servicio.estado),
        ("Descripción", servicio.descripcion),
        ("Observaciones", servicio.observaciones),
    ]
    if servicio.fecha_entrega:
        labels.append(("Entrega", servicio.fecha_entrega.strftime('%d/%m/%Y')))

    current_y = y_offset + 215
    for label, value in labels:
        c.setFont("Helvetica", 9)
        c.drawString(margen_x + 10, current_y, f"{label}:")
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margen_x + 75, current_y, str(value))
        current_y -= 15

    # QR más abajo, sin tapar datos
    qr_img = generar_qr_cliente(servicio)
    qr_path = os.path.join(settings.MEDIA_ROOT, f"comprobantes/tempqr_onlywh_{servicio.codigo}.png")
    qr_img.save(qr_path)

    qr_size = 90
    qr_x = margen_x + (ancho_comprobante - qr_size) / 2
    qr_y = y_offset + 30  # más abajo que antes
    c.drawImage(qr_path, qr_x, qr_y, width=qr_size, height=qr_size)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(margen_x + ancho_comprobante / 2, qr_y - 10, "WhatsApp")

    try:
        os.remove(qr_path)
    except Exception as e:
        print(f"Advertencia: No se pudo eliminar QR interno: {e}")

def _dibuja_comprobante_accesorios(c, servicio, y_offset):
    margen_x = 310  # Posición a la derecha de la copia interna
    ancho = 230
    alto = 130
    c.setStrokeColor(colors.lightgrey)
    c.rect(margen_x, y_offset - 20, ancho, alto, stroke=1, fill=0)

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(margen_x + ancho / 2, y_offset + 90, "Etiqueta Accesorios")

    campos = [
        ("Cliente", servicio.cliente.nombre),
        ("Teléfono", servicio.cliente.telefono or "N/A"),
        ("Código", servicio.codigo),
        ("Accesorios", servicio.accesorios),
    ]
    current_y = y_offset + 75
    for label, valor in campos:
        c.setFont("Helvetica", 9)
        c.drawString(margen_x + 10, current_y, f"{label}:")
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margen_x + 80, current_y, str(valor))
        current_y -= 15


def generar_comprobante_pdf(servicio):
    filename = f"{servicio.codigo}.pdf"
    ruta = os.path.join(settings.MEDIA_ROOT, 'comprobantes', filename)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    c = canvas.Canvas(ruta, pagesize=A4)

    # Parte superior: comprobante para el cliente
    _dibuja_comprobante_cliente(c, servicio, y_offset=445)

    # Parte inferior - Segunda copia (más abajo)
    _dibuja_comprobante_interno(c, servicio, y_offset=80)
    _dibuja_comprobante_accesorios(c, servicio, y_offset=80)

    c.save()
    servicio.ruta_comprobante.name = f"comprobantes/{filename}"
    servicio.save()



def generar_factura_pdf(factura):
    filename = f"{factura.codigo}.pdf"
    ruta = os.path.join(settings.MEDIA_ROOT, 'facturas_pdfs', filename)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    c = canvas.Canvas(ruta, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "FACTURA")
    c.setFont("Helvetica", 11)
    c.drawString(100, 780, f"Código: {factura.codigo}")
    cliente_nombre = factura.cliente.nombre if factura.cliente else "Consumidor Final"
    c.drawString(100, 760, f"Cliente: {cliente_nombre}")
    c.drawString(100, 740, f"Total: ${factura.total}")
    c.drawString(100, 720, "Gracias por su preferencia - COMPUSERV")

    c.save()
    factura.ruta_archivo.name = f"facturas_pdfs/{filename}"
    factura.save()
