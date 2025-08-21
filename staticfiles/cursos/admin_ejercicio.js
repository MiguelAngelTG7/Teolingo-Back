// Actualiza el combo de respuesta correcta según las opciones ingresadas
(function() {
  function updateChoices() {
    var opcionesText = document.getElementById('id_opciones_text');
    var respuestaSelect = document.getElementById('id_respuesta_correcta');
    if (!opcionesText || !respuestaSelect) return;
    var opciones = opcionesText.value.split('\n').map(function(line) {
      return line.trim();
    }).filter(function(line) { return line.length > 0; });
    // Limpiar opciones actuales
    respuestaSelect.innerHTML = '<option value="">---------</option>';
    opciones.forEach(function(op) {
      var opt = document.createElement('option');
      opt.value = op;
      opt.textContent = op;
      respuestaSelect.appendChild(opt);
    });
  }
  document.addEventListener('DOMContentLoaded', function() {
    var opcionesText = document.getElementById('id_opciones_text');
    if (opcionesText) {
      opcionesText.addEventListener('input', updateChoices);
      updateChoices();
    }
  });
})();
