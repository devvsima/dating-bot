import asyncio
import hashlib
import hmac
import json
import os
import secrets
import sys
import urllib.parse
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

# Add root directory to path for importing bot modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.config import tgbot, webapp
from database.connect import get_session
from database.services.stats import Stats

app = FastAPI(title="Dating Bot Admin Panel")

# Simple authentication
security = HTTPBasic()

# Template and static files setup
templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")


def verify_telegram_web_app_data(init_data: str) -> Optional[Dict]:
    """Verifies Telegram Web App data"""
    try:
        # Parse data
        parsed_data = urllib.parse.parse_qs(init_data)

        # Extract hash
        received_hash = parsed_data.get("hash", [None])[0]
        if not received_hash:
            return None

        # Create check string
        check_string_items = []
        for key, value in parsed_data.items():
            if key != "hash":
                if isinstance(value, list) and len(value) > 0:
                    check_string_items.append(f"{key}={value[0]}")

        check_string = "\n".join(sorted(check_string_items))

        # Create secret key
        secret_key = hmac.new(
            "WebAppData".encode(), tgbot.BOT_TOKEN.encode(), hashlib.sha256
        ).digest()

        # Calculate hash
        calculated_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()

        # Verify hash
        if calculated_hash == received_hash:
            # Parse user data
            user_data = parsed_data.get("user", [None])[0]
            if user_data:
                user_info = json.loads(user_data)
                return user_info

        return None
    except Exception:
        return None


def authenticate_telegram_user(init_data: Optional[str] = Query(None, alias="tgWebAppData")):
    """Authentication via Telegram Web App"""
    if init_data:
        user_info = verify_telegram_web_app_data(init_data)
        if user_info and user_info.get("id") in tgbot.ADMINS:
            return user_info

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access allowed only for bot administrators",
    )


def authenticate_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """Simple admin authentication (fallback)"""
    is_correct_username = secrets.compare_digest(credentials.username, webapp.ADMIN_USERNAME)
    is_correct_password = secrets.compare_digest(credentials.password, webapp.ADMIN_PASSWORD)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    session: AsyncSession = Depends(get_session),
    init_data: Optional[str] = Query(None, alias="tgWebAppData"),
):
    """Main page with general statistics"""

    # Temporarily simplified check for testing
    # In production, enable full Telegram Web App verification

    try:
        # Get statistics
        user_stats = await Stats.user_stats(session)
        profile_stats = await Stats.profile_stats(session)
        match_stats = await Stats.match_stats(session)
        referral_stats = await Stats.referral_stats(session)

        # Get registration data for the last 30 days
        registration_data = await Stats.get_registration_data(session)

        # Prepare data for charts
        registration_by_day = {}
        for reg in registration_data:
            day = reg["timestamp"].strftime("%Y-%m-%d")
            registration_by_day[day] = registration_by_day.get(day, 0) + 1

        # Data for template
        context = {
            "request": request,
            "user_stats": user_stats,
            "profile_stats": profile_stats,
            "match_stats": match_stats,
            "referral_stats": referral_stats,
            "registration_data": registration_by_day,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_telegram_webapp": bool(init_data),
        }

        return templates.TemplateResponse("dashboard.html", context)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")


@app.get("/api/stats", response_model=Dict[str, Any])
async def get_stats_api(
    session: AsyncSession = Depends(get_session), admin: str = Depends(authenticate_admin)
):
    """API for getting statistics in JSON format"""
    try:
        user_stats = await Stats.user_stats(session)
        profile_stats = await Stats.profile_stats(session)
        match_stats = await Stats.match_stats(session)
        referral_stats = await Stats.referral_stats(session)

        return {
            "user_stats": user_stats,
            "profile_stats": profile_stats,
            "match_stats": match_stats,
            "referral_stats": referral_stats,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")


@app.get("/users")
async def users_page(
    request: Request,
    session: AsyncSession = Depends(get_session),
    admin: str = Depends(authenticate_admin),
):
    """Page with list of users"""
    # Here you can add pagination and filters
    try:
        # Get last 100 users
        registration_data = await Stats.get_registration_data(session)

        context = {
            "request": request,
            "users": registration_data[:100],  # First 100
            "total_users": len(registration_data),
        }

        return templates.TemplateResponse("users.html", context)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting users: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
