import numpy as np
import cv2
import os


def crop_face(input_folder_path, output_folder_path):
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    images = os.listdir(input_folder_path)
    for image in images:
        image_path = os.path.join(input_folder_path, image)
        img = cv2.imread(image_path)
        height, width, channels = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        
        # 无法识别面部的图片
        if len(faces)==0:
            print(f"No face found in {image_path}")
            return
        
        if len(faces) > 0:
            # 取第一个脸部位置，这里假设一张图片只有一个脸部特征
            x, y, w, h = faces[0]
            # 确定最大正方形的位置
            square_size=min(width-x,x,y,height-y)
           
                
            # 根据最大正方形位置裁剪图片并保存
            cropped_img = img[y-square_size:y+h+square_size, x-square_size:x+w+square_size] #img[y1:y2, x1:x2]
            # 调整图像大小为512x512
            resized = cv2.resize(cropped_img, (512, 512), interpolation=cv2.INTER_AREA)
            output_path = os.path.join(output_folder_path, image)
            cv2.imwrite(output_path, resized)


if __name__ == "__main__":
    input_folder = r"D:\pytest\testphoto"  
    output_folder = r"D:\pytest\tt2" 
    # 创建输出目录
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    crop_face(input_folder, output_folder)
    print('Done!')