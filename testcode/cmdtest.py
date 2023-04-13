import subprocess

# 아파치 로그 경로
log_file = "/var/log/apache2/access.log"

# 실시간으로 로그를 가져오기 위한 명령어
command = "tail -f " + log_file

# 포함된 단어 필터링을 위한 키워드
filter_keywords = ["GET", "POST", "HEAD"]

# 명령어 실행
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

# 실시간 로그 출력
while True:
    output = process.stdout.readline().decode()
    if output:
        if any("GET" in output for keyword in filter_keywords):
            print(output.strip())
    else:
        continue

