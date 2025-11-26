from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import psycopg2
from psycopg2.extras import DictCursor
from fastapi import FastAPI, Request, HTTPException, Depends, Query, Header
from oauthlib.oauth2 import WebApplicationClient
import requests
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

import json
import random
import hmac
import hashlib
import base64
import json

from pathlib import Path


app = FastAPI()

DB_HOST = "postgresss.postgres.database.azure.com"
DB_NAME = "postgres"
DB_USER = "chatezzy_pg_admin"
DB_PASS = "@Apjpakir123"
DB_PORT = 5432


GOOGLE_CLIENT_ID = "722483342463-vd0i1fqmadt70qkumsbul9ms1g18hhbr.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"



STATIC_DIR = Path("static")
STATIC_DIR.mkdir(exist_ok=True)


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
        redirect_uri="https://googlenanobanana.com/login/callback/v2",
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


def encode_parameters(params, secret_key = "@AAAApjpakier4546120$#%!"):
    json_str = json.dumps(params)
    json_bytes = json_str.encode('utf-8')
    signature = hmac.new(secret_key.encode('utf-8'), json_bytes, hashlib.sha256).hexdigest()
    data_with_signature = json_bytes + signature.encode('utf-8')
    encoded_str = base64.urlsafe_b64encode(data_with_signature).decode('utf-8')
    return encoded_str
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
            redirect_url="https://googlenanobanana.com/login/callback/v2",
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
        
        # Your existing database logic - UPDATED to include refer_code and source
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        # Updated query to include both refer_code and source columns
        cursor.execute("""
        INSERT INTO future_ai.users (mail, password, name, country, image_url, refer_code, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (mail) DO UPDATE
        SET password = EXCLUDED.password,
            name = EXCLUDED.name,
            country = EXCLUDED.country,
            image_url = EXCLUDED.image_url,
            source = EXCLUDED.source
        RETURNING id, premium_user, subscription_end_date;
        """, (email, '', name, locale, profile_pic, refer_code, 'nano'))
        
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
        print("Exception while login :::: ", str(e))
        return HTMLResponse("<html><body><h2>Login failed</h2></body></html>", status_code=400)


@app.get("/llms.txt")
async def get_llms_txt():
    """
    Serve the llms.txt file for AI crawlers and LLMs
    This file helps AI systems understand your website structure and content
    """
    file_path = STATIC_DIR / "llms.txt"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="llms.txt file not found")
    
    return FileResponse(
        path=file_path,
        media_type="text/plain",
        headers={
            "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
            "Content-Type": "text/plain; charset=utf-8"
        }
    )


@app.get("/llms-full.txt")
async def get_llms_full_txt():
    """
    Serve the complete llms-full.txt file with comprehensive site content
    This provides AI systems with complete access to all content in one file
    """
    file_path = STATIC_DIR / "llms-full.txt"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="llms-full.txt file not found")
    
    return FileResponse(
        path=file_path,
        media_type="text/plain",
        headers={
            "Cache-Control": "public, max-age=3600",
            "Content-Type": "text/plain; charset=utf-8"
        }
    )

# Alternative approach: Serve from root directory if you prefer
@app.get("/robots.txt")
async def get_robots_txt():
    """Serve robots.txt file"""
    file_path = STATIC_DIR / "robots.txt"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="robots.txt file not found")
    
    return FileResponse(
        path=file_path,
        media_type="text/plain"
    )


@app.get("/sitemap.xml")
async def get_sitemap():
    """
    Serve the sitemap.xml file for search engines and AI crawlers
    This helps with content discovery and indexing
    """
    file_path = STATIC_DIR / "sitemap.xml"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="sitemap.xml file not found")
    
    return FileResponse(
        path=file_path,
        media_type="application/xml",
        headers={
            "Cache-Control": "public, max-age=86400",  # Cache for 24 hours
            "Content-Type": "application/xml; charset=utf-8"
        }
    )


import razorpay
from datetime import datetime
from fastapi import HTTPException

RAZORPAY_AUTH_HEADER = "Basic cnpwX2xpdmVfUkw4cEJYT0NOUkp4WHk6dm55cTFuVHpjOUJHc1BVTERUSWNyR1NX"



def decode_parameters(encoded_str, secret_key="@AAAApjpakier4546120$#%!"):
    data_with_signature = base64.urlsafe_b64decode(encoded_str)
    json_bytes = data_with_signature[:-64]
    signature = data_with_signature[-64:].decode('utf-8')
    expected_signature = hmac.new(secret_key.encode('utf-8'), json_bytes, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected_signature):
        raise ValueError("HMAC verification failed")
    json_str = json_bytes.decode('utf-8')
    return json.loads(json_str)


@app.post("/api/create-razorpay-order-pro")
async def create_razorpay_order_pro(request: dict):
    """
    Create Razorpay order using your working authorization
    """
    try:
        # Extract request data
        print(":::::::::::::::::::::::::::::::::")
        plan_type = request.get("plan_type")
        authToken = request.get("authToken")
        currency = request.get("currency", 'USD')
        amount = request.get("amount", '6')
        customer_phone = request.get("customer_phone", '9999999999')
        
        # Decode user details from token
        userDetailsMap = decode_parameters(authToken)
        user_id = userDetailsMap.get("userId", "")
        customer_email = userDetailsMap.get("mail", "")
        customer_name = userDetailsMap.get("name", "")
        
        # Generate receipt
        timestamp = int(datetime.now().timestamp() * 1000)
        receipt = f"{customer_email}"
        
        # Amount in cents (for USD)
        amount_in_cents = int(float(amount) * 100)
        
        # Prepare payload exactly like your working curl
        payload = {
            "amount": amount_in_cents,
            "currency": currency,
            "receipt": receipt,
            "notes": {
                "plan_type": plan_type,
                "user_id": str(user_id),
                "customer_name": customer_name,
                "customer_email": customer_email,
                "customer_phone": customer_phone
            }
        }
        
        # Make request with exact same headers as your curl
        headers = {
            "content-type": "application/json",
            "Authorization": RAZORPAY_AUTH_HEADER
        }
        
        response = requests.post(
            "https://api.razorpay.com/v1/orders",
            json=payload,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Razorpay Error: {response.text}"
            )
        
        razorpay_order = response.json()
        
        # Decode key_id from the auth header for frontend
        import base64
        decoded = base64.b64decode("cnpwX2xpdmVfUkw4cEJYT0NOUkp4WHk6dm55cTFuVHpjOUJHc1BVTERUSWNyR1NX").decode('utf-8')
        razorpay_key_id = decoded.split(':')[0]
        
        return {
            "order_id": razorpay_order['id'],
            "razorpay_key_id": razorpay_key_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
@app.post("/")
async def home(device: str = None):
    return FileResponse("templates/home.html")

@app.get("/redirecthandler")
@app.post("/redirecthandler")
async def redirecthandler():
    return FileResponse("templates/redire.html")

@app.get("/aaaaaaaaaaaaaaa")
async def home():
    return FileResponse("templates/home_copy.html")


@app.get("/new_playground")
async def newPlayGround():
    return FileResponse("templates/new_image_playground.html")


@app.get("/nanobananapro")
async def newPlayGround():
    return FileResponse("templates/nano_banana_pro.html")

@app.get("/privacy")
async def privacy_policy():
    return FileResponse("templates/privacy.html")

@app.get("/veo-3")
async def privacy_policy():
    return FileResponse("templates/veo_ext.html")


@app.get("/termsconditions")
async def terms_and_conditions():
    return FileResponse("templates/terms.html")

@app.get("/remove-background")
async def remove_background():
    return FileResponse("templates/remove_background.html")

@app.get("/blog")
async def blog():
    return FileResponse("templates/nanoblog.html")

@app.get("/sora")
async def sora():
    return FileResponse("templates/sora.html")

@app.get("/bulk-image-generator")
async def bulk():
    return FileResponse("templates/bulk_image_generator.html")

@app.get("/support")
async def support():
    return FileResponse("templates/support.html")

@app.get("/pricing")
async def support():
    return FileResponse("templates/pricing2.html")

@app.get("/allprompts")
async def support():
    return FileResponse("templates/allprompts.html")

@app.get("/shipping-terms")
async def shipping(request: Request):
    return FileResponse("templates/shipping.html")
    
@app.get("/subscription-terms")
async def Subterms(request: Request):
    return FileResponse("templates/subscription-terms.html")

@app.get("/about-us")
async def AboutUs(request: Request):
    return FileResponse("templates/about.html")

@app.get("/nano-banana-checkout")
async def nanobloggpricing(request: Request):
    return FileResponse("templates/nano_pricing.html")

@app.get("/ru")
async def nanobloggpricing(request: Request):
    return FileResponse("templates/home_russian.html")


@app.get("/ru-desk")
async def nanoRussiaDesk(request: Request):
    return FileResponse("templates/new_russian_desktop.html")


@app.get("/nl-desk")
async def nanoRussiaDesk(request: Request):
    return FileResponse("templates/home_dutch.html")



@app.get("/virtual-trial-room")
async def virtualtrail(request: Request):
    return FileResponse("templates/virtualtryon.html")

@app.get("/pro/rus")
async def sorass():
    return FileResponse("templates/pro_russian.html")


@app.get("/rus/blog1")
async def rusblog1():
    return FileResponse("templates/blog1.html")

@app.get("/rus/blog2")
async def rusblog2():
    return FileResponse("templates/blog2_compre.html")

@app.get("/rus/blog3")
async def rusblog2():
    return FileResponse("templates/blog3.html")


@app.get("/rus/blog4")
async def rusblog4():
    return FileResponse("templates/blog4.html")

@app.get("/rus/blog5")
async def rusblog4():
    return FileResponse("templates/blog5.html")


@app.get("/rus/blog6")
async def rusblog4():
    return FileResponse("templates/blog6.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)