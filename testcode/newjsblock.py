import time
import subprocess

access_log_file = "/var/log/apache2/access.log"
blocked_js_file = "/var/log/apache2/blocked_js.log"
ip_count = {}
BLOCK_THRESHOLD = 5
#BLOCK_TIME = 60 #1분뒤에 차단 해제


#이전에 확인한 로그 파일 이후의 IP 주소를 추출하는 함수
def get_new_ip(prev_ip):
    new_ip = []
    with open(access_log_file, "r") as f:
       lines = f.readlines()
       # 모든 줄을 읽어들인 후 이전에 확인한 로그 파일 이후의 IP주소만 추출
       for line in lines[len(prev_ip):]:
           if "js" in line: 
               new_ip.append(line.split()[0])
    # 새로운 IP 주소와 마지막으로 확인된 로그 파일의 마지막 줄을 반환
    return new_ip, lines[-1]

# IP 주소를 차단 하는 함수
def block_ip(list_blocked_ip):
    subprocess.call(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
    print("Blocking IP address")
    with open(blocked_js_file, "w") as f:
        for x in list_blocked_ip:
            f.write(str(x) + "\n")
    #time.sleep(BLOCK_TIME)
    #subprocess.call(["iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"])
    #unblock_ip(ip)


blocked_ip = set() # 중복된 IP 제거
last_line = ""
# 새로운 IP 주소를 추출하고 마지막으로 확인된 로그 파일의 마지막 줄을 갱신
while True:
    new_ip, last_line = get_new_ip(last_line)
    for ip in new_ip:
        if ip not in blocked_ip:
            if new_ip.count(ip) >= BLOCK_THRESHOLD:
                # BLOCK_THRESHOLD 이상의 요청을 보낸 IP 주소를 차단
                blocked_ip.add(ip)
                list_blocked_ip = list(blocked_ip)
                block_ip(list_blocked_ip)
            else:
                continue
        else:
            continue
    # 1초마다 로그 파일을 확인
    time.sleep(1)


