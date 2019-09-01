import face_recognition
import cv2
import pathlib
import time
import os

def screen():
    cap = cv2.VideoCapture(0)

    for i in range(30):
        cap.read()

    ret, frame = cap.read()

    data = str(time.time()).split('.')[0]

    PROJECT_ROOT = pathlib.Path(__file__).parent.parent

    static_dir = str(PROJECT_ROOT / 'static')

    login_photo = os.path.join(static_dir + '/photoLogin/login_photo' + data + '.jpg')

    cv2.imwrite(login_photo, frame)

    cap.release()

    return login_photo


def ident(photo_user, login_photo):
    known_image = face_recognition.load_image_file(photo_user)
    unknown_image = face_recognition.load_image_file(login_photo)

    biden_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.compare_faces([biden_encoding], unknown_encoding)[0]

    return results


if __name__ == '__main__':
    print(ident('1.jpg', '2.jpg'))
