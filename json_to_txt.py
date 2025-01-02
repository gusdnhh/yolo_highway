import json
import os

# 클래스 매핑 딕셔너리
CLASS_MAPPING = {
    "pedestrian": 0,
    "trafficLight": 1,
    "trafficSign": 2,
    "twoWheeler": 3,
    "vehicle": 4
}

def convert_bbox_to_yolo_format(bbox, img_width, img_height):
    """
    YOLO 형식으로 변환하는 함수.
    bbox: [x_min, y_min, x_max, y_max]
    반환: x_center, y_center, width, height (모두 정규화된 값)
    """
    x_min, y_min, x_max, y_max = bbox

    # 바운딩 박스 중심 좌표, 너비 및 높이 계산
    x_center = (x_min + x_max) / 2.0
    y_center = (y_min + y_max) / 2.0
    width = x_max - x_min
    height = y_max - y_min

    # YOLO 형식에 맞게 정규화 (0~1 사이 값으로 변환)
    x_center /= img_width
    y_center /= img_height
    width /= img_width
    height /= img_height

    return x_center, y_center, width, height

def process_json_file(json_path, output_dir):
    # JSON 파일 로드
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 이미지 크기 정보 추출
    img_width, img_height = data['information']['resolution']
    
    # 파일명 설정
    filename = os.path.splitext(data['information']['filename'])[0]
    output_txt_path = os.path.join(output_dir, f"{filename}.txt")

    # YOLO 형식의 라벨 파일 생성
    with open(output_txt_path, 'w') as f:
        for annotation in data["annotations"]:
            class_name = annotation["class"]
            bbox = annotation["bbox"]

            # 클래스 매핑에서 클래스 ID 가져오기
            class_id = CLASS_MAPPING.get(class_name)
            if class_id is None:
                continue  # 매핑되지 않은 클래스는 건너뜀

            # YOLO 형식으로 변환
            x_center, y_center, width, height = convert_bbox_to_yolo_format(
                bbox, img_width, img_height
            )

            # 라벨 파일에 작성
            f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

    print(f"변환 완료: {output_txt_path}")

def convert_all_jsons_in_folder(input_folder, output_folder):
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 모든 JSON 파일 탐색
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.json'):
                json_path = os.path.join(root, file)
                process_json_file(json_path, output_folder)

    print(f"모든 JSON 파일을 YOLO 형식으로 변환하여 {output_folder}에 저장 완료.")

# 사용 예시
input_folder = r"D:\091.승용 자율주행차 야간 자동차 전용도로 데이터\01-1.정식개방데이터\Validation\02.라벨링데이터\VL\3D"  # JSON 파일이 포함된 폴더 경로
output_folder = r'night_data\valid\labels'  # 변환된 YOLO txt 파일을 저장할 폴더 경로
convert_all_jsons_in_folder(input_folder, output_folder)



