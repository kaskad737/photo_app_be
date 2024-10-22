import jwt
from django.conf import settings
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from datetime import timedelta, timezone, datetime
from rest_framework.exceptions import AuthenticationFailed


def make_invitation_reset_link(user, type):
    token = jwt.encode(
        payload={
            "pk": str(user.pk)
        },
        key=settings.SECRET_KEY,
        algorithm="HS256",
    )

    signer = TimestampSigner()
    signed_user_token = signer.sign(token)

    FRONT_END_HOST = str(settings.FE_HOST)

    url = FRONT_END_HOST + f"/{type}/?{type}={signed_user_token}"

    return url


def data_unsigner(invitation_signed_token):
    signer = TimestampSigner()
    try:
        unsigned_user_token = signer.unsign(invitation_signed_token, max_age=timedelta(days=14))
        return jwt.decode(jwt=unsigned_user_token, key=settings.SECRET_KEY, algorithms=["HS256"])
    except (SignatureExpired, BadSignature):
        return None


def password_validation(password) -> None:
    # At least 1 capital character
    count_of_capital_chars = sum([1 for char in password if char.isupper()])
    if count_of_capital_chars < 1:
        raise AuthenticationFailed({"message": "The password must contain at least one capital letter"})

    # At least 1 number
    count_of_number_chars = sum([1 for char in password if char.isnumeric()])
    if count_of_number_chars < 1:
        raise AuthenticationFailed({"message": "The password must contain at least one digit"})

    total_password_length = len(password)
    # at least 8 characters total
    if total_password_length < 8:
        raise AuthenticationFailed(
            {"message": "the password must be longer than 8 characters (9 or more characters in total)."}
        )

    return None


def create_password(user_to_update, password):
    user_to_update.set_password(raw_password=password)
    user_to_update.password_changed_at = datetime.now(timezone.utc)
    user_to_update.is_active = True
    user_to_update.save(update_fields=["password", "password_changed_at", 'is_active'])
