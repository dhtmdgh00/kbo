import subprocess

# 실행할 Python 파일 목록
python_files = ['next_lineup.py', 'LINEUP_UPDATE.py']

# 각 Python 파일을 순차적으로 실행
for file in python_files:
    try:
        subprocess.run(['python3', file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"에러 발생: {file} 실행 오류발생됨")
        break