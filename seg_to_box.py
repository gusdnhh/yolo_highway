import os
import json

# CLASS_MAPPING을 제공된 값으로 수정
CLASS_MAPPING = {
    "pedestrian": 0,          # pedestrian
    "trafficLight": 1,        # trafficLight
    "trafficSign": 2,         # trafficSign
    "twoWheeler": 3,          # bicycle, motorcycle, twoWheeler
    "vehicle": 4              # ambulance, bus, eogVehicle, otherCar, policeCar, truck, vehicle, schoolBus
}

# 클래스 이름을 CLASS_MAPPING에 맞게 변환하는 함수
def map_class_name(class_name):
    if class_name in ['bicycle', 'motorcycle', 'twoWheeler']:
        return 'twoWheeler'
    elif class_name in ['ambulance', 'bus', 'eogVehicle', 'otherCar', 'policeCar', 'truck', 'vehicle', 'schoolBus']:
        return 'vehicle'
    else:
        return class_name  # 변환할 필요 없는 경우 그대로 반환

def polygon_to_bbox(polygon):
    """
    폴리곤 좌표 리스트를 받아 바운딩 박스 [x_min, y_min, x_max, y_max]를 반환하는 함수
    """
    x_coords = polygon[::2]  # 짝수 인덱스: x 좌표
    y_coords = polygon[1::2]  # 홀수 인덱스: y 좌표
    x_min = min(x_coords)
    y_min = min(y_coords)
    x_max = max(x_coords)
    y_max = max(y_coords)
    return [x_min, y_min, x_max, y_max]

def process_json_file(json_file_path, labels_dir):
    """
    단일 JSON 파일을 처리하여 YOLO 라벨 파일을 생성하는 함수
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    image_info = data.get('information', {})
    image_filename = image_info.get('filename')
    if not image_filename:
        print(f"이미지 파일명을 찾을 수 없습니다: {json_file_path}")
        return

    image_width, image_height = image_info.get('resolution', [1920, 1080])

    annotations = data.get('annotations', [])

    # 라벨 파일 경로 설정 (이미지 파일명과 동일하게, 확장자만 .txt로 변경)
    base_filename = os.path.splitext(image_filename)[0]
    label_file_path = os.path.join(labels_dir, base_filename + '.txt')

    with open(label_file_path, 'w', encoding='utf-8') as f_label:
        for annotation in annotations:
            class_name = annotation.get('class')
            # 클래스 이름을 CLASS_MAPPING에 맞게 변환
            mapped_class_name = map_class_name(class_name)
            # CLASS_MAPPING에 해당하는 클래스만 처리
            if mapped_class_name in CLASS_MAPPING:
                polygon = annotation.get('polygon')
                if polygon:
                    bbox = polygon_to_bbox(polygon)
                    class_id = CLASS_MAPPING[mapped_class_name]  # 클래스 이름을 ID로 매핑
                    x_min, y_min, x_max, y_max = bbox
                    x_center = (x_min + x_max) / 2.0 / image_width
                    y_center = (y_min + y_max) / 2.0 / image_height
                    width = (x_max - x_min) / image_width
                    height = (y_max - y_min) / image_height
                    # 좌표 값을 소수점 6자리까지 표현
                    f_label.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    print(f"라벨 파일 생성 완료: {label_file_path}")

def process_all_json_files(input_dir, output_labels_dir):
    """
    입력 디렉토리 내의 모든 JSON 파일을 처리하여 YOLO 라벨 파일을 생성하는 함수
    """
    # 출력 라벨 디렉토리가 없으면 생성
    if not os.path.exists(output_labels_dir):
        os.makedirs(output_labels_dir)

    # 입력 디렉토리 내의 모든 JSON 파일 찾기
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                json_file_path = os.path.join(root, file)
                labels_dir = output_labels_dir
                process_json_file(json_file_path, labels_dir)

# 사용 예시
if __name__ == "__main__":
    # JSON 파일들이 담긴 최하위 폴더의 경로
    input_dir = r"D:\091.승용 자율주행차 야간 자동차 전용도로 데이터\01-1.정식개방데이터\Validation\02.라벨링데이터\TL\2D"  # 여기에 실제 JSON 파일들이 있는 폴더 경로를 입력하세요
    # 라벨 파일을 저장할 디렉토리 경로
    output_labels_dir = r'night_data\train\labels'  # 생성될 라벨 파일들이 저장될 폴더 경로를 입력하세요

    process_all_json_files(input_dir, output_labels_dir)
