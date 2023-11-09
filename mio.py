import qrcode
import sqlite3  
from PIL import Image
import cv2
from pyzbar.pyzbar import decode
from twilio.rest import Client

# Primero, el código para generar un código QR y guardarlo en un archivo
telefono = "5566778899"
datos = f"Teléfono: {telefono}"
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(datos)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
nombre_archivo = "X.png"
img.save(nombre_archivo)
print(f"El código QR se ha generado y guardado como {nombre_archivo}")

# Luego, el código para crear la base de datos y la tabla si no existen
conn = sqlite3.connect('Registro_de_Entrada_UAEM.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        telefono TEXT,
        correo TEXT,
        numero_de_cuenta TEXT,
        codigo_qr BLOB
    )
''')
conn.commit()
conn.close()

# Después, el código para insertar un usuario en la base de datos
conn = sqlite3.connect('Registro_de_Entrada_UAEM.db')
cursor = conn.cursor()
nombre = "José Eduardo Muñoz Meja"
telefono = "+525644298735"
correo = "Lord_Eduard030301@alumno.uaemex.mx"
numero_de_cuenta = "1926587"
with open('Eduardo.png', 'rb') as qr_file:
    codigo_qr = qr_file.read()
cursor.execute("INSERT INTO usuarios (nombre, telefono, correo, numero_de_cuenta, codigo_qr) VALUES (?, ?, ?, ?, ?)",
               (nombre, telefono, correo, numero_de_cuenta, codigo_qr))
conn.commit()
conn.close()

# Después, el código para eliminar un usuario de la base de datos
conn = sqlite3.connect('Registro_de_Entrada_UAEM.db')
cursor = conn.cursor()
nombre = "José Eduardo Muñoz Meja"
numero_de_cuenta = "1926587"
cursor.execute("DELETE FROM usuarios WHERE nombre = ? OR numero_de_cuenta = ?", (nombre, numero_de_cuenta))
conn.commit()
conn.close()

# Finalmente, el código para escanear un código QR desde la cámara y enviar un mensaje de Twilio
def scan_qr_code_and_send_message():
    cap = cv2.VideoCapture(0)
    account_sid = 'AC03379f5c7cd5b6161ac5908ff2bdcbaa'
    auth_token = 'c823bbddb5ea5a87a61f68c45de1aacb'
    client = Client(account_sid, auth_token)
    while True:
        _, frame = cap.read()
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print("Datos leídos del código QR:", qr_data)
            numero_telefono = '+525542694307'
            mensaje = f'El alumno con el siguiente número ha llegado a la institución: {qr_data}'
            message = client.messages.create(
                from_='+12055985431',
                body=mensaje,
                to=numero_telefono
            )
            print(f"Mensaje de Twilio enviado a {numero_telefono}. SID: {message.sid}")
            cap.release()
            cv2.destroyAllWindows()
            return
        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

scan_qr_code_and_send_message()