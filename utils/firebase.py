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
    def delete_from_firebase(filename):
        try:
            blob = bucket.blob(filename)
            blob.delete()
            print(f"Archivo {filename} eliminado correctamente de Firebase Storage.")
        except Exception as e:
            print(f"Error al eliminar archivo de Firebase Storage: {str(e)}")

    @staticmethod
    def update_image(file, old_filename=None):
        if old_filename:
            FirebaseUtils.delete_from_firebase(old_filename)
        return FirebaseUtils.post_image(file)
