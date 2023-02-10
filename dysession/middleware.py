from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware as DjSessionMiddleware


class SessionMiddleware(DjSessionMiddleware):
    def process_request(self, request):
        # SESSION_COOKIE_NAME can be change by developers
        # https://docs.djangoproject.com/en/3.2/ref/settings/#session-cookie-name
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.SessionStore(session_key=session_key)
