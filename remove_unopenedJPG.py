import os
from PIL import Image

def remove_corrupted_images_and_labels(images_folder, labels_folder):
    """
    이미지 폴더에서 손상된 이미지를 제거하고, 해당 이미지와 동일한 이름의 라벨 파일을 라벨 폴더에서 제거합니다.

    Parameters:
    - images_folder (str): 이미지 파일들이 모여있는 폴더 경로
    - labels_folder (str): 라벨 파일들이 모여있는 폴더 경로
    """
    # 이미지 폴더의 이미지 파일 목록 가져오기
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    corrupted_files = []
    for image_file in image_files:
        image_path = os.path.join(images_folder, image_file)
        try:
            # 이미지 파일 열어서 검증하기
            with Image.open(image_path) as img:
                img.verify()  # 이미지가 손상되지 않았는지 확인
        except (IOError, SyntaxError) as e:
            print(f"손상된 이미지 발견 및 삭제: {image_file}")
            os.remove(image_path)  # 손상된 이미지 파일 삭제
            corrupted_files.append(os.path.splitext(image_file)[0])  # 파일명(확장자 제외) 저장

    # 손상된 이미지와 동일한 이름의 라벨 파일 삭제
    for base_name in corrupted_files:
        label_file = base_name + '.txt'
        label_path = os.path.join(labels_folder, label_file)
        if os.path.exists(label_path):
            print(f"라벨 파일 삭제: {label_file}")
            os.remove(label_path)
        else:
            print(f"해당 라벨 파일이 존재하지 않음: {label_file}")

    print("손상된 이미지 및 해당 라벨 파일 삭제 완료.")

# 사용 예시
images_folder = r'night_data\valid\images'  # 이미지 폴더 경로
labels_folder = r'night_data\valid\labels'  # 라벨 폴더 경로

remove_corrupted_images_and_labels(images_folder, labels_folder)
