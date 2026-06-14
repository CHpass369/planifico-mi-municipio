import hashlib
import requests
from django.conf import settings


def sha256_text(value: str) -> str:
    if not value:
        return ''
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def get_client_ip(request) -> str:
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def verify_turnstile(token: str, remote_ip: str = '') -> tuple[bool, str]:
    """
    Valida Cloudflare Turnstile contra Siteverify.
    En desarrollo, si no se configuró SECRET_KEY, se permite continuar.
    En producción, se debe configurar TURNSTILE_SECRET_KEY.
    """
    secret = settings.TURNSTILE_SECRET_KEY
    if not secret:
        if settings.DEBUG:
            return True, 'Turnstile omitido en modo DEBUG.'
        return False, 'TURNSTILE_SECRET_KEY no está configurado.'

    if not token:
        return False, 'No se recibió token de verificación humana.'

    try:
        response = requests.post(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data={'secret': secret, 'response': token, 'remoteip': remote_ip},
            timeout=8,
        )
        payload = response.json()
    except Exception as exc:
        return False, f'No se pudo verificar Turnstile: {exc}'

    if payload.get('success') is True:
        return True, 'Verificación correcta.'
    return False, f'Verificación fallida: {payload.get("error-codes", [])}'
