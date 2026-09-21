/**
 * Calculadora de Sistemas Numéricos - Álgebra Lineal UAM
 * Frontend Controller & UI Logic
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
    allowedRegex: /^[0-1]+$/,
    allowedDesc: '[0, 1]',
    examples: ['10110', '11111111', '101', '0'],
    placeholder: 'Ej. 10110'
  },
  8: {
    name: 'Octal',
    label: 'Base 8 (Octal)',
    allowedRegex: /^[0-7]+$/,
    allowedDesc: '[0-7]',
    examples: ['377', '1647', '52', '0'],
    placeholder: 'Ej. 377'
  },
  16: {
    name: 'Hexadecimal',
    label: 'Base 16 (Hexadecimal)',
    allowedRegex: /^[0-9A-Fa-f]+$/,
    allowedDesc: '[0-9, A-F]',
    examples: ['3A7', 'FF', '1A', '0'],
    placeholder: 'Ej. 3A7'
  }
};

// Inicialización cuando carga el DOM
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initTabs();
  initForms();
  // Disparar conversiones iniciales por defecto para que la vista tenga contenido inmediato
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
    icon.textContent = AppState.theme === 'dark' ? '☀️' : '🌙';
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
      // Remover clase active de todas las pestañas
      tabs.forEach(t => {
        document.getElementById(t.id)?.classList.remove('active');
        document.getElementById(t.panel)?.classList.remove('active');
        document.getElementById(t.id)?.setAttribute('aria-selected', 'false');
      });

      // Activar la seleccionada
      btn.classList.add('active');
      document.getElementById(tab.panel)?.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      // Si se abre el módulo 2 por primera vez sin resultado, ejecutar ejemplo
      if (tab.id === 'tab-module2' && !document.getElementById('result-container-m2').innerHTML) {
        handleConvertToDecimal();
      }
    });
  });
}

/* ===================================================================
   Controles y Ejemplos de Módulo 1 (Decimal -> Bases)
   =================================================================== */

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

  // Actualizar etiqueta, placeholders y ejemplos
  const conf = BASE_CONFIGS[base];
  document.getElementById('label-source-input').textContent = `Número en ${conf.label}`;
  document.getElementById('allowed-digits-badge').textContent = conf.allowedDesc;
  
  const input = document.getElementById('input-base-val');
  input.placeholder = conf.placeholder;
  input.value = conf.examples[0];

  // Actualizar barra de ejemplos
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

function initForms() {
  // Listeners para submits se configuraron inline en onsubmit
}

/* ===================================================================
   Sistema de Notificaciones Toast
   =================================================================== */

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type === 'error' ? 'toast-error' : 'toast-success'}`;
  const icon = type === 'error' ? '⚠️' : '✅';
  toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    showToast('Copiado al portapapeles: ' + text, 'success');
  }).catch(() => {
    showToast('No se pudo copiar automáticamente', 'error');
  });
}
