from wsgiref.simple_server import make_server
from own_framework.main import Framework
from urls import routes, fronts

application = Framework(routes, fronts)

with make_server('', 9999, application) as httpd:
    print("Launching on port 9999...")
    httpd.serve_forever()
