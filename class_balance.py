import os
from collections import Counter
import glob
import matplotlib.pyplot as plt

def check_label_balance(label_folder_path):
    # 모든 .txt 라벨 파일 가져오기
    label_files = glob.glob(os.path.join(label_folder_path, "*.txt"))
    
    # 모든 클래스 ID를 저장할 리스트 초기화
    class_ids = []
    
    # 각 파일에서 클래스 ID 읽어오기
    for label_file in label_files:
        with open(label_file, 'r') as file:
            for line in file:
                # YOLO 형식의 첫 번째 값은 클래스 ID이므로 추출
                class_id = line.split()[0]
                class_ids.append(class_id)
    
    # 클래스 빈도 계산
    class_count = Counter(class_ids)
    
    # 결과 출력
    print("클래스별 개수:", class_count)
    
    # 막대 그래프 출력
    plt.bar(class_count.keys(), class_count.values())
    plt.xlabel("Class ID")
    plt.ylabel("Frequency")
    plt.title("Class Distribution in YOLO Labels")
    plt.show()

# 함수 호출 예시
label_folder_path = "data/train/labels"  # 라벨 파일이 모여있는 폴더 경로를 입력하세요
check_label_balance(label_folder_path)
