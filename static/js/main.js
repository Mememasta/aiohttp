navigator.getUserMedia = navigator.getUserMedia ||
navigator.webkitGetUserMedia ||
navigator.mozGetUserMedia;

if (navigator.getUserMedia) {
navigator.getUserMedia({ audio: false, video: { width: 1920, height: 1080 } },
  function(stream) {
     var video = document.querySelector('video');
     video.srcObject = stream;
     video.onloadedmetadata = function(e) {
       video.play();
     };
  },
  function(err) {
     console.log("The following error occurred: " + err.name);
  }
);
} else {
console.log("getUserMedia not supported");
}

window.onload = function () {
    var canvas = document.getElementById('canvas');
    var video = document.getElementById('video');
    var button = document.getElementById('button');
    var allow = document.getElementById('allow');
    var context = canvas.getContext('2d');

    var captureMe = function () {
        context.translate(canvas.width, 0);
        context.scale(-1, 1);
        context.drawImage(video, 0, 0, video.width, video.height);
        var base64dataUrl = canvas.toDataURL('image/jpg');
        context.setTransform(1, 0, 0, 1, 0, 0);
        var img = new Image();
        img.src = base64dataUrl;

        function b64toBlob(b64Data, contentType, sliceSize) {
            contentType = contentType || '';
            sliceSize = sliceSize || 512;

            var byteCharacters = atob(b64Data);
            var byteArrays = [];

            for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
                var slice = byteCharacters.slice(offset, offset + sliceSize);

                var byteNumbers = new Array(slice.length);
                for (var i = 0; i < slice.length; i++) {
                    byteNumbers[i] = slice.charCodeAt(i);
                }

                var byteArray = new Uint8Array(byteNumbers);

                byteArrays.push(byteArray);
            }

          var blob = new Blob(byteArrays, {type: contentType});
          return blob;
        }

        var block = base64dataUrl.split(";");
        var contentType = block[0].split(":")[1];
        var realData = block[1].split(",")[1];

        var blob = b64toBlob(realData, contentType);



        var servResponse = document.querySelector('#response');

        document.forms.ourForm.onsubmit = function (e) {
            e.preventDefault();

            var boundary = String(Math.random()).slice(2);
            var boundaryMiddle = '--' + boundary + '\r\n';
            var boundaryLast = '--' + boundary + '--\r\n'

            var body = ['\r\n'];

            body.push('Content-Disposition: form-data; name="log_photo"; filename="log_user.jpg"\nContent-Type: image/jpeg\r\n\r\n' + img.src + '\r\n');


            body = body.join(boundaryMiddle) + boundaryLast;


            var xhr = new XMLHttpRequest()

            xhr.open('POST', 'screen', true);

            xhr.setRequestHeader('Content-Type', 'multipart/form-data; boundary=' + boundary)

            xhr.send(body);
        }

    };


    button.addEventListener('click', captureMe);
}