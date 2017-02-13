from boxcomtools.box import Client

CLIENT_ID = ""
CLIENT_SECRET = ""

ACCESS_TOKEN = None
REFRESH_TOKEN = None


def store_tokens(self, access_token, refresh_token):

    ACCESS_TOKEN = access_token
    REFRESH_TOKEN = refresh_token

    print ("ACCESS_TOKEN: ", access_token)
    print ("REFRESH_TOKEN: ", refresh_token)

    
def print_user():
    cli = Client(CLIENT_ID, CLIENT_SECRET, callback=store_tokens)
    with cli as client:
        print(client.user().get())

if __name__ == "__main__":
    print_user()
