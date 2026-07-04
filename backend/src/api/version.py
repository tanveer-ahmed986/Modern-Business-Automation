from fastapi import APIRouter
import sys
import platform

router = APIRouter(prefix="/version", tags=["version"])

@router.get("")
def get_version_info():
    """Get API version and system information.

    Useful for PWA clients to verify backend compatibility.
    """
    return {
        "api_version": "v1",
        "app_version": "2.1.0",
        "app_name": "MBAS - Modern Business Automation System",
        "vendor": "Z&T Technologies",
        "website": "www.zttechnologies.org",
        "python_version": sys.version,
        "python_min": "3.10",
        "python_max": "3.12",
        "platform": platform.system(),
        "platform_release": platform.release(),
        "pwa_enabled": True,
        "offline_capable": True,
        "features": {
            "inventory": True,
            "billing": True,
            "reports": True,
            "dashboard": True,
            "suppliers": True,
            "purchases": True,
            "users": True,
            "ai_analytics": True,
            "automatic_backup": True
        }
    }
