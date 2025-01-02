import os
import shutil

def move_jpg_files(input_vs_folder, output_folder):
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # VS 폴더 안의 하위 폴더 목록을 가져옴
    subfolders = [folder for folder in os.listdir(input_vs_folder) if os.path.isdir(os.path.join(input_vs_folder, folder))]

    # 각 하위 폴더를 순회하며 'camera' 폴더의 jpg 파일을 이동
    for foldername in subfolders:
        camera_folder = os.path.join(input_vs_folder, foldername, 'sensor_raw_data', 'camera')
        
        # camera 폴더가 존재하는지 확인
        if os.path.exists(camera_folder):
            for file in os.listdir(camera_folder):
                if file.lower().endswith('.jpg'):
                    src_path = os.path.join(camera_folder, file)
                    dst_path = os.path.join(output_folder, file)

                    # 파일 이동 (중복 파일 이름이 있을 경우 덮어쓰기)
                    shutil.copy(src_path, dst_path)
                    print(f"파일 이동 완료: {src_path} -> {dst_path}")
        else:
            print(f"'camera' 폴더가 존재하지 않습니다: {camera_folder}")

    print(f"모든 JPG 파일을 {output_folder}로 이동 완료.")

# 사용 예시
input_vs_folder = r"C:\Users\SBA\Desktop\data1"  # VS 폴더 경로
output_folder = r"C:\Users\SBA\Desktop\images"  # jpg 파일을 이동할 경로
move_jpg_files(input_vs_folder, output_folder)
