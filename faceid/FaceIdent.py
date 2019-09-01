import dlib
import os
from skimage import io
from scipy.spatial import distance
import pathlib


def get_bool(photo1, photo2):
    PROJECT_ROOT = pathlib.Path(__file__).parent.parent


    file1 = os.path.join(PROJECT_ROOT / 'handlers' / 'shape_predictor.dat')
    file2 = os.path.join(PROJECT_ROOT / 'handlers' / 'dlib_face.dat')
    sp = dlib.shape_predictor(file1)
    facerec = dlib.face_recognition_model_v1(file2)
    detector = dlib.get_frontal_face_detector()

    img = io.imread(photo1)

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

    face_descriptor1 = facerec.compute_face_descriptor(img, shape)

    img2 = io.imread(photo2)

    win2 = dlib.image_window()
    win2.clear_overlay()
    win2.set_image(img2)

    dets_webcam = detector(img2, 1)
    for k, d in enumerate(dets_webcam):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
    shape = sp(img2, d)
    win2.clear_overlay()
    win2.add_overlay(d)
    win2.add_overlay(shape)

    face_descriptor2 = facerec.compute_face_descriptor(img2, shape)

    a = distance.euclidean(face_descriptor1, face_descriptor2)
    print(a)
    i = 1 - a
    print(i)
    if a <= 0.5999:
        return True
    else:
        return False

if __name__ == '__main__':
    get_bool('1.jpg', 'index.png')