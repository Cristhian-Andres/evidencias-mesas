import subprocess, sys, os, io
subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "pandas", "openpyxl", "lxml", "-q"], check=True)

from playwright.sync_api import sync_playwright
import pandas as pd

htmlview_url = (
    "https://docs.google.com/spreadsheets/d/1re_7dntD3PCO_8OWDZMApfCixEO2OeMp/htmlview"
    "?usp=drive_link&ouid=101456306008062258019&rtpof=true&sd=true"
    "&pru=AAABnq03h7E*TRFTLJVnXgkrVD6qsMC1-g"
)

output_file = os.path.abspath("evidencias_mesas.xlsx")
sheet_responses = {}

def handle_response(response):
    url = response.url
    if "htmlview/sheet" in url and "headers=true" in url:
        try:
            body = response.body()
            if len(body) > 1000:
                sheet_responses[url] = body
                print(f"  Capturado: {len(body)} bytes — {url[-60:]}")
        except:
            pass

print("Cargando página e interceptando datos...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.on("response", handle_response)
    page.goto(htmlview_url, wait_until="load", timeout=30000)
    page.wait_for_timeout(8000)
    browser.close()

if not sheet_responses:
    print("No se capturaron datos. Intenta de nuevo.")
    exit(1)

print(f"\nProcesando {len(sheet_responses)} hoja(s)...")
all_sheets = {}
for url, body in sheet_responses.items():
    # Extraer gid del URL para nombrar la hoja
    gid = url.split("gid=")[-1].split("&")[0] if "gid=" in url else "Hoja"
    html_content = body.decode("utf-8", errors="replace")
    tables = pd.read_html(io.StringIO(html_content))
    if tables:
        df = tables[0]
        # Usar primera fila como headers si aplica
        if df.iloc[0].notna().all():
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)
        all_sheets[gid] = df
        print(f"  Hoja {gid}: {len(df)} filas x {len(df.columns)} columnas")

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for name, df in all_sheets.items():
        df.to_excel(writer, sheet_name=str(name)[:31], index=False)

print(f"\nArchivo guardado: {output_file}")
