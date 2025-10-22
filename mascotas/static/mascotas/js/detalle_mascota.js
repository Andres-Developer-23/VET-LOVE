// Funcionalidad para la página de detalle de mascota
// Imprimir el carnet renderizándolo como imagen para evitar problemas de carga/estilos en ventanas nuevas
async function exportarCarnet(contenedorId, titulo) {
  try {
    const el = document.getElementById(contenedorId);
    if (!el) return;
    // Asegurar que html2canvas está disponible (se carga en extra_js)
    if (typeof html2canvas === 'undefined') {
      alert('No se pudo cargar el motor de impresión. Intente de nuevo.');
      return;
    }
    const canvas = await html2canvas(el, { scale: 2, useCORS: true, backgroundColor: '#ffffff' });
    const img = canvas.toDataURL('image/png');
    const w = window.open('', '_blank');
    w.document.write('<html><head><meta charset="utf-8"><title>' + titulo + '</title>');
    w.document.write('<style>@page{size:A4;margin:15mm;} body{margin:0;padding:0;text-align:center;background:#fff;} img{max-width:100%;width:100%;}</style>');
    w.document.write('</head><body>');
    w.document.write('<img src="' + img + '" alt="' + titulo + '">');
    w.document.write('</body></html>');
    w.document.close();
    w.onload = function(){
      setTimeout(function(){
        w.focus();
        w.print();
        w.close();
      }, 300);
    };
  } catch (e) {
    console.error(e);
    alert('No se pudo imprimir el carnet. Use Descargar PDF como alternativa.');
  }
}

// Descarga directa del carnet como PDF (cliente)
window.descargarCarnetPDF = async function(contenedorId, fileBaseName) {
  try {
    const el = document.getElementById(contenedorId);
    if (!el) return;
    const { jsPDF } = window.jspdf;
    const canvas = await html2canvas(el, { scale: 2, useCORS: true, backgroundColor: '#ffffff' });
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const margin = 10;
    let imgWidth = pageWidth - margin * 2;
    let imgHeight = canvas.height * imgWidth / canvas.width;
    if (imgHeight > pageHeight - margin * 2) {
      // Si es más alto que la página, ajusta a altura
      imgHeight = pageHeight - margin * 2;
      imgWidth = canvas.width * imgHeight / canvas.height;
    }
    const x = (pageWidth - imgWidth) / 2;
    const y = margin;
    pdf.addImage(imgData, 'PNG', x, y, imgWidth, imgHeight, undefined, 'FAST');
    pdf.save(fileBaseName + '.pdf');
  } catch (e) {
    console.error(e);
    alert('No se pudo generar el PDF. Intente usar el botón Imprimir.');
  }
};

document.addEventListener('DOMContentLoaded', function() {
  var el = document.getElementById('calendario-vacunas');
  if (!el) return;
  var calendar = new FullCalendar.Calendar(el, {
    initialView: 'dayGridMonth',
    height: 'auto',
    locale: 'es',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,listMonth'
    },
    events: window.calendarioVacunasUrl,
    displayEventTime: false,
    eventClick: function(info) {
      info.jsEvent.preventDefault();
    }
  });
  calendar.render();
});
