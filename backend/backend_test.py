"""
Backend API tests for appsaavy.space
Tests all endpoints using the public URL
"""
import requests
import sys
import json
import time

BASE_URL = "https://agentic-signals.preview.emergentagent.com/api"

class APITester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.failures = []

    def test(self, name, func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n{'='*60}")
        print(f"🔍 Test {self.tests_run}: {name}")
        print('='*60)
        try:
            func()
            self.tests_passed += 1
            print(f"✅ PASSED")
            return True
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            self.failures.append({"test": name, "error": str(e)})
            return False
        except Exception as e:
            print(f"❌ ERROR: {e}")
            self.failures.append({"test": name, "error": f"Exception: {e}"})
            return False

    def summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print(f"📊 TEST SUMMARY")
        print('='*60)
        print(f"Total: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.failures:
            print(f"\n❌ FAILED TESTS:")
            for f in self.failures:
                print(f"  - {f['test']}: {f['error']}")
        
        return 0 if self.tests_passed == self.tests_run else 1


def test_graph(tester):
    """Test GET /api/graph - NEW: expect ~52 signals, 32 providers, 6 aggregators, 210+ links"""
    def run():
        r = requests.get(f"{BASE_URL}/graph", timeout=30)
        print(f"Status: {r.status_code}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        
        data = r.json()
        print(f"Response keys: {list(data.keys())}")
        
        assert "nodes" in data, "Missing 'nodes' key"
        assert "links" in data, "Missing 'links' key"
        assert "stats" in data, "Missing 'stats' key"
        
        nodes = data["nodes"]
        links = data["links"]
        stats = data["stats"]
        
        print(f"Nodes count: {len(nodes)}")
        print(f"Links count: {len(links)}")
        print(f"Stats: {stats}")
        
        # NEW: Check stats match expected counts
        assert stats.get("providers") == 32, f"Expected 32 providers in stats, got {stats.get('providers')}"
        assert stats.get("signals") == 52, f"Expected 52 signals in stats, got {stats.get('signals')}"
        assert stats.get("aggregators") == 6, f"Expected 6 aggregators in stats, got {stats.get('aggregators')}"
        assert stats.get("links") >= 210, f"Expected at least 210 links in stats, got {stats.get('links')}"
        
        # Check node counts (expect ~90 nodes: 32+52+6)
        assert len(nodes) >= 85, f"Expected at least 85 nodes, got {len(nodes)}"
        assert len(nodes) <= 100, f"Expected at most 100 nodes, got {len(nodes)}"
        
        # Check link counts (expect ~210+ links)
        assert len(links) >= 210, f"Expected at least 210 links, got {len(links)}"
        assert len(links) <= 300, f"Expected at most 300 links, got {len(links)}"
        
        # Check node types
        node_types = set(n.get("type") for n in nodes)
        print(f"Node types: {node_types}")
        assert "provider" in node_types, "Missing 'provider' type nodes"
        assert "signal" in node_types, "Missing 'signal' type nodes"
        assert "aggregator" in node_types, "Missing 'aggregator' type nodes"
        
        # Check node structure
        sample_node = nodes[0]
        print(f"Sample node keys: {list(sample_node.keys())}")
        required_keys = ["id", "label", "type", "color", "size", "universes"]
        for key in required_keys:
            assert key in sample_node, f"Node missing required key: {key}"
        
        # Check link structure
        sample_link = links[0]
        print(f"Sample link keys: {list(sample_link.keys())}")
        assert "source" in sample_link, "Link missing 'source'"
        assert "target" in sample_link, "Link missing 'target'"
        assert "kind" in sample_link, "Link missing 'kind'"
        
        print(f"✓ Graph structure valid with NEW signal counts")
    
    tester.test("GET /api/graph (NEW: 52 signals)", run)


def test_universes(tester):
    """Test GET /api/universes"""
    def run():
        r = requests.get(f"{BASE_URL}/universes", timeout=10)
        print(f"Status: {r.status_code}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        
        data = r.json()
        print(f"Universes count: {len(data)}")
        
        # Expect 4 universes
        assert len(data) == 4, f"Expected 4 universes, got {len(data)}"
        
        # Check structure
        for u in data:
            print(f"Universe: {u.get('name')} - {u.get('slug')} - {u.get('color_hex')}")
            assert "name" in u, "Universe missing 'name'"
            assert "slug" in u, "Universe missing 'slug'"
            assert "color_hex" in u, "Universe missing 'color_hex'"
        
        # Check expected universe names (partial match)
        names = [u["name"] for u in data]
        expected_keywords = ["Intent", "Enrichment", "Technographic", "MCP"]
        for keyword in expected_keywords:
            found = any(keyword in name for name in names)
            assert found, f"Missing expected universe keyword: {keyword}"
        
        print(f"✓ All 4 universes present with correct structure")
    
    tester.test("GET /api/universes", run)


def test_providers(tester):
    """Test GET /api/providers"""
    def run():
        r = requests.get(f"{BASE_URL}/providers", timeout=10)
        print(f"Status: {r.status_code}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        
        data = r.json()
        print(f"Providers count: {len(data)}")
        
        # Expect ~32 providers
        assert len(data) >= 25, f"Expected at least 25 providers, got {len(data)}"
        assert len(data) <= 50, f"Expected at most 50 providers, got {len(data)}"
        
        # Check structure
        sample = data[0]
        print(f"Sample provider: {sample.get('name')} - {sample.get('slug')}")
        required_keys = ["name", "slug", "pricing_tier", "universes"]
        for key in required_keys:
            assert key in sample, f"Provider missing required key: {key}"
        
        print(f"✓ Providers list valid")
    
    tester.test("GET /api/providers", run)


def test_provider_apollo(tester):
    """Test GET /api/provider/apollo-io"""
    def run():
        r = requests.get(f"{BASE_URL}/provider/apollo-io", timeout=10)
        print(f"Status: {r.status_code}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        
        data = r.json()
        print(f"Provider name: {data.get('name')}")
        print(f"Slug: {data.get('slug')}")
        
        # Check name
        assert data.get("name") == "Apollo.io", f"Expected name 'Apollo.io', got {data.get('name')}"
        
        # Check structure
        required_keys = ["name", "slug", "connectors", "signals", "aggregators"]
        for key in required_keys:
            assert key in data, f"Provider detail missing key: {key}"
        
        # Check connectors
        connectors = data["connectors"]
        print(f"Connectors count: {len(connectors)}")
        assert len(connectors) > 0, "Expected at least 1 connector"
        
        connector_types = [c.get("connector_type") for c in connectors]
        print(f"Connector types: {connector_types}")
        
        # Check for expected connector types
        expected_types = ["REST API", "MCP Server", "Clay Native"]
        for exp in expected_types:
            assert exp in connector_types, f"Missing expected connector type: {exp}"
        
        # Check MCP URL
        mcp_url = data.get("mcp_url")
        print(f"MCP URL: {mcp_url}")
        assert mcp_url == "https://mcp.apollo.io", f"Expected MCP URL 'https://mcp.apollo.io', got {mcp_url}"
        
        # Check signals
        signals = data["signals"]
        print(f"Signals count: {len(signals)}")
        assert len(signals) > 0, "Expected at least 1 signal"
        
        # Check signal structure
        sample_signal = signals[0]
        print(f"Sample signal: {sample_signal.get('signal_name')} - {sample_signal.get('coverage_quality')}")
        assert "signal_name" in sample_signal, "Signal missing 'signal_name'"
        assert "coverage_quality" in sample_signal, "Signal missing 'coverage_quality'"
        
        # Check aggregators
        aggregators = data["aggregators"]
        print(f"Aggregators count: {len(aggregators)}")
        
        print(f"✓ Apollo.io provider detail valid")
    
    tester.test("GET /api/provider/apollo-io", run)


def test_provider_zoominfo(tester):
    """Test GET /api/provider/zoominfo"""
    def run():
        r = requests.get(f"{BASE_URL}/provider/zoominfo", timeout=10)
        print(f"Status: {r.status_code}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        
        data = r.json()
        print(f"Provider name: {data.get('name')}")
        
        # Check structure
        assert "name" in data, "Missing 'name'"
        assert "connectors" in data, "Missing 'connectors'"
        assert "signals" in data, "Missing 'signals'"
        
        print(f"✓ ZoomInfo provider detail valid")
    
    tester.test("GET /api/provider/zoominfo", run)


def test_provider_crustdata(tester):
    """Test GET /api/provider/crustdata - NEW: check for new signals like Web Traffic, Glassdoor Rating, LinkedIn Followers"""
    def run():
        r = requests.get(f"{BASE_URL}/provider/crustdata", timeout=10)
        print(f"Status: {r.status_code}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        
        data = r.json()
        print(f"Provider name: {data.get('name')}")
        print(f"Slug: {data.get('slug')}")
        
        # Check name
        assert data.get("name") == "Crustdata", f"Expected name 'Crustdata', got {data.get('name')}"
        
        # Check structure
        required_keys = ["name", "slug", "connectors", "signals", "aggregators"]
        for key in required_keys:
            assert key in data, f"Provider detail missing key: {key}"
        
        # Check signals
        signals = data["signals"]
        print(f"Signals count: {len(signals)}")
        assert len(signals) > 0, "Expected at least 1 signal"
        
        # NEW: Check for new signals added from Crustdata research
        signal_names = [s.get("signal_name") for s in signals]
        print(f"Signal names: {signal_names}")
        
        new_signals = ["Web Traffic", "Glassdoor Rating", "LinkedIn Followers"]
        found_new = [s for s in new_signals if s in signal_names]
        print(f"Found new signals: {found_new}")
        
        # At least one of the new signals should be present
        assert len(found_new) > 0, f"Expected at least one of {new_signals} in Crustdata signals, found: {signal_names}"
        
        print(f"✓ Crustdata provider detail includes new signals: {found_new}")
    
    tester.test("GET /api/provider/crustdata (NEW signals)", run)


def test_provider_404(tester):
    """Test GET /api/provider/non-existent-slug returns 404"""
    def run():
        r = requests.get(f"{BASE_URL}/provider/non-existent-provider-xyz", timeout=10)
        print(f"Status: {r.status_code}")
        assert r.status_code == 404, f"Expected 404 for non-existent provider, got {r.status_code}"
        
        print(f"✓ Non-existent provider returns 404")
    
    tester.test("GET /api/provider/non-existent (404)", run)


def test_signals(tester):
    """Test GET /api/signals - NEW: expect ~52 signals with provider details"""
    def run():
        r = requests.get(f"{BASE_URL}/signals", timeout=10)
        print(f"Status: {r.status_code}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        
        data = r.json()
        print(f"Signals count: {len(data)}")
        
        # NEW: Expect ~52 signals (was 28 before)
        assert len(data) >= 50, f"Expected at least 50 signals, got {len(data)}"
        assert len(data) <= 60, f"Expected at most 60 signals, got {len(data)}"
        
        # Check structure
        sample = data[0]
        print(f"Sample signal: {sample.get('name')} - {sample.get('signal_type')} - {sample.get('universe')}")
        required_keys = ["name", "slug", "signal_type", "universe", "field_type", "field_name", 
                        "update_cadence", "description", "providers", "provider_count"]
        for key in required_keys:
            assert key in sample, f"Signal missing required key: {key}"
        
        # Check signal_type distribution
        type_counts = {}
        for s in data:
            st = s.get("signal_type", "Unknown")
            type_counts[st] = type_counts.get(st, 0) + 1
        
        print(f"Signal type distribution: {type_counts}")
        
        # NEW: Verify counts - expect ~30 Property, ~18 Signal, ~4 Entity
        assert type_counts.get("Property", 0) >= 25, f"Expected at least 25 Property signals, got {type_counts.get('Property', 0)}"
        assert type_counts.get("Signal", 0) >= 15, f"Expected at least 15 Signal signals, got {type_counts.get('Signal', 0)}"
        assert type_counts.get("Entity", 0) >= 3, f"Expected at least 3 Entity signals, got {type_counts.get('Entity', 0)}"
        
        # NEW: Check 'Verified Email' has provider_count >= 8
        verified_email = next((s for s in data if s.get("name") == "Verified Email"), None)
        if verified_email:
            print(f"Verified Email provider_count: {verified_email.get('provider_count')}")
            assert verified_email.get("provider_count", 0) >= 8, \
                f"Expected 'Verified Email' to have at least 8 providers, got {verified_email.get('provider_count')}"
        else:
            print("WARNING: 'Verified Email' signal not found in response")
        
        # Check providers array structure
        if sample.get("providers"):
            prov_sample = sample["providers"][0]
            print(f"Sample provider in signal: {prov_sample}")
            assert "name" in prov_sample, "Provider missing 'name'"
            assert "slug" in prov_sample, "Provider missing 'slug'"
            assert "quality" in prov_sample, "Provider missing 'quality'"
        
        print(f"✓ Signals endpoint returns ~52 items with correct structure")
    
    tester.test("GET /api/signals (NEW: ~52 items)", run)


def test_crawl_jobs(tester):
    """Test GET /api/crawl-jobs"""
    def run():
        r = requests.get(f"{BASE_URL}/crawl-jobs", timeout=10)
        print(f"Status: {r.status_code}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        
        data = r.json()
        print(f"Crawl jobs count: {len(data)}")
        print(f"Response type: {type(data)}")
        
        # Should return a list (may be empty)
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        
        print(f"✓ Crawl jobs endpoint returns list")
    
    tester.test("GET /api/crawl-jobs", run)


def test_intel_chat(tester):
    """Test POST /api/intel/chat (SSE streaming)"""
    def run():
        payload = {"message": "Best providers for verified mobile numbers in EMEA?"}
        print(f"Sending message: {payload['message']}")
        
        r = requests.post(f"{BASE_URL}/intel/chat", json=payload, stream=True, timeout=60)
        print(f"Status: {r.status_code}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        
        # Check content type
        content_type = r.headers.get("content-type", "")
        print(f"Content-Type: {content_type}")
        assert "text/event-stream" in content_type, f"Expected SSE content-type, got {content_type}"
        
        # Parse SSE stream
        events = []
        full_answer = ""
        buffer = ""
        
        print("\nStreaming response:")
        for chunk in r.iter_content(chunk_size=1024, decode_unicode=True):
            if chunk:
                buffer += chunk
                parts = buffer.split("\n\n")
                buffer = parts[-1]
                
                for part in parts[:-1]:
                    if part.strip().startswith("data:"):
                        data_str = part.strip()[5:].strip()
                        if data_str:
                            try:
                                event = json.loads(data_str)
                                events.append(event)
                                
                                if event.get("type") == "session":
                                    print(f"  Session: {event.get('session_id')}")
                                elif event.get("type") == "delta":
                                    content = event.get("content", "")
                                    full_answer += content
                                    print(f"  Delta: {content[:50]}..." if len(content) > 50 else f"  Delta: {content}")
                                elif event.get("type") == "done":
                                    print(f"  Done")
                                elif event.get("type") == "error":
                                    print(f"  Error: {event.get('content')}")
                            except json.JSONDecodeError:
                                pass
        
        print(f"\nTotal events received: {len(events)}")
        print(f"Full answer length: {len(full_answer)} chars")
        
        # Check we got expected event types
        event_types = [e.get("type") for e in events]
        print(f"Event types: {event_types}")
        
        assert "session" in event_types, "Missing 'session' event"
        assert "delta" in event_types, "Missing 'delta' events (no streaming)"
        assert "done" in event_types, "Missing 'done' event"
        
        # Check we got multiple delta events (streaming, not one blob)
        delta_count = event_types.count("delta")
        print(f"Delta events count: {delta_count}")
        assert delta_count > 1, f"Expected multiple delta events (streaming), got {delta_count}"
        
        # Check answer is not empty
        assert len(full_answer) > 50, f"Answer too short: {len(full_answer)} chars"
        
        # Check answer mentions real providers (should be wrapped in [[brackets]])
        print(f"\nAnswer preview (first 300 chars):")
        print(full_answer[:300])
        
        # Check for [[entity]] pattern
        has_brackets = "[[" in full_answer and "]]" in full_answer
        print(f"\nContains [[entity]] links: {has_brackets}")
        
        # Check for known provider names (case-insensitive)
        known_providers = ["cognism", "lusha", "apollo", "zoominfo", "clearbit"]
        answer_lower = full_answer.lower()
        found_providers = [p for p in known_providers if p in answer_lower]
        print(f"Found known providers: {found_providers}")
        
        assert len(found_providers) > 0, "Answer should reference at least one real provider from the graph"
        
        print(f"✓ Intel chat streaming works correctly")
    
    tester.test("POST /api/intel/chat (SSE streaming)", run)


def main():
    print("="*60)
    print("🚀 APPSAAVY.SPACE BACKEND API TESTS")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print()
    
    tester = APITester()
    
    # Run all tests
    test_graph(tester)
    test_signals(tester)  # NEW
    test_universes(tester)
    test_providers(tester)
    test_provider_apollo(tester)
    test_provider_zoominfo(tester)
    test_provider_crustdata(tester)  # NEW
    test_provider_404(tester)
    test_crawl_jobs(tester)
    test_intel_chat(tester)
    
    # Print summary
    return tester.summary()


if __name__ == "__main__":
    sys.exit(main())
