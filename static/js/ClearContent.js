// ClearContent.js — CreditPulse v2.0
// Handles reset of the premium results panel, gauge, and form state

document.addEventListener('DOMContentLoaded', function () {
  const clearBtn = document.getElementById('clear-button');
  if (!clearBtn) return;

  clearBtn.addEventListener('click', function () {
    // Clear Flask-rendered content
    const predEl = document.getElementById('prediction-result');
    const summaryEl = document.getElementById('summary-content');
    if (predEl) predEl.innerHTML = '';
    if (summaryEl) summaryEl.innerHTML = '';

    // Hide & reset the results panel
    const panel = document.getElementById('results-panel');
    if (panel) {
      panel.classList.remove('visible', 'high-risk-pulse');
      panel.style.display = 'none';
    }

    // Reset gauge arc
    const arc = document.getElementById('gauge-arc-path');
    if (arc) {
      arc.style.strokeDashoffset = '235';
      arc.style.stroke = '#10b981';
    }

    // Reset gauge needle to far-left
    const needle = document.getElementById('gauge-needle');
    if (needle) {
      needle.style.transform = 'rotate(-135deg)';
    }

    // Reset gauge text
    const pctText = document.getElementById('gauge-pct-text');
    if (pctText) pctText.textContent = '—';

    // Reset badge
    const badge = document.getElementById('risk-badge');
    if (badge) {
      badge.textContent = 'Awaiting Analysis';
      badge.style.background = 'rgba(255,255,255,0.05)';
      badge.style.color = 'rgba(148,163,184,0.7)';
      badge.style.border = '1px solid rgba(255,255,255,0.08)';
    }

    // Hide summary rows
    const dataSummary = document.getElementById('data-summary');
    if (dataSummary) dataSummary.style.display = 'none';

    // Reset headline
    const headline = document.getElementById('result-headline');
    if (headline) {
      headline.textContent = 'Analysis Complete';
      headline.style.color = 'white';
    }

    // Clear session storage
    sessionStorage.removeItem('cp_form_snapshot');
  });
});
