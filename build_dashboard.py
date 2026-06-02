import json, os

with open('dashboard_data.json', encoding='utf-8') as f:
    DATA = f.read()

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Dashboard Electoral — Evidencias de Mesas</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root{
  --bg:#f0f4f8;--card:#fff;--border:#e2e8f0;
  --accent:#2563eb;--accent-light:#eff6ff;
  --green:#16a34a;--green-light:#f0fdf4;
  --red:#dc2626;--red-light:#fef2f2;
  --yellow:#d97706;--yellow-light:#fffbeb;
  --purple:#7c3aed;--purple-light:#f5f3ff;
  --text:#1e293b;--muted:#64748b;--muted2:#94a3b8;
  --sidebar:240px;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;display:flex;min-height:100vh;}

/* ── SIDEBAR ── */
.sidebar{width:var(--sidebar);min-height:100vh;background:#1e293b;position:fixed;top:0;left:0;display:flex;flex-direction:column;z-index:100;overflow-y:auto;}
.sidebar-logo{padding:22px 18px 16px;border-bottom:1px solid rgba(255,255,255,.08);}
.sidebar-logo h2{color:#fff;font-size:15px;font-weight:700;line-height:1.3;}
.sidebar-logo p{color:#94a3b8;font-size:11px;margin-top:3px;}
.nav{padding:12px 0;flex:1;}
.nav-group{padding:6px 14px 2px;font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#475569;font-weight:600;}
.nav-item{display:flex;align-items:center;gap:10px;padding:10px 18px;color:#cbd5e1;font-size:13px;cursor:pointer;transition:all .15s;border:none;background:none;width:100%;text-align:left;text-decoration:none;}
.nav-item:hover{background:rgba(255,255,255,.06);color:#fff;}
.nav-item.active{background:rgba(37,99,235,.25);color:#93c5fd;border-left:3px solid #3b82f6;}
.nav-item .icon{font-size:16px;width:20px;text-align:center;flex-shrink:0;}
.nav-badge{margin-left:auto;background:var(--red);color:#fff;font-size:10px;font-weight:700;padding:1px 7px;border-radius:10px;}
.sidebar-footer{padding:14px 18px;border-top:1px solid rgba(255,255,255,.08);}
.sidebar-footer p{color:#475569;font-size:11px;}

/* ── MAIN ── */
.main{margin-left:var(--sidebar);flex:1;min-height:100vh;}
.topbar{background:var(--card);border-bottom:1px solid var(--border);padding:14px 28px;display:flex;align-items:center;gap:12px;position:sticky;top:0;z-index:50;}
.topbar-title{font-size:15px;font-weight:600;color:var(--text);}
.topbar-sub{font-size:12px;color:var(--muted);margin-left:auto;}

/* ── SECTIONS ── */
.section{padding:28px;display:none;}
.section.active{display:block;}
.section-header{margin-bottom:24px;}
.section-header h2{font-size:22px;font-weight:700;color:var(--text);margin-bottom:6px;}
.section-header p{font-size:14px;color:var(--muted);line-height:1.5;}

/* ── CARDS GRID ── */
.cards-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px;margin-bottom:28px;}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;transition:box-shadow .15s;}
.card:hover{box-shadow:0 4px 12px rgba(0,0,0,.08);}
.card-icon{width:44px;height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:14px;}
.card-icon.blue{background:var(--accent-light);}
.card-icon.green{background:var(--green-light);}
.card-icon.red{background:var(--red-light);}
.card-icon.yellow{background:var(--yellow-light);}
.card-icon.purple{background:var(--purple-light);}
.card-val{font-size:28px;font-weight:800;line-height:1;margin-bottom:4px;}
.card-val.blue{color:var(--accent);}
.card-val.green{color:var(--green);}
.card-val.red{color:var(--red);}
.card-val.yellow{color:var(--yellow);}
.card-val.purple{color:var(--purple);}
.card-label{font-size:13px;font-weight:600;color:var(--text);margin-bottom:3px;}
.card-desc{font-size:12px;color:var(--muted);}

/* ── BLOCK (chart container) ── */
.block{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:22px;margin-bottom:20px;}
.block-title{font-size:14px;font-weight:700;color:var(--text);margin-bottom:4px;}
.block-sub{font-size:12px;color:var(--muted);margin-bottom:18px;}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;}
.grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;margin-bottom:20px;}
.grid-big{display:grid;grid-template-columns:3fr 2fr;gap:20px;margin-bottom:20px;}

/* ── ANOMALIAS ── */
.anom-hero{background:linear-gradient(135deg,#fef2f2,#fff5f5);border:1px solid rgba(220,38,38,.2);border-radius:12px;padding:22px;margin-bottom:22px;display:flex;align-items:center;gap:20px;}
.anom-hero-icon{font-size:48px;flex-shrink:0;}
.anom-hero h3{font-size:18px;font-weight:700;color:var(--red);margin-bottom:4px;}
.anom-hero p{font-size:13px;color:var(--muted);line-height:1.5;}
.anom-stats{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-bottom:20px;}
.anom-stat{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 16px;text-align:center;}
.anom-stat .n{font-size:26px;font-weight:800;margin-bottom:2px;}
.anom-stat .n.red{color:var(--red);}
.anom-stat .n.green{color:var(--green);}
.anom-stat .n.yellow{color:var(--yellow);}
.anom-stat .n.blue{color:var(--accent);}
.anom-stat small{font-size:11px;color:var(--muted);}

/* ── TABS ── */
.tabs{display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap;}
.tab{padding:8px 18px;border-radius:8px;border:1px solid var(--border);background:var(--bg);font-size:13px;cursor:pointer;transition:all .15s;font-weight:500;}
.tab:hover{background:var(--accent-light);border-color:var(--accent);color:var(--accent);}
.tab.active{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600;}
.tab.active.red{background:var(--red);border-color:var(--red);}
.tab.active.green{background:var(--green);border-color:var(--green);}

/* ── SEV LEGEND ── */
.sev-legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-bottom:14px;padding:10px 14px;background:var(--bg);border-radius:8px;}
.sev-dot{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:5px;}
.dot-critico{background:var(--red);}
.dot-alto{background:var(--yellow);}
.dot-moderado{background:var(--accent);}
.dot-positivo{background:var(--green);}
tr.sev-critico  td:first-child{border-left:4px solid var(--red);padding-left:10px;}
tr.sev-alto     td:first-child{border-left:4px solid var(--yellow);padding-left:10px;}
tr.sev-moderado td:first-child{border-left:4px solid var(--accent);padding-left:10px;}
tr.sev-positivo td:first-child{border-left:4px solid var(--green);padding-left:10px;}

/* ── TABLE ── */
.tbl-controls{display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap;align-items:center;}
.search{background:#fff;border:1px solid var(--border);color:var(--text);padding:9px 14px;border-radius:8px;font-size:13px;flex:1;min-width:200px;}
.search:focus{outline:2px solid var(--accent);}
.tbl-info{font-size:12px;color:var(--muted);}
.tbl-wrap{overflow-x:auto;border-radius:10px;border:1px solid var(--border);}
table{width:100%;border-collapse:collapse;font-size:13px;}
thead th{background:#f8fafc;padding:11px 14px;text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);border-bottom:1px solid var(--border);white-space:nowrap;cursor:pointer;user-select:none;font-weight:600;}
thead th:hover{color:var(--text);}
tbody tr{border-bottom:1px solid #f1f5f9;transition:background .1s;}
tbody tr:hover{background:#f8fafc;}
tbody td{padding:10px 14px;white-space:nowrap;}

/* ── BADGE ── */
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;}
.b-green{background:rgba(22,163,74,.12);color:var(--green);}
.b-red{background:rgba(220,38,38,.12);color:var(--red);}
.b-yellow{background:rgba(217,119,6,.12);color:var(--yellow);}
.b-blue{background:rgba(37,99,235,.12);color:var(--accent);}
.b-purple{background:rgba(124,58,237,.12);color:var(--purple);}
.b-gray{background:#f1f5f9;color:var(--muted);}

/* ── PAGINATION ── */
.pages{display:flex;gap:5px;margin-top:14px;justify-content:center;align-items:center;flex-wrap:wrap;}
.pages button{background:var(--card);border:1px solid var(--border);color:var(--text);padding:7px 13px;border-radius:7px;cursor:pointer;font-size:13px;}
.pages button:hover{border-color:var(--accent);color:var(--accent);}
.pages button.cur{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600;}
.pages button:disabled{opacity:.35;cursor:default;}
.pages .pg-info{font-size:12px;color:var(--muted);padding:0 8px;}

/* ── FILTERS BAR ── */
.fbar{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 18px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:20px;}
.fbar label{font-size:12px;color:var(--muted);font-weight:500;}
.fbar select{background:#fff;border:1px solid var(--border);color:var(--text);padding:7px 10px;border-radius:7px;font-size:13px;cursor:pointer;}
.fbar select:focus{outline:2px solid var(--accent);}
.btn-reset{background:var(--red-light);border:1px solid rgba(220,38,38,.3);color:var(--red);padding:7px 16px;border-radius:7px;font-size:13px;cursor:pointer;font-weight:500;}

/* ── INSIGHT BOX ── */
.insight{background:var(--accent-light);border:1px solid rgba(37,99,235,.2);border-radius:10px;padding:16px 18px;margin-bottom:16px;display:flex;gap:12px;align-items:flex-start;}
.insight.warn{background:var(--red-light);border-color:rgba(220,38,38,.2);}
.insight.ok{background:var(--green-light);border-color:rgba(22,163,74,.2);}
.insight.tip{background:var(--yellow-light);border-color:rgba(217,119,6,.2);}
.insight-icon{font-size:20px;flex-shrink:0;margin-top:1px;}
.insight p{font-size:13px;color:var(--text);line-height:1.6;}
.insight strong{font-weight:600;}

/* ── FOOTER ── */
.sec-footer{background:var(--card);border-top:1px solid var(--border);padding:36px 28px;text-align:center;}
.footer-t{font-size:18px;font-weight:700;margin-bottom:5px;}
.footer-s{font-size:13px;color:var(--muted);margin-bottom:22px;}
.social-row{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:22px;}
.soc{display:flex;align-items:center;gap:8px;background:var(--bg);border:1px solid var(--border);color:var(--text);padding:10px 18px;border-radius:8px;text-decoration:none;font-size:13px;font-weight:500;transition:all .15s;}
.soc:hover{border-color:var(--accent);color:var(--accent);background:var(--accent-light);}
.soc svg{width:18px;height:18px;flex-shrink:0;}
.copy{font-size:11px;color:var(--muted2);}

@media(max-width:900px){
  .sidebar{transform:translateX(-100%);transition:transform .2s;}
  .sidebar.open{transform:translateX(0);}
  .main{margin-left:0;}
  .grid-2,.grid-3,.grid-big{grid-template-columns:1fr;}
  .cards-grid{grid-template-columns:repeat(2,1fr);}
}
</style>
</head>
<body>

<!-- ═══ SIDEBAR ═══ -->
<aside class="sidebar" id="sidebar">
  <div class="sidebar-logo">
    <h2>&#128202; Dashboard Electoral</h2>
    <p>Evidencias de Mesas · Colombia 2026</p>
  </div>
  <nav class="nav">
    <div class="nav-group">Inicio</div>
    <button class="nav-item active" onclick="showSection('resumen',this)">
      <span class="icon">&#128203;</span> Resumen General
    </button>
    <div class="nav-group">Analisis</div>
    <button class="nav-item" onclick="showSection('anomalias',this)">
      <span class="icon">&#9888;&#65039;</span> Anomalias
      <span class="nav-badge">1,051</span>
    </button>
    <button class="nav-item" onclick="showSection('geografia',this)">
      <span class="icon">&#127757;</span> Por Region
    </button>
    <button class="nav-item" onclick="showSection('participacion',this)">
      <span class="icon">&#128200;</span> Participacion
    </button>
    <button class="nav-item" onclick="showSection('calidad',this)">
      <span class="icon">&#9989;</span> Calidad del Proceso
    </button>
    <div class="nav-group">Datos</div>
    <button class="nav-item" onclick="showSection('datos',this)">
      <span class="icon">&#128196;</span> Ver Todas las Mesas
    </button>
    <button class="nav-item" onclick="showSection('social',this)">
      <span class="icon">&#128279;</span> Redes Sociales
    </button>
  </nav>
  <div class="sidebar-footer">
    <p>5,637 mesas · 164 municipios</p>
  </div>
</aside>

<!-- ═══ MAIN ═══ -->
<div class="main">
  <div class="topbar">
    <span class="topbar-title" id="topbar-title">Resumen General</span>
    <span class="topbar-sub">Datos de escrutinio electoral · Colombia 2026</span>
  </div>

  <!-- ══ RESUMEN ══ -->
  <section class="section active" id="sec-resumen">
    <div class="section-header">
      <h2>Resumen General</h2>
      <p>Una mirada rapida a los numeros mas importantes del proceso electoral analizado.</p>
    </div>

    <div class="insight ok">
      <span class="insight-icon">&#128204;</span>
      <p>Se analizaron <strong>5,637 mesas de votacion</strong> distribuidas en <strong>164 municipios</strong> y <strong>26 departamentos</strong> del pais, incluyendo consulados en el exterior. En total se registraron <strong>983,031 votos</strong> del candidato en el escrutinio preliminar.</p>
    </div>

    <div class="cards-grid" id="kpi-cards"></div>

    <div class="grid-2">
      <div class="block">
        <div class="block-title">Votos por Region</div>
        <div class="block-sub">Los 5 departamentos con mas votos del candidato</div>
        <div style="height:220px"><canvas id="ch-top5"></canvas></div>
      </div>
      <div class="block">
        <div class="block-title">Estado del Proceso</div>
        <div class="block-sub">Resumen de integridad de las mesas reportadas</div>
        <div id="integrity-list" style="margin-top:8px"></div>
      </div>
    </div>

    <div class="insight warn">
      <span class="insight-icon">&#9888;&#65039;</span>
      <p><strong>1,051 mesas presentan anomalias</strong> en el conteo de votos (diferencias entre el acta y la urna). El 64% corresponde a Consulados en el exterior. En Colombia, los departamentos con mas anomalias son <strong>Bogota D.C. (138 mesas)</strong>, <strong>Cundinamarca (65)</strong> y <strong>Valle (36)</strong>.</p>
    </div>
    <div style="text-align:right;margin-top:-12px;margin-bottom:20px">
      <button class="tab active" onclick="showSection('anomalias',null)" style="display:inline-flex;align-items:center;gap:6px">&#128269; Ver detalle de anomalias &rarr;</button>
    </div>
  </section>

  <!-- ══ ANOMALIAS ══ -->
  <section class="section" id="sec-anomalias">
    <div class="section-header">
      <h2>&#9888;&#65039; Anomalias en el Escrutinio</h2>
      <p>Una anomalia ocurre cuando el numero de votos contados no coincide con lo registrado en el acta. Cuanto mayor sea la diferencia, mas relevante es la mesa.</p>
    </div>

    <div class="anom-hero">
      <div class="anom-hero-icon">&#128204;</div>
      <div>
        <h3>1,051 mesas con diferencias encontradas</h3>
        <p>De 5,637 mesas analizadas, <strong>1,051 (18.6%)</strong> tienen diferencias entre lo que dice el acta y lo que se conto en la urna. La peor diferencia registrada es de <strong>-942 votos</strong> en una sola mesa de Consulados.</p>
      </div>
    </div>

    <div class="anom-stats" id="anom-stats"></div>

    <div class="block">
      <div class="block-title">Departamentos con mas anomalias</div>
      <div class="block-sub">Numero de mesas con diferencias y total de votos faltantes por departamento</div>
      <div style="height:280px"><canvas id="ch-anom2"></canvas></div>
    </div>

    <div class="block">
      <div class="block-title">Lista completa de mesas con anomalias</div>
      <div class="block-sub">Puedes filtrar por tipo de anomalia y buscar por municipio o puesto de votacion</div>

      <div class="tabs" id="anom-tabs">
        <button class="tab active red" onclick="switchTab('col',this)">&#127464;&#127476; Colombia sin Consulados (375)</button>
        <button class="tab" onclick="switchTab('cons',this)">&#9992;&#65039; Consulados (676)</button>
        <button class="tab" onclick="switchTab('pos',this)">&#128200; Votos de mas (76)</button>
        <button class="tab" onclick="switchTab('all',this)">&#128203; Todas las anomalias (1,051)</button>
      </div>

      <div class="sev-legend">
        <span><span class="sev-dot dot-critico"></span><strong>Critico:</strong> Mas de 300 votos de diferencia</span>
        <span><span class="sev-dot dot-alto"></span><strong>Alto:</strong> Entre 100 y 300 votos</span>
        <span><span class="sev-dot dot-moderado"></span><strong>Moderado:</strong> Menos de 100 votos</span>
        <span><span class="sev-dot dot-positivo"></span><strong>Positivo:</strong> Hay mas votos que en el acta</span>
      </div>

      <div class="tbl-controls">
        <input class="search" id="anom-search" placeholder="&#128269; Buscar municipio o puesto..." oninput="renderAnom(1)"/>
        <span id="anom-info" class="tbl-info"></span>
      </div>
      <div class="tbl-wrap">
        <table>
          <thead><tr>
            <th onclick="sortAnom('DEPARTAMENTO')">Departamento &#8597;</th>
            <th onclick="sortAnom('MUNICIPIO')">Municipio &#8597;</th>
            <th onclick="sortAnom('PUESTO')">Puesto de Votacion &#8597;</th>
            <th onclick="sortAnom('MESA')">Mesa &#8597;</th>
            <th onclick="sortAnom('Votos Mesa PRE')">Votos en Urna &#8597;</th>
            <th onclick="sortAnom('Votos Cand. PRE')">Votos Candidato &#8597;</th>
            <th onclick="sortAnom('Dif. Mesa Neta')">Diferencia &#8597;</th>
            <th>Nivel</th>
            <th>Estado</th>
          </tr></thead>
          <tbody id="anom-body"></tbody>
        </table>
      </div>
      <div class="pages" id="anom-pages"></div>
    </div>
  </section>

  <!-- ══ GEOGRAFIA ══ -->
  <section class="section" id="sec-geografia">
    <div class="section-header">
      <h2>&#127757; Distribucion por Region</h2>
      <p>Como se distribuyen los votos del candidato en los distintos departamentos y municipios del pais.</p>
    </div>

    <div class="insight">
      <span class="insight-icon">&#128204;</span>
      <p><strong>Bogota D.C.</strong> concentra el <strong>34% de todos los votos</strong> con 335,919 votos en 2,190 mesas. Le siguen <strong>Antioquia</strong> (175,908) y <strong>Consulados en el exterior</strong> (162,983). Los 3 municipios con mas votos son Bogota, Medellin y las circunscripciones de Estados Unidos.</p>
    </div>

    <div class="grid-big">
      <div class="block">
        <div class="block-title">Votos del candidato por departamento</div>
        <div class="block-sub">Cada barra muestra el total acumulado de votos en ese departamento</div>
        <div style="height:380px"><canvas id="ch-dept"></canvas></div>
      </div>
      <div class="block">
        <div class="block-title">Participacion promedio por departamento</div>
        <div class="block-sub">Porcentaje de votantes que acudio a las urnas</div>
        <div style="height:380px"><canvas id="ch-partic-dept"></canvas></div>
      </div>
    </div>

    <div class="block">
      <div class="block-title">Top 20 municipios con mas votos</div>
      <div class="block-sub">Los municipios donde el candidato obtuvo mayor cantidad de votos</div>
      <div style="height:340px"><canvas id="ch-mun"></canvas></div>
    </div>
  </section>

  <!-- ══ PARTICIPACION ══ -->
  <section class="section" id="sec-participacion">
    <div class="section-header">
      <h2>&#128200; Participacion Electoral</h2>
      <p>Analisis de cuantas personas votaron en cada mesa y que porcentaje representa del total habilitado.</p>
    </div>

    <div class="cards-grid" style="grid-template-columns:repeat(auto-fill,minmax(180px,1fr))">
      <div class="card">
        <div class="card-icon green">&#9989;</div>
        <div class="card-val green">78.1%</div>
        <div class="card-label">Participacion Promedio</div>
        <div class="card-desc">Promedio de personas que votaron por mesa</div>
      </div>
      <div class="card">
        <div class="card-icon blue">&#128200;</div>
        <div class="card-val blue">86.1%</div>
        <div class="card-label">Participacion Mediana</div>
        <div class="card-desc">La mitad de las mesas superan este porcentaje</div>
      </div>
      <div class="card">
        <div class="card-icon yellow">&#128101;</div>
        <div class="card-val yellow">2,055,525</div>
        <div class="card-label">Votantes Habilitados</div>
        <div class="card-desc">Total de personas aptas para votar</div>
      </div>
      <div class="card">
        <div class="card-icon green">&#128683;</div>
        <div class="card-val green">1,813,541</div>
        <div class="card-label">Votos Depositados</div>
        <div class="card-desc">Total de votos contados en urna (PRE)</div>
      </div>
    </div>

    <div class="insight tip">
      <span class="insight-icon">&#128161;</span>
      <p>La <strong>participacion del 78.1%</strong> es alta comparada con el promedio nacional. Sin embargo, los <strong>Consulados en el exterior tienen solo un 26.7% de participacion</strong>, lo cual es normal dado que muchos colombianos en el exterior no siempre acuden a votar.</p>
    </div>

    <div class="grid-2">
      <div class="block">
        <div class="block-title">&#128202; Como se distribuye la participacion</div>
        <div class="block-sub">Cada barra muestra cuantas mesas tuvieron ese rango de participacion. La mayoria se concentra en el rango 80%-100%</div>
        <div style="height:260px"><canvas id="ch-partic-hist"></canvas></div>
      </div>
      <div class="block">
        <div class="block-title">&#127919; Como se distribuyen los votos del candidato</div>
        <div class="block-sub">Que porcentaje de los votos de cada mesa corresponden al candidato. La mayoria de mesas le dan entre 40%-70% de los votos</div>
        <div style="height:260px"><canvas id="ch-cand-hist"></canvas></div>
      </div>
    </div>
  </section>

  <!-- ══ CALIDAD ══ -->
  <section class="section" id="sec-calidad">
    <div class="section-header">
      <h2>&#9989; Calidad del Proceso Electoral</h2>
      <p>Indicadores que miden si el proceso siguio los procedimientos correctos y si los resultados son consistentes.</p>
    </div>

    <div class="insight ok">
      <span class="insight-icon">&#127775;</span>
      <p>El proceso muestra <strong>indicadores de integridad muy altos</strong>: el 99.8% de sobres estan en buen estado, solo 2 mesas fueron excluidas del analisis y 23 requirieron reconteo. Esto sugiere un proceso bien ejecutado en la mayoria del territorio.</p>
    </div>

    <div id="integrity-cards"></div>

    <div class="grid-3">
      <div class="block">
        <div class="block-title">Variacion sospechosa de votos</div>
        <div class="block-sub">Mide si el cambio de votos de una mesa a otra es inusual. "Muy Alta" puede indicar irregularidades</div>
        <div style="height:240px"><canvas id="ch-var"></canvas></div>
      </div>
      <div class="block">
        <div class="block-title">Nivel de apoyo al candidato</div>
        <div class="block-sub">Cuantas mesas muestran un nivel de apoyo "Alto" o "Muy Alto" comparado con otros candidatos</div>
        <div style="height:240px"><canvas id="ch-conc"></canvas></div>
      </div>
      <div class="block">
        <div class="block-title">Estado fisico del sobre</div>
        <div class="block-sub">Si el sobre con los votos llego en buen estado o con problemas al momento del escrutinio</div>
        <div style="height:240px"><canvas id="ch-estado"></canvas></div>
      </div>
    </div>
  </section>

  <!-- ══ DATOS ══ -->
  <section class="section" id="sec-datos">
    <div class="section-header">
      <h2>&#128196; Datos Completos por Mesa</h2>
      <p>Consulta la informacion detallada de cada una de las 5,637 mesas. Usa los filtros para encontrar una mesa especifica.</p>
    </div>

    <div class="fbar">
      <div><label>Departamento</label><br/><select id="f-dept" onchange="applyFilters()"><option value="">Todos</option></select></div>
      <div><label>Municipio</label><br/><select id="f-mun" onchange="applyFilters()"><option value="">Todos</option></select></div>
      <div><label>Estado del Sobre</label><br/><select id="f-estado" onchange="applyFilters()">
        <option value="">Todos</option><option>BUENO</option><option>MAL</option>
      </select></div>
      <div><label>Variacion</label><br/><select id="f-var" onchange="applyFilters()">
        <option value="">Todas</option>
        <option>0. Mínima</option><option>1. Baja</option>
        <option>2. Media</option><option>3. Alta</option><option>4. Muy Alta</option>
      </select></div>
      <div><label>Excluida</label><br/><select id="f-excl" onchange="applyFilters()">
        <option value="">Todas</option><option>SI</option><option>NO</option>
      </select></div>
      <button class="btn-reset" onclick="resetFilters()">&#8635; Limpiar</button>
      <span id="f-count" class="tbl-info" style="margin-left:auto"></span>
    </div>

    <div class="tbl-controls">
      <input class="search" id="tbl-search" placeholder="&#128269; Buscar por municipio, puesto o departamento..." oninput="renderTable(1)"/>
      <span id="tbl-info" class="tbl-info"></span>
    </div>
    <div class="tbl-wrap">
      <table>
        <thead><tr>
          <th onclick="sortTable('DEPARTAMENTO')">Departamento &#8597;</th>
          <th onclick="sortTable('MUNICIPIO')">Municipio &#8597;</th>
          <th onclick="sortTable('PUESTO')">Puesto &#8597;</th>
          <th onclick="sortTable('MESA')">Mesa &#8597;</th>
          <th onclick="sortTable('POTENCIAL')">Habilitados &#8597;</th>
          <th onclick="sortTable('Votos Mesa PRE')">Votos en Urna &#8597;</th>
          <th onclick="sortTable('Votos Cand. PRE')">Votos Candidato &#8597;</th>
          <th onclick="sortTable('% Partic. Mesa PRE')">% Participacion &#8597;</th>
          <th onclick="sortTable('% Cand. Mesa PRE')">% Candidato &#8597;</th>
          <th onclick="sortTable('Dif. Mesa Neta')">Diferencia &#8597;</th>
          <th>Variacion</th>
          <th>Estado</th>
        </tr></thead>
        <tbody id="tbl-body"></tbody>
      </table>
    </div>
    <div class="pages" id="tbl-pages"></div>
  </section>

  <!-- ══ REDES ══ -->
  <section class="section" id="sec-social">
    <div class="sec-footer" style="border:none;padding-top:60px;min-height:400px">
      <div class="footer-t">Dashboard Electoral</div>
      <div class="footer-s">Analisis de Evidencias de Mesas &nbsp;·&nbsp; Colombia 2026</div>
      <div class="social-row">
        <a href="#" class="soc" id="sl-twitter">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.73-8.835L1.254 2.25H8.08l4.259 5.631zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
          X / Twitter
        </a>
        <a href="#" class="soc" id="sl-instagram">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
          Instagram
        </a>
        <a href="#" class="soc" id="sl-facebook">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          Facebook
        </a>
        <a href="#" class="soc" id="sl-linkedin">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          LinkedIn
        </a>
        <a href="#" class="soc" id="sl-tiktok">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>
          TikTok
        </a>
        <a href="#" class="soc" id="sl-youtube">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
          YouTube
        </a>
      </div>
      <div class="copy">Elaborado con datos oficiales de escrutinio &nbsp;·&nbsp; 2026</div>
    </div>
  </section>

</div><!-- /main -->

<script>
const RAW=""" + DATA + """;

// ── NAVIGATION ──
const SECTIONS=['resumen','anomalias','geografia','participacion','calidad','datos','social'];
const TITLES={resumen:'Resumen General',anomalias:'Anomalias en el Escrutinio',geografia:'Distribucion por Region',participacion:'Participacion Electoral',calidad:'Calidad del Proceso',datos:'Datos por Mesa',social:'Redes Sociales'};

function showSection(id, btn){
  SECTIONS.forEach(s=>{
    document.getElementById('sec-'+s).classList.toggle('active',s===id);
  });
  document.querySelectorAll('.nav-item').forEach(b=>b.classList.remove('active'));
  if(btn) btn.classList.add('active');
  else document.querySelectorAll('.nav-item').forEach(b=>{
    if(b.getAttribute('onclick')&&b.getAttribute('onclick').includes("'"+id+"'")) b.classList.add('active');
  });
  document.getElementById('topbar-title').textContent = TITLES[id]||id;
  window.scrollTo(0,0);
}

// ── INIT ──
window.addEventListener('DOMContentLoaded',()=>{
  renderKPIs();
  renderIntegrity();
  renderIntegrityCards();
  buildFilters();
  renderCharts();
  renderAnomStats();
  renderAnom(1);
  applyFilters();
});

// ── HELPERS ──
function fmt(n){return typeof n==='number'?n.toLocaleString('es-CO'):n||'';}
function badge(v,map){const c=map?.[v]||'gray';return `<span class="badge b-${c}">${v||'-'}</span>`;}
const COLORS=['#2563eb','#16a34a','#d97706','#dc2626','#7c3aed','#0891b2','#db2777','#65a30d','#ea580c','#6366f1'];

// ── KPIs ──
function renderKPIs(){
  const k=RAW.kpis;
  const items=[
    {val:fmt(k.total_mesas),   label:'Mesas Analizadas',     desc:'Total de mesas incluidas en el analisis', icon:'&#128203;',cls:'blue'},
    {val:fmt(k.municipios),    label:'Municipios',            desc:'Municipios con mesas en este analisis',   icon:'&#127968;',cls:'blue'},
    {val:fmt(k.votos_cand_pre),label:'Votos del Candidato',  desc:'Total de votos en el escrutinio PRE',     icon:'&#9989;',  cls:'green'},
    {val:k.participacion_avg+'%',label:'Participacion Media',desc:'Promedio de personas que votaron por mesa',icon:'&#128200;',cls:'yellow'},
    {val:k.pct_cand_avg+'%',   label:'Apoyo por Mesa',       desc:'Promedio del porcentaje obtenido en cada mesa',icon:'&#127919;',cls:'purple'},
    {val:fmt(k.mesas_anomalia),label:'Mesas con Anomalias',  desc:'Mesas donde los votos no cuadran',        icon:'&#9888;&#65039;',cls:'red'},
  ];
  document.getElementById('kpi-cards').innerHTML=items.map(i=>`
    <div class="card">
      <div class="card-icon ${i.cls}">${i.icon}</div>
      <div class="card-val ${i.cls}">${i.val}</div>
      <div class="card-label">${i.label}</div>
      <div class="card-desc">${i.desc}</div>
    </div>`).join('');
}

// ── INTEGRITY LIST ──
function renderIntegrity(){
  const k=RAW.kpis;
  const items=[
    {icon:'&#128230;',label:'Sobres en buen estado',val:fmt(k.mesas_bueno),pct:'99.8%',ok:true},
    {icon:'&#9989;', label:'Mesas en terminos',     val:fmt(k.mesas_en_terminos),pct:'84%',ok:true},
    {icon:'&#128260;',label:'Recontadas por comision',val:fmt(k.recontadas),pct:'0.4%',ok:false},
    {icon:'&#128683;',label:'Mesas excluidas',       val:fmt(k.excluidas),pct:'0.04%',ok:true},
  ];
  document.getElementById('integrity-list').innerHTML=items.map(i=>`
    <div style="display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--border)">
      <span style="font-size:20px">${i.icon}</span>
      <div style="flex:1"><div style="font-size:13px;font-weight:600">${i.label}</div><div style="font-size:12px;color:var(--muted)">${i.val} mesas · ${i.pct}</div></div>
      <span class="badge ${i.ok?'b-green':'b-yellow'}">${i.ok?'Normal':'Revisar'}</span>
    </div>`).join('');
}

// ── INTEGRITY CARDS ──
function renderIntegrityCards(){
  const k=RAW.kpis;
  document.getElementById('integrity-cards').innerHTML=`
    <div class="cards-grid" style="grid-template-columns:repeat(auto-fill,minmax(170px,1fr));margin-bottom:22px">
      <div class="card"><div class="card-icon green">&#128230;</div><div class="card-val green">99.8%</div><div class="card-label">Sobres en Buen Estado</div><div class="card-desc">${fmt(k.mesas_bueno)} de ${fmt(k.mesas_bueno+10)} sobres llegaron en perfecto estado</div></div>
      <div class="card"><div class="card-icon green">&#9989;</div><div class="card-val green">${fmt(k.mesas_en_terminos)}</div><div class="card-label">Mesas en Terminos</div><div class="card-desc">Mesas que cumplieron todos los requisitos legales</div></div>
      <div class="card"><div class="card-icon yellow">&#128260;</div><div class="card-val yellow">${fmt(k.recontadas)}</div><div class="card-label">Recontadas</div><div class="card-desc">Mesas que necesitaron ser recontadas por la comision</div></div>
      <div class="card"><div class="card-icon red">&#128683;</div><div class="card-val red">${k.excluidas}</div><div class="card-label">Mesas Excluidas</div><div class="card-desc">Solo ${k.excluidas} mesas fueron excluidas del analisis total</div></div>
    </div>`;
}

// ── ANOMALIAS STATS ──
function renderAnomStats(){
  const all=RAW.table.filter(r=>r['Dif. Mesa Neta']!==null&&r['Dif. Mesa Neta']!==undefined&&r['Dif. Mesa Neta']!==0);
  const neg=all.filter(r=>r['Dif. Mesa Neta']<0);
  const pos=all.filter(r=>r['Dif. Mesa Neta']>0);
  const col=neg.filter(r=>r.DEPARTAMENTO!=='88 CONSULADOS');
  const crit=neg.filter(r=>r['Dif. Mesa Neta']<-300);
  const suma=neg.reduce((s,r)=>s+(r['Dif. Mesa Neta']||0),0);
  const peor=neg.reduce((m,r)=>r['Dif. Mesa Neta']<m?r['Dif. Mesa Neta']:m,0);
  document.getElementById('anom-stats').innerHTML=`
    <div class="anom-stat"><div class="n red">${all.length}</div><small>Total anomalias</small></div>
    <div class="anom-stat"><div class="n red">${neg.length}</div><small>Votos faltantes</small></div>
    <div class="anom-stat"><div class="n green">${pos.length}</div><small>Votos de mas</small></div>
    <div class="anom-stat"><div class="n blue">${col.length}</div><small>En Colombia (sin Consulados)</small></div>
    <div class="anom-stat"><div class="n red">${crit.length}</div><small>Nivel critico (&gt;300 votos)</small></div>
    <div class="anom-stat"><div class="n yellow">${suma.toLocaleString('es-CO')}</div><small>Total votos faltantes</small></div>
    <div class="anom-stat"><div class="n red">${peor}</div><small>Peor diferencia (1 mesa)</small></div>`;
}

// ── ANOMALIAS TABLE ──
let anomTab='col', anomSortKey='Dif. Mesa Neta', anomSortDir=1, anomPage=1;
const ANOM_PS=50;

function getAnomRows(tab){
  const all=RAW.table.filter(r=>r['Dif. Mesa Neta']!==null&&r['Dif. Mesa Neta']!==undefined&&r['Dif. Mesa Neta']!==0);
  if(tab==='col')  return all.filter(r=>r.DEPARTAMENTO!=='88 CONSULADOS'&&r['Dif. Mesa Neta']<0);
  if(tab==='cons') return all.filter(r=>r.DEPARTAMENTO==='88 CONSULADOS');
  if(tab==='pos')  return all.filter(r=>r['Dif. Mesa Neta']>0);
  return all;
}
function sevInfo(d){
  if(d>0)    return {cls:'sev-positivo', badge:'<span class="badge b-green">&#128200; Votos de mas</span>'};
  if(d>-100) return {cls:'sev-moderado', badge:'<span class="badge b-blue">Moderado</span>'};
  if(d>-300) return {cls:'sev-alto',     badge:'<span class="badge b-yellow">Alto</span>'};
  return           {cls:'sev-critico',  badge:'<span class="badge b-red">&#9888; Critico</span>'};
}

function switchTab(tab,btn){
  anomTab=tab; anomSortKey='Dif. Mesa Neta'; anomSortDir=1;
  document.querySelectorAll('#anom-tabs .tab').forEach(b=>b.classList.remove('active','red','green'));
  btn.classList.add('active');
  if(tab==='pos') btn.classList.add('green'); else btn.classList.add('red');
  renderAnom(1);
}

function sortAnom(k){if(anomSortKey===k)anomSortDir*=-1;else{anomSortKey=k;anomSortDir=1;}renderAnom(anomPage);}

function renderAnom(page){
  anomPage=page;
  const q=(document.getElementById('anom-search')?.value||'').toLowerCase();
  let rows=getAnomRows(anomTab);
  if(q) rows=rows.filter(r=>(r.DEPARTAMENTO||'').toLowerCase().includes(q)||(r.MUNICIPIO||'').toLowerCase().includes(q)||(r.PUESTO||'').toLowerCase().includes(q));
  rows.sort((a,b)=>{const av=a[anomSortKey]??0,bv=b[anomSortKey]??0;return typeof av==='number'?(av-bv)*anomSortDir:String(av).localeCompare(String(bv))*anomSortDir;});
  const total=rows.length, pages=Math.max(1,Math.ceil(total/ANOM_PS)), start=(page-1)*ANOM_PS;
  document.getElementById('anom-info').textContent=`${total.toLocaleString('es-CO')} mesas`;
  document.getElementById('anom-body').innerHTML=rows.slice(start,start+ANOM_PS).map(r=>{
    const d=r['Dif. Mesa Neta'], s=sevInfo(d);
    const difCell=d<0?`<span class="badge b-red">${d.toLocaleString('es-CO')}</span>`:`<span class="badge b-green">+${d}</span>`;
    return `<tr class="${s.cls}">
      <td>${r.DEPARTAMENTO||''}</td><td>${r.MUNICIPIO||''}</td>
      <td style="max-width:160px;overflow:hidden;text-overflow:ellipsis" title="${r.PUESTO||''}">${r.PUESTO||''}</td>
      <td>${r.MESA??''}</td>
      <td>${fmt(r['Votos Mesa PRE']||0)}</td>
      <td style="font-weight:600;color:var(--accent)">${fmt(r['Votos Cand. PRE']||0)}</td>
      <td>${difCell}</td><td>${s.badge}</td>
      <td>${badge(r['Estado del sobre'],{BUENO:'green',MAL:'red'})}</td>
    </tr>`;
  }).join('');
  renderPages('anom-pages',page,pages,renderAnom);
}

// ── MAIN TABLE ──
let filteredData=[...RAW.table], tSortKey=null, tSortDir=1, tPage=1;
const TBL_PS=50;

function buildFilters(){
  const ds=[...new Set(RAW.table.map(r=>r.DEPARTAMENTO).filter(Boolean))].sort();
  const sel=document.getElementById('f-dept');
  ds.forEach(d=>{const o=document.createElement('option');o.value=d;o.textContent=d;sel.appendChild(o);});
}
function applyFilters(){
  const dept=document.getElementById('f-dept').value;
  const mun=document.getElementById('f-mun').value;
  const est=document.getElementById('f-estado').value;
  const varS=document.getElementById('f-var').value;
  const excl=document.getElementById('f-excl').value;
  const munSel=document.getElementById('f-mun');
  const curM=munSel.value;
  const muns=[...new Set(RAW.table.filter(r=>!dept||r.DEPARTAMENTO===dept).map(r=>r.MUNICIPIO).filter(Boolean))].sort();
  munSel.innerHTML='<option value="">Todos</option>';
  muns.forEach(m=>{const o=document.createElement('option');o.value=m;o.textContent=m;if(m===curM)o.selected=true;munSel.appendChild(o);});
  filteredData=RAW.table.filter(r=>{
    if(dept&&r.DEPARTAMENTO!==dept)return false;
    if(mun&&r.MUNICIPIO!==mun)return false;
    if(est&&r['Estado del sobre']!==est)return false;
    if(varS&&r['Var. Súbita PRE']!==varS)return false;
    if(excl&&r.Excluida!==excl)return false;
    return true;
  });
  if(tSortKey)filteredData.sort((a,b)=>{const av=a[tSortKey]??'',bv=b[tSortKey]??'';return typeof av==='number'?(av-bv)*tSortDir:String(av).localeCompare(String(bv))*tSortDir;});
  document.getElementById('f-count').textContent=filteredData.length.toLocaleString('es-CO')+' mesas';
  renderTable(1);
}
function resetFilters(){['f-dept','f-mun','f-estado','f-var','f-excl'].forEach(id=>document.getElementById(id).value='');filteredData=[...RAW.table];document.getElementById('f-count').textContent='';renderTable(1);}
function sortTable(k){if(tSortKey===k)tSortDir*=-1;else{tSortKey=k;tSortDir=1;}applyFilters();}

const VARMAP={'0. Mínima':'blue','1. Baja':'blue','2. Media':'yellow','3. Alta':'yellow','4. Muy Alta':'red'};
const CONMAP={'0. Baja':'blue','1. Normal':'green','2. Alta':'yellow','3. Muy Alta':'red'};

function renderTable(page){
  tPage=page;
  const q=(document.getElementById('tbl-search')?.value||'').toLowerCase();
  let rows=filteredData;
  if(q)rows=rows.filter(r=>(r.DEPARTAMENTO||'').toLowerCase().includes(q)||(r.MUNICIPIO||'').toLowerCase().includes(q)||(r.PUESTO||'').toLowerCase().includes(q));
  const total=rows.length, pages=Math.max(1,Math.ceil(total/TBL_PS)), start=(page-1)*TBL_PS;
  document.getElementById('tbl-info').textContent=`Mostrando ${(start+1).toLocaleString('es-CO')}–${Math.min(start+TBL_PS,total).toLocaleString('es-CO')} de ${total.toLocaleString('es-CO')}`;
  const VARMAP2={'0. Mínima':'blue','1. Baja':'blue','2. Media':'yellow','3. Alta':'yellow','4. Muy Alta':'red'};
  document.getElementById('tbl-body').innerHTML=rows.slice(start,start+TBL_PS).map(r=>{
    const d=r['Dif. Mesa Neta'];
    const dBadge=d===null||d===undefined?'':d<0?`<span class="badge b-red">${d.toLocaleString('es-CO')}</span>`:d>0?`<span class="badge b-green">+${d}</span>`:`<span class="badge b-gray">0</span>`;
    return `<tr>
      <td>${r.DEPARTAMENTO||''}</td><td>${r.MUNICIPIO||''}</td>
      <td style="max-width:150px;overflow:hidden;text-overflow:ellipsis" title="${r.PUESTO||''}">${r.PUESTO||''}</td>
      <td>${r.MESA??''}</td><td>${fmt(r.POTENCIAL||0)}</td>
      <td>${fmt(r['Votos Mesa PRE']||0)}</td>
      <td style="font-weight:700;color:var(--accent)">${fmt(r['Votos Cand. PRE']||0)}</td>
      <td>${r['% Partic. Mesa PRE']!=null?r['% Partic. Mesa PRE']+'%':''}</td>
      <td>${r['% Cand. Mesa PRE']!=null?r['% Cand. Mesa PRE']+'%':''}</td>
      <td>${dBadge}</td>
      <td>${badge(r['Var. Súbita PRE'],VARMAP2)}</td>
      <td>${badge(r['Estado del sobre'],{BUENO:'green',MAL:'red'})}</td>
    </tr>`;
  }).join('');
  renderPages('tbl-pages',page,pages,renderTable);
}

// ── SHARED PAGINATION ──
function renderPages(id,page,pages,fn){
  let b=`<button onclick="${fn.name}(${Math.max(1,page-1)})" ${page===1?'disabled':''}>&#8592;</button>`;
  let from=Math.max(1,page-3),to=Math.min(pages,from+6);
  if(to-from<6)from=Math.max(1,to-6);
  if(from>1)b+=`<button onclick="${fn.name}(1)">1</button><span class="pg-info">...</span>`;
  for(let i=from;i<=to;i++)b+=`<button class="${i===page?'cur':''}" onclick="${fn.name}(${i})">${i}</button>`;
  if(to<pages)b+=`<span class="pg-info">...</span><button onclick="${fn.name}(${pages})">${pages}</button>`;
  b+=`<button onclick="${fn.name}(${Math.min(pages,page+1)})" ${page===pages?'disabled':''}>&#8594;</button>`;
  b+=`<span class="pg-info">Pag. ${page} / ${pages}</span>`;
  document.getElementById(id).innerHTML=b;
}

// ── CHARTS ──
const baseOpts=(extra={})=>({responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},...extra});
const gridOpts={x:{ticks:{color:'#94a3b8',font:{size:10}},grid:{color:'rgba(226,232,240,.8)'}},y:{ticks:{color:'#94a3b8'},grid:{color:'rgba(226,232,240,.8)'}}};

function renderCharts(){
  // Top 5 departamentos (resumen)
  const top5=RAW.by_dept.slice(0,5);
  new Chart(document.getElementById('ch-top5'),{
    type:'bar',
    data:{labels:top5.map(d=>d.DEPARTAMENTO.replace(/^\\d+\\s*/,'')),
      datasets:[{data:top5.map(d=>Math.round(d.votos_cand)),backgroundColor:COLORS.slice(0,5).map(c=>c+'cc'),borderColor:COLORS.slice(0,5),borderWidth:1,borderRadius:6}]},
    options:{...baseOpts(),scales:gridOpts}
  });

  // Por departamento (geografia)
  const dept=RAW.by_dept;
  new Chart(document.getElementById('ch-dept'),{
    type:'bar',
    data:{labels:dept.map(d=>d.DEPARTAMENTO.replace(/^\\d+\\s*/,'')),
      datasets:[{data:dept.map(d=>Math.round(d.votos_cand)),backgroundColor:COLORS.map(c=>c+'cc'),borderColor:COLORS,borderWidth:1,borderRadius:4}]},
    options:{...baseOpts(),indexAxis:'y',scales:{x:{...gridOpts.x,ticks:{...gridOpts.x.ticks,callback:v=>v>=1e5?(v/1e3).toFixed(0)+'k':v}},y:{...gridOpts.y,ticks:{...gridOpts.y.ticks,font:{size:10}}}}}
  });

  // Participacion por depto
  new Chart(document.getElementById('ch-partic-dept'),{
    type:'bar',
    data:{labels:dept.map(d=>d.DEPARTAMENTO.replace(/^\\d+\\s*/,'')),
      datasets:[{data:dept.map(d=>+d.pct_partic_avg.toFixed(1)),backgroundColor:'#16a34acc',borderColor:'#16a34a',borderWidth:1,borderRadius:4}]},
    options:{...baseOpts(),indexAxis:'y',scales:{x:{...gridOpts.x,ticks:{...gridOpts.x.ticks,callback:v=>v+'%'},max:100},y:{...gridOpts.y,ticks:{...gridOpts.y.ticks,font:{size:10}}}}}
  });

  // Top 20 municipios
  const mun=RAW.by_mun;
  new Chart(document.getElementById('ch-mun'),{
    type:'bar',
    data:{labels:mun.map(m=>m.MUNICIPIO.replace(/^\\d+-/,'')),
      datasets:[{data:mun.map(m=>Math.round(m.votos_cand)),backgroundColor:'#2563ebcc',borderColor:'#2563eb',borderWidth:1,borderRadius:4}]},
    options:{...baseOpts(),indexAxis:'y',scales:{x:{...gridOpts.x,ticks:{...gridOpts.x.ticks,callback:v=>v>=1e3?(v/1e3).toFixed(0)+'k':v}},y:{...gridOpts.y,ticks:{...gridOpts.y.ticks,font:{size:10}}}}}
  });

  // Histograma participacion
  const ph=RAW.partic_hist;
  new Chart(document.getElementById('ch-partic-hist'),{
    type:'bar',
    data:{labels:ph.map(b=>b.label),datasets:[{data:ph.map(b=>b.count),backgroundColor:'#16a34acc',borderColor:'#16a34a',borderWidth:1,borderRadius:4}]},
    options:{...baseOpts(),scales:gridOpts}
  });

  // Histograma candidato
  const ch=RAW.cand_hist;
  new Chart(document.getElementById('ch-cand-hist'),{
    type:'bar',
    data:{labels:ch.map(b=>b.label),datasets:[{data:ch.map(b=>b.count),backgroundColor:'#7c3aedcc',borderColor:'#7c3aed',borderWidth:1,borderRadius:4}]},
    options:{...baseOpts(),scales:gridOpts}
  });

  // Var subita
  const vs=RAW.var_subita;
  const vsColors=['#2563eb','#16a34a','#d97706','#dc2626','#7c3aed'];
  new Chart(document.getElementById('ch-var'),{
    type:'bar',
    data:{labels:vs.map(v=>v.categoria),datasets:[{data:vs.map(v=>v.count),backgroundColor:vsColors.map(c=>c+'cc'),borderColor:vsColors,borderWidth:1,borderRadius:4}]},
    options:{...baseOpts(),scales:gridOpts}
  });

  // Concentracion
  const co=RAW.concent;
  const coColors=['#2563eb','#16a34a','#d97706','#dc2626'];
  new Chart(document.getElementById('ch-conc'),{
    type:'bar',
    data:{labels:co.map(c=>c.categoria),datasets:[{data:co.map(c=>c.count),backgroundColor:coColors.map(c=>c+'cc'),borderColor:coColors,borderWidth:1,borderRadius:4}]},
    options:{...baseOpts(),scales:gridOpts}
  });

  // Estado sobre doughnut
  const es=RAW.estado;
  new Chart(document.getElementById('ch-estado'),{
    type:'doughnut',
    data:{labels:es.map(e=>e.categoria),datasets:[{data:es.map(e=>e.count),backgroundColor:['#16a34acc','#dc2626cc'],borderColor:['#16a34a','#dc2626'],borderWidth:2}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:true,position:'bottom',labels:{color:'#64748b',padding:16,font:{size:12}}}}}
  });

  // Anomalias por depto
  const an=RAW.anom_by_dept.slice(0,12);
  new Chart(document.getElementById('ch-anom2'),{
    type:'bar',
    data:{labels:an.map(a=>a.DEPARTAMENTO.replace(/^\\d+\\s*/,'')),
      datasets:[
        {label:'Mesas con anomalias',data:an.map(a=>a.mesas_anom),backgroundColor:'#d97706cc',borderColor:'#d97706',borderWidth:1,borderRadius:4},
        {label:'Votos faltantes (valor absoluto)',data:an.map(a=>Math.abs(a.suma_dif)),backgroundColor:'#dc2626aa',borderColor:'#dc2626',borderWidth:1,borderRadius:4}
      ]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:true,position:'top',labels:{color:'#64748b',font:{size:11}}}},
      scales:{x:{ticks:{color:'#94a3b8',font:{size:10}},grid:{color:'rgba(226,232,240,.8)'}},y:{ticks:{color:'#94a3b8',callback:v=>v>=1e3?(v/1e3).toFixed(0)+'k':v},grid:{color:'rgba(226,232,240,.8)'}}}}
  });
}
</script>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f'index.html generado: {os.path.getsize("index.html")//1024} KB')
