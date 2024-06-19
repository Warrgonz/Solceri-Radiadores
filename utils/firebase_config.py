# utils/firebase_config.py
import firebase_admin
from firebase_admin import credentials, storage
import os

# Configurar Firebase
cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'solceri-1650a-firebase-adminsdk-vf2d0-4592ae5a29.json'))
firebase_admin.initialize_app(cred, {
    'storageBucket': 'solceri-1650a.appspot.com'
})

bucket = storage.bucket()

