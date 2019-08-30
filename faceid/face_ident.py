import dlib
from skimage import io
from scipy.spatial import distance

sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()


def descriptor(photo):
    img = io.imread(photo)

    win1 = dlib.image_window()
    win1.clear_overlay()
    win1.set_image(img)

    dets = detector(img, 1)
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        shape = sp(img, d)
        win1.clear_overlay()
        win1.add_overlay(d)
        win1.add_overlay(shape)

    face_descriptor = facerec.compute_face_descriptor(img, shape)

    return face_descriptor



def euclid(face1, face2):
    model = distance.euclidean(face1, face2)

    if model < 0.666:
        this_user = True
    else:
        this_user = False

    return this_user

def main():
    face_descriptor1 = descriptor('1.jpg')
    face_descriptor2 = descriptor('2.jpg')
    bool = euclid(face_descriptor1, face_descriptor2)
    return bool


if __name__ == '__main__':
    main()