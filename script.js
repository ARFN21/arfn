const reportFrame = document.querySelector('[data-report-frame]');
const statusText = document.querySelector('[data-report-status]');
const refreshButton = document.querySelector('[data-refresh-report]');

function setStatus(message, type = 'info') {
  if (!statusText) return;

  statusText.textContent = message;
  statusText.dataset.status = type;
}

function refreshReport() {
  if (!reportFrame) return;

  const baseSrc = reportFrame.getAttribute('src').split('?')[0];
  reportFrame.src = `${baseSrc}?t=${Date.now()}`;
  setStatus('Memuat ulang laporan hasil_ml.html...', 'loading');
}

if (reportFrame) {
  reportFrame.addEventListener('load', () => {
    setStatus('Laporan dimuat. Jika isinya belum sesuai, jalankan ulang proses_worldbank_ml.py lalu klik Refresh Laporan.', 'success');
  });
}

if (refreshButton) {
  refreshButton.addEventListener('click', refreshReport);
}
