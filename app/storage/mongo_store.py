import os
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import PyMongoError


_client = None
_db = None


def init_mongo(app):
    global _client, _db

    mongo_uri = os.getenv("MONGODB_URI", "").strip()
    db_name = os.getenv("MONGODB_DB_NAME", "secure_governance")

    if not mongo_uri:
        app.logger.info("MongoDB disabled: MONGODB_URI not set")
        _client = None
        _db = None
        return

    try:
        _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=4000)
        _client.admin.command("ping")
        _db = _client[db_name]
        app.logger.info("MongoDB connected: db=%s", db_name)
    except PyMongoError as exc:
        app.logger.warning("MongoDB connection failed, continuing with SQL storage only: %s", exc)
        _client = None
        _db = None


def _upsert(collection_name, filter_doc, set_doc):
    if _db is None:
        return False

    try:
        _db[collection_name].update_one(filter_doc, {"$set": set_doc}, upsert=True)
        return True
    except PyMongoError:
        return False


def sync_user(user):
    return _upsert(
        "users",
        {"sql_id": user.id},
        {
            "sql_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name,
            "aadhaar_id": user.aadhaar_id,
            "address": user.address,
            "updated_at": datetime.utcnow(),
        },
    )


def sync_application(app_obj):
    return _upsert(
        "applications",
        {"sql_id": app_obj.id},
        {
            "sql_id": app_obj.id,
            "user_id": app_obj.user_id,
            "application_number": app_obj.application_number,
            "application_type": app_obj.application_type,
            "purpose": app_obj.purpose,
            "original_payload": app_obj.original_payload,
            "encrypted_payload": app_obj.encrypted_payload,
            "status": app_obj.status,
            "approved_by": app_obj.approved_by,
            "officer_remark": app_obj.officer_remark,
            "digital_signature": app_obj.digital_signature,
            "signature_timestamp": app_obj.signature_timestamp,
            "signature_verification_hash": app_obj.signature_verification_hash,
            "created_at": app_obj.created_at,
            "updated_at": app_obj.updated_at,
        },
    )


def update_application_status(app_obj):
    return _upsert(
        "applications",
        {"sql_id": app_obj.id},
        {
            "status": app_obj.status,
            "approved_by": app_obj.approved_by,
            "officer_remark": app_obj.officer_remark,
            "digital_signature": app_obj.digital_signature,
            "signature_timestamp": app_obj.signature_timestamp,
            "signature_verification_hash": app_obj.signature_verification_hash,
            "updated_at": datetime.utcnow(),
        },
    )


def sync_audit_log(log_obj):
    return _upsert(
        "audit_logs",
        {"sql_id": log_obj.id},
        {
            "sql_id": log_obj.id,
            "user_id": log_obj.user_id,
            "action": log_obj.action,
            "details": log_obj.details,
            "ip_address": log_obj.ip_address,
            "severity": log_obj.severity,
            "timestamp": log_obj.timestamp,
        },
    )
