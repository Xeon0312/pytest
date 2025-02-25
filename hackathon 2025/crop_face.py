import numpy as np
import cv2
import os

def expand_image_to_square(image, target_size=512, border_type=cv2.BORDER_REPLICATE):
    h, w, _ = image.shape
    max_dim = max(h, w)
    pad_top = (max_dim - h) // 2
    pad_bottom = max_dim - h - pad_top
    pad_left = (max_dim - w) // 2
    pad_right = max_dim - w - pad_left
    
    # Use the selected border fill method
    padded_img = cv2.copyMakeBorder(image, pad_top, pad_bottom, pad_left, pad_right, border_type)
    return cv2.resize(padded_img, (target_size, target_size), interpolation=cv2.INTER_AREA)

def crop_face(input_folder_path, output_folder_path):
    # Loading the DNN face detection model
    model_folder = r"D:\pytest\face_models"
    modelFile = os.path.join(model_folder, "res10_300x300_ssd_iter_140000.caffemodel")
    configFile = os.path.join(model_folder, "deploy.prototxt")
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    
    images = os.listdir(input_folder_path)
    print(f"Processing {len(images)} images...")
    
    for image in images:
        image_path = os.path.join(input_folder_path, image)
        img = cv2.imread(image_path)
        height, width, _ = img.shape
        
        # Preprocessing images for DNN detection
        blob = cv2.dnn.blobFromImage(img, scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()
        
        if detections.shape[2] == 0:
            print(f"No face found in {image_path}")
            continue
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (x, y, x2, y2) = box.astype("int")
                
                # Adjust the face area size to keep the face in the center
                expansion_factor = 2
                w, h = x2 - x, y2 - y
                new_w, new_h = int(w * expansion_factor), int(h * expansion_factor)
                new_x = max(0, x - (new_w - w) // 2)
                new_y = max(0, y - (new_h - h) // 2)
                new_x2 = min(width, new_x + new_w)
                new_y2 = min(height, new_y + new_h)
                
                cropped_img = img[new_y:new_y2, new_x:new_x2]
                
                # Make sure the cropped image is a square and expand it
                squared_img = expand_image_to_square(cropped_img, target_size=512)
                
                # Process the file name, keep only the part before the email "@", and output in JPG format
                base_name = os.path.splitext(image)[0]  # 去除扩展名
                email_prefix = base_name.split('_')[0] if '_' in base_name else base_name
                output_path = os.path.join(output_folder_path, f"{email_prefix}.jpg")
                
                # Save the file in JPG format
                cv2.imwrite(output_path, squared_img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
                print(f"Saved cropped face to {output_path}")
                break  # Only process the most likely face

if __name__ == "__main__":
    input_folder = r"D:\pytest\photo_input"  
    output_folder = r"D:\pytest\photo_output" 
    
    # Create Output Directory
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    crop_face(input_folder, output_folder)
    print('Done!')