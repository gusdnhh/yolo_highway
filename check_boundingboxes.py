import os
import cv2

def display_labeled_images(img_folder, label_folder, class_names=None):
    for img_file in os.listdir(img_folder):
        if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            # 이미지 파일 경로 및 레이블 파일 경로 설정
            img_path = os.path.join(img_folder, img_file)
            label_path = os.path.join(label_folder, os.path.splitext(img_file)[0] + '.txt')
            
            # 이미지 로드
            img = cv2.imread(img_path)
            if img is None:
                print(f"Could not read image: {img_file}")
                continue

            # 이미지 크기
            img_height, img_width = img.shape[:2]
            
            # 레이블 파일 존재 확인
            if not os.path.exists(label_path):
                print(f"Label file not found for {img_file}")
                continue
            
            # 레이블 파일 읽기 및 경계 상자 표시
            with open(label_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        print(f"Invalid label format in {label_path}")
                        continue
                    
                    # YOLO 형식에서 클래스, 중심 좌표, 크기 추출
                    class_id = int(parts[0])
                    x_center = float(parts[1]) * img_width
                    y_center = float(parts[2]) * img_height
                    box_width = float(parts[3]) * img_width
                    box_height = float(parts[4]) * img_height
                    
                    # 왼쪽 상단, 오른쪽 하단 좌표 계산kkkkkkk
                    x1 = int(x_center - box_width / 2)
                    y1 = int(y_center - box_height / 2)
                    x2 = int(x_center + box_width / 2)
                    y2 = int(y_center + box_height / 2)
                    
                    # 경계 상자와 클래스 텍스트 표시
                    color = (0, 255, 0)  # 초록색
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                    label_text = class_names[class_id] if class_names and class_id < len(class_names) else str(class_id)
                    cv2.putText(img, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                
            cv2.putText(img, label_path, (50, img_height - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            # 이미지 표시
            cv2.imshow("Labeled Image", img)
            cv2.waitKey(0)  # 아무 키나 누르면 다음 이미지로
            cv2.destroyAllWindows()

# 이미지와 레이블 폴더 경로 설정
img_folder = r"data/valid/images"
label_folder = r'data\valid\labels'
class_names = ["pedestrian", "trafficLight", "trafficSign", "twoWheeler", "vehicle"]  # 클래스 이름

# 이미지와 레이블 확인 실행
display_labeled_images(img_folder, label_folder, class_names)

# CLASS_MAPPING = {
#     "pedestrian": 0,
#     "trafficLight": 1,
#     "trafficSign": 2,
#     "twoWheeler": 3,
#     "vehicle": 4
# }

# 21_215126_220914_01
# 21_215126_220914_01