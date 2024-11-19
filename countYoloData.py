import os
from collections import defaultdict
import matplotlib.pyplot as plt

# 映射表：ID 對應的分類名稱
class_mapping = {
    0: "Normal",
    1: "SCF type 1",
    2: "SCF type 2",
    3: "SCF type 3",
    4: "LCF",
    5: "MCF",
    6: "Elbow dislocation",
    7: "SCF Flexion type",
    8: "Other"
}

def count_yolo_classes(folder_path):
    """
    統計 YOLO 標註資料中每個類別的數量。

    :param folder_path: 包含 YOLO 標註文件（.txt）的資料夾路徑
    :return: 每個類別的數量，格式為字典
    """
    # 初始化統計結果
    class_counts = defaultdict(int)
    
    # 遍歷資料夾中的所有 .txt 文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            
            # 讀取 YOLO 標註文件
            with open(file_path, 'r') as f:
                for line in f:
                    # 提取類別 ID
                    class_id = int(line.split()[0])
                    class_counts[class_id] += 1

    # 確保所有類別都被計算，未出現的類別數量為 0
    mapped_counts = {class_mapping[class_id]: class_counts.get(class_id, 0) for class_id in class_mapping}

    return mapped_counts

def plot_class_distribution(class_counts):
    """
    繪製分類直方圖。

    :param class_counts: 每個分類的數量，格式為字典
    """
    # 提取分類名稱和數量
    categories = list(class_counts.keys())
    counts = list(class_counts.values())
    
    # 計算總數量
    total_count = sum(counts)
    
    # 繪製直方圖
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, counts, color='skyblue', edgecolor='black')
    
    # 在每個條形圖上方標示數量
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(count), 
                 ha='center', va='bottom', fontsize=10)

    # 添加總數量標示
    plt.text(len(categories) - 1, max(counts) * 1.1, f"Total: {total_count}",
             ha='right', va='top', fontsize=12, color='red')
    
    # 設定標題和標籤
    plt.title("YOLO Data Class Distribution", fontsize=14)
    plt.xlabel("Class", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 顯示圖表
    plt.show()

# 使用範例
folder_path = "yolo_data"  # 替換為你的 YOLO 資料夾路徑
class_stats = count_yolo_classes(folder_path)

# 顯示統計結果
print("Class Distribution:")
for category, count in class_stats.items():
    print(f"{category}: {count} images")

# 繪製直方圖
plot_class_distribution(class_stats)
