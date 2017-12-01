from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from app.utils import json_response
from datastore.auth import generate_consumer_token


@require_GET
@login_required
@json_response
def token(request):
    #http://example.com/api/token
    user = request.user
    if user.is_authenticated:
        user_id = user.id
    else:
        user_id = None
    token = generate_consumer_token(user.id)
    return token


@require_POST
@login_required
@json_response
def change_collection_status(request):
    data = json.loads(request.body.decode('utf-8'))
    collection = get_object_or_404(Collection, id=data['collection_id'])
    artwork = get_object_or_404(Artwork, id=data['artwork_id'])
    user = request.user
    if not collection.user.id == user.id:
        raise Http404("What collection?")

    change = data['change']
    if change == 'add':
        collection.artworks.add(artwork)
        in_collection = True
    elif change == 'remove':
        collection.artworks.remove(artwork)
        in_collection = False
    collection.save()
    return to_dict({
        'in_collection': in_collection,
        'collection': collection,
        'collections': artwork.collections.all(),
        'artwork': artwork,
    })
