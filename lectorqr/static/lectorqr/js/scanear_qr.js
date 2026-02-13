document.addEventListener("DOMContentLoaded", function () {

  let initial_code_result = true;

  const video = document.createElement("video");
  const canvasElement = document.getElementById("canvas");
  const canvas = canvasElement.getContext("2d");
  const loadingMessage = document.getElementById("loadingMessage");
  const outputContainer = document.getElementById("output");
  const outputMessage = document.getElementById("outputMessage");
  const outputData = document.getElementById("outputData");
  const sonido = document.getElementById("sonido_qr");

  function drawLine(begin, end, color) {
    canvas.beginPath();
    canvas.moveTo(begin.x, begin.y);
    canvas.lineTo(end.x, end.y);
    canvas.lineWidth = 4;
    canvas.strokeStyle = color;
    canvas.stroke();
  }

  navigator.mediaDevices.getUserMedia({
    video: { facingMode: "environment" }
  })
  .then(function (stream) {
    video.srcObject = stream;
    video.setAttribute("playsinline", true);
    video.play();
    requestAnimationFrame(tick);
  })
  .catch(function (err) {
    loadingMessage.innerText = "❌ No se pudo acceder a la cámara";
    console.error(err);
  });

  function tick() {
    loadingMessage.innerText = "⌛ Cargando Video...";

    if (video.readyState === video.HAVE_ENOUGH_DATA) {
      loadingMessage.hidden = true;
      canvasElement.hidden = false;
      outputContainer.hidden = false;

      canvasElement.height = video.videoHeight;
      canvasElement.width = video.videoWidth;
      canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);

      const imageData = canvas.getImageData(
        0, 0, canvasElement.width, canvasElement.height
      );

      const code = jsQR(
        imageData.data,
        imageData.width,
        imageData.height,
        { inversionAttempts: "dontInvert" }
      );

      if (code && initial_code_result && code.data) {

        drawLine(code.location.topLeftCorner, code.location.topRightCorner, "#FF3B58");
        drawLine(code.location.topRightCorner, code.location.bottomRightCorner, "#FF3B58");
        drawLine(code.location.bottomRightCorner, code.location.bottomLeftCorner, "#FF3B58");
        drawLine(code.location.bottomLeftCorner, code.location.topLeftCorner, "#FF3B58");

        outputMessage.hidden = true;
        outputData.parentElement.hidden = false;
        outputData.innerText = code.data;

        sonido.play().catch(() => {});

        guardar_codigo_escaneado(code.data);
        console.log(code.data);

        initial_code_result = false;
        setTimeout(() => {
          initial_code_result = true;
        }, 6000);
      }
    }

    requestAnimationFrame(tick);
  }

});
