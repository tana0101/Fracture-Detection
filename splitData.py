import os
import random
import shutil
import yaml

def set_random_seed(seed=42):
    """設定隨機種子以確保結果可重現"""
    random.seed(seed)

def split_dataset(source_folder, train_folder, valid_folder, test_folder, train_ratio=0.7, valid_ratio=0.15, test_ratio=0.15, seed=42):
    # 設定隨機種子
    set_random_seed(seed)
    
    # 確保目標資料夾存在
    for folder in [train_folder, valid_folder, test_folder]:
        os.makedirs(os.path.join(folder, 'images'), exist_ok=True)
        os.makedirs(os.path.join(folder, 'labels'), exist_ok=True)
    
    # 取得 source 資料夾內的所有 JPG 和 TXT 檔案
    all_files = [f for f in os.listdir(source_folder) if f.endswith('.jpg')]
    
    # 隨機打亂檔案順序
    random.shuffle(all_files)
    
    # 計算分割數量
    total_files = len(all_files)
    train_count = int(total_files * train_ratio)
    valid_count = int(total_files * valid_ratio)
    
    # 切割檔案列表
    train_files = all_files[:train_count]
    valid_files = all_files[train_count:train_count + valid_count]
    test_files = all_files[train_count + valid_count:]
    
    # 移動檔案到相應資料夾
    def move_files(files, folder):
        for file in files:
            # 檔案名稱去除副檔名
            base_name = os.path.splitext(file)[0]
            
            # 圖片與標註檔案路徑
            image_src = os.path.join(source_folder, file)
            label_src = os.path.join(source_folder, base_name + '.txt')
            
            # 目標資料夾路徑
            image_dest = os.path.join(folder, 'images', file)
            label_dest = os.path.join(folder, 'labels', base_name + '.txt')
            
            # 移動圖片和標註檔案
            shutil.copy(image_src, image_dest)
            shutil.copy(label_src, label_dest)
            print(f"已移動：{file} 和 {base_name}.txt 到 {folder}")
    
    # 分別移動檔案到訓練、驗證與測試資料夾
    move_files(train_files, train_folder)
    move_files(valid_files, valid_folder)
    move_files(test_files, test_folder)

    # 儲存資料集配置至 YAML 檔案
    dataset_yaml = {
        'test': {
            'images': './test/images',
            'labels': './test/labels'
        },
        'train': {
            'images': './train/images',
            'labels': './train/labels'
        },
        'val': {
            'images': './valid/images',
            'labels': './valid/labels'
        }
    }
    
    yaml_path = os.path.join(target_folder, 'data.yaml')
    with open(yaml_path, 'w') as yaml_file:
        yaml.dump(dataset_yaml, yaml_file, default_flow_style=False, allow_unicode=True)
    print(f"YAML 配置已保存到 {yaml_path}")

# 使用範例
source_folder = "SCF_data"  # 替換為源資料夾路徑
target_folder = "data"  # 目標資料夾路徑
train_folder = os.path.join(target_folder, 'train')
valid_folder = os.path.join(target_folder, 'valid')
test_folder = os.path.join(target_folder, 'test')

split_dataset(source_folder, train_folder, valid_folder, test_folder)
