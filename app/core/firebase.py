from __future__ import annotations

import json
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.client import Client
from app.core.config import Settings


def initialize_firestore(settings: Settings) -> Client:
    if firebase_admin._apps:
        return firestore.client()

    options = {"projectId": settings.firebase_project_id} if settings.firebase_project_id else None
    if settings.firebase_credentials_json:
        cred = credentials.Certificate(json.loads(settings.firebase_credentials_json))
        firebase_admin.initialize_app(cred, options)
    elif settings.firebase_credentials_path:
        cred = credentials.Certificate(settings.firebase_credentials_path)
        firebase_admin.initialize_app(cred, options)
    else:
        # Uses Application Default Credentials (useful on Google Cloud).
        firebase_admin.initialize_app(options=options)
    return firestore.client()
