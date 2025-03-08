import numpy as np
import cv2
import os

def crop_face(input_folder_path, output_folder_path):
    # 加载 DNN 人脸检测模型
    model_folder = r"D:\pytest\face_models"
    modelFile = os.path.join(model_folder, "res10_300x300_ssd_iter_140000.caffemodel")
    configFile = os.path.join(model_folder, "deploy.prototxt")
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    
    for team_folder in os.listdir(input_folder_path):
        team_input_path = os.path.join(input_folder_path, team_folder)
        team_output_path = os.path.join(output_folder_path, team_folder)
        
        if not os.path.isdir(team_input_path):
            continue
        
        # 创建输出目录
        if not os.path.exists(team_output_path):
            os.makedirs(team_output_path)
        
        images = os.listdir(team_input_path)
        print(f"Processing {len(images)} images in {team_folder}...")
        
        for image in images:
            image_path = os.path.join(team_input_path, image)
            img = cv2.imread(image_path)
            if img is None:
                print(f"Error reading {image_path}")
                continue
            
            height, width, _ = img.shape
            
            # 预处理图像用于 DNN 检测
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
                    
                    # 调整人脸区域大小，使面部始终居中，且保持正方形
                    expansion_factor = 2

                    # 原始人脸框的宽和高
                    w = x2 - x
                    h = y2 - y

                    # 以更长的一边为基准进行扩展，确保最后区域是正方形
                    side = int(max(w, h) * expansion_factor)

                    # 计算人脸框中心
                    center_x = x + w // 2
                    center_y = y + h // 2

                    # 根据正方形 side 计算新的起始和结束点
                    new_x = center_x - side // 2
                    new_y = center_y - side // 2
                    new_x2 = new_x + side
                    new_y2 = new_y + side

                    # 边界检查，防止超出原图范围
                    if new_x < 0:
                        new_x = 0
                        new_x2 = side  # 若超出左边界，则让左边从0开始
                    if new_y < 0:
                        new_y = 0
                        new_y2 = side  # 若超出上边界，则让上边从0开始
                    if new_x2 > width:
                        new_x2 = width
                        new_x = width - side  # 右边超出时，让方形向左移动
                    if new_y2 > height:
                        new_y2 = height
                        new_y = height - side  # 底部超出时，让方形向上移动

                    # 再次检查，避免因图太小导致 new_x 或 new_y 依然小于0
                    new_x = max(0, new_x)
                    new_y = max(0, new_y)

                    # 此时 (new_x, new_y) ~ (new_x2, new_y2) 就是正方形区域
                    cropped_img = img[new_y:new_y2, new_x:new_x2]

                    
                    # 确保裁剪的图片是正方形，并在必要时扩展
                    h_cropped, w_cropped, _ = cropped_img.shape
                    if h_cropped == w_cropped:
                        final_img = cv2.resize(cropped_img, (512, 512), interpolation=cv2.INTER_AREA)
                    else:
                        max_side = max(h_cropped, w_cropped)
                        pad_top = (max_side - h_cropped) // 2
                        pad_bottom = max_side - h_cropped - pad_top
                        pad_left = (max_side - w_cropped) // 2
                        pad_right = max_side - w_cropped - pad_left
                        
                        # 仅在图片尺寸不足时才使用扩展
                        final_img = cv2.copyMakeBorder(cropped_img, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_REPLICATE)
                        final_img = cv2.resize(final_img, (512, 512), interpolation=cv2.INTER_AREA)
                    
                    # 处理文件名，只保留邮箱“@”前面的部分，并输出 JPG 格式
                    base_name = os.path.splitext(image)[0]  # 去除扩展名
                    email_prefix = base_name.split('_')[0] if '_' in base_name else base_name
                    output_path = os.path.join(team_output_path, f"{email_prefix}.jpg")
                    
                    # 保存文件为 JPG 格式
                    cv2.imwrite(output_path, final_img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
                    print(f"Saved cropped face to {output_path}")
                    break  # 只处理最有可能的一个人脸

if __name__ == "__main__":
    input_folder = r"D:\pytest\photo_input"  
    output_folder = r"D:\pytest\photo_output" 
    
    # 创建输出目录
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    crop_face(input_folder, output_folder)
    print('Done!')
