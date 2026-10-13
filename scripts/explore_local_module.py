#!/usr/bin/env python3
"""Explore local Estyma module API

Set your local Vide.Net module IP in MODULE_IP variable.
Find it in your boiler's network configuration or admin panel.
"""

import requests
import json
from urllib.parse import urljoin

MODULE_IP = "YOUR_MODULE_IP"  # e.g., 192.168.1.100
PORTS = [80, 8080, 5000, 3000, 9000, 8000]
PATHS = [
    "/",
    "/index.html",
    "/api",
    "/api/v1",
    "/api/device",
    "/api/data",
    "/api/status",
    "/api/boiler",
    "/api/info",
    "/status",
    "/info",
    "/version",
    "/config",
]

def test_port(port):
    """Test if port is open."""
    url = f"http://{MODULE_IP}:{port}/"
    try:
        response = requests.get(url, timeout=2)
        return True, response.status_code
    except requests.exceptions.ConnectionError:
        return False, None
    except requests.exceptions.Timeout:
        return False, "timeout"
    except Exception as e:
        return False, str(e)

def test_endpoint(port, path):
    """Test specific endpoint."""
    url = f"http://{MODULE_IP}:{port}{path}"
    try:
        response = requests.get(url, timeout=3)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("content-type", ""),
            "size": len(response.text),
            "text": response.text[:500],
            "json": response.json() if "json" in response.headers.get("content-type", "") else None,
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    print("\n" + "="*70)
    print("🔍 Estyma Module Explorer - Local Network")
    print(f"Target: {MODULE_IP}")
    print("="*70 + "\n")

    # Step 1: Port scan
    print("🔌 Scanning ports...\n")
    open_ports = []
    for port in PORTS:
        is_open, status = test_port(port)
        symbol = "✓" if is_open else "✗"
        print(f"  {symbol} Port {port:5} → {status}")
        if is_open:
            open_ports.append(port)

    if not open_ports:
        print("\n❌ No open ports found!")
        return

    # Step 2: Explore endpoints
    print(f"\n\n📍 Testing endpoints on open ports...\n")

    results = {}
    for port in open_ports:
        print(f"\n--- Port {port} ---")
        results[port] = {}

        for path in PATHS:
            result = test_endpoint(port, path)

            if "error" not in result:
                print(f"  GET {path:25} → {result['status']}")
                results[port][path] = result

                # Show content preview
                if result["status"] == 200 and result["json"]:
                    print(f"      JSON: {str(result['json'])[:100]}")
                elif result["status"] == 200:
                    print(f"      Content: {result['text'][:80]}")

    # Step 3: Save results
    output_file = "module_exploration.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n\n✅ Results saved to: {output_file}")
    print("Please share this file!")

if __name__ == "__main__":
    main()
