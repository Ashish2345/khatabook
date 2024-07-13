from random import randint

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .features.encryption import _decrypt, _encrypt, _isEncrypted


class OTPEncryptionDec:
    def _encrypt_otp(self):
        rand_otp = randint(100000, 999999)
        encrypted_otp = _encrypt(str(rand_otp))
        return {"otp": rand_otp, "encrypted_otp": encrypted_otp}

    def _decrypt_otp(self, encrypted_otp):
        if _isEncrypted(encrypted_otp):
            dec_otp = _decrypt(encrypted_otp)
            return dec_otp
        return encrypted_otp

    def _decrypt_validate_otp(self, encrypted_otp, otp):
        if _isEncrypted(encrypted_otp):
            dec_otp = _decrypt(encrypted_otp)
            if dec_otp == otp:
                return True
        return False


class TokenEncodeDecode:
    def _encode(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(bytes(str(user.uuid), "utf-8"))
        return {"token": token, "uid": uid}

    def _decode(self, uid, token):
        try:
            uid = urlsafe_base64_decode(uid)
            uid = uid.decode("utf-8")  # Decode bytes to str using utf-8
            user = uid.objects.get(uuid=uid)
            if default_token_generator.check_token(user, token):
                return {"user": user}
        except Exception as e:
            print(e)


def get_ui_avatars(first_name, last_name):
    base_url = "https://ui-avatars.com/api/"
    params = (
        f"?background=0D8ABC"
        f"&color=fff"
        f"&name={first_name}+{last_name}"
        f"&size=256"
        f"&format=png"
    )
    url = base_url + params
    return url
