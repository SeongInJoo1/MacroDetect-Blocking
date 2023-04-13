import time
import subprocess
import re

# 로그 파일 경로 설정
log_path = "/var/log/apache2/access.log"
blocked_js_file = "/var/log/apache2/blocked_js.log"

# 로그 파일 실시간 모니터링 함수
def block_ip_address(ip):
    subprocess.call(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
    with open(blocked_js_file, "a") as f:
        f.write(ip + "\n")


def tail_log_store():
    # 로그 파일을 실시간으로 읽기 위한 subprocess 실행
    
    command = "tail -f " + log_path

    #filter_keywords = ["GET", "POST", "HEAD"]

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    line = []
    count = 0 #로그 개수를 저장할 변수
    # subprocess의 stdout에서 로그 라인을 읽어들여 처리
    while True:
        line.append(process.stdout.readline().decode()) #로그 문자열을 리스트에 추가
        count += 1 #로그 개수 1증가

        if count == 15:
            return line
            break
def tail_log_file():

    line = tail_log_store()
    
    #ip_list = []
    #uri_list = []

    for log in line:
        #match = re.search(r'^(\S+)', log)  # 첫 번째 단어, 즉 IP 주소 추출
        #if match:
        #    ip_list.append(match.group(1))


        #if count >= 5 an
        match = re.search(r'(?<=\s)(/\S+)', log)
        if match:
            uri = match.group(1)
            if 'static' in uri:
                match1 = re.search(r'^(\S+)', log)
                ip = match1.group(1)
                print(f"Macro detection! Blocking {ip} address!")
                block_ip_address(ip)
            else:
                print("Macro not detected")
        else:
            print("Uri not detected")
              


        #match = re.search(r'(?<=\s)(/\S+)', log)  # 슬래시(/)로 시작하는 URI 추출
        #if match:
        #    uri_list.append(match.group(1))
        #    print(uri_list)
        
    #ip_count = {}
    #for ip in ip_list:
    #    if ip not in ip_count:
    #        ip_count[ip] = 0
    #    else:
    #        ip_count[ip] += 1
    #        print(ip_count[ip])
    #for ip, count in ip_count.items():
    #    if count >= 5 and 'static' in uri_list:
    #        print(f"IP {ip} 차단")
    #        block_ip_address(ip)
    #    else:
    #        print("정상 작동 중입니다.")

            
# IP 주소 차단하는 함수

while(1):
    tail_log_file()
