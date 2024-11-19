import os
import json
import shutil
from PIL import Image

def convert_json_to_yolo(source_folder, target_folder):
    os.makedirs(target_folder, exist_ok=True)
    
    for file_name in os.listdir(source_folder):
        if file_name.endswith(".json"):
            json_path = os.path.join(source_folder, file_name)
            
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            image_path = os.path.join(source_folder, data['imagePath'])
            if not os.path.exists(image_path):
                print(f"警告：圖像 {data['imagePath']} 不存在。")
                continue
            
            with Image.open(image_path) as img:
                img_width, img_height = img.size
            
            yolo_annotations = []
            for shape in data['shapes']:
                if shape['shape_type'] == 'rectangle':
                    label = shape['label']
                    x1, y1 = shape['points'][0]
                    x2, y2 = shape['points'][1]
                    
                    # YOLO format：class, x_center, y_center, width, height
                    x_center = (x1 + x2) / 2 / img_width
                    y_center = (y1 + y2) / 2 / img_height
                    width = abs(x2 - x1) / img_width
                    height = abs(y2 - y1) / img_height
                    
                    yolo_annotations.append(f"{label} {x_center} {y_center} {width} {height}")
            
            yolo_file_name = os.path.splitext(file_name)[0] + ".txt"
            yolo_file_path = os.path.join(target_folder, yolo_file_name)
            with open(yolo_file_path, 'w') as f:
                f.write("\n".join(yolo_annotations))
            
            target_image_path = os.path.join(target_folder, os.path.basename(image_path))
            shutil.copy(image_path, target_image_path)
            
            print(f"轉換完成：{file_name} -> {yolo_file_name}。")

source_folder = "source_data"  
target_folder = "yolo_data"   

convert_json_to_yolo(source_folder, target_folder)
