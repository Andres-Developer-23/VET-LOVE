// Funcionalidad para la página de detalle de mascota
// Imprimir el carnet renderizándolo como imagen para evitar problemas de carga/estilos en ventanas nuevas
async function exportarCarnet(contenedorId, titulo) {
  console.log('Iniciando exportarCarnet para:', contenedorId);

  try {
    const el = document.getElementById(contenedorId);
    if (!el) {
      console.error('Contenedor no encontrado:', contenedorId);
      alert('Contenedor no encontrado.');
      return;
    }

    console.log('Contenedor encontrado, verificando html2canvas...');
    // Asegurar que html2canvas está disponible
    if (typeof html2canvas === 'undefined') {
      console.error('html2canvas no está disponible');
      alert('No se pudo cargar el motor de impresión. Intente de nuevo.');
      return;
    }

    console.log('Buscando cards para imprimir...');
    const cards = el.querySelectorAll('.print-card');
    console.log('Cards encontradas:', cards.length);

    if (cards.length === 0) {
      alert('No se encontraron cards para imprimir.');
      return;
    }

    // Mostrar indicador de carga
    const originalContent = el.innerHTML;
    el.innerHTML = '<div class="text-center p-4"><div class="spinner-border" role="status"><span class="visually-hidden">Generando impresión...</span></div><p>Generando vista de impresión...</p></div>';

    try {
      console.log('Creando contenedor temporal...');
      // Crear un contenedor temporal visible para renderizado correcto
      const tempContainer = document.createElement('div');
      tempContainer.style.position = 'fixed';
      tempContainer.style.left = '0';
      tempContainer.style.top = '0';
      tempContainer.style.width = '800px';
      tempContainer.style.background = '#ffffff';
      tempContainer.style.padding = '20px';
      tempContainer.style.zIndex = '9999';
      tempContainer.style.opacity = '1';

      // Clonar las cards con estilos aplicados
      cards.forEach((card, index) => {
        console.log('Clonando card', index + 1);
        const clonedCard = card.cloneNode(true);
        clonedCard.style.width = '100%';
        clonedCard.style.marginBottom = '0';
        clonedCard.style.boxShadow = 'none';
        clonedCard.style.border = '1px solid #dee2e6';
        tempContainer.appendChild(clonedCard);

        // Agregar separador entre cards
        if (index < cards.length - 1) {
          const separator = document.createElement('div');
          separator.style.height = '40px';
          tempContainer.appendChild(separator);
        }
      });

      document.body.appendChild(tempContainer);
      console.log('Contenedor temporal agregado al DOM');

      // Esperar a que se renderice completamente
      await new Promise(resolve => {
        setTimeout(() => {
          console.log('Forzando reflow...');
          tempContainer.offsetHeight;
          resolve();
        }, 500);
      });

      console.log('Capturando canvas con html2canvas...');
      const canvas = await html2canvas(tempContainer, {
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff',
        allowTaint: false,
        logging: true,
        width: tempContainer.offsetWidth,
        height: tempContainer.offsetHeight
      });

      console.log('Canvas capturado, dimensiones:', canvas.width, 'x', canvas.height);

      // Limpiar contenedor temporal
      document.body.removeChild(tempContainer);
      console.log('Contenedor temporal removido');

      // Restaurar contenido original
      el.innerHTML = originalContent;

      const img = canvas.toDataURL('image/png');
      console.log('Imagen generada, abriendo ventana...');

      const w = window.open('', '_blank');

      if (!w) {
        alert('El navegador bloqueó la ventana emergente. Permita popups para este sitio.');
        return;
      }

      const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <title>${titulo}</title>
          <style>
            @page { size: A4; margin: 15mm; }
            body {
              margin: 0;
              padding: 0;
              text-align: center;
              background: #fff;
              font-family: Arial, sans-serif;
            }
            img {
              max-width: 100%;
              width: 100%;
              height: auto;
              display: block;
              margin: 0 auto;
            }
            .print-controls {
              position: fixed;
              top: 10px;
              right: 10px;
              background: #f8f9fa;
              padding: 10px;
              border-radius: 5px;
              box-shadow: 0 2px 10px rgba(0,0,0,0.1);
              z-index: 1000;
            }
            @media print {
              .print-controls { display: none; }
            }
          </style>
        </head>
        <body>
          <div class="print-controls">
            <button onclick="window.print()" style="margin-right: 10px;">Imprimir</button>
            <button onclick="window.close()">Cerrar</button>
          </div>
          <img src="${img}" alt="${titulo}" onload="console.log('Imagen cargada en ventana de impresión')">
        </body>
        </html>
      `;

      w.document.write(htmlContent);
      w.document.close();

      // Usar setTimeout en lugar de onload para evitar problemas de message channel
      setTimeout(function(){
        try {
          console.log('Ejecutando impresión...');
          w.focus();
          w.print();
          setTimeout(function(){
            w.close();
          }, 1000);
        } catch (e) {
          console.error('Error al imprimir:', e);
        }
      }, 500);

      console.log('Vista de impresión generada exitosamente');

    } catch (error) {
      console.error('Error generando vista de impresión:', error);
      el.innerHTML = originalContent;
      alert('Error generando la vista de impresión. Intente descargar PDF.');
    }
  } catch (e) {
    console.error('Error en exportarCarnet:', e);
    alert('No se pudo preparar la impresión. Intente descargar PDF.');
  }
}

// Descarga directa del carnet como PDF (cliente)
window.descargarCarnetPDF = async function(contenedorId, fileBaseName) {
  console.log('Iniciando descargarCarnetPDF para:', contenedorId);

  try {
    const el = document.getElementById(contenedorId);
    if (!el) {
      console.error('Contenedor no encontrado:', contenedorId);
      alert('Contenedor no encontrado.');
      return;
    }

    console.log('Verificando jsPDF...');
    if (!window.jspdf || typeof window.jspdf.jsPDF !== 'function') {
      console.error('jsPDF no está disponible');
      alert('No se pudo cargar el generador de PDF. Intente usar Imprimir.');
      return;
    }
    const jsPDF = window.jspdf.jsPDF;

    console.log('Buscando cards para PDF...');
    const cards = el.querySelectorAll('.print-card');
    console.log('Cards encontradas:', cards.length);

    if (cards.length === 0) {
      alert('No se encontraron cards para generar PDF.');
      return;
    }

    // Mostrar indicador de carga
    const originalContent = el.innerHTML;
    el.innerHTML = '<div class="text-center p-4"><div class="spinner-border" role="status"><span class="visually-hidden">Generando PDF...</span></div><p>Generando PDF...</p></div>';

    try {
      console.log('Creando instancia de jsPDF...');
      const pdf = new jsPDF('p', 'mm', 'a4');
      console.log('jsPDF creado exitosamente');

      console.log('Procesando', cards.length, 'cards...');

      for (let i = 0; i < cards.length; i++) {
        console.log('Procesando card', i + 1);
        const card = cards[i];

        // Crear contenedor temporal visible para renderizado correcto
        const tempContainer = document.createElement('div');
        tempContainer.style.position = 'fixed';
        tempContainer.style.left = '0';
        tempContainer.style.top = '0';
        tempContainer.style.width = '794px'; // 210mm en pixels
        tempContainer.style.minHeight = '1123px'; // 297mm en pixels
        tempContainer.style.background = '#ffffff';
        tempContainer.style.padding = '0';
        tempContainer.style.zIndex = '9999';
        tempContainer.style.opacity = '1';
        tempContainer.style.fontFamily = "'Times New Roman', serif";
        tempContainer.style.transform = 'scale(1)';
        tempContainer.style.transformOrigin = 'top left';
        tempContainer.style.overflow = 'visible';

        // Aplicar estilos inline para asegurar que se mantengan
        const clonedCard = card.cloneNode(true);
        clonedCard.style.width = '794px';
        clonedCard.style.minHeight = '1123px';
        clonedCard.style.boxShadow = 'none';
        clonedCard.style.border = 'none';
        clonedCard.style.margin = '0';
        clonedCard.style.padding = '0';
        clonedCard.style.background = '#ffffff';

        // Copiar todos los estilos computados
        const computedStyles = window.getComputedStyle(card);
        const allStyles = [
          'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'color',
          'backgroundColor', 'border', 'padding', 'margin', 'textAlign',
          'display', 'flexDirection', 'justifyContent', 'alignItems'
        ];

        allStyles.forEach(style => {
          clonedCard.style[style] = computedStyles[style];
        });

        // Copiar estilos de elementos hijos recursivamente
        function copyStyles(source, target) {
          const children = source.children;
          const targetChildren = target.children;

          for (let i = 0; i < children.length; i++) {
            if (targetChildren[i]) {
              const childComputed = window.getComputedStyle(children[i]);
              const childStyles = [
                'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'color',
                'backgroundColor', 'border', 'padding', 'margin', 'textAlign',
                'display', 'flexDirection', 'justifyContent', 'alignItems',
                'width', 'height', 'position'
              ];

              childStyles.forEach(style => {
                targetChildren[i].style[style] = childComputed[style];
              });

              // Recursivo para hijos
              copyStyles(children[i], targetChildren[i]);
            }
          }
        }

        copyStyles(card, clonedCard);

        tempContainer.appendChild(clonedCard);

        document.body.appendChild(tempContainer);
        console.log('Contenedor temporal creado para card', i + 1);

        try {
          // Esperar renderizado completo
          await new Promise(resolve => setTimeout(resolve, 1000));

          console.log('Capturando canvas para card', i + 1);
          const canvas = await html2canvas(tempContainer, {
            scale: 2,
            useCORS: true,
            backgroundColor: '#ffffff',
            allowTaint: false,
            logging: false,
            width: tempContainer.offsetWidth,
            height: tempContainer.offsetHeight,
            scrollX: 0,
            scrollY: 0,
            windowWidth: tempContainer.offsetWidth,
            windowHeight: tempContainer.offsetHeight,
            x: 0,
            y: 0
          });

          console.log('Canvas capturado para card', i + 1, 'dimensiones:', canvas.width, 'x', canvas.height);

          const imgData = canvas.toDataURL('image/png', 1.0);

          // Calcular dimensiones manteniendo proporción
          const canvasAspectRatio = canvas.width / canvas.height;
          const pageWidth = 210;
          const pageHeight = 297;
          const pageAspectRatio = pageWidth / pageHeight;

          let imgWidth, imgHeight, x, y;

          if (canvasAspectRatio > pageAspectRatio) {
            // Canvas más ancho que A4
            imgWidth = pageWidth;
            imgHeight = pageWidth / canvasAspectRatio;
            x = 0;
            y = (pageHeight - imgHeight) / 2;
          } else {
            // Canvas más alto que A4
            imgHeight = pageHeight;
            imgWidth = pageHeight * canvasAspectRatio;
            x = (pageWidth - imgWidth) / 2;
            y = 0;
          }

          if (i > 0) {
            pdf.addPage();
            console.log('Nueva página agregada para card', i + 1);
          }

          console.log('Agregando imagen al PDF para card', i + 1, 'pos:', x, y, 'size:', imgWidth, imgHeight);
          pdf.addImage(imgData, 'PNG', x, y, imgWidth, imgHeight, undefined, 'FAST');

        } finally {
          document.body.removeChild(tempContainer);
          console.log('Contenedor temporal removido para card', i + 1);
        }
      }

      // Restaurar contenido original
      el.innerHTML = originalContent;
      console.log('Contenido original restaurado');

      // Descargar PDF
      console.log('Descargando PDF...');
      pdf.save(fileBaseName + '.pdf');
      console.log('PDF descargado exitosamente');

    } catch (error) {
      console.error('Error generando PDF:', error);
      el.innerHTML = originalContent;
      alert('Error generando PDF. Intente usar Imprimir.');
    }
  } catch (e) {
    console.error('Error en descargarCarnetPDF:', e);
    alert('No se pudo iniciar la descarga del PDF.');
  }
};

// Descarga plantilla vacía para llenado manual
function descargarPlantillaVacia(contenedorId, fileBaseName) {
  console.log('Función descargarPlantillaVacia ejecutándose con:', contenedorId, fileBaseName);
  alert('Función descargarPlantillaVacia ejecutándose. Esta es una versión simplificada.');
}

// Función para exportar tabla de vacunas a PDF
async function exportarTablaVacunasPDF(nombreMascota) {
  console.log('Iniciando exportarTablaVacunasPDF para:', nombreMascota);

  try {
    // Verificar jsPDF
    if (!window.jspdf || typeof window.jspdf.jsPDF !== 'function') {
      console.error('jsPDF no está disponible');
      alert('No se pudo cargar el generador de PDF.');
      return;
    }
    const jsPDF = window.jspdf.jsPDF;

    // Crear PDF
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const margin = 20;
    const contentWidth = pageWidth - (margin * 2);

    // Título
    pdf.setFontSize(16);
    pdf.setFont('helvetica', 'bold');
    pdf.text('Registro de Vacunación', pageWidth / 2, margin, { align: 'center' });

    pdf.setFontSize(12);
    pdf.setFont('helvetica', 'normal');
    pdf.text(`Mascota: ${nombreMascota}`, pageWidth / 2, margin + 10, { align: 'center' });
    pdf.text(`Fecha de emisión: ${new Date().toLocaleDateString('es-ES')}`, pageWidth / 2, margin + 18, { align: 'center' });

    // Obtener datos de la tabla
    const table = document.querySelector('.table-excel');
    if (!table) {
      alert('No se encontró la tabla de vacunas.');
      return;
    }

    const headers = [];
    const data = [];

    // Extraer encabezados
    const headerCells = table.querySelectorAll('thead th');
    headerCells.forEach(cell => {
      headers.push(cell.textContent.trim());
    });

    // Extraer filas de datos
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
      const rowData = [];
      const cells = row.querySelectorAll('td');
      cells.forEach(cell => {
        // Remover badges y obtener solo texto
        const badge = cell.querySelector('.badge');
        if (badge) {
          rowData.push(badge.textContent.trim());
        } else {
          rowData.push(cell.textContent.trim());
        }
      });
      data.push(rowData);
    });

    // Configurar tabla
    const startY = margin + 30;
    const rowHeight = 8;
    const colWidth = contentWidth / headers.length;

    // Dibujar encabezados
    pdf.setFillColor(240, 240, 240); // Gris claro
    pdf.rect(margin, startY, contentWidth, rowHeight, 'F');

    pdf.setFont('helvetica', 'bold');
    pdf.setFontSize(10);
    headers.forEach((header, index) => {
      const x = margin + (colWidth * index) + 2;
      pdf.text(header, x, startY + 6);
    });

    // Dibujar borde del encabezado
    pdf.setDrawColor(0, 0, 0);
    pdf.setLineWidth(0.5);
    pdf.rect(margin, startY, contentWidth, rowHeight);

    // Dibujar filas de datos
    let currentY = startY + rowHeight;
    pdf.setFont('helvetica', 'normal');
    pdf.setFontSize(9);

    data.forEach((row, rowIndex) => {
      // Fondo alterno
      if (rowIndex % 2 === 0) {
        pdf.setFillColor(249, 249, 249);
        pdf.rect(margin, currentY, contentWidth, rowHeight, 'F');
      }

      // Dibujar celdas
      row.forEach((cell, cellIndex) => {
        const x = margin + (colWidth * cellIndex) + 2;
        const maxWidth = colWidth - 4;
        const lines = pdf.splitTextToSize(cell, maxWidth);
        pdf.text(lines, x, currentY + 5);
      });

      // Dibujar borde de fila
      pdf.rect(margin, currentY, contentWidth, rowHeight);

      currentY += rowHeight;

      // Nueva página si es necesario
      if (currentY > pageHeight - margin) {
        pdf.addPage();
        currentY = margin;

        // Repetir encabezados en nueva página
        pdf.setFillColor(240, 240, 240);
        pdf.rect(margin, currentY, contentWidth, rowHeight, 'F');
        pdf.setFont('helvetica', 'bold');
        pdf.setFontSize(10);
        headers.forEach((header, index) => {
          const x = margin + (colWidth * index) + 2;
          pdf.text(header, x, currentY + 6);
        });
        pdf.rect(margin, currentY, contentWidth, rowHeight);
        currentY += rowHeight;
        pdf.setFont('helvetica', 'normal');
        pdf.setFontSize(9);
      }
    });

    // Pie de página
    const footerY = pageHeight - 15;
    pdf.setFontSize(8);
    pdf.setFont('helvetica', 'italic');
    pdf.text('Documento generado por Veterinaria Vet Love', pageWidth / 2, footerY, { align: 'center' });

    // Descargar PDF
    const fileName = `Registro_Vacunacion_${nombreMascota.replace(/\s+/g, '_')}.pdf`;
    pdf.save(fileName);
    console.log('PDF de tabla de vacunas generado exitosamente');

  } catch (error) {
    console.error('Error generando PDF de tabla de vacunas:', error);
    alert('Error generando el PDF. Intente de nuevo.');
  }
}

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