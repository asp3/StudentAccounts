from django.contrib.auth.views import login 
from django.shortcuts import redirect

class RequireLoginMiddleware(object):                                                                                                                                                             
    """ 
    Require Login middleware. If enabled, each Django-powered page will
    require authentication.

    If an anonymous user requests a page, he/she is redirected to the login
    page set by REQUIRE_LOGIN_PATH or /accounts/login/ by default.                                                                                                                                
    """ 
    def __init__(self):
        self.require_login_path = '/student/login/'
                                                                                                                 
    def process_request(self, request):
        print "request path"
        print request.path

        ## if you need to force login before getting to home page, comment out return None
        return None
        if request.path == "/student/signup/" or request.path == "/student/signup" or request.path == '/admin/login' or request.path == '/admin/login/' or request.path == '/admin/':
            return None

        if request.path != self.require_login_path and request.user.is_anonymous(): 
            if request.POST:
                return login(request)
            else:
                return redirect('%s?next=%s' % (self.require_login_path, request.path))
