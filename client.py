import re
from typing import Dict, Any, List, Optional

class DOMSemanticAccessibilityTreePruner:
    """
    Strips non-semantic elements (scripts, styles, SVGs, nested wrappers)
    and produces an interactive accessibility map annotated with discrete selector IDs.
    """
    INTERACTIVE_ROLES = {"button", "link", "input", "select", "textarea", "checkbox", "radio", "tab", "menuitem"}

    def prune_dom_tree(self, raw_elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        compact_tree: List[Dict[str, Any]] = []
        interactive_lookup: Dict[str, Dict[str, Any]] = {}
        element_counter = 1

        for el in raw_elements:
            tag = el.get("tag", "").lower()
            role = el.get("role", "").lower()
            is_visible = el.get("visible", True)

            # Skip hidden or script tags
            if not is_visible or tag in ["script", "style", "noscript", "meta", "link"]:
                continue

            text = el.get("text", "").strip()
            aria_label = el.get("aria_label", "").strip()
            effective_label = aria_label or text

            is_interactive = (
                tag in ["button", "a", "input", "select", "textarea"] or
                role in self.INTERACTIVE_ROLES or
                el.get("onclick") or
                el.get("tabindex") is not None
            )

            if is_interactive:
                node_id = f"el_{element_counter:03d}"
                element_counter += 1
                node_info = {
                    "id": node_id,
                    "tag": tag,
                    "role": role if role else tag,
                    "label": effective_label,
                    "bbox": el.get("bbox", {"x": 0, "y": 0, "w": 0, "h": 0}),
                    "disabled": el.get("disabled", False)
                }
                compact_tree.append(node_info)
                interactive_lookup[node_id] = node_info
            elif effective_label and len(effective_label) > 1:
                # Keep significant static text
                compact_tree.append({
                    "id": None,
                    "tag": tag,
                    "role": "text",
                    "label": effective_label[:150],
                    "bbox": el.get("bbox", {"x": 0, "y": 0, "w": 0, "h": 0})
                })

        return {
            "total_raw_elements": len(raw_elements),
            "retained_elements_count": len(compact_tree),
            "interactive_targets_count": len(interactive_lookup),
            "compression_ratio": round((1.0 - (len(compact_tree) / max(1, len(raw_elements)))) * 100, 1),
            "accessibility_tree": compact_tree,
            "interactive_lookup": interactive_lookup
        }
