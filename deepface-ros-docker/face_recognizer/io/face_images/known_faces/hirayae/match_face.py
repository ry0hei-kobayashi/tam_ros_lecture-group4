from deepface import DeepFace
import cv2

IMAGES = []

for image in IMAGES:
   face_objs = DeepFace.extract_faces(img_path = image, detector_backend = backend, enforce_detection = False, align = False)

   img = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)
   for face_obj in face_objs:
     box = face_obj['facial_area']
     if box['left_eye'] is not None:
       cv2.rectangle(img, (box['x'], box['y']), (box['x'] + box['w'], box['y'] + box['h']), (255, 0, 0), 5)
   cv2.imwrite(f'{backend}_{image}', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

  s = time.perf_counter()
  for i in range(10):
    for image in IMAGES:
      face_objs = DeepFace.extract_faces(img_path = image, detector_backend = backend, enforce_detection = False, align = False)
  print(f'{backend}: {(time.perf_counter()-s)/100} s')
