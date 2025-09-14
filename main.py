from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import psycopg2
from psycopg2.extras import DictCursor
from fastapi import FastAPI, Request, HTTPException, Depends, Query, Header
from oauthlib.oauth2 import WebApplicationClient
import requests


app = FastAPI()

DB_HOST = "postgresss.postgres.database.azure.com"
DB_NAME = "postgres"
DB_USER = "chatezzy_pg_admin"
DB_PASS = "@Apjpakir123"
DB_PORT = 5432


GOOGLE_CLIENT_ID = "722483342463-vd0i1fqmadt70qkumsbul9ms1g18hhbr.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"




client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

    
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        sslmode='require',  # Azure requirement
        options="-c client_encoding=utf8"
    )
    return conn



@app.get("/logggin/v2")
def login_v2(refer_code: str = None):
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Include refer_code in the state parameter to pass it through OAuth flow
    state_data = {}
    # Handle empty string and whitespace cases
    if refer_code and refer_code.strip():
        state_data["refer_code"] = refer_code.strip()
    
    # Convert state to string (you might want to encode/encrypt this for security)
    state = json.dumps(state_data) if state_data else None

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="https://chatezzy.com/login/callback/v2",
        scope=["openid", "email", "profile"],
        state=state  # Pass the refer_code through state parameter
    )
    print(f"Redirect URI: {request_uri}")
    response = JSONResponse(content={"redirect_uri": request_uri})
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
    response.headers["Cross-Origin-Embedder-Policy"] = "unsafe-none"
    return response


@app.get("/oauth-success")
def oauth_success(token: str = None, name: str = None, id: str = None):
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login Success</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <h2>Login Successful!</h2>
        <p>Welcome, {name}!</p>
        <p>Redirecting...</p>
        
        <script>
            // Detect if mobile
            const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
            
            // Save auth token to localStorage
            if ('{token}') {{
                localStorage.setItem('authToken', '{token}');
                localStorage.setItem('user_id', '{id}');
                
                // If mobile, redirect to home page
                if (isMobile) {{
                    setTimeout(() => {{
                        window.location.href = '/';
                    }}, 1000);
                }} else {{
                    // Desktop - just show the message
                    document.querySelector('p:last-of-type').textContent = 'You can close this window.';
                }}
            }}
        </script>
    </body>
    </html>
    """)
# Modify your existing /login/callback/v2 to return HTML for popup:
@app.get("/login/callback/v2")
def callback_v2(request: Request):
    # Get the authorization code from the request
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    
    # Extract refer_code from state parameter
    refer_code = None
    if state:
        try:
            state_data = json.loads(state)
            refer_code = state_data.get("refer_code")
            # Additional validation: ensure it's not empty string
            if refer_code and not refer_code.strip():
                refer_code = None
            elif refer_code:
                refer_code = refer_code.strip()
        except (json.JSONDecodeError, AttributeError):
            refer_code = None
    
    try:
        # Your existing OAuth processing logic (keep it exactly as it is)
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=str(request.url),
            redirect_url="https://chatezzy.com/login/callback/v2",
            code=code
        )
        
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )
        
        client.parse_request_body_response(json.dumps(token_response.json()))
        
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        user_info = userinfo_response.json()
        
        # Extract user details
        name = user_info.get("name")
        email = user_info.get("email")
        profile_pic = user_info.get("picture")
        locale = user_info.get("locale", "")
        
        # Your existing database logic - UPDATED to include refer_code
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        # Updated query to include refer_code column
        cursor.execute("""
        INSERT INTO future_ai.users (mail, password, name, country, image_url, refer_code)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (mail) DO UPDATE
        SET password = EXCLUDED.password,
            name = EXCLUDED.name,
            country = EXCLUDED.country,
            image_url = EXCLUDED.image_url
        RETURNING id, premium_user, subscription_end_date;
        """, (email, '', name, locale, profile_pic, refer_code))
        
        user_details = cursor.fetchone()
        user_id = user_details.get('id')
        is_premium_user = user_details.get('premium_user', False)
        subscription_end_date = user_details.get('subscription_end_date', "2000-04-23 22:18:08.237")
        
        params = {
            'userId': user_id, 
            'mail': email, 
            'name': name, 
            'profile_pic': profile_pic, 
            'is_premium_user': is_premium_user, 
            'subscription_end_date': str(subscription_end_date)
        }
        
        auth_token = encode_parameters(params)
        conn.commit()
        cursor.close()
        conn.close()

        escaped_name = name.replace("'", "\\'")
        
        # Rest of your existing HTML response code remains the same
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Login Success</title></head>
        <body>
            <h2>Login Successful!</h2>
            <p>Welcome, {name}!</p>
            <script>
                const authData = {{
                    type: 'OAUTH_SUCCESS',
                    auth_token: '{auth_token}',
                    id: {user_id},
                    user: {{
                        id: {user_id},
                        name: '{escaped_name}',
                        email: '{email}',
                        profile_pic: '{profile_pic}',
                        is_premium: {str(is_premium_user).lower()},
                        subscription_end_date: '{subscription_end_date}'
                    }}
                }};
                
                if (window.opener) {{
                    window.opener.postMessage(authData, '*');
                    window.close();
                }} else {{
                    console.log('Token:', '{auth_token}');
                }}
            </script>
        </body>
        </html>
        """

        response = HTMLResponse(content=html_content)
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
        response.headers["Cross-Origin-Embedder-Policy"] = "unsafe-none"
        return RedirectResponse(f"/oauth-success?token={auth_token}&name={name}&id={user_id}")
        
    except Exception as e:
        # Handle errors appropriately
        return HTMLResponse("<html><body><h2>Login failed</h2></body></html>", status_code=400)

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home():
    return FileResponse("templates/home.html")

@app.get("/privacy")
async def privacy_policy():
    return FileResponse("templates/privacy.html")

@app.get("/termsconditions")
async def terms_and_conditions():
    return FileResponse("templates/terms.html")

@app.get("/remove-background")
async def remove_background():
    return FileResponse("templates/remove_background.html")

@app.get("/blog")
async def blog():
    return FileResponse("templates/nanoblog.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)