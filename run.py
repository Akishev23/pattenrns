from wsgiref.simple_server import make_server

from own_framework.main import Framework
from urls import fronts
from views import routs
from own_framework.settings import DEBUG
from own_framework.main import DebugApplication
from all_patterns.structural import Router

if DEBUG:
    application = DebugApplication(routs, fronts)
else:
    application = Framework(routs, fronts)

with make_server('', 9999, application) as httpd:
    print("Launching on port 9999...")
    httpd.serve_forever()
