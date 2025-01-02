import yaml

# data.yaml 파일 내용
data_yaml_content = {
    'train': '/home/jupyter/data/train/images',       # train 이미지 경로
    'val': '/home/jupyter/data/valid/images',         # val 이미지 경로
    'nc': 5,                                   # 클래스 개수
    'names': ['pedestrian', 'trafficLight', 'trafficSign', 'twoWheeler', 'vehicle']  # 클래스 이름 목록
}

# data.yaml 파일 생성
with open('data.yaml', 'w') as file:
    yaml.dump(data_yaml_content, file)

print("data.yaml 파일이 생성되었습니다.")