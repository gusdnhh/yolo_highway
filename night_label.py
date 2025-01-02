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

def determine_bbox_order(bbox):
    """
    bbox 좌표 순서를 판단하는 함수.
    좌표 순서가 [x_min, y_min, x_max, y_max] 또는 [x_min, x_max, y_min, y_max]일 수 있으므로,
    올바른 좌표 순서를 결정하여 반환합니다.
    """
    # 옵션 1: [x_min, y_min, x_max, y_max]
    x_min1, y_min1, x_max1, y_max1 = bbox
    width1 = x_max1 - x_min1

    # 옵션 2: [x_min, x_max, y_min, y_max]
    x_min2, x_max2, y_min2, y_max2 = bbox
    width2 = x_max2 - x_min2

    # 두 옵션 모두에서 폭이 양수인 경우 라벨을 폐기
    if width1 > 0 and width2 > 0:
        return None

    # 폭이 양수인 옵션을 선택
    if width1 > 0:
        # 높이도 계산하여 양수인지 확인
        height1 = y_max1 - y_min1
        if height1 > 0:
            return [x_min1, y_min1, x_max1, y_max1]
    elif width2 > 0:
        # 높이도 계산하여 양수인지 확인
        height2 = y_max2 - y_min2
        if height2 > 0:
            return [x_min2, y_min2, x_max2, y_max2]

    # 두 옵션 모두 폭이 양수가 아닌 경우 라벨을 폐기
    return None

def convert_bbox_to_yolo_format(bbox, img_width, img_height):
    """
    YOLO 형식으로 변환하는 함수.
    bbox: [x_min, y_min, x_max, y_max]
    반환: x_center, y_center, width, height (모두 정규화된 값)
    """
    # 박스 좌표 순서를 판단하여 올바른 좌표를 가져옴
    corrected_bbox = determine_bbox_order(bbox)
    if corrected_bbox is None:
        return None  # 유효하지 않은 bbox

    x_min, y_min, x_max, y_max = corrected_bbox

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
            bbox = annotation.get("bbox")

            if not bbox:
                continue  # bbox 정보가 없으면 건너뜀

            # 클래스 매핑에서 클래스 ID 가져오기
            class_id = CLASS_MAPPING.get(class_name)
            if class_id is None:
                continue  # 매핑되지 않은 클래스는 건너뜀

            # YOLO 형식으로 변환
            yolo_bbox = convert_bbox_to_yolo_format(
                bbox, img_width, img_height
            )
            if yolo_bbox is None:
                continue  # 유효하지 않은 bbox는 건너뜀

            x_center, y_center, width, height = yolo_bbox

            # 라벨 파일에 작성 (소수점 6자리까지 표시)
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

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
output_folder = r'night_data\valid\labels2'  # 변환된 YOLO txt 파일을 저장할 폴더 경로
convert_all_jsons_in_folder(input_folder, output_folder)
