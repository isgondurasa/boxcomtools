from boxcomtools.box import Client

from flask import Flask
from flask import redirect, request, render_template

try:
    from settings import (BOX_CLIENT_ID, BOX_CLIENT_SECRET,
                          SMARTSHEET_CLIENT_ID, SMARTSHEET_CLIENT_SECRET)

except ImportError:
    print("Please, do 'cp settings.py.default settings.py' first")
    sys.exit(0)

    
app = Flask(__name__)

ACCESS_TOKEN = None
REFRESH_TOKEN = None

@app.route("/")
def index():
    cli = Client(BOX_CLIENT_ID, BOX_CLIENT_SECRET, callback=store_tokens)
    auth_url, csrf_token = cli.auth_url
    return redirect(auth_url)

@app.route("/api/oauth/login")
def auth():

    _args = request.args
    code, state = _args.get("code"), _args.get("state")

    client = Client(BOX_CLIENT_ID, BOX_CLIENT_SECRET, callback=store_tokens)
    tokens = client.authenticate(code)
    access_token, refresh_token = tokens
    
    user = None
    with client as cli:
        user = cli.user().get().__dict__
        print(user)

    params = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'current_user': user
    }
        
    return render_template("index.html", **params)

def store_tokens(self, access_token, refresh_token):

    ACCESS_TOKEN = access_token
    REFRESH_TOKEN = refresh_token


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
