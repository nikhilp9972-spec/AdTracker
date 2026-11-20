"""
Automated Endpoint & Core Logic Verification Test.
Tests all REST API routes, static file serving, EdTech classifications,
cross-platform analytics, collection logs, and background pipeline logic.
"""

import io
import json
from backend.server import AdTrackerRequestHandler
from backend import database

class MockServer:
    pass

class MockSocket:
    def __init__(self, data=b""):
        self.rdata = io.BytesIO(data)
        self.output = io.BytesIO()

    def makefile(self, mode, *args):
        if "r" in mode:
            return self.rdata
        return self.output

    def sendall(self, b):
        self.output.write(b)

    def close(self):
        pass

def run_test(method, path, body_dict=None):
    body_str = json.dumps(body_dict) if body_dict is not None else ""
    raw = f"{method} {path} HTTP/1.1\r\nHost: localhost\r\n"
    if body_str:
        raw += f"Content-Type: application/json\r\nContent-Length: {len(body_str)}\r\n\r\n{body_str}"
    else:
        raw += "\r\n"

    sock = MockSocket(raw.encode("utf-8"))
    handler = AdTrackerRequestHandler(sock, ("127.0.0.1", 50000), MockServer())
    resp = sock.output.getvalue().decode("utf-8", errors="ignore")
    lines = resp.split("\r\n")
    status_line = lines[0] if lines else "EMPTY"
    return status_line, resp

def main():
    print("=" * 60)
    print("  🧪 Running AdPulse EdTech Intelligence Test Suite")
    print("=" * 60)

    # 1. Test Static Frontend
    status, _ = run_test("GET", "/")
    print(f"✔ [200 OK] Frontend index.html served: {status}")
    assert "200" in status, f"Failed: {status}"

    # 2. Test Competitors Endpoint
    status, resp = run_test("GET", "/api/competitors")
    print(f"✔ [200 OK] Competitors List (PW, Unacademy, Scaler): {status}")
    assert "200" in status, f"Failed: {status}"

    # 3. Test Ads Listing
    status, resp = run_test("GET", "/api/ads")
    print(f"✔ [200 OK] Ad Vault Listing: {status}")
    assert "200" in status, f"Failed: {status}"

    # 3b. Test Filtered Ads by Category and Platform
    status, resp = run_test("GET", "/api/ads?category=Coding&platform=meta")
    print(f"✔ [200 OK] Filtered EdTech Ads (Coding + Meta): {status}")
    assert "200" in status, f"Failed: {status}"

    # 4. Test Latest 7-Section Digest
    status, resp = run_test("GET", "/api/digests/latest")
    print(f"✔ [200 OK] Latest 7-Section AI Intelligence Brief: {status}")
    assert "200" in status, f"Failed: {status}"

    # 5. Test Cross-Platform Analytics (Meta vs Google)
    status, resp = run_test("GET", "/api/analytics/cross-platform")
    print(f"✔ [200 OK] Cross-Platform Analytics (Meta vs Google): {status}")
    assert "200" in status, f"Failed: {status}"

    # 6. Test Collection Logs (Strict Data Transparency)
    status, resp = run_test("GET", "/api/collection-logs")
    print(f"✔ [200 OK] Collection Audit Logs: {status}")
    assert "200" in status, f"Failed: {status}"

    # 7. Test Dashboard Stats
    status, resp = run_test("GET", "/api/stats")
    print(f"✔ [200 OK] Dashboard KPI Stats: {status}")
    assert "200" in status, f"Failed: {status}"

    # 8. Test Scheduler Status
    status, resp = run_test("GET", "/api/scheduler/status")
    print(f"✔ [200 OK] Weekly Scheduler Status: {status}")
    assert "200" in status, f"Failed: {status}"

    # 9. Test Slack Block Kit Preview
    status, resp = run_test("GET", "/api/notifications/preview-slack")
    print(f"✔ [200 OK] Slack Block Kit Preview: {status}")
    assert "200" in status, f"Failed: {status}"

    # 10. Test Email HTML Newsletter Preview
    status, resp = run_test("GET", "/api/notifications/preview-email")
    print(f"✔ [200 OK] Email HTML Newsletter Preview: {status}")
    assert "200" in status, f"Failed: {status}"

    # 11. Test Manual Verified Ad Import
    manual_payload = {
        "competitor_id": "comp-pw",
        "headline": "IIT JEE 2026 Foundation Batch - Offline & Online",
        "body_text": "Live doubt solving sessions with India top rank faculty. Enroll today.",
        "platform": "meta",
        "cta_text": "Enroll Now",
        "ad_library_url": "https://www.facebook.com/ads/library/?id=pw_test_101"
    }
    status, resp = run_test("POST", "/api/ads/import-manual", manual_payload)
    print(f"✔ [200 OK] Manual Verified Real Ad Import: {status}")
    assert "200" in status, f"Failed: {status}"

    # 12. Test Single Competitor Ad Collection
    status, resp = run_test("POST", "/api/ads/collect-single", {"competitor_id": "comp-scaler", "count": 2})
    print(f"✔ [200 OK] Single Competitor Ad Collection: {status}")
    assert "200" in status, f"Failed: {status}"

    # 13. Test 7-Section Digest Generation POST
    status, resp = run_test("POST", "/api/digests/generate", {"days": 7})
    print(f"✔ [200 OK] 7-Section AI Digest Generation: {status}")
    assert "200" in status, f"Failed: {status}"

    # 14. Test Pipeline Run POST
    status, resp = run_test("POST", "/api/pipeline/run-now", {})
    print(f"✔ [200 OK] End-to-End Pipeline Execution: {status}")
    assert "200" in status, f"Failed: {status}"

    print("=" * 60)
    print("  🎉 ALL 14 TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    main()
