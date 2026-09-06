import json
from client import DOMSemanticAccessibilityTreePruner

def main():
    pruner = DOMSemanticAccessibilityTreePruner()
    raw_nodes = [
        {"tag": "script", "text": "var analytics = 1;", "visible": True},
        {"tag": "div", "role": "banner", "text": "Acme Portal", "visible": True},
        {"tag": "input", "role": "input", "aria_label": "Search docs", "visible": True, "bbox": {"x": 100, "y": 20, "w": 200, "h": 35}},
        {"tag": "button", "role": "button", "text": "Sign In", "visible": True, "bbox": {"x": 400, "y": 20, "w": 80, "h": 35}},
        {"tag": "style", "text": ".btn { color: red; }", "visible": True}
    ]
    result = pruner.prune_dom_tree(raw_nodes)
    print("Pruned Accessibility Tree:")
    print(json.dumps(result, indent=2))
    assert result["interactive_targets_count"] == 2
    assert "el_001" in result["interactive_lookup"]
    print("DOM pruner verification complete: PASS")

if __name__ == "__main__":
    main()
