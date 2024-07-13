from random import randint

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core import serializers

from .features.encryption import _decrypt, _encrypt, _isEncrypted
from accounts.models import AuditTrail, User


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def store_audit(*, request, instance, action, previous_instance=None):
    audit = AuditTrail()
    audit.model_type = instance._meta.verbose_name.title()
    audit.object_id = instance.pk
    audit.object_str = str(instance)
    audit.action = action
    audit.user = request.user
    audit.ip = get_client_ip(request)
    audit.instance = serializers.serialize("json", [instance])
    if previous_instance:
        audit.previous_instance = serializers.serialize("json", [previous_instance])
    audit.save()


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
            user = User.objects.get(uuid=uid)
            if default_token_generator.check_token(user, token):
                return {"user": user}
        except Exception as e:
            print(e)
