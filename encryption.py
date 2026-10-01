import os
import base64
import hashlib
import hmac
import json

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from dotenv import load_dotenv
load_dotenv()

# IMPORTANT:
# Keep this in an environment variable in production.
# Do NOT hardcode the real key in source code.
ENCRYPTION_KEY = base64.b64decode(os.environ["USER_ENCRYPTION_KEY"])
HASH_KEY = os.environ["USER_HASH_KEY"].encode()


def encrypt_value(value: str) -> str:
    if value is None:
        return None
    value = str(value)

    # Generate a new nonce every time
    nonce = os.urandom(12)
    aesgcm = AESGCM(ENCRYPTION_KEY)
    encrypted = aesgcm.encrypt(
        nonce,
        value.encode("utf-8"),
        None
    )
    # Store nonce + encrypted data together
    result = nonce + encrypted
    return base64.b64encode(result).decode("utf-8")


def decrypt_value(value: str) -> str:
    if value is None:
        return None
    raw = base64.b64decode(value)
    nonce = raw[:12]
    encrypted = raw[12:]
    aesgcm = AESGCM(ENCRYPTION_KEY)

    decrypted = aesgcm.decrypt(
        nonce,
        encrypted,
        None
    )
    return decrypted.decode("utf-8")


def blind_index(value: str) -> str:
    """
    Used for equality checks / uniqueness checks.

    We DON'T use normal SHA256 because aadhar/PAN values
    have a limited search space.

    HMAC requires a secret key.
    """
    if value is None:
        return None
    normalized = str(value).strip().upper()

    return hmac.new(
        HASH_KEY,
        normalized.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


ENCRYPTED_USER_FIELDS = {
    "aadhar_number",
    "panCardNumber",
    "panCardUrl",
   "aadhar_front_image_url",
  "aadhar_back_image_url"
}

def decrypt_user_data(user_data: dict) -> dict:
    if not user_data:
        return user_data

    user_data = dict(user_data)
    for field in ENCRYPTED_USER_FIELDS:
        if user_data.get(field):
            user_data[field] = decrypt_value(
                user_data[field]
            )
        # Don't send hash values to the user
        user_data.pop(
            f"{field}_hash",
            None
        )
    return user_data    

ENCRYPTED_NOMINEE_FIELDS = {
    "aadhar_number",
    "pancard_number",
    "aadhar_photo_url",
    "pancard_photo_url",
}


def encrypt_nominee_fields(fields: dict) -> dict:
    """
    Encrypt sensitive nominee fields before storing them in Neo4j.
    Also creates blind indexes for Aadhaar/PAN so equality checks
    can still be performed without storing plaintext.
    """
    fields = dict(fields)

    for field in ENCRYPTED_NOMINEE_FIELDS:
        if fields.get(field) is not None:
            fields[field] = encrypt_value(fields[field])

    if fields.get("aadhar_number") is not None:
        fields["aadhar_number_hash"] = blind_index(
            fields["aadhar_number"]
        )

    if fields.get("pancard_number") is not None:
        fields["pancard_number_hash"] = blind_index(
            fields["pancard_number"]
        )

    return fields

def decrypt_nominee_fields(nominee_data: dict) -> dict:
    """
    Decrypt sensitive nominee fields when reading them from Neo4j.
    """
    if not nominee_data:
        return nominee_data

    nominee_data = dict(nominee_data)

    for field in ENCRYPTED_NOMINEE_FIELDS:
        if nominee_data.get(field):
            nominee_data[field] = decrypt_value(
                nominee_data[field]
            )

        nominee_data.pop(
            f"{field}_hash",
            None
        )

    return nominee_data        

def encrypt_response_data(data) -> str:
    """
    Encrypt the complete API response.

    The response is first converted to JSON,
    then encrypted using the existing AES-GCM helper.
    """
    json_data = json.dumps(
        data,
        ensure_ascii=False,
        default=str
    )
    return encrypt_value(json_data)    