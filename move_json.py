import os

def check_matching_files(labels_dir, images_dir):
    # 라벨 파일과 이미지 파일의 이름을 수집
    label_files = {os.path.splitext(f)[0] for f in os.listdir(labels_dir) if os.path.isfile(os.path.join(labels_dir, f))}
    image_files = {os.path.splitext(f)[0] for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))}

    # 이름이 일치하는 파일 체크
    unmatched_labels = label_files - image_files
    unmatched_images = image_files - label_files

    # 결과 출력
    if unmatched_labels:
        print(f"Matching image not found for the following label files: {unmatched_labels}")
    if unmatched_images:
        print(f"Matching label not found for the following image files: {unmatched_images}")

    if not unmatched_labels and not unmatched_images:
        print("All label files have matching image files.")

# 사용 예시
labels_directory = r"C:\Users\SBA\Desktop\highway_segmentation\json"
images_directory = r"C:\Users\SBA\Desktop\highway_segmentation\labels"

check_matching_files(labels_directory, images_directory)
