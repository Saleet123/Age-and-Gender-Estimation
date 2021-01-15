from pathlib import Path
import cv2
import dlib
import numpy as np
import os
from AGE_GENDER_PREDICTION.settings import BASE_DIR,STATICFILES_DIRS
from omegaconf import OmegaConf
from .src.factory import get_model

pretrained_model = "EfficientNetB3_224_weights.11-3.44.hdf5"
modhash = '6d7f7b7ced093a8b3ef6399163da6ece'

def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
               font_scale=0.8, thickness=1):
    size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    x, y = point
    cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
    cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness, lineType=cv2.LINE_AA)

age=""
gender=""
def main(img,picname):
    path="model"
    outputpath="output"
    age=[]
    gender=[]
    filename = os.path.join(STATICFILES_DIRS[0], path, pretrained_model)
    weight_file = filename
    margin = 0.4
    # for face detection
    detector = dlib.get_frontal_face_detector()
    # load model and weights
    model_name, img_size = Path(weight_file).stem.split("_")[:2]
    img_size = int(img_size)
    cfg = OmegaConf.from_dotlist([f"model.model_name={model_name}", f"model.img_size={img_size}"])
    model = get_model(cfg)
    model.load_weights(weight_file)
    img = cv2.imread(img)

    if img is not None:
        h, w, _ = img.shape
        r = 640 / max(w, h)
        img=cv2.resize(img, (int(w * r), int(h * r)))

    input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_h, img_w, _ = np.shape(input_img)

    # detect faces using dlib detector
    detected = detector(input_img, 1)
    faces = np.empty((len(detected), img_size, img_size, 3))

    if len(detected) > 0:
        for i, d in enumerate(detected):
            x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
            xw1 = max(int(x1 - margin * w), 0)
            yw1 = max(int(y1 - margin * h), 0)
            xw2 = min(int(x2 + margin * w), img_w - 1)
            yw2 = min(int(y2 + margin * h), img_h - 1)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # cv2.rectangle(img, (xw1, yw1), (xw2, yw2), (255, 0, 0), 2)
            faces[i] = cv2.resize(img[yw1:yw2 + 1, xw1:xw2 + 1], (img_size, img_size))

        # predict ages and genders of the detected faces
        results = model.predict(faces)
        predicted_genders = results[0]
        ages = np.arange(0, 101).reshape(101, 1)
        predicted_ages = results[1].dot(ages).flatten()
        # draw results
        for i, d in enumerate(detected):
            label = "{}, {}".format(int(predicted_ages[i]),
                                    "Male" if predicted_genders[i][0] < 0.5 else "Female")

            age.append(label.split(",")[0])
            gender.append(label.split(",")[1])
            draw_label(img, (d.left(), d.top()), label)

    # cv2.imshow("result", img)
    # cv2.waitKey(0)
    output_filename = os.path.join(STATICFILES_DIRS[0], outputpath, picname)
    cv2.imwrite(output_filename, img)
    # cv2.destroyAllWindows()
    return age,gender
