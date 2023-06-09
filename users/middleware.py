# from django.utils import timezone
from bson import ObjectId

from main.models import User
from datetime import datetime


class UpdateLastActivityMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # assert hasattr(request.session, 'user'), 'The UpdateLastActivityMiddleware requires
        # authentication middleware to be installed.'
        if 'user' in request.session:
            user = User.find_one({'_id': ObjectId(request.session['user']['id'])})
            user.online = datetime.utcnow()  # timezone.now()
            user.save()
