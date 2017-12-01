import datetime
import jwt

# Replace these with your details
ANNOTATOR_CONSUMER_TTL = 86400
ANNOTATOR_CONSUMER_KEY = 'yourconsumerkey'
ANNOTATOR_CONSUMER_SECRET = 'yourconsumersecret'
ANNOTATOR_PROVIDER_KEY = 'yourproviderkey'
ANNOTATOR_PROVIDER_SECRET = 'yourprovidersecret'

def now():
    return datetime.datetime.utcnow().replace(microsecond=0)

def generate_consumer_token(user_id):
    return jwt.encode({
      'consumerKey': ANNOTATOR_CONSUMER_KEY,
      'userId': user_id,
      'issuedAt': now().isoformat() + 'Z',
      'ttl': ANNOTATOR_CONSUMER_TTL
    }, ANNOTATOR_CONSUMER_SECRET)
