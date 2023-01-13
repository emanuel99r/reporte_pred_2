function addScript(url) {
    var script = document.createElement('script');
    script.type = 'application/javascript';
    script.src = url;
    document.head.appendChild(script);
}

//addScript('https://raw.githack.com/eKoopmans/html2pdf/master/dist/html2pdf.bundle.js');
addScript('https://html2canvas.hertzen.com/dist/html2canvas.js');

//addScript('https://cdnjs.cloudflare.com/ajax/libs/html2canvas/0.4.1/html2canvas.js');
//addScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/1.5.1/jspdf.debug.js');