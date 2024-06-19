# utils/firebase_utils.py
from utils.firebase_config import bucket

class FirebaseUtils:

    @staticmethod
    def PostImagen(file):
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        blob.make_public()
        return blob.public_url

    @staticmethod
    def GetImage(filename):
        blob = bucket.blob(filename)
        if blob.exists():
            blob.make_public()
            return blob.public_url
        else:
            return None

    @staticmethod
    def DeleteImage(filename):
        blob = bucket.blob(filename)
        if blob.exists():
            blob.delete()
            return True
        else:
            return False

    @staticmethod
    def UpdateImage(file, old_filename=None):
        if old_filename:
            FirebaseUtils.DeleteImage(old_filename)
        return FirebaseUtils.PostImagen(file)
