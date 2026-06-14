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
    """Test GET /api/graph"""
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
        
        # Check node counts (expect ~66 nodes)
        assert len(nodes) >= 50, f"Expected at least 50 nodes, got {len(nodes)}"
        assert len(nodes) <= 100, f"Expected at most 100 nodes, got {len(nodes)}"
        
        # Check link counts (expect ~150 links)
        assert len(links) >= 100, f"Expected at least 100 links, got {len(links)}"
        assert len(links) <= 250, f"Expected at most 250 links, got {len(links)}"
        
        # Check node types
        node_types = set(n.get("type") for n in nodes)
        print(f"Node types: {node_types}")
        assert "provider" in node_types, "Missing 'provider' type nodes"
        assert "signal" in node_types, "Missing 'signal' type nodes"
        
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
        
        print(f"✓ Graph structure valid")
    
    tester.test("GET /api/graph", run)


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


def test_provider_404(tester):
    """Test GET /api/provider/non-existent-slug returns 404"""
    def run():
        r = requests.get(f"{BASE_URL}/provider/non-existent-provider-xyz", timeout=10)
        print(f"Status: {r.status_code}")
        assert r.status_code == 404, f"Expected 404 for non-existent provider, got {r.status_code}"
        
        print(f"✓ Non-existent provider returns 404")
    
    tester.test("GET /api/provider/non-existent (404)", run)


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
    test_universes(tester)
    test_providers(tester)
    test_provider_apollo(tester)
    test_provider_zoominfo(tester)
    test_provider_404(tester)
    test_crawl_jobs(tester)
    test_intel_chat(tester)
    
    # Print summary
    return tester.summary()


if __name__ == "__main__":
    sys.exit(main())
