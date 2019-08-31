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

        var img_url = img.src;
        var img_base64 = img_url.split(',');

        var servResponse = document.querySelector('#response');

        document.forms.ourForm.onsubmit = function (e) {
            e.preventDefault();

            var id = String(Math.random()).slice(3)
            var boundary = String(Math.random()).slice(2);
            var boundaryMiddle = '--' + boundary + '\r\n';
            var boundaryLast = '--' + boundary + '--\r\n'

            var body = ['\r\n'];

            body.push('Content-Disposition: form-data; name="log_photo"; filename="od_image_user' + id + '.jpg"\nContent-Type: image/jpeg\r\n\r\n' + img_base64[1] + '\r\n');


            body = body.join(boundaryMiddle) + boundaryLast;


            var xhr = new XMLHttpRequest()

            xhr.open('POST', 'screen', true);

            xhr.setRequestHeader('Content-Type', 'multipart/form-data; boundary=' + boundary)

            xhr.send(body);
        }



    };


    button.addEventListener('click', captureMe);
}