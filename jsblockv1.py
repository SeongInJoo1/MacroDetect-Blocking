import time
import subprocess
import re

# 로그 파일 경로 설정
log_path = "/var/log/apache2/access.log"
blocked_js_file = "/var/log/apache2/blocked_js.log"

# IP 차단 & 차단한 IP관리
def block_ip_address(ip):
    subprocess.call(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
    with open(blocked_js_file, "a") as f:
        f.write(ip + "\n")


# 실시간으로 생성되는 로그 저장
def tail_log_store():
    # 로그 파일을 실시간으로 읽기 위한 subprocess 실행
    
    command = "tail -f " + log_path

    #filter_keywords = ["GET", "POST", "HEAD"]
    
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    line = []
    count = 0 
    # subprocess의 stdout에서 로그 라인을 읽어들여 처리
    while True:
        log_string = process.stdout.readline().decode()

        if not log_string:
            continue

        line.append(log_string) #로그 문자열을 리스트에 추가
        count += 1 #로그 개수 1증가

        if count == 20:
            break
    return line

# 자바스크립트 차단 함수
def tail_log_file():
    line = []
    line = tail_log_store()
    
    #ip_list = []
    #uri_list = []
    if not line:
        print("no log")
    else:
        for log in line:
        #match = re.search(r'^(\S+)', log)  # 첫 번째 단어, 즉 IP 주소 추출
        #if match:
        #    ip_list.append(match.group(1))


        #if count >= 5 an
            match = re.search(r'(?<=\s)(/\S+)', log)
            if match:
                uri = match.group(1)
                if 'static' in uri and 'js' in uri:
                    match1 = re.search(r'^(\S+)', log)
                    ip = match1.group(1)
                    print(f"Macro detection! Blocking {ip} address!")
                    block_ip_address(ip)
                else:
                    print("Macro not detected")
            else:
                print("Uri not detected")
              


while(1):
    tail_log_file()
