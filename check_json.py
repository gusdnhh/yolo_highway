import os
import json
import cv2

def draw_bboxes_on_image(image_path, bboxes):
    """
    이미지를 열고 바운딩 박스를 그리는 함수.
    바운딩 박스를 그린 이미지를 반환합니다.
    """
    # 이미지를 BGR 모드로 읽기
    img = cv2.imread(image_path)
    if img is None:
        print(f"이미지 파일 {image_path}을(를) 열 수 없습니다.")
        return None

    for bbox_info in bboxes:
        bbox = bbox_info['bbox']
        class_name = bbox_info['class']
        x_min, y_min, x_max, y_max = bbox

        # 바운딩 박스 그리기
        cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 0, 255), 2)
        # 클래스 이름 표시 (원하지 않으면 주석 처리 가능)
        cv2.putText(img, class_name, (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    return img

def process_json_and_images(json_folder, image_folder):
    """
    JSON 파일을 처리하고 이미지를 열어 바운딩 박스를 그리는 함수.
    이미지를 화면에 표시하고 키 입력을 기다립니다.
    """
    # JSON 폴더의 모든 파일에 대해 반복
    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
    json_files.sort()  # 파일을 정렬하여 순서대로 보여줌

    for filename in json_files:
        json_path = os.path.join(json_folder, filename)
        # JSON 파일 읽기
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        image_filename = data['information']['filename']
        image_path = os.path.join(image_folder, image_filename)
        # 이미지 파일이 존재하는지 확인
        if not os.path.exists(image_path):
            print(f"이미지 파일 {image_filename}을(를) 찾을 수 없습니다. JSON 파일 {filename}을(를) 건너뜁니다.")
            continue
        # 어노테이션에서 bbox 정보 추출
        annotations = data.get('annotations', [])
        bboxes = []
        for annotation in annotations:
            if 'bbox' in annotation and annotation['bbox']:
                bbox = annotation['bbox']
                class_name = annotation['class']
                bboxes.append({
                    'bbox': bbox,
                    'class': class_name
                })
        # 이미지에 바운딩 박스 그리기
        img = draw_bboxes_on_image(image_path, bboxes)
        if img is None:
            continue
        
        
        cv2.putText(img, image_path, (50, 1080 - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        # 이미지 표시
        cv2.imshow('Image with Bounding Boxes', img)
        print(f"{image_filename} 표시 중... 다음 이미지로 넘어가려면 아무 키나 누르세요. 종료하려면 'q'를 누르세요.")
        key = cv2.waitKey(0)  # 키 입력을 기다림

        if key == ord('q'):
            break  # 'q' 키를 누르면 종료

    cv2.destroyAllWindows()

# 사용 예시:
json_folder = r"D:\091.승용 자율주행차 야간 자동차 전용도로 데이터\01-1.정식개방데이터\Validation\02.라벨링데이터\VL\3D\21_215126_220914\sensor_raw_data\camera"  # JSON 파일들이 저장된 폴더 경로
image_folder = r"night_data\valid\images"  # 이미지 파일들이 저장된 폴더 경로

process_json_and_images(json_folder, image_folder)
