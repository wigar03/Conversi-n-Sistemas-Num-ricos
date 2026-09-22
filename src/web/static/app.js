/**
 * Calculadora de Sistemas Numéricos - Álgebra Lineal UAM
 * Frontend Controller & UI Logic con Visualizadores Interactivos
 */

// Estado global de la aplicación
const AppState = {
  theme: localStorage.getItem('uam_theme') || 'dark',
  activeTab: 'module1',
  m1: {
    targetBase: 16
  },
  m2: {
    sourceBase: 16
  }
};

// Configuraciones de bases
const BASE_CONFIGS = {
  2: {
    name: 'Binario',
    label: 'Base 2 (Binario)',
    allowedDesc: '[0, 1]',
    examples: ['10110', '11111111', '101', '0'],
    placeholder: 'Ej. 10110'
  },
  8: {
    name: 'Octal',
    label: 'Base 8 (Octal)',
    allowedDesc: '[0 - 7]',
    examples: ['377', '1647', '52', '0'],
    placeholder: 'Ej. 377'
  },
  16: {
    name: 'Hexadecimal',
    label: 'Base 16 (Hexadecimal)',
    allowedDesc: '[0 - 9, A - F]',
    examples: ['3A7', 'FF', '1A', '0'],
    placeholder: 'Ej. 3A7'
  }
};

// Iconos SVG Minimalistas (Open Source / Lucide Icons - MIT License)
const ICONS = {
  sun: `<svg class="theme-svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="4"></circle>
    <path d="M12 2v2"></path>
    <path d="M12 20v2"></path>
    <path d="m4.93 4.93 1.41 1.41"></path>
    <path d="m17.66 17.66 1.41 1.41"></path>
    <path d="M2 12h2"></path>
    <path d="M20 12h2"></path>
    <path d="m6.34 17.66-1.41 1.41"></path>
    <path d="m19.07 4.93-1.41 1.41"></path>
  </svg>`,
  moon: `<svg class="theme-svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path>
  </svg>`,
  copy: `<svg class="btn-copy-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect width="14" height="14" x="8" y="8" rx="2" ry="2"></rect>
    <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"></path>
  </svg>`,
  check: `<svg class="btn-copy-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M20 6 9 17l-5-5"></path>
  </svg>`,
  flowTrail: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="m3 16 4 4 4-4"></path>
    <path d="M7 20V4"></path>
    <path d="m21 8-4-4-4 4"></path>
    <path d="M17 4v16"></path>
  </svg>`,
  toastSuccess: `<svg class="toast-icon-svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="10"></circle>
    <path d="m9 12 2 2 4-4"></path>
  </svg>`,
  toastError: `<svg class="toast-icon-svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="10"></circle>
    <line x1="12" y1="8" x2="12" y2="12"></line>
    <line x1="12" y1="16" x2="12.01" y2="16"></line>
  </svg>`
};

// Inicialización cuando carga el DOM
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initTabs();
  initStepper();
  // Ejecutar conversiones por defecto para mostrar vistas ricas inmediatas
  handleConvertFromDecimal();
});

/* ===================================================================
   Gestión de Tema (Dark / Light)
   =================================================================== */

function initTheme() {
  document.documentElement.setAttribute('data-theme', AppState.theme);
  updateThemeIcon();

  const toggleBtn = document.getElementById('theme-toggle-btn');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      AppState.theme = AppState.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', AppState.theme);
      localStorage.setItem('uam_theme', AppState.theme);
      updateThemeIcon();
    });
  }
}

function updateThemeIcon() {
  const icon = document.getElementById('theme-icon');
  if (icon) {
    icon.innerHTML = AppState.theme === 'dark' ? ICONS.sun : ICONS.moon;
  }
}

/* ===================================================================
   Navegación de Pestañas
   =================================================================== */

function initTabs() {
  const tabs = [
    { id: 'tab-module1', panel: 'panel-module1' },
    { id: 'tab-module2', panel: 'panel-module2' },
    { id: 'tab-theory', panel: 'panel-theory' }
  ];

  tabs.forEach(tab => {
    const btn = document.getElementById(tab.id);
    if (!btn) return;

    btn.addEventListener('click', () => {
      tabs.forEach(t => {
        document.getElementById(t.id)?.classList.remove('active');
        document.getElementById(t.panel)?.classList.remove('active');
        document.getElementById(t.id)?.setAttribute('aria-selected', 'false');
      });

      btn.classList.add('active');
      document.getElementById(tab.panel)?.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      // Si se abre el módulo 2 y no tiene resultado aún, ejecutar ejemplo
      if (tab.id === 'tab-module2' && !document.getElementById('result-container-m2').innerHTML) {
        handleConvertToDecimal();
      }
    });
  });
}

/* ===================================================================
   Controles y Stepper (+ / -) de Módulo 1 (Decimal -> Bases)
   =================================================================== */

function initStepper() {
  const input = document.getElementById('input-decimal-val');
  const btnMinus = document.getElementById('btn-dec-minus');
  const btnPlus = document.getElementById('btn-dec-plus');

  if (!input || !btnMinus || !btnPlus) return;

  // Prevenir que el scroll con rueda de ratón (mouse wheel) cambie el número
  input.addEventListener('wheel', (e) => {
    e.preventDefault();
  }, { passive: false });

  // Función para modificar el valor de forma segura
  function stepValue(delta) {
    const current = parseInt(input.value, 10);
    const baseVal = isNaN(current) ? 0 : current;
    const newVal = Math.max(0, baseVal + delta);
    input.value = newVal;
    handleConvertFromDecimal();
  }

  // Soporte de pulsación sostenida (press and hold)
  function attachHoldListener(btn, delta) {
    let holdTimeout = null;
    let holdInterval = null;

    const start = (e) => {
      e.preventDefault();
      stepValue(delta);

      holdTimeout = setTimeout(() => {
        holdInterval = setInterval(() => {
          stepValue(delta);
        }, 70);
      }, 350);
    };

    const stop = () => {
      if (holdTimeout) clearTimeout(holdTimeout);
      if (holdInterval) clearInterval(holdInterval);
      holdTimeout = null;
      holdInterval = null;
    };

    btn.addEventListener('mousedown', start);
    btn.addEventListener('touchstart', start, { passive: false });

    btn.addEventListener('mouseup', stop);
    btn.addEventListener('mouseleave', stop);
    btn.addEventListener('touchend', stop);
    btn.addEventListener('touchcancel', stop);
  }

  attachHoldListener(btnMinus, -1);
  attachHoldListener(btnPlus, 1);

  // Escuchar entrada de teclado directa
  input.addEventListener('input', () => {
    const val = parseInt(input.value, 10);
    if (!isNaN(val) && val >= 0) {
      handleConvertFromDecimal();
    }
  });
}

function selectTargetBase(base) {
  AppState.m1.targetBase = base;
  const container = document.getElementById('chips-target-base');
  if (!container) return;

  container.querySelectorAll('.base-chip').forEach(chip => {
    if (parseInt(chip.getAttribute('data-base')) === base) {
      chip.classList.add('active');
    } else {
      chip.classList.remove('active');
    }
  });

  handleConvertFromDecimal();
}

function setDecimalExample(val) {
  const input = document.getElementById('input-decimal-val');
  if (input) {
    input.value = val;
    handleConvertFromDecimal();
  }
}

async function handleConvertFromDecimal() {
  const inputElem = document.getElementById('input-decimal-val');
  const resultContainer = document.getElementById('result-container-m1');
  if (!inputElem || !resultContainer) return;

  const rawVal = inputElem.value.trim();
  if (rawVal === '') {
    showToast('Por favor ingrese un número decimal válido.', 'error');
    return;
  }

  const decimalNum = parseInt(rawVal, 10);
  if (isNaN(decimalNum)) {
    showToast('El valor ingresado no es un número entero válido.', 'error');
    return;
  }

  try {
    const response = await fetch('/api/convert/from-decimal', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ decimal: decimalNum, base: AppState.m1.targetBase })
    });

    const resJson = await response.json();
    if (!resJson.success) {
      showToast(resJson.error || 'Error al procesar la conversión.', 'error');
      return;
    }

    renderModule1Result(resJson.data);
  } catch (err) {
    showToast('Error de comunicación con el servidor local.', 'error');
    console.error(err);
  }
}

function renderModule1Result(data) {
  const container = document.getElementById('result-container-m1');
  container.style.display = 'block';

  // Filas de la tabla de divisiones euclidianas
  const tableRowsHtml = data.steps.map(s => `
    <tr>
      <td><span class="procedure-badge">#${s.step_number}</span></td>
      <td><strong>${s.dividend}</strong></td>
      <td><span style="color:var(--text-muted)">÷</span> ${s.divisor}</td>
      <td><span class="quotient-highlight">${s.quotient}</span></td>
      <td><strong>${s.remainder}</strong></td>
      <td><span class="remainder-pill">${s.remainder_symbol}</span></td>
      <td style="color:var(--text-muted); font-size:0.85rem">${s.equation}</td>
    </tr>
  `).join('');

  // Nodos del flujo de residuos (leídos de abajo hacia arriba)
  const trailHtml = data.remainders_reversed.map((sym, idx) => `
    <div class="trail-node" title="Residuo posición ${data.remainders_reversed.length - 1 - idx}">
      <span class="trail-node-char">${sym}</span>
      <span class="trail-node-sub">r<sub>${data.remainders_reversed.length - 1 - idx}</sub></span>
    </div>
    ${idx < data.remainders_reversed.length - 1 ? '<span class="trail-arrow">→</span>' : ''}
  `).join('');

  container.innerHTML = `
    <!-- Hero Result Banner -->
    <div class="result-hero">
      <div class="result-hero-left">
        <span class="result-hero-label">Resultado Equivalente (${data.base_name})</span>
        <div class="result-hero-value">(${data.result_str})<sub>${data.target_base}</sub></div>
        <span style="color:var(--text-secondary); font-size:0.88rem">
          Equivalencia: (${data.decimal_input})<sub>10</sub> = (${data.result_str})<sub>${data.target_base}</sub>
        </span>
      </div>
      <div class="result-hero-actions">
        <button class="btn-copy" onclick="copyToClipboard('${data.result_str}', this)">
          ${ICONS.copy}
          <span>Copiar Número</span>
        </button>
      </div>
    </div>

    <!-- Procedure Card -->
    <div class="card procedure-section">
      <div class="procedure-header">
        <h3 class="procedure-title">
          <span>Procedimiento: Algoritmo de Divisiones Sucesivas</span>
          <span class="procedure-badge">${data.steps.length} ${data.steps.length === 1 ? 'paso' : 'pasos'}</span>
        </h3>
        <span style="font-size:0.8rem; color:var(--text-muted)">Dividendo = (Cociente × Base) + Residuo</span>
      </div>

      <!-- Division Table -->
      <div class="table-responsive">
        <table class="division-table">
          <thead>
            <tr>
              <th>Paso</th>
              <th>Dividendo</th>
              <th>Divisor</th>
              <th>Cociente</th>
              <th>Residuo</th>
              <th>Símbolo</th>
              <th>Comprobación Euclidiana</th>
            </tr>
          </thead>
          <tbody>
            ${tableRowsHtml}
          </tbody>
        </table>
      </div>

      <!-- Trail of Remainders -->
      <div class="flow-trail-card">
        <div class="flow-trail-title">
          ${ICONS.flowTrail}
          <span>Construcción del Número (Residuos en Orden Inverso)</span>
        </div>
        <p style="font-size:0.82rem; color:var(--text-secondary); margin-bottom:8px">
          El residuo de la última división es el dígito más significativo (MSD), y el de la primera división es el menos significativo (LSD):
        </p>
        <div class="trail-nodes-container">
          ${trailHtml}
        </div>
        <p style="font-size:0.85rem; font-weight:600; color:var(--accent-cyan); margin-top:8px">
          Número resultante concatenado: ${data.result_str}
        </p>
      </div>
    </div>
  `;
}

/* ===================================================================
   Controles y Ejemplos de Módulo 2 (Bases -> Decimal)
   =================================================================== */

function selectSourceBase(base) {
  AppState.m2.sourceBase = base;
  const container = document.getElementById('chips-source-base');
  if (!container) return;

  container.querySelectorAll('.base-chip').forEach(chip => {
    if (parseInt(chip.getAttribute('data-base')) === base) {
      chip.classList.add('active');
    } else {
      chip.classList.remove('active');
    }
  });

  const conf = BASE_CONFIGS[base];
  document.getElementById('label-source-input').textContent = `Número en ${conf.label}`;
  document.getElementById('allowed-digits-badge').textContent = conf.allowedDesc;
  
  const input = document.getElementById('input-base-val');
  input.placeholder = conf.placeholder;
  input.value = conf.examples[0];

  const exBar = document.getElementById('examples-bar-m2');
  if (exBar) {
    exBar.innerHTML = `<span class="examples-label">Ejemplos rápidos:</span>` +
      conf.examples.map(ex => `<button type="button" class="example-badge" onclick="setBaseExample('${ex}')">${ex}</button>`).join(' ');
  }

  handleConvertToDecimal();
}

function setBaseExample(val) {
  const input = document.getElementById('input-base-val');
  if (input) {
    input.value = val;
    handleConvertToDecimal();
  }
}

async function handleConvertToDecimal() {
  const inputElem = document.getElementById('input-base-val');
  const resultContainer = document.getElementById('result-container-m2');
  if (!inputElem || !resultContainer) return;

  const rawVal = inputElem.value.trim();
  if (rawVal === '') {
    showToast('Por favor ingrese el número a convertir.', 'error');
    return;
  }

  try {
    const response = await fetch('/api/convert/to-decimal', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ value: rawVal, base: AppState.m2.sourceBase })
    });

    const resJson = await response.json();
    if (!resJson.success) {
      showToast(resJson.error || 'Error en la conversión.', 'error');
      return;
    }

    renderModule2Result(resJson.data);
  } catch (err) {
    showToast('Error de comunicación con el servidor local.', 'error');
    console.error(err);
  }
}

function renderModule2Result(data) {
  const container = document.getElementById('result-container-m2');
  container.style.display = 'block';

  // Tarjetas para cada columna de la descomposición polinómica/vectorial
  const vectorCardsHtml = data.terms.map(t => `
    <div class="vector-col-card">
      <span class="vector-pos-badge">Pos ${t.exponent}</span>
      <div class="vector-digit">${t.char}</div>
      <div class="vector-scalar-sub">Escalar d<sub>${t.exponent}</sub> = ${t.scalar_value}</div>
      <div class="vector-divider"></div>
      <div class="vector-weight-label">${t.base}<sup>${t.exponent}</sup> =</div>
      <div class="vector-weight-val">${t.weight}</div>
      <div class="vector-product-val">+ ${t.product}</div>
    </div>
  `).join('');

  container.innerHTML = `
    <!-- Hero Result Banner -->
    <div class="result-hero">
      <div class="result-hero-left">
        <span class="result-hero-label">Equivalente Decimal (Base 10)</span>
        <div class="result-hero-value">(${data.decimal_result})<sub>10</sub></div>
        <span style="color:var(--text-secondary); font-size:0.88rem">
          Equivalencia: (${data.raw_input.trim()})<sub>${data.source_base}</sub> = (${data.decimal_result})<sub>10</sub>
        </span>
      </div>
      <div class="result-hero-actions">
        <button class="btn-copy" onclick="copyToClipboard('${data.decimal_result}', this)">
          ${ICONS.copy}
          <span>Copiar Número</span>
        </button>
      </div>
    </div>

    <!-- Procedure Card -->
    <div class="card procedure-section">
      <div class="procedure-header">
        <h3 class="procedure-title">
          <span>Demostración de la Combinación Lineal Posicional</span>
          <span class="procedure-badge">${data.terms.length} ${data.terms.length === 1 ? 'término' : 'términos'}</span>
        </h3>
        <span style="font-size:0.8rem; color:var(--text-muted)">N = ∑ (d<sub>i</sub> × b<sup>i</sup>)</span>
      </div>

      <!-- Vectorial Cards Grid -->
      <div class="vector-grid">
        ${vectorCardsHtml}
      </div>

      <!-- Vector Notation Card -->
      <div class="vector-notation-card">
        <div class="vector-notation-title">Representación en Álgebra Lineal</div>
        <p style="color:var(--text-secondary); margin-bottom:4px">
          El número representa un vector de coordenadas escalares proyectado sobre la base canónica polinomial del espacio vectorial:
        </p>
        <p style="font-family:var(--font-mono); font-size:0.88rem; color:var(--text-primary)">
          <strong>Vector de Escalares:</strong> [${data.vector_scalars.join(', ')}]<br>
          <strong>Base de Ponderaciones:</strong> [${data.vector_weights.join(', ')}]<br>
          <strong>Producto Escalar:</strong> [${data.vector_scalars.join(', ')}] • [${data.vector_weights.join(', ')}] = <strong>${data.decimal_result}</strong>
        </p>
      </div>

      <!-- Formula Expansion Box -->
      <div class="formula-box">
        <span class="formula-line" style="color:var(--text-muted)">// Expresión formal polinómica de la combinación lineal:</span>
        <span class="formula-line">N = ${data.linear_combination_formula}</span>
        <span class="formula-line" style="color:var(--text-muted)">// Sustitución de ponderaciones b^i:</span>
        <span class="formula-line">  = ${data.linear_combination_eval}</span>
        <span class="formula-line" style="color:var(--text-muted)">// Productos escalares individuales:</span>
        <span class="formula-line">  = ${data.linear_combination_products}</span>
        <span class="formula-line formula-highlight">  = ${data.decimal_result} (decimal)</span>
      </div>
    </div>
  `;
}

/* ===================================================================
   Utilidades (Toast & Clipboard)
   =================================================================== */

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type === 'error' ? 'toast-error' : 'toast-success'}`;
  const iconSvg = type === 'error' ? ICONS.toastError : ICONS.toastSuccess;
  toast.innerHTML = `<span>${iconSvg}</span><span>${message}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function copyToClipboard(text, btnElement = null) {
  navigator.clipboard.writeText(text).then(() => {
    showToast('Copiado al portapapeles: ' + text, 'success');
    if (btnElement) {
      const originalHtml = btnElement.innerHTML;
      btnElement.classList.add('copied');
      btnElement.innerHTML = `${ICONS.check}<span>¡Copiado!</span>`;
      setTimeout(() => {
        btnElement.classList.remove('copied');
        btnElement.innerHTML = originalHtml;
      }, 1600);
    }
  }).catch(() => {
    showToast('No se pudo copiar automáticamente', 'error');
  });
}
