from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer, BadData


def generate_access_token(oppenid):
    token = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=600)
    data = {'openid': oppenid}
    token_dumps = token.dumps(data)
    return token_dumps.decode()


def check_access_token(access_token):
    token = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=600)
    try:
        data = token.loads(access_token)
    except BadData:
        return None
    return data.get('openid')
