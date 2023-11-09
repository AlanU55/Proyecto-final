import qrcode

# Datos que quieres codificar en el QR
nombre_equipo = "+525542694307"

# Crea el código QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(nombre_equipo)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("pase_de_lista1.png")
