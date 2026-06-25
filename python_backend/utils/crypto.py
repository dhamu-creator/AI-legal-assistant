import pyotp
import qrcode
from io import BytesIO

class MultiFactorAuth:
    @staticmethod
    def generate_new_secret() -> str:
        return pyotp.random_base32()

    @staticmethod
    def get_totp_uri(secret: str, user_email: str) -> str:
        return pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email, 
            issuer_name="AI_Legal_Assistant"
        )

    @staticmethod
    def verify_token(secret: str, token: str) -> bool:
        if not secret or not token:
            return False
        totp = pyotp.totp.TOTP(secret)
        # Allows 30-second clock-drift window for mobile devices
        return totp.verify(token, valid_window=1)
