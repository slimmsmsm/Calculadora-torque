"""
CALCULADORA DE TORQUE DE PERNOS — Streamlit Web App
=====================================================
Basada en fundamentos de ingeniería mecánica:
- Fórmula de Shigley: T = K × Fi × d
- Factor K según condición de superficie
- Límite de prueba según SAE/ISO/ASTM
- Precarga recomendada: 75% del Sp
- Ajuste en etapas según ASME PCC-1
"""

import streamlit as st

# ─── CONFIGURACIÓN DE PÁGINA ─────────────────────────────────────────────────

st.set_page_config(
    page_title="Calculadora de Torque de Pernos",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS PERSONALIZADO ────────────────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Rajdhani:wght@600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
  }

  /* Fondo general */
  .stApp { background-color: #0d1117; color: #e6edf3; }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #30363d;
  }

  /* Encabezado principal */
  .main-header {
    background: linear-gradient(135deg, #0a0e14 0%, #161b22 100%);
    border: 1px solid #f0a500;
    border-radius: 8px;
    padding: 20px 28px;
    margin-bottom: 24px;
  }
  .main-header h1 {
    font-family: 'Rajdhani', sans-serif;
    color: #f0a500;
    font-size: 2rem;
    margin: 0;
    letter-spacing: 2px;
  }
  .main-header p {
    color: #8b949e;
    font-size: 0.78rem;
    margin: 4px 0 0 0;
    letter-spacing: 1px;
  }

  /* Tarjetas de resultado */
  .result-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 8px 0;
  }
  .result-card.accent { border-left: 4px solid #f0a500; }
  .result-card.blue   { border-left: 4px solid #58a6ff; }
  .result-card.green  { border-left: 4px solid #3fb950; }
  .result-card.red    { border-left: 4px solid #f85149; }

  /* Valor grande */
  .big-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #3fb950;
    line-height: 1;
  }
  .big-unit {
    font-size: 1.1rem;
    color: #8b949e;
    margin-left: 8px;
  }

  /* Etapas */
  .stage-box {
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 10px 16px;
    margin: 4px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .stage-num  { color: #f0a500; font-weight: 700; font-size: 0.9rem; }
  .stage-pct  { color: #8b949e; font-size: 0.85rem; }
  .stage-val  { color: #58a6ff; font-weight: 700; font-size: 1rem; }

  /* Sección subtítulo */
  .section-title {
    color: #58a6ff;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    border-bottom: 1px solid #30363d;
    padding-bottom: 6px;
    margin: 20px 0 10px 0;
  }

  /* Inputs */
  .stSelectbox label, .stSlider label, .stRadio label {
    color: #8b949e !important;
    font-size: 0.82rem !important;
    letter-spacing: 1px !important;
  }

  /* Botón calcular */
  .stButton > button {
    background: linear-gradient(135deg, #f0a500, #d4900a) !important;
    color: #0d1117 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    letter-spacing: 2px !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 12px 32px !important;
    width: 100% !important;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #ffc107, #f0a500) !important;
    transform: translateY(-1px);
  }

  /* Métricas */
  [data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px 16px;
  }
  [data-testid="metric-container"] label {
    color: #8b949e !important;
    font-size: 0.75rem !important;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #f0a500 !important;
    font-size: 1.4rem !important;
  }

  /* Footer */
  .footer {
    background: #0a0e14;
    border-top: 1px solid #30363d;
    padding: 12px 20px;
    margin-top: 32px;
    border-radius: 6px;
    text-align: center;
    color: #8b949e;
    font-size: 0.72rem;
    letter-spacing: 1px;
  }

  /* Ocultar menú hamburguesa de streamlit */
  #MainMenu { visibility: hidden; }
  footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── DATOS TÉCNICOS ──────────────────────────────────────────────────────────

METRIC_THREADS = {
    "M6":  {"d": 6.0,  "stress_area": 20.1},
    "M8":  {"d": 8.0,  "stress_area": 36.6},
    "M10": {"d": 10.0, "stress_area": 58.0},
    "M12": {"d": 12.0, "stress_area": 84.3},
    "M14": {"d": 14.0, "stress_area": 115.0},
    "M16": {"d": 16.0, "stress_area": 157.0},
    "M18": {"d": 18.0, "stress_area": 192.0},
    "M20": {"d": 20.0, "stress_area": 245.0},
    "M22": {"d": 22.0, "stress_area": 303.0},
    "M24": {"d": 24.0, "stress_area": 353.0},
    "M27": {"d": 27.0, "stress_area": 459.0},
    "M30": {"d": 30.0, "stress_area": 561.0},
    "M36": {"d": 36.0, "stress_area": 817.0},
    "M42": {"d": 42.0, "stress_area": 1120.0},
    "M48": {"d": 48.0, "stress_area": 1470.0},
}

UNF_UNC_THREADS = {
    '1/4"-20 UNC':  {"d": 6.35,  "stress_area": 20.1},
    '1/4"-28 UNF':  {"d": 6.35,  "stress_area": 23.2},
    '5/16"-18 UNC': {"d": 7.94,  "stress_area": 32.3},
    '5/16"-24 UNF': {"d": 7.94,  "stress_area": 36.5},
    '3/8"-16 UNC':  {"d": 9.53,  "stress_area": 52.0},
    '3/8"-24 UNF':  {"d": 9.53,  "stress_area": 60.7},
    '7/16"-14 UNC': {"d": 11.11, "stress_area": 70.3},
    '7/16"-20 UNF': {"d": 11.11, "stress_area": 82.5},
    '1/2"-13 UNC':  {"d": 12.70, "stress_area": 92.1},
    '1/2"-20 UNF':  {"d": 12.70, "stress_area": 110.0},
    '9/16"-12 UNC': {"d": 14.29, "stress_area": 120.0},
    '5/8"-11 UNC':  {"d": 15.88, "stress_area": 161.0},
    '3/4"-10 UNC':  {"d": 19.05, "stress_area": 227.0},
    '7/8"-9 UNC':   {"d": 22.23, "stress_area": 316.0},
    '1"-8 UNC':     {"d": 25.40, "stress_area": 414.0},
    '1 1/4"-7 UNC': {"d": 31.75, "stress_area": 657.0},
    '1 1/2"-6 UNC': {"d": 38.10, "stress_area": 958.0},
}

GRADES = {
    "Métrico": {
        "4.8  — Uso general, baja carga":           {"Su": 420,  "Sy": 340,  "Sp": 310},
        "6.8  — Uso general, carga moderada":        {"Su": 600,  "Sy": 480,  "Sp": 380},
        "8.8  — Alta resistencia, industrial":       {"Su": 830,  "Sy": 660,  "Sp": 600},
        "10.9 — Muy alta resistencia, automotriz":   {"Su": 1040, "Sy": 940,  "Sp": 830},
        "12.9 — Máxima resistencia, crítico":        {"Su": 1220, "Sy": 1100, "Sp": 970},
    },
    "SAE/UNF/UNC": {
        "SAE 2 — Uso general, bajo carbono":         {"Su": 510,  "Sy": 390,  "Sp": 380},
        "SAE 5 — Media resistencia, templado":       {"Su": 830,  "Sy": 635,  "Sp": 585},
        "SAE 7 — Alta resistencia":                  {"Su": 1030, "Sy": 895,  "Sp": 860},
        "SAE 8 — Alta resistencia, crítico":         {"Su": 1035, "Sy": 930,  "Sp": 900},
    }
}

K_FACTORS = {
    "Seco (sin lubricante)":           0.20,
    "Ligeramente lubricado (aceite)":  0.18,
    "Lubricado (grasa molibdeno)":     0.15,
    "Cadmiado / Zinc (galvanizado)":   0.17,
    "Acero inoxidable seco":           0.22,
    "Acero inoxidable lubricado":      0.18,
    "PTFE / Neverseize":               0.13,
}

STAGES_CONFIG = {
    "2 etapas (estándar)":     [0.50, 1.00],
    "3 etapas (recomendado)":  [0.33, 0.67, 1.00],
    "4 etapas (crítico)":      [0.25, 0.50, 0.75, 1.00],
    "5 etapas (bridas ASME)":  [0.20, 0.40, 0.60, 0.80, 1.00],
}

UNIT_FACTORS = {
    "N·m":    1.0,
    "kN·m":   0.001,
    "N·cm":   100.0,
    "lbf·ft": 0.73756,
    "lbf·in": 8.85075,
    "kgf·m":  0.10197,
    "kgf·cm": 10.197,
}

# ─── MOTOR DE CÁLCULO ────────────────────────────────────────────────────────

def calcular(d_mm, stress_area, Sp, K, preload_pct):
    Fi   = Sp * stress_area * (preload_pct / 100.0)   # N
    T_Nm = K * Fi * (d_mm / 1000.0)                   # N·m
    return Fi, T_Nm

# ─── SIDEBAR — PARÁMETROS ────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px 0;'>
      <span style='font-family:Rajdhani,sans-serif; font-size:1.4rem;
                   color:#f0a500; letter-spacing:3px; font-weight:700;'>
        ⚙ PARÁMETROS
      </span>
    </div>
    """, unsafe_allow_html=True)

    # Sistema de rosca
    sistema = st.radio("**Sistema de rosca**",
        ["Métrico", "SAE/UNF/UNC"], horizontal=True)

    thread_dict = METRIC_THREADS if sistema == "Métrico" else UNF_UNC_THREADS
    grade_dict  = GRADES[sistema]

    rosca = st.selectbox("**Rosca / Diámetro**", list(thread_dict.keys()))
    grado = st.selectbox("**Grado / Clase**",    list(grade_dict.keys()), index=2)

    st.divider()

    lubricacion = st.selectbox("**Condición de superficie**", list(K_FACTORS.keys()))

    preload = st.slider("**Precarga (% del límite de prueba Sp)**",
        min_value=50, max_value=100, value=75, step=1,
        help="75% para uso general · 85% para aplicaciones críticas")

    st.divider()

    etapas  = st.selectbox("**Etapas de ajuste**", list(STAGES_CONFIG.keys()), index=1)
    unidad  = st.selectbox("**Unidad de torque**",  list(UNIT_FACTORS.keys()))

    st.divider()

    calcular_btn = st.button("▶  CALCULAR TORQUE")

# ─── ENCABEZADO ──────────────────────────────────────────────────────────────

st.markdown("""
<div class="main-header">
  <h1>⚙ CALCULADORA DE TORQUE DE PERNOS</h1>
  <p>Método: Shigley T = K × Fi × d  ·  Norma: ASME PCC-1  ·  ISO 898-1  ·  SAE J429</p>
</div>
""", unsafe_allow_html=True)

# ─── RESULTADO ───────────────────────────────────────────────────────────────

if calcular_btn:
    td  = thread_dict[rosca]
    gd  = grade_dict[grado]
    K   = K_FACTORS[lubricacion]
    stg = STAGES_CONFIG[etapas]
    uf  = UNIT_FACTORS[unidad]

    Fi, T_Nm = calcular(td["d"], td["stress_area"], gd["Sp"], K, preload)
    T_conv   = T_Nm * uf
    util_pct = (Fi / (gd["Sp"] * td["stress_area"])) * 100

    # ── Resultado principal ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Torque final", f"{T_conv:.2f}", unidad)
    with col2:
        st.metric("Precarga Fi", f"{Fi/1000:.2f} kN", f"{preload}% de Sp")
    with col3:
        st.metric("Factor K", f"{K:.3f}", lubricacion.split("(")[0].strip())
    with col4:
        st.metric("Utilización", f"{util_pct:.1f}%", "del límite de prueba")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Dos columnas principales ──
    left, right = st.columns([1, 1], gap="large")

    # ── COLUMNA IZQUIERDA ──
    with left:

        # Resultado destacado
        st.markdown(f"""
        <div class="result-card accent">
          <div style="color:#8b949e; font-size:0.75rem; letter-spacing:2px; margin-bottom:6px;">
            TORQUE DE APRIETE FINAL
          </div>
          <span class="big-value">{T_conv:.3f}</span>
          <span class="big-unit">{unidad}</span>
          <div style="color:#8b949e; font-size:0.8rem; margin-top:8px;">
            = {T_Nm:.2f} N·m &nbsp;|&nbsp; {T_Nm*0.73756:.2f} lbf·ft &nbsp;|&nbsp; {T_Nm*0.10197:.2f} kgf·m
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Tolerancia
        T_min = T_conv * 0.95
        T_max = T_conv * 1.05
        st.markdown(f"""
        <div class="result-card blue">
          <div style="color:#58a6ff; font-size:0.75rem; letter-spacing:2px; margin-bottom:8px;">
            TOLERANCIA ACEPTABLE ± 5%
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span style="color:#8b949e;">Mínimo</span>
            <span style="color:#e6edf3; font-weight:700;">{T_min:.3f} {unidad}</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin:4px 0;">
            <span style="color:#f0a500;">Nominal</span>
            <span style="color:#f0a500; font-weight:700;">{T_conv:.3f} {unidad}</span>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span style="color:#8b949e;">Máximo</span>
            <span style="color:#e6edf3; font-weight:700;">{T_max:.3f} {unidad}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Alerta utilización
        if util_pct > 90:
            st.markdown(f"""
            <div class="result-card red">
              <b style="color:#f85149;">⚠ ADVERTENCIA</b><br>
              <span style="color:#e6edf3; font-size:0.85rem;">
              Utilización {util_pct:.1f}% supera el 90%.<br>
              Considere subir el grado del perno o aumentar el diámetro.
              </span>
            </div>
            """, unsafe_allow_html=True)
        elif util_pct > 80:
            st.markdown(f"""
            <div class="result-card" style="border-left:4px solid #f0a500;">
              <b style="color:#f0a500;">▲ UTILIZACIÓN ALTA</b><br>
              <span style="color:#e6edf3; font-size:0.85rem;">
              {util_pct:.1f}% — Apropiado para aplicaciones críticas controladas.
              </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card green">
              <b style="color:#3fb950;">✔ UTILIZACIÓN SEGURA</b><br>
              <span style="color:#e6edf3; font-size:0.85rem;">
              {util_pct:.1f}% — Dentro del rango recomendado (≤ 80%).
              </span>
            </div>
            """, unsafe_allow_html=True)

        # Resumen del cálculo
        st.markdown('<div class="section-title">▸ RESUMEN DEL CÁLCULO</div>',
            unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-card">
          <div style="font-family:'JetBrains Mono',monospace; font-size:0.82rem; line-height:1.9; color:#e6edf3;">
            <span style="color:#8b949e;">Fórmula     :</span> T = K × Fi × d<br>
            <span style="color:#8b949e;">Diámetro d  :</span> {td['d']:.2f} mm<br>
            <span style="color:#8b949e;">Área esfuerzo:</span> {td['stress_area']:.1f} mm²<br>
            <span style="color:#8b949e;">Límite Sp   :</span> {gd['Sp']} MPa<br>
            <span style="color:#8b949e;">Factor K    :</span> {K:.3f}<br>
            <span style="color:#8b949e;">Precarga    :</span> {preload}% de Sp<br>
            <div style="border-top:1px solid #30363d; margin:8px 0;"></div>
            Fi = {gd['Sp']} × {td['stress_area']:.1f} × {preload/100:.2f}<br>
            <span style="color:#3fb950; font-weight:700;">Fi = {Fi:.0f} N  ({Fi/1000:.2f} kN)</span><br><br>
            T  = {K:.3f} × {Fi:.0f} × {td['d']/1000:.4f}<br>
            <span style="color:#3fb950; font-weight:700;">T  = {T_Nm:.2f} N·m</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── COLUMNA DERECHA ──
    with right:

        # Etapas
        st.markdown('<div class="section-title">▸ SECUENCIA DE APRIETE EN ETAPAS</div>',
            unsafe_allow_html=True)
        st.markdown(f"""
        <div style="color:#8b949e; font-size:0.78rem; margin-bottom:10px;">
          {etapas} · Patrón cruzado (estrella) · ASME PCC-1
        </div>
        """, unsafe_allow_html=True)

        colores_etapa = ["#f0a500","#58a6ff","#3fb950","#e8a838","#c084fc"]
        for i, pct in enumerate(stg):
            T_etapa = T_conv * pct
            color   = colores_etapa[i % len(colores_etapa)]
            st.markdown(f"""
            <div class="stage-box">
              <span class="stage-num" style="color:{color};">ETAPA {i+1}</span>
              <span class="stage-pct">{pct*100:.0f}% del torque final</span>
              <span class="stage-val" style="color:{color};">
                {T_etapa:.3f} <small style="color:#8b949e;">{unidad}</small>
              </span>
            </div>
            """, unsafe_allow_html=True)

        # ¿Por qué etapas?
        st.markdown('<div class="section-title">▸ ¿POR QUÉ AJUSTE EN ETAPAS?</div>',
            unsafe_allow_html=True)
        st.markdown("""
        <div class="result-card" style="font-size:0.82rem; line-height:1.8; color:#c9d1d9;">
          <b style="color:#58a6ff;">Relajación elástica (Embedment)</b><br>
          Al apretar un perno, las superficies de contacto se asientan
          elásticamente. Los pernos apretados primero pierden precarga
          cuando se aprietan los siguientes. El ajuste en etapas compensa
          este efecto redistribuyendo la carga progresivamente.<br><br>
          <b style="color:#58a6ff;">Distribución uniforme de carga</b><br>
          Un flange o tapa apretada de un solo paso queda con distribución
          no uniforme de presión de junta, lo que genera fugas o
          deformaciones asimétricas.<br><br>
          <b style="color:#58a6ff;">Norma ASME PCC-1</b><br>
          • Uniones a presión: mínimo 3 pasadas.<br>
          • Estructuras generales: 2 pasadas aceptables.<br>
          • Bridas críticas: 4-5 pasadas + verificación con llave calibrada.<br><br>
          <b style="color:#58a6ff;">Patrón cruzado (estrella)</b><br>
          Siempre apretar en patrón opuesto/cruzado, nunca en círculo,
          para evitar pandeo y deformación de la junta.
        </div>
        """, unsafe_allow_html=True)

        # Datos de material
        st.markdown('<div class="section-title">▸ PROPIEDADES DEL MATERIAL</div>',
            unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-card">
          <div style="font-size:0.82rem; line-height:1.9; color:#e6edf3;">
            <span style="color:#8b949e;">Grado/Clase    :</span> {grado}<br>
            <span style="color:#8b949e;">Resist. última :</span> {gd['Su']} MPa
              <small style="color:#8b949e;">({gd['Su']*0.145:.0f} ksi)</small><br>
            <span style="color:#8b949e;">Límite fluencia:</span> {gd['Sy']} MPa
              <small style="color:#8b949e;">({gd['Sy']*0.145:.0f} ksi)</small><br>
            <span style="color:#8b949e;">Límite prueba  :</span> {gd['Sp']} MPa
              <small style="color:#8b949e;">({gd['Sp']*0.145:.0f} ksi)</small><br>
            <span style="color:#8b949e;">Cap. perno     :</span>
              {gd['Sp']*td['stress_area']/1000:.2f} kN
              ({gd['Sp']*td['stress_area']*0.2248/1000:.2f} kips)<br>
            <span style="color:#8b949e;">Área de esfuerzo:</span>
              {td['stress_area']:.1f} mm²
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Footer ──
    st.markdown("""
    <div class="footer">
      Cálculo basado en · Shigley's Mechanical Engineering Design, 10ª Ed.
      · ASME PCC-1-2019 · ISO 898-1 · SAE J429
      · Para uso referencial — verificar con ingeniero responsable en aplicaciones críticas
    </div>
    """, unsafe_allow_html=True)

else:
    # ── Pantalla de bienvenida ──
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px;">
          <div style="font-size:4rem; margin-bottom:20px;">⚙️</div>
          <div style="font-family:Rajdhani,sans-serif; font-size:1.6rem;
                      color:#f0a500; letter-spacing:3px; margin-bottom:12px;">
            LISTO PARA CALCULAR
          </div>
          <div style="color:#8b949e; font-size:0.88rem; line-height:1.8;">
            Configure los parámetros en el panel izquierdo<br>
            y presione <b style="color:#f0a500;">▶ CALCULAR TORQUE</b>
          </div>
          <div style="margin-top:40px; background:#161b22; border:1px solid #30363d;
                      border-radius:8px; padding:20px; text-align:left;">
            <div style="color:#58a6ff; font-size:0.75rem; letter-spacing:2px;
                        margin-bottom:12px;">FÓRMULA BASE</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:1rem;
                        color:#3fb950; margin-bottom:8px;">
              T = K × Fi × d
            </div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.82rem;
                        color:#8b949e; line-height:1.8;">
              Fi = Sp × At × (Precarga% / 100)<br>
              K  = Factor de par (condición superficie)<br>
              d  = Diámetro nominal del perno
            </div>
          </div>
          <div style="margin-top:16px; color:#8b949e; font-size:0.72rem; letter-spacing:1px;">
            Shigley · ASME PCC-1 · ISO 898-1 · SAE J429
          </div>
        </div>
        """, unsafe_allow_html=True)
