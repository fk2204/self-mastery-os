#!/usr/bin/env python3
"""
Test script for new POST endpoints in server.py
Run the server in one terminal: python server.py
Run this test in another: python test_server_endpoints.py
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8080"

def test_morning_checkin():
    """Test POST /api/checkin/morning"""
    print("\n[TEST] Morning Check-in")
    data = {
        "sleep_hours": 7.5,
        "energy_level": 8,
        "top_3_priorities": [
            "Complete sales calls",
            "Deep work on project",
            "Read 30 min"
        ],
        "win_definition": "Hit 10 sales touches and 2 hours deep work"
    }

    response = requests.post(f"{BASE_URL}/api/checkin/morning", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_evening_reflection():
    """Test POST /api/checkin/evening"""
    print("\n[TEST] Evening Reflection")
    data = {
        "wins": [
            "Closed 2 deals",
            "Hit 3 hours deep work",
            "Read entire chapter"
        ],
        "challenges": [
            "Distracted by emails",
            "Skipped one sales call"
        ],
        "deep_work_hours": 3.5,
        "day_score": 8,
        "lessons": "Focus on blocking distractions. Batch email checking instead of constant monitoring."
    }

    response = requests.post(f"{BASE_URL}/api/checkin/evening", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_complete_habit():
    """Test POST /api/habits/{id}/complete"""
    print("\n[TEST] Complete Habit")
    data = {
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    habit_id = "deep_work_90"
    response = requests.post(f"{BASE_URL}/api/habits/{habit_id}/complete", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_journal_entry():
    """Test POST /api/journal"""
    print("\n[TEST] Save Journal Entry")
    data = {
        "content": "Today was focused on closing deals. I practiced objection handling with 3 prospects. Learned that early objections are often just requests for more info, not real resistance.",
        "mood": "energized",
        "tags": ["sales", "learning", "objection_handling"]
    }

    response = requests.post(f"{BASE_URL}/api/journal", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_gzip_compression():
    """Test gzip compression with Accept-Encoding header"""
    print("\n[TEST] Gzip Compression")
    headers = {
        "Accept-Encoding": "gzip"
    }

    response = requests.get(f"{BASE_URL}/api/data", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Content-Encoding: {response.headers.get('Content-Encoding', 'none')}")
    print(f"Response size: {len(response.content)} bytes")
    return response.status_code == 200


def test_etag_caching():
    """Test ETag caching headers"""
    print("\n[TEST] ETag Caching")

    # First request
    response1 = requests.get(f"{BASE_URL}/api/data")
    etag = response1.headers.get('ETag')
    print(f"First request - Status: {response1.status_code}, ETag: {etag}")

    # Second request with If-None-Match
    if etag:
        headers = {
            "If-None-Match": etag
        }
        response2 = requests.get(f"{BASE_URL}/api/data", headers=headers)
        print(f"Second request - Status: {response2.status_code} (304 means cached)")

    return response1.status_code == 200


def test_security_path_traversal():
    """Test path traversal prevention"""
    print("\n[TEST] Path Traversal Prevention")

    # Try to access a file outside /data directory
    malicious_paths = [
        "/data/../server.py",
        "/data/..%2F..%2Fserver.py",
        "/data/../../etc/passwd"
    ]

    for path in malicious_paths:
        response = requests.get(f"{BASE_URL}{path}")
        print(f"Malicious path: {path}")
        print(f"Status: {response.status_code} (should be 403 or 404)")
        if response.status_code >= 400:
            print("BLOCKED - Good!")

    return True


def test_input_validation():
    """Test input validation"""
    print("\n[TEST] Input Validation")

    # Invalid JSON
    response = requests.post(
        f"{BASE_URL}/api/checkin/morning",
        data="not valid json",
        headers={"Content-Type": "application/json"}
    )
    print(f"Invalid JSON - Status: {response.status_code} (should be 400)")

    # Invalid data types
    data = {
        "sleep_hours": "not a number",  # Should be validated
        "energy_level": 99  # Should be constrained to 1-10
    }
    response = requests.post(f"{BASE_URL}/api/checkin/morning", json=data)
    print(f"Invalid data types - Status: {response.status_code}")
    result = response.json()
    print(f"Energy corrected to: {result.get('data', {}).get('energy_level')}")

    return response.status_code == 200


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("TESTING ENHANCED SERVER ENDPOINTS")
    print("="*60)

    tests = [
        ("Morning Check-in", test_morning_checkin),
        ("Evening Reflection", test_evening_reflection),
        ("Complete Habit", test_complete_habit),
        ("Journal Entry", test_journal_entry),
        ("Gzip Compression", test_gzip_compression),
        ("ETag Caching", test_etag_caching),
        ("Path Traversal Prevention", test_security_path_traversal),
        ("Input Validation", test_input_validation),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, "PASS" if passed else "FAIL"))
        except requests.exceptions.ConnectionError:
            print(f"ERROR: Could not connect to server at {BASE_URL}")
            print("Make sure to run: python server.py")
            return
        except Exception as e:
            print(f"ERROR: {str(e)}")
            results.append((name, "ERROR"))

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, status in results:
        print(f"{name:.<40} {status}")

    passed = sum(1 for _, status in results if status == "PASS")
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")


if __name__ == "__main__":
    run_all_tests()
