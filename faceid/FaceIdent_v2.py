import face_recognition


def ident(photo_user, login_photo):
    known_image = face_recognition.load_image_file(photo_user)
    unknown_image = face_recognition.load_image_file(login_photo)

    biden_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.compare_faces([biden_encoding], unknown_encoding)[0]
    return results

if __name__ == '__main__':
    ident('1.jpg', '8.jpg')