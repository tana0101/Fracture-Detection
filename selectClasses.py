import os
import shutil

def copy_selected_classes(source_folder, target_folder, selected_classes):
    os.makedirs(target_folder, exist_ok=True)
    
    # 遍歷資料夾中的所有 .txt 文件
    for file_name in os.listdir(source_folder):
        if file_name.endswith(".txt"):
            txt_path = os.path.join(source_folder, file_name)
            
            # 讀取標註文件
            with open(txt_path, 'r') as f:
                lines = f.readlines()
            
            # 檢查是否有包含選定的類別（0~3）
            selected_lines = [line for line in lines if int(line.split()[0]) in selected_classes]
            
            if selected_lines:
                # 複製標註文件
                target_txt_path = os.path.join(target_folder, file_name)
                with open(target_txt_path, 'w') as f:
                    f.writelines(selected_lines)
                
                # 複製對應的圖片
                image_name = file_name.replace(".txt", ".jpg")  # 假設圖片是 .jpg 格式
                image_path = os.path.join(source_folder, image_name)
                if os.path.exists(image_path):
                    target_image_path = os.path.join(target_folder, image_name)
                    shutil.copy(image_path, target_image_path)
                    print(f"已複製圖片和標註文件：{image_name}")
                else:
                    print(f"警告：圖片 {image_name} 不存在，無法複製。")

# 使用範例
source_folder = "yolo_data"  # 替換為你的目標資料夾路徑
target_folder = "SCF_data"  # 新資料夾
selected_classes = {0, 1, 2, 3}  # 需要複製的類別 ID

copy_selected_classes(source_folder, target_folder, selected_classes)
