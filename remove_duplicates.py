import os

def find_and_remove_duplicates(label_folder):
    duplicate_count = 0  # 중복 개수 기록

    # 라벨 파일 목록 가져오기
    label_files = [f for f in os.listdir(label_folder) if f.lower().endswith('.txt')]

    # 각 라벨 파일에서 중복된 레이블 확인 및 제거
    for label_file in label_files:
        label_path = os.path.join(label_folder, label_file)

        # 라벨 파일 읽기
        with open(label_path, "r") as f:
            lines = f.readlines()

        # 라벨 정보 파싱 및 중복 제거
        seen_labels = set()
        unique_lines = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line not in seen_labels:
                seen_labels.add(stripped_line)
                unique_lines.append(line)
            else:
                duplicate_count += 1

        # 중복이 있는 경우 파일을 덮어쓰고 중복 경고 출력
        if len(unique_lines) != len(lines):
            with open(label_path, "w") as f:
                f.writelines(unique_lines)
            print(f"{label_path}: {len(lines) - len(unique_lines)}개의 중복 레이블이 제거되었습니다.")
            print(f'{label_path}에 중복 레이블이 있습니다.')
        else:
            print(f"{label_path}: 중복 레이블 없음")

    print(f"총 {duplicate_count}개의 중복 레이블이 제거되었습니다.")

# 라벨 폴더 경로 설정
train_label_folder = r"C:\Users\SBA\Desktop\highway_segmentation\labels"  # 라벨 파일 폴더
valid_label_folder = r"data\valid\labels"  # 라벨 파일 폴더

# 함수 실행
print("Train 데이터셋 중복 제거:")
find_and_remove_duplicates(train_label_folder)