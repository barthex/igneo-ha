#!/usr/bin/env python3
"""Explore igneo.pl API - reverse engineering."""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_path = Path(__file__).parent.parent / "envs" / ".env.local"
load_dotenv(env_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

if not USERNAME or not PASSWORD:
    raise ValueError("Missing USERNAME or PASSWORD in envs/.env.local")

BASE_URL = "https://igneo.pl"
SESSION = requests.Session()

def log(message: str, data=None):
    """Print formatted log message."""
    print(f"\n{'='*60}")
    print(f"🔍 {message}")
    print('='*60)
    if data:
        if isinstance(data, dict):
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(data)

def login():
    """Attempt login to igneo.pl."""
    log("Attempting login", {"username": USERNAME})

    try:
        response = SESSION.post(
            f"{BASE_URL}/login",
            data={"username": USERNAME, "password": PASSWORD},
            allow_redirects=True,
            timeout=5
        )

        print(f"Login response status: {response.status_code}")
        print(f"Final URL: {response.url}")

        if response.status_code == 200:
            log("✅ Login successful")

            # Check cookies
            if SESSION.cookies:
                log("Session cookies", dict(SESSION.cookies))

            return True

    except Exception as e:
        log("❌ Login error", str(e))

    return False

def explore_endpoints():
    """Probe API endpoints."""
    log("Exploring API endpoints")

    paths = [
        "/api",
        "/api/v1",
        "/api/user",
        "/api/devices",
        "/api/device",
        "/api/boiler",
        "/api/data",
        "/api/status",
    ]

    for path in paths:
        url = f"{BASE_URL}{path}"
        try:
            response = SESSION.get(url, timeout=3)
            print(f"GET {path:25} → {response.status_code}")

            if response.status_code == 200 and response.text:
                try:
                    data = response.json()
                    log(f"Data from {path}", data)
                except:
                    pass
        except Exception as e:
            print(f"GET {path:25} → Error: {e}")

def main():
    """Main exploration flow."""
    print("\n" + "="*60)
    print("🚀 Estyma Igneo Slim API Explorer")
    print("="*60)

    login()
    explore_endpoints()

if __name__ == "__main__":
    main()
