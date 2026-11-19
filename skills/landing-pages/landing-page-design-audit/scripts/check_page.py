#!/usr/bin/env python3
"""Page QA: links, console errors, widths, form, keyboard. Usage: python check_page.py <file-or-url> [--json]"""
import sys, json, os, re
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

WIDTHS = [1440, 768, 390]

def main(target, as_json=False):
    url = target if re.match(r"^https?://|^file://", target) else "file://" + os.path.abspath(target)
    out = {"target": target, "errors": [], "widths": {}, "links": [], "form": [], "keyboard": {}}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        console = []
        pg.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: console.append(str(e)))
        pg.goto(url, wait_until="load", timeout=30000)
        out["console_errors"] = console
        # widths: horizontal scroll and cut-off
        for w in WIDTHS:
            pg.set_viewport_size({"width": w, "height": 900})
            pg.wait_for_timeout(200)
            sw, cw = pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            small = pg.evaluate("""() => [...document.querySelectorAll('a,button,input,select,textarea')]
                .filter(e => { const r = e.getBoundingClientRect(); return r.width>0 && (r.height < 44 || r.width < 44) && getComputedStyle(e).visibility!='hidden'; }).length""")
            out["widths"][w] = {"horizontal_scroll": sw > cw + 1, "scrollWidth": sw, "clientWidth": cw, "small_tap_targets": small}
        pg.set_viewport_size({"width": 1440, "height": 900})
        # links
        hrefs = pg.evaluate("[...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'))")
        seen = set()
        for h in hrefs:
            if h in seen or h.startswith(("mailto:", "tel:", "javascript:")): continue
            seen.add(h)
            if h.startswith("#"):
                ok = h == "#" or pg.evaluate("id => !!document.getElementById(id)", h[1:])
                out["links"].append({"href": h, "ok": bool(ok), "kind": "anchor"})
            else:
                full = urljoin(url, h)
                if full.startswith("file://"):
                    out["links"].append({"href": h, "ok": os.path.exists(urlparse(full).path), "kind": "file"})
                else:
                    try:
                        r = pg.request.get(full, timeout=15000)
                        out["links"].append({"href": h, "ok": r.status < 400, "status": r.status, "kind": "http"})
                    except Exception as e:
                        out["links"].append({"href": h, "ok": False, "error": str(e)[:80], "kind": "http"})
        # forms: empty submit, bad email
        forms = pg.query_selector_all("form")
        out["form_count"] = len(forms)
        for i, f in enumerate(forms):
            res = {"form": i}
            res["labels_missing"] = pg.evaluate("""f => [...f.querySelectorAll('input:not([type=hidden]):not([type=submit]),select,textarea')]
                .filter(e => !(e.id && document.querySelector('label[for="'+e.id+'"]')) && !e.closest('label') && !e.getAttribute('aria-label')).length""", f)
            email = f.query_selector("input[type=email], input[name*=mail i]")
            if email:
                email.fill("not-an-email")
            btn = f.query_selector("button[type=submit], input[type=submit], button")
            if btn:
                btn.click(); pg.wait_for_timeout(300)
                res["shows_error_on_bad_input"] = pg.evaluate("f => !!f.querySelector(':invalid') || !!document.querySelector('[role=alert], .error, .invalid-feedback, [class*=error]')", f)
            out["form"].append(res)
        # keyboard: tab through, count reachable focusables and focus visibility
        total = pg.evaluate("[...document.querySelectorAll('a[href],button,input,select,textarea,[tabindex]:not([tabindex=\"-1\"])')].length")
        reached, visible_focus, last = 0, 0, None
        for _ in range(min(total + 3, 80)):
            pg.keyboard.press("Tab")
            info = pg.evaluate("""() => { const e = document.activeElement; if (!e || e===document.body) return null; const s = getComputedStyle(e);
                return {id: e.outerHTML.slice(0,60), outline: s.outlineStyle!=='none' && parseFloat(s.outlineWidth)>0, shadow: s.boxShadow!=='none'}; }""")
            if info and info["id"] != last:
                reached += 1; last = info["id"]
                if info["outline"] or info["shadow"]: visible_focus += 1
        out["keyboard"] = {"focusable": total, "reached_by_tab": reached, "with_visible_focus": visible_focus}
        out["h1_count"] = pg.evaluate("document.querySelectorAll('h1').length")
        out["lang_dir"] = pg.evaluate("[document.documentElement.lang, document.documentElement.dir || getComputedStyle(document.body).direction]")
        b.close()
    bad_links = [l for l in out["links"] if not l["ok"]]
    out["summary"] = {"console_errors": len(out["console_errors"]), "broken_links": len(bad_links),
                      "horizontal_scroll_at": [w for w, v in out["widths"].items() if v["horizontal_scroll"]],
                      "h1_count": out["h1_count"]}
    print(json.dumps(out, ensure_ascii=False, indent=2) if as_json else json.dumps(out["summary"], ensure_ascii=False, indent=2))
    return out

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    main(sys.argv[1], "--json" in sys.argv)
