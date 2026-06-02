import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "-q"], check=True)

from playwright.sync_api import sync_playwright

htmlview_url = (
    "https://docs.google.com/spreadsheets/d/1re_7dntD3PCO_8OWDZMApfCixEO2OeMp/htmlview"
    "?usp=drive_link&ouid=101456306008062258019&rtpof=true&sd=true"
    "&pru=AAABnq03h7E*TRFTLJVnXgkrVD6qsMC1-g"
)

captured = []

def handle_response(response):
    url = response.url
    if any(x in url for x in ["tq?", "gviz", "export", "download", "waffle", "spreadsheets"]):
        try:
            body = response.body()
            if len(body) > 200:
                captured.append({"url": url[:120], "size": len(body), "status": response.status})
        except:
            pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.on("response", handle_response)

    page.goto(htmlview_url, wait_until="load", timeout=30000)
    page.wait_for_timeout(8000)

    # Ver qué hay en el viewport renderizado
    viewport_content = page.evaluate("""() => {
        const vp = document.getElementById('sheets-viewport');
        if (!vp) return 'no viewport';
        const children = vp.children;
        const result = [];
        for (let i = 0; i < Math.min(children.length, 5); i++) {
            result.push({tag: children[i].tagName, cls: children[i].className.substring(0, 50)});
        }
        return result;
    }""")
    print("Contenido del viewport:", viewport_content)

    # Buscar table.waffle via JavaScript
    waffle_info = page.evaluate("""() => {
        const waffle = document.querySelector('table.waffle');
        if (!waffle) return 'no waffle table found';
        const rows = waffle.querySelectorAll('tr');
        const first_row = rows[0] ? Array.from(rows[0].querySelectorAll('td, th')).map(c => c.innerText.substring(0, 20)) : [];
        return {rows: rows.length, first_row: first_row};
    }""")
    print("Waffle table:", waffle_info)

    browser.close()

print(f"\nURLs capturadas ({len(captured)}):")
for c in captured[:15]:
    print(f"  [{c['status']}] {c['size']} bytes — {c['url']}")
