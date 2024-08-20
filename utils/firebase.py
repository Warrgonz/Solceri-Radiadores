import firebase_admin
from firebase_admin import credentials, storage
import os
import uuid

# Configurar Firebase
cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'solceri-1650a-firebase-adminsdk-vf2d0-4592ae5a29.json'))
firebase_admin.initialize_app(cred, {
    'storageBucket': 'solceri-1650a.appspot.com'
})

bucket = storage.bucket()

class FirebaseUtils:

    @staticmethod
    def post_image(file):
        try:
            # Generar un nombre único para la imagen usando UUID
            unique_filename = str(uuid.uuid4()) + "_" + file.filename
            blob = bucket.blob(unique_filename)
            blob.upload_from_file(file)
            blob.make_public()
            return blob.public_url
        except Exception as e:
            print(f"Error al subir la imagen a Firebase: {str(e)}")
            return None


    @staticmethod
    def get_image(filename):
        try:
            blob = bucket.blob(filename)
            if blob.exists():
                blob.make_public()
                return blob.public_url
            else:
                return None
        except Exception as e:
            print(f"Error al obtener la imagen de Firebase: {str(e)}")
            return None

    @staticmethod
    def post_cotizacion(file, filename=None):
        try:
            # Generar un nombre único para la cotización usando UUID si no se proporciona un nombre de archivo
            if filename is None:
                unique_filename = str(uuid.uuid4()) + ".xlsx"
            else:
                unique_filename = filename

            # Crear un blob en Firebase y subir el archivo
            blob = bucket.blob(unique_filename)
            blob.upload_from_file(file)
            blob.make_public()
            return blob.public_url
        except Exception as e:
            print(f"Error al subir la cotización a Firebase: {str(e)}")
            return None
        
    # Nuevo método para subir archivos desde BytesIO
    @staticmethod
    def post_excel(file_bytes, filename):
        try:
            # Subir el archivo BytesIO a Firebase con el nombre de archivo proporcionado
            blob = bucket.blob(filename)
            blob.upload_from_string(file_bytes.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            blob.make_public()
            return blob.public_url
        except Exception as e:
            print(f"Error al subir el archivo Excel a Firebase: {str(e)}")
            return None
                        
    @staticmethod
    def update_image(file, old_filename=None):
        try:
            # Subir la nueva imagen
            new_image_url = FirebaseUtils.post_image(file)

            # Verificar que la nueva imagen se haya subido correctamente antes de intentar eliminar la anterior
            if new_image_url and old_filename:
                old_blob = bucket.blob(old_filename)
                if old_blob.exists():
                    old_blob.delete()

            return new_image_url
        except Exception as e:
            print(f"Error al actualizar la imagen en Firebase: {str(e)}")
            return None
