from flask import Flask, redirect, url_for, session
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random key

# Replace these values with your Google API credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'http://localhost:5000/callback'  # Should match your Google API Console settings


@app.route('/')
def home():
    return 'Welcome to the OAuth with Google Example! <a href="/login">Login with Google</a>'


@app.route('/login')
def login():
    # Generate the Google OAuth URL
    google_oauth_url = (
        "https://accounts.google.com/o/oauth2/auth?"
        f"client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=openid%20profile%20email"
    )
    return redirect(google_oauth_url)


@app.route('/callback')
def callback():
    # Exchange the authorization code for an access token
    code = request.args.get('code')
    token_url = "https://oauth2.googleapis.com/token"
    token_params = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    response = requests.post(token_url, data=token_params)
    token_data = response.json()

    # Verify the ID token
    try:
        id_info = id_token.verify_oauth2_token(token_data['id_token'], requests.Request(), CLIENT_ID)
    except GoogleAuthError as e:
        return f'Error: {str(e)}'

    # Store user information in session
    session['user_info'] = id_info

    return f'Hello, {id_info["name"]}! <a href="/logout">Logout</a>'


@app.route('/logout')
def logout():
    # Clear user information from session
    session.pop('user_info', None)
    return 'You have been logged out. <a href="/">Home</a>'


if __name__ == '__main__':
    app.run(debug=True)
