import os

def remove_unmatched_images_and_labels(images_folder, labels_folder):
    """
    이미지 폴더와 라벨 폴더에서 파일명을 비교하여 매칭되지 않는 파일을 삭제합니다.

    Parameters:
    - images_folder (str): 이미지 파일들이 모여있는 폴더 경로
    - labels_folder (str): 라벨 파일들이 모여있는 폴더 경로
    """
    # 이미지와 라벨 파일 목록 가져오기
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    label_files = [f for f in os.listdir(labels_folder) if f.lower().endswith('.txt')]

    # 파일명(확장자 제외) 추출
    image_basenames = set(os.path.splitext(f)[0] for f in image_files)
    label_basenames = set(os.path.splitext(f)[0] for f in label_files)

    # 매칭되지 않는 이미지와 라벨 찾기
    unmatched_images = image_basenames - label_basenames
    unmatched_labels = label_basenames - image_basenames

    # 매칭되지 않는 이미지 삭제
    for basename in unmatched_images:
        for ext in ['.jpg', '.jpeg', '.png']:
            image_path = os.path.join(images_folder, basename + ext)
            if os.path.exists(image_path):
                print(f"매칭되지 않는 이미지 삭제: {image_path}")
                os.remove(image_path)

    # 매칭되지 않는 라벨 삭제
    for basename in unmatched_labels:
        label_path = os.path.join(labels_folder, basename + '.txt')
        if os.path.exists(label_path):
            print(f"매칭되지 않는 라벨 삭제: {label_path}")
            os.remove(label_path)

    print("매칭되지 않는 이미지와 라벨 파일 삭제 완료.")

# 사용 예시
images_folder = r"C:\Users\SBA\Downloads\imgs\valid\imgs"  # 이미지 폴더 경로
labels_folder = r"C:\Users\SBA\Downloads\imgs\valid\labels"  # 라벨 폴더 경로

remove_unmatched_images_and_labels(images_folder, labels_folder)
