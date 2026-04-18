import logging
from google.cloud import firestore
from fastapi import Request, HTTPException, status

logger = logging.getLogger(__name__)

DEMO_LIMIT = 2
CONTACT_EMAIL = 'ingenieroedissonia@gmail.com'

db = firestore.AsyncClient()

async def check_demo_limit(request: Request):
    forwarded_for = request.headers.get('X-Forwarded-For')
    ip = forwarded_for.split(',')[0].strip() if forwarded_for else request.client.host
    doc_ref = db.collection('demo_limits').document(ip)
    doc = await doc_ref.get()
    if doc.exists:
        count = doc.to_dict().get('count', 0)
        if count >= DEMO_LIMIT:
            logger.warning(f'IP {ip} alcanzó el límite de demo.')
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f'Demo limit reached. Contact {CONTACT_EMAIL} to unlock full access.'
            )
        await doc_ref.update({'count': firestore.Increment(1)})
    else:
        await doc_ref.set({'count': 1, 'ip': ip})