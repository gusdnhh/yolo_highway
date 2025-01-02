import os
import shutil

def select_images_and_labels(image_input_folder, label_input_folder, image_output_folder, label_output_folder, group_size=40, images_per_group=10):
    # 출력 폴더가 없으면 생성
    if not os.path.exists(image_output_folder):
        os.makedirs(image_output_folder)
    if not os.path.exists(label_output_folder):
        os.makedirs(label_output_folder)
    
    # 입력 폴더의 이미지 파일 목록 가져오기
    image_files = [f for f in os.listdir(image_input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    image_files.sort()  # 파일명 순서대로 정렬 (필요 시 수정)

    total_images = len(image_files)
    total_groups = total_images // group_size
    selected_images = []

    for group_index in range(total_groups):
        group_start = group_index * group_size
        group_end = group_start + group_size
        group_images = image_files[group_start:group_end]
        
        # 그룹 내에서 일정한 간격으로 이미지 선택
        interval = group_size // images_per_group
        for i in range(images_per_group):
            index = i * interval
            if index >= group_size:
                index = group_size - 1  # 인덱스가 범위를 벗어나지 않도록 조정
            selected_images.append(group_images[index])

    # 남은 이미지 처리 (총 이미지 수가 그룹 크기로 나누어떨어지지 않을 경우)
    remaining_images = image_files[total_groups * group_size:]
    if remaining_images:
        # 남은 이미지를 모두 추가하거나 필요에 따라 처리
        selected_images.extend(remaining_images[:images_per_group])

    print(f"총 선택된 이미지 수: {len(selected_images)}장")

    # 선택된 이미지와 라벨을 출력 폴더로 복사
    for filename in selected_images:
        # 이미지 파일 복사
        src_image_path = os.path.join(image_input_folder, filename)
        dst_image_path = os.path.join(image_output_folder, filename)
        shutil.copy(src_image_path, dst_image_path)
        # 진행 상황 출력 (선택 사항)
        # print(f"이미지 복사 완료: {filename}")

        # 라벨 파일 복사
        label_filename = os.path.splitext(filename)[0] + '.txt'
        src_label_path = os.path.join(label_input_folder, label_filename)
        dst_label_path = os.path.join(label_output_folder, label_filename)

        # 라벨 파일이 존재하는지 확인 후 복사
        if os.path.exists(src_label_path):
            shutil.copy(src_label_path, dst_label_path)
            # 진행 상황 출력 (선택 사항)
            # print(f"라벨 복사 완료: {label_filename}")
        else:
            print(f"라벨 파일이 존재하지 않습니다: {label_filename}")

    print(f"이미지와 라벨 선택 및 복사 완료.")
    print(f"이미지 출력 폴더: {image_output_folder}")
    print(f"라벨 출력 폴더: {label_output_folder}")

image_input_folder = 'night_data/train/images'  # 이미지 파일이 있는 폴더 경로
label_input_folder = 'night_data/train/labels'  # 라벨 파일이 있는 폴더 경로
image_output_folder = 'data/train/images'  # 선택된 이미지를 저장할 폴더 경로
label_output_folder = 'data/train/labels'  # 선택된 라벨을 저장할 폴더 경로

select_images_and_labels(image_input_folder, label_input_folder, image_output_folder, label_output_folder, group_size=40, images_per_group=6)


image_input_folder = 'night_data/valid/images'  # 이미지 파일이 있는 폴더 경로
label_input_folder = 'night_data/valid/labels'  # 라벨 파일이 있는 폴더 경로  # 라벨 파일이 있는 폴더 경로
image_output_folder = 'data/valid/images'  # 선택된 이미지를 저장할 폴더 경로
label_output_folder = 'data/valid/labels'  # 선택된 라벨을 저장할 폴더 경로

select_images_and_labels(image_input_folder, label_input_folder, image_output_folder, label_output_folder, group_size=40, images_per_group=10)
