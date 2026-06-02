import json, os

with open('dashboard_data.json', encoding='utf-8') as f:
    DATA = f.read()

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Dashboard Electoral — Abelardo De La Espriella</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root{--bg:#0d1117;--card:#161b22;--border:#30363d;--accent:#58a6ff;--green:#3fb950;--red:#f85149;--yellow:#d29922;--purple:#bc8cff;--text:#e6edf3;--muted:#8b949e;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;}
.hero{background:linear-gradient(135deg,#0d1117 0%,#1a2744 50%,#0d1117 100%);border-bottom:1px solid var(--border);padding:32px 24px 24px;text-align:center;position:relative;overflow:hidden;}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% -20%,rgba(88,166,255,.15) 0%,transparent 60%);}
.hero-badge{display:inline-block;background:rgba(88,166,255,.1);border:1px solid rgba(88,166,255,.3);color:var(--accent);padding:4px 14px;border-radius:20px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px;}
.hero h1{font-size:clamp(22px,4vw,38px);font-weight:700;letter-spacing:-.5px;margin-bottom:6px;}
.hero h1 span{color:var(--accent);}
.hero p{color:var(--muted);font-size:14px;}
.filters{background:var(--card);border-bottom:1px solid var(--border);padding:14px 24px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;}
.filters label{font-size:12px;color:var(--muted);margin-right:4px;}
.filters select,.filters input{background:#21262d;border:1px solid var(--border);color:var(--text);padding:6px 10px;border-radius:6px;font-size:13px;cursor:pointer;min-width:160px;}
.filters select:focus,.filters input:focus{outline:2px solid var(--accent);border-color:var(--accent);}
.btn-reset{background:rgba(248,81,73,.15);border:1px solid rgba(248,81,73,.4);color:var(--red);padding:6px 14px;border-radius:6px;font-size:13px;cursor:pointer;}
.btn-reset:hover{background:rgba(248,81,73,.25);}
.filter-label{background:rgba(88,166,255,.1);border:1px solid rgba(88,166,255,.2);color:var(--accent);padding:4px 10px;border-radius:4px;font-size:12px;}
.container{max-width:1400px;margin:0 auto;padding:24px;}
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px;margin-bottom:28px;}
.kpi{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:18px 20px;position:relative;overflow:hidden;transition:transform .15s,border-color .15s;}
.kpi:hover{transform:translateY(-2px);border-color:var(--accent);}
.kpi::after{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:10px 10px 0 0;}
.kpi.blue::after{background:var(--accent);}
.kpi.green::after{background:var(--green);}
.kpi.yellow::after{background:var(--yellow);}
.kpi.red::after{background:var(--red);}
.kpi.purple::after{background:var(--purple);}
.kpi-icon{font-size:22px;margin-bottom:8px;}
.kpi-val{font-size:26px;font-weight:700;line-height:1;margin-bottom:4px;}
.kpi-label{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;}
.kpi-sub{font-size:12px;color:var(--muted);margin-top:4px;}
.section-title{font-size:16px;font-weight:600;color:var(--text);margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;}
.section-title::before{content:'';width:3px;height:18px;background:var(--accent);border-radius:2px;display:inline-block;}
.charts-row{display:grid;gap:18px;margin-bottom:22px;}
.charts-2{grid-template-columns:1fr 1fr;}
.charts-3{grid-template-columns:1fr 1fr 1fr;}
.charts-half{grid-template-columns:2fr 1fr;}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px;}
.chart-card h3{font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:16px;}
.chart-wrap{position:relative;}
.alerts-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-bottom:22px;}
.alert-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:16px;}
.alert-card.warn{border-color:rgba(248,81,73,.4);background:rgba(248,81,73,.05);}
.alert-card.ok{border-color:rgba(63,185,80,.3);background:rgba(63,185,80,.04);}
.alert-card h4{font-size:13px;font-weight:600;margin-bottom:10px;}
.alert-card .big{font-size:32px;font-weight:700;line-height:1;}
.alert-card .big.red{color:var(--red);}
.alert-card .big.green{color:var(--green);}
.alert-card p{font-size:12px;color:var(--muted);margin-top:4px;}
.analysis{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:22px;margin-bottom:22px;}
.analysis-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin-top:16px;}
.finding{padding:14px;background:#0d1117;border-radius:8px;border-left:3px solid var(--accent);}
.finding.warn{border-color:var(--red);}
.finding.info{border-color:var(--yellow);}
.finding h5{font-size:13px;font-weight:600;margin-bottom:6px;}
.finding p{font-size:12px;color:var(--muted);line-height:1.5;}
.table-controls{display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap;align-items:center;}
.search-box{background:#21262d;border:1px solid var(--border);color:var(--text);padding:8px 12px;border-radius:6px;font-size:13px;flex:1;min-width:200px;}
.search-box:focus{outline:2px solid var(--accent);}
.table-info{font-size:12px;color:var(--muted);margin-left:auto;}
.table-wrap{overflow-x:auto;border-radius:8px;border:1px solid var(--border);}
table{width:100%;border-collapse:collapse;font-size:12px;}
thead th{background:#21262d;padding:10px 12px;text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);border-bottom:1px solid var(--border);white-space:nowrap;cursor:pointer;user-select:none;}
thead th:hover{color:var(--text);}
tbody tr{border-bottom:1px solid rgba(48,54,61,.6);}
tbody tr:hover{background:rgba(88,166,255,.04);}
tbody td{padding:8px 12px;white-space:nowrap;}
.badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:600;}
.badge-green{background:rgba(63,185,80,.15);color:var(--green);}
.badge-red{background:rgba(248,81,73,.15);color:var(--red);}
.badge-yellow{background:rgba(210,153,34,.15);color:var(--yellow);}
.badge-blue{background:rgba(88,166,255,.15);color:var(--accent);}
.badge-purple{background:rgba(188,140,255,.15);color:var(--purple);}
.pagination{display:flex;gap:6px;margin-top:12px;justify-content:center;align-items:center;flex-wrap:wrap;}
.pagination button{background:var(--card);border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:13px;}
.pagination button:hover{border-color:var(--accent);color:var(--accent);}
.pagination button.active{background:var(--accent);border-color:var(--accent);color:#000;font-weight:600;}
.pagination button:disabled{opacity:.4;cursor:default;}
.page-info{font-size:12px;color:var(--muted);padding:0 8px;}
footer{background:var(--card);border-top:1px solid var(--border);margin-top:40px;padding:40px 24px;text-align:center;}
.footer-title{font-size:20px;font-weight:700;margin-bottom:6px;}
.footer-sub{color:var(--muted);font-size:13px;margin-bottom:24px;}
.social-links{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-bottom:24px;}
.social-link{display:flex;align-items:center;gap:8px;background:#21262d;border:1px solid var(--border);color:var(--text);padding:10px 20px;border-radius:8px;text-decoration:none;font-size:14px;transition:all .15s;}
.social-link:hover{border-color:var(--accent);color:var(--accent);background:rgba(88,166,255,.08);}
.social-icon{width:20px;height:20px;flex-shrink:0;}
.footer-copy{font-size:11px;color:var(--muted);margin-top:20px;}
@media(max-width:768px){.charts-2,.charts-3,.charts-half{grid-template-columns:1fr;}.filters{flex-direction:column;align-items:stretch;}.kpi-grid{grid-template-columns:repeat(2,1fr);}}
</style>
</head>
<body>

<div class="hero">
  <div class="hero-badge">&#128202; Analisis Electoral</div>
  <h1>Evidencias de Mesas &#8212; <span>Abelardo De La Espriella</span></h1>
  <p>5,637 mesas analizadas &nbsp;&#183;&nbsp; 164 municipios &nbsp;&#183;&nbsp; 26 departamentos &nbsp;&#183;&nbsp; Colombia 2026</p>
</div>

<div class="filters">
  <span class="filter-label">&#128269; Filtros</span>
  <div><label>Departamento</label><select id="f-dept" onchange="applyFilters()"><option value="">Todos</option></select></div>
  <div><label>Municipio</label><select id="f-mun" onchange="applyFilters()"><option value="">Todos</option></select></div>
  <div><label>Estado Sobre</label><select id="f-estado" onchange="applyFilters()">
    <option value="">Todos</option><option>BUENO</option><option>MAL</option>
  </select></div>
  <div><label>Var. Subita</label><select id="f-var" onchange="applyFilters()">
    <option value="">Todas</option>
    <option>0. Mínima</option><option>1. Baja</option>
    <option>2. Media</option><option>3. Alta</option><option>4. Muy Alta</option>
  </select></div>
  <div><label>Concentracion</label><select id="f-conc" onchange="applyFilters()">
    <option value="">Todas</option>
    <option>0. Baja</option><option>1. Normal</option>
    <option>2. Alta</option><option>3. Muy Alta</option>
  </select></div>
  <div><label>Excluida</label><select id="f-excl" onchange="applyFilters()">
    <option value="">Todas</option><option>SI</option><option>NO</option>
  </select></div>
  <button class="btn-reset" onclick="resetFilters()">&#8635; Resetear</button>
  <span id="filter-count" class="table-info"></span>
</div>

<div class="container">

<div class="kpi-grid" id="kpi-grid"></div>

<div class="analysis">
  <div class="section-title">Hallazgos Clave del Analisis</div>
  <div class="analysis-grid">
    <div class="finding warn">
      <h5>&#9888;&#65039; Consulados: Mayor Concentracion de Anomalias</h5>
      <p>El 100% de las 676 mesas de Consulados presentan diferencias negativas, acumulando -269,605 votos en diferencias. La participacion promedio es de solo 26.7%, la mas baja de todos los departamentos.</p>
    </div>
    <div class="finding">
      <h5>&#127775; Bogota D.C.: Epicentro Electoral</h5>
      <p>Con 335,919 votos en 2,190 mesas, Bogota representa el 34.2% del total de votos. Participacion promedio del 87.3% y 48.6% de votos para el candidato por mesa.</p>
    </div>
    <div class="finding info">
      <h5>&#128200; Alta Participacion General</h5>
      <p>Participacion media del 78.1% (mediana 86.1%). El 75% de las mesas supera el 83.9% de participacion. Solo el 3% de mesas tienen participacion inferior al 50%.</p>
    </div>
    <div class="finding">
      <h5>&#127919; Concentracion del Candidato</h5>
      <p>El 54.2% de las mesas califica como "Alta" o "Muy Alta" concentracion del candidato. Promedio de 54% de votos por mesa. Antioquia lidera con 69% promedio.</p>
    </div>
    <div class="finding warn">
      <h5>&#128204; 1,051 Mesas con Diferencias</h5>
      <p>El 18.6% de mesas presenta diferencias negativas en el escrutinio. La diferencia promedio es de -302 votos y la peor mesa registro -942 votos de diferencia neta.</p>
    </div>
    <div class="finding">
      <h5>&#9989; Alta Integridad del Proceso</h5>
      <p>El 99.8% de sobres en estado BUENO. Solo 2 mesas excluidas de 5,637 analizadas. 23 mesas requirieron reconteo por la comision electoral.</p>
    </div>
  </div>
</div>

<div class="section-title">Distribucion Geografica de Votos</div>
<div class="charts-row charts-half" style="margin-bottom:18px;">
  <div class="chart-card"><h3>Votos del Candidato por Departamento</h3><div class="chart-wrap" style="height:380px"><canvas id="ch-dept"></canvas></div></div>
  <div class="chart-card"><h3>Top 20 Municipios por Votos</h3><div class="chart-wrap" style="height:380px"><canvas id="ch-mun"></canvas></div></div>
</div>

<div class="section-title">Participacion y Rendimiento Electoral</div>
<div class="charts-row charts-2" style="margin-bottom:18px;">
  <div class="chart-card"><h3>Distribucion % Participacion por Mesa (PRE)</h3><div class="chart-wrap" style="height:260px"><canvas id="ch-partic"></canvas></div></div>
  <div class="chart-card"><h3>Distribucion % Candidato por Mesa (PRE)</h3><div class="chart-wrap" style="height:260px"><canvas id="ch-cand-pct"></canvas></div></div>
</div>

<div class="section-title">Indicadores de Calidad Electoral</div>
<div class="charts-row charts-3" style="margin-bottom:18px;">
  <div class="chart-card"><h3>Variacion Subita PRE</h3><div class="chart-wrap" style="height:240px"><canvas id="ch-var"></canvas></div></div>
  <div class="chart-card"><h3>Concentracion Candidato PRE</h3><div class="chart-wrap" style="height:240px"><canvas id="ch-conc"></canvas></div></div>
  <div class="chart-card"><h3>Estado del Sobre</h3><div class="chart-wrap" style="height:240px"><canvas id="ch-estado"></canvas></div></div>
</div>

<div class="section-title">Analisis de Anomalias &mdash; Diferencias en Escrutinio</div>
<div class="charts-row" style="margin-bottom:18px;">
  <div class="chart-card"><h3>Mesas con Diferencias y Suma de Diferencias por Departamento</h3><div class="chart-wrap" style="height:320px"><canvas id="ch-anom"></canvas></div></div>
</div>

<div class="section-title">Resumen de Integridad del Proceso</div>
<div class="alerts-grid" id="alerts-grid"></div>

<div class="section-title">Detalle por Mesa &mdash; Datos Completos</div>
<div class="table-controls">
  <input class="search-box" id="tbl-search" placeholder="&#128269; Buscar por municipio, puesto, departamento..." oninput="renderTable(1)"/>
  <span id="tbl-info" class="table-info"></span>
</div>
<div class="table-wrap">
<table id="main-table">
  <thead>
    <tr>
      <th onclick="sortTable('DEPARTAMENTO')">Departamento &#8597;</th>
      <th onclick="sortTable('MUNICIPIO')">Municipio &#8597;</th>
      <th onclick="sortTable('PUESTO')">Puesto &#8597;</th>
      <th onclick="sortTable('MESA')">Mesa &#8597;</th>
      <th onclick="sortTable('POTENCIAL')">Potencial &#8597;</th>
      <th onclick="sortTable('Votos Mesa PRE')">Votos Mesa &#8597;</th>
      <th onclick="sortTable('Votos Cand. PRE')">Votos Cand. &#8597;</th>
      <th onclick="sortTable('% Partic. Mesa PRE')">% Partic. &#8597;</th>
      <th onclick="sortTable('% Cand. Mesa PRE')">% Cand. &#8597;</th>
      <th>Var. Subita</th>
      <th>Concentracion</th>
      <th onclick="sortTable('Dif. Mesa Neta')">Dif. Neta &#8597;</th>
      <th>Estado Sobre</th>
      <th>En Terminos</th>
      <th>Excluida</th>
    </tr>
  </thead>
  <tbody id="tbl-body"></tbody>
</table>
</div>
<div class="pagination" id="pagination"></div>

</div>

<footer>
  <div class="footer-title">Abelardo De La Espriella</div>
  <div class="footer-sub">Dashboard Electoral &nbsp;&#183;&nbsp; Analisis de Evidencias de Mesas &nbsp;&#183;&nbsp; Colombia 2026</div>
  <div class="social-links">
    <a href="#" class="social-link" id="sl-twitter">
      <svg class="social-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.73-8.835L1.254 2.25H8.08l4.259 5.631zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
      <span id="sl-twitter-text">X / Twitter</span>
    </a>
    <a href="#" class="social-link" id="sl-instagram">
      <svg class="social-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
      <span id="sl-instagram-text">Instagram</span>
    </a>
    <a href="#" class="social-link" id="sl-facebook">
      <svg class="social-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
      <span id="sl-facebook-text">Facebook</span>
    </a>
    <a href="#" class="social-link" id="sl-linkedin">
      <svg class="social-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
      <span id="sl-linkedin-text">LinkedIn</span>
    </a>
    <a href="#" class="social-link" id="sl-tiktok">
      <svg class="social-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>
      <span id="sl-tiktok-text">TikTok</span>
    </a>
    <a href="#" class="social-link" id="sl-youtube">
      <svg class="social-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
      <span id="sl-youtube-text">YouTube</span>
    </a>
  </div>
  <div class="footer-copy">Elaborado con datos oficiales de escrutinio &nbsp;&#183;&nbsp; Dashboard generado automaticamente &nbsp;&#183;&nbsp; 2026</div>
</footer>

<script>
const RAW = """ + DATA + """;

let filteredData = [...RAW.table];
let sortKey = null, sortDir = 1;
let currentPage = 1;
const PAGE_SIZE = 50;

window.addEventListener('DOMContentLoaded', () => {
  renderKPIs();
  buildFilters();
  renderCharts();
  renderAlerts();
  applyFilters();
});

function fmt(n){ return typeof n==='number' ? n.toLocaleString('es-CO') : n; }

function renderKPIs(){
  const k = RAW.kpis;
  const cards = [
    {val:fmt(k.total_mesas),      label:'Total Mesas',          sub:'analizadas',              cls:'blue',   icon:'&#128203;'},
    {val:fmt(k.municipios),       label:'Municipios',            sub:'en todo el pais',         cls:'blue',   icon:'&#127968;'},
    {val:fmt(k.departamentos),    label:'Departamentos',         sub:'+ Consulados',            cls:'blue',   icon:'&#127757;'},
    {val:fmt(k.puestos),          label:'Puestos de Votacion',   sub:'registrados',             cls:'blue',   icon:'&#127960;'},
    {val:fmt(k.potencial_total),  label:'Potencial Electoral',   sub:'votantes habilitados',    cls:'purple', icon:'&#128101;'},
    {val:fmt(k.votos_mesa_pre),   label:'Votos Depositados',     sub:'escrutinio PRE',          cls:'green',  icon:'&#128683;'},
    {val:fmt(k.votos_cand_pre),   label:'Votos Candidato',       sub:'en escrutinio PRE',       cls:'green',  icon:'&#9989;'},
    {val:k.participacion_avg+'%', label:'Participacion Media',   sub:'promedio por mesa',       cls:'yellow', icon:'&#128200;'},
    {val:k.pct_cand_avg+'%',      label:'% Candidato x Mesa',    sub:'promedio PRE',            cls:'yellow', icon:'&#127919;'},
    {val:fmt(k.mesas_anomalia),   label:'Mesas con Anomalias',   sub:'diferencia neta != 0',   cls:'red',    icon:'&#9888;&#65039;'},
    {val:fmt(k.recontadas),       label:'Recontadas Comision',   sub:'mesas recontadas',        cls:'red',    icon:'&#128204;'},
    {val:fmt(k.excluidas),        label:'Mesas Excluidas',       sub:'del total analizado',     cls:'red',    icon:'&#128683;'},
  ];
  document.getElementById('kpi-grid').innerHTML = cards.map(c=>`
    <div class="kpi ${c.cls}">
      <div class="kpi-icon">${c.icon}</div>
      <div class="kpi-val">${c.val}</div>
      <div class="kpi-label">${c.label}</div>
      <div class="kpi-sub">${c.sub}</div>
    </div>`).join('');
}

function renderAlerts(){
  const k = RAW.kpis;
  const pctBueno = ((k.mesas_bueno/(k.mesas_bueno+10))*100).toFixed(1);
  const pctTerminos = ((k.mesas_en_terminos/k.total_mesas)*100).toFixed(1);
  const pctAnom = ((k.mesas_anomalia/k.total_mesas)*100).toFixed(1);
  document.getElementById('alerts-grid').innerHTML = `
    <div class="alert-card ok"><h4>&#128230; Estado del Sobre</h4>
      <div class="big green">${pctBueno}%</div>
      <p>${fmt(k.mesas_bueno)} sobres BUENOS de ${fmt(k.mesas_bueno+10)} reportados</p></div>
    <div class="alert-card ok"><h4>&#9989; En Terminos</h4>
      <div class="big green">${pctTerminos}%</div>
      <p>${fmt(k.mesas_en_terminos)} mesas en terminos legales</p></div>
    <div class="alert-card warn"><h4>&#9888;&#65039; Mesas con Diferencias</h4>
      <div class="big red">${pctAnom}%</div>
      <p>${fmt(k.mesas_anomalia)} mesas con diferencia neta != 0</p></div>
    <div class="alert-card ok"><h4>&#128203; Mesas Excluidas</h4>
      <div class="big green">${k.excluidas}</div>
      <p>Solo ${k.excluidas} mesas excluidas del analisis</p></div>
    <div class="alert-card warn"><h4>&#128260; Recontadas Comision</h4>
      <div class="big red">${fmt(k.recontadas)}</div>
      <p>${k.recontadas} mesas requirieron reconteo</p></div>
    <div class="alert-card ok"><h4>&#127775; Rendimiento Candidato</h4>
      <div class="big green">${k.pct_cand_avg}%</div>
      <p>Promedio votos candidato por mesa PRE</p></div>`;
}

function buildFilters(){
  const depts=[...new Set(RAW.table.map(r=>r.DEPARTAMENTO).filter(Boolean))].sort();
  const dSel=document.getElementById('f-dept');
  depts.forEach(d=>{const o=document.createElement('option');o.value=d;o.textContent=d;dSel.appendChild(o);});
}

function applyFilters(){
  const dept=document.getElementById('f-dept').value;
  const mun=document.getElementById('f-mun').value;
  const est=document.getElementById('f-estado').value;
  const varS=document.getElementById('f-var').value;
  const conc=document.getElementById('f-conc').value;
  const excl=document.getElementById('f-excl').value;

  const munSel=document.getElementById('f-mun');
  const curMun=munSel.value;
  const muns=[...new Set(RAW.table.filter(r=>!dept||r.DEPARTAMENTO===dept).map(r=>r.MUNICIPIO).filter(Boolean))].sort();
  munSel.innerHTML='<option value="">Todos</option>';
  muns.forEach(m=>{const o=document.createElement('option');o.value=m;o.textContent=m;if(m===curMun)o.selected=true;munSel.appendChild(o);});

  filteredData=RAW.table.filter(r=>{
    if(dept&&r.DEPARTAMENTO!==dept)return false;
    if(mun&&r.MUNICIPIO!==mun)return false;
    if(est&&r['Estado del sobre']!==est)return false;
    if(varS&&r['Var. Súbita PRE']!==varS)return false;
    if(conc&&r['Concent. Cand. PRE']!==conc)return false;
    if(excl&&r.Excluida!==excl)return false;
    return true;
  });

  if(sortKey) filteredData.sort((a,b)=>{
    const av=a[sortKey]??'',bv=b[sortKey]??'';
    return typeof av==='number'?(av-bv)*sortDir:String(av).localeCompare(String(bv))*sortDir;
  });
  document.getElementById('filter-count').textContent=filteredData.length.toLocaleString('es-CO')+' mesas';
  renderTable(1);
}

function resetFilters(){
  ['f-dept','f-mun','f-estado','f-var','f-conc','f-excl'].forEach(id=>document.getElementById(id).value='');
  filteredData=[...RAW.table];
  document.getElementById('filter-count').textContent='';
  renderTable(1);
}

function sortTable(key){
  if(sortKey===key)sortDir*=-1;else{sortKey=key;sortDir=1;}
  applyFilters();
}

const VARCOLOR={'0. Mínima':'blue','1. Baja':'blue','2. Media':'yellow','3. Alta':'yellow','4. Muy Alta':'red'};
const CONCCOLOR={'0. Baja':'blue','1. Normal':'green','2. Alta':'yellow','3. Muy Alta':'red'};
function badge(val,colorMap){const cls=colorMap?.[val]||'blue';return `<span class="badge badge-${cls}">${val||''}</span>`;}

function renderTable(page){
  currentPage=page;
  const search=document.getElementById('tbl-search').value.toLowerCase();
  let rows=filteredData;
  if(search)rows=rows.filter(r=>
    (r.DEPARTAMENTO||'').toLowerCase().includes(search)||
    (r.MUNICIPIO||'').toLowerCase().includes(search)||
    (r.PUESTO||'').toLowerCase().includes(search)
  );
  const total=rows.length;
  const pages=Math.max(1,Math.ceil(total/PAGE_SIZE));
  const start=(page-1)*PAGE_SIZE;
  const slice=rows.slice(start,start+PAGE_SIZE);

  document.getElementById('tbl-info').textContent=`Mostrando ${(start+1).toLocaleString('es-CO')}–${Math.min(start+PAGE_SIZE,total).toLocaleString('es-CO')} de ${total.toLocaleString('es-CO')} mesas`;
  document.getElementById('tbl-body').innerHTML=slice.map(r=>{
    const dif=r['Dif. Mesa Neta'];
    const difBadge=dif===null||dif===undefined?'':dif<0?`<span class="badge badge-red">${dif.toLocaleString('es-CO')}</span>`:dif>0?`<span class="badge badge-green">+${dif}</span>`:`<span class="badge badge-blue">0</span>`;
    return `<tr>
      <td>${r.DEPARTAMENTO||''}</td>
      <td>${r.MUNICIPIO||''}</td>
      <td style="max-width:160px;overflow:hidden;text-overflow:ellipsis" title="${r.PUESTO||''}">${r.PUESTO||''}</td>
      <td>${r.MESA??''}</td>
      <td>${(r.POTENCIAL||0).toLocaleString('es-CO')}</td>
      <td>${(r['Votos Mesa PRE']||0).toLocaleString('es-CO')}</td>
      <td style="font-weight:600;color:var(--accent)">${(r['Votos Cand. PRE']||0).toLocaleString('es-CO')}</td>
      <td>${r['% Partic. Mesa PRE']!=null?r['% Partic. Mesa PRE']+'%':''}</td>
      <td>${r['% Cand. Mesa PRE']!=null?r['% Cand. Mesa PRE']+'%':''}</td>
      <td>${badge(r['Var. Súbita PRE'],VARCOLOR)}</td>
      <td>${badge(r['Concent. Cand. PRE'],CONCCOLOR)}</td>
      <td>${difBadge}</td>
      <td>${badge(r['Estado del sobre'],{BUENO:'green',MAL:'red'})}</td>
      <td>${r['En términos']==='SI'?'<span class="badge badge-green">SI</span>':'<span class="badge badge-yellow">-</span>'}</td>
      <td>${r.Excluida==='SI'?'<span class="badge badge-red">SI</span>':r.Excluida==='NO'?'<span class="badge badge-green">NO</span>':''}</td>
    </tr>`;
  }).join('');

  const pg=document.getElementById('pagination');
  let btns=`<button onclick="renderTable(${Math.max(1,page-1)})" ${page===1?'disabled':''}>&#8592;</button>`;
  let from=Math.max(1,page-3),to=Math.min(pages,from+6);
  if(to-from<6)from=Math.max(1,to-6);
  if(from>1)btns+=`<button onclick="renderTable(1)">1</button><span class="page-info">...</span>`;
  for(let i=from;i<=to;i++)btns+=`<button class="${i===page?'active':''}" onclick="renderTable(${i})">${i}</button>`;
  if(to<pages)btns+=`<span class="page-info">...</span><button onclick="renderTable(${pages})">${pages}</button>`;
  btns+=`<button onclick="renderTable(${Math.min(pages,page+1)})" ${page===pages?'disabled':''}>&#8594;</button>`;
  btns+=`<span class="page-info">Pag. ${page} / ${pages}</span>`;
  pg.innerHTML=btns;
}

const COLORS=['#58a6ff','#3fb950','#d29922','#f85149','#bc8cff','#79c0ff','#56d364','#e3b341','#ff7b72','#d2a8ff'];
const baseOpts=(extra={})=>({responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},...extra});

function renderCharts(){
  const dept=RAW.by_dept;
  new Chart(document.getElementById('ch-dept'),{
    type:'bar',
    data:{labels:dept.map(d=>d.DEPARTAMENTO.replace(/^\\d+\\s*/,'')),datasets:[{
      data:dept.map(d=>Math.round(d.votos_cand)),
      backgroundColor:dept.map((_,i)=>COLORS[i%COLORS.length]+'bb'),
      borderColor:dept.map((_,i)=>COLORS[i%COLORS.length]),
      borderWidth:1,borderRadius:4
    }]},
    options:{...baseOpts(),indexAxis:'y',
      scales:{x:{ticks:{color:'#8b949e',callback:v=>v>=1e5?(v/1e3).toFixed(0)+'k':v},grid:{color:'rgba(48,54,61,.5)'}},
              y:{ticks:{color:'#8b949e',font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}}}}
  });

  const mun=RAW.by_mun;
  new Chart(document.getElementById('ch-mun'),{
    type:'bar',
    data:{labels:mun.map(m=>m.MUNICIPIO.replace(/^\\d+-/,'')),datasets:[{
      data:mun.map(m=>Math.round(m.votos_cand)),
      backgroundColor:'#58a6ffbb',borderColor:'#58a6ff',borderWidth:1,borderRadius:4
    }]},
    options:{...baseOpts(),indexAxis:'y',
      scales:{x:{ticks:{color:'#8b949e',callback:v=>v>=1e3?(v/1e3).toFixed(0)+'k':v},grid:{color:'rgba(48,54,61,.5)'}},
              y:{ticks:{color:'#8b949e',font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}}}}
  });

  const ph=RAW.partic_hist;
  new Chart(document.getElementById('ch-partic'),{
    type:'bar',
    data:{labels:ph.map(b=>b.label),datasets:[{data:ph.map(b=>b.count),backgroundColor:'#3fb95099',borderColor:'#3fb950',borderWidth:1,borderRadius:4}]},
    options:{...baseOpts(),scales:{x:{ticks:{color:'#8b949e',font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}},y:{ticks:{color:'#8b949e'},grid:{color:'rgba(48,54,61,.5)'}}}}
  });

  const ch=RAW.cand_hist;
  new Chart(document.getElementById('ch-cand-pct'),{
    type:'bar',
    data:{labels:ch.map(b=>b.label),datasets:[{data:ch.map(b=>b.count),backgroundColor:'#bc8cff99',borderColor:'#bc8cff',borderWidth:1,borderRadius:4}]},
    options:{...baseOpts(),scales:{x:{ticks:{color:'#8b949e',font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}},y:{ticks:{color:'#8b949e'},grid:{color:'rgba(48,54,61,.5)'}}}}
  });

  const vs=RAW.var_subita;
  new Chart(document.getElementById('ch-var'),{
    type:'bar',
    data:{labels:vs.map(v=>v.categoria),datasets:[{
      data:vs.map(v=>v.count),
      backgroundColor:['#58a6ff99','#3fb95099','#d2992299','#f8514999','#bc8cff99'],
      borderColor:['#58a6ff','#3fb950','#d29922','#f85149','#bc8cff'],
      borderWidth:1,borderRadius:4
    }]},
    options:{...baseOpts(),scales:{x:{ticks:{color:'#8b949e',font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}},y:{ticks:{color:'#8b949e'},grid:{color:'rgba(48,54,61,.5)'}}}}
  });

  const co=RAW.concent;
  new Chart(document.getElementById('ch-conc'),{
    type:'bar',
    data:{labels:co.map(c=>c.categoria),datasets:[{
      data:co.map(c=>c.count),
      backgroundColor:['#58a6ff99','#3fb95099','#d2992299','#f8514999'],
      borderColor:['#58a6ff','#3fb950','#d29922','#f85149'],
      borderWidth:1,borderRadius:4
    }]},
    options:{...baseOpts(),scales:{x:{ticks:{color:'#8b949e',font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}},y:{ticks:{color:'#8b949e'},grid:{color:'rgba(48,54,61,.5)'}}}}
  });

  const es=RAW.estado;
  new Chart(document.getElementById('ch-estado'),{
    type:'doughnut',
    data:{labels:es.map(e=>e.categoria),datasets:[{
      data:es.map(e=>e.count),
      backgroundColor:['#3fb95099','#f8514999'],
      borderColor:['#3fb950','#f85149'],borderWidth:2
    }]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:true,position:'bottom',labels:{color:'#8b949e',padding:16,font:{size:11}}}}}
  });

  const an=RAW.anom_by_dept.slice(0,15);
  new Chart(document.getElementById('ch-anom'),{
    type:'bar',
    data:{
      labels:an.map(a=>a.DEPARTAMENTO.replace(/^\\d+\\s*/,'')),
      datasets:[
        {label:'Mesas con anomalias',data:an.map(a=>a.mesas_anom),backgroundColor:'#d2992299',borderColor:'#d29922',borderWidth:1,borderRadius:4},
        {label:'Suma diferencias (valor absoluto)',data:an.map(a=>Math.abs(a.suma_dif)),backgroundColor:'#f8514966',borderColor:'#f85149',borderWidth:1,borderRadius:4}
      ]
    },
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:true,position:'top',labels:{color:'#8b949e',font:{size:11}}}},
      scales:{x:{ticks:{color:'#8b949e',font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}},
              y:{ticks:{color:'#8b949e',callback:v=>v>=1e3?(v/1e3).toFixed(0)+'k':v},grid:{color:'rgba(48,54,61,.5)'}}}}
  });
}
</script>
</body>
</html>"""

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

size = os.path.getsize('dashboard.html')
print(f'Dashboard: dashboard.html ({size/1024/1024:.1f} MB)')
