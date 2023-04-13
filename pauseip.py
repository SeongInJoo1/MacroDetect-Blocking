import time
import subprocess
import re
from datetime import datetime
from datetime import timedelta
import threading

log_path = "/var/log/apache2/access.log"

#block_duration 시간만큼 IP 차단
def block_ip_address(ip, block_duration):
    subprocess.call(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])

    unblock_time = datetime.now() + block_duration
    unblock_command = f'iptables -D INPUT -s {ip} -j DROP'

    while datetime.now() < unblock_time:
        continue
    subprocess.run(unblock_command.split())

def extract_time(log_string):
    # access.log에서 시간을 추출하는 정규표현식
    pattern = r'\[(.*?)\]'
    match = re.search(pattern, log_string)

    if match:
        time_str = match.group(1)
        access_time = datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S %z')
        #return time_str
        return access_time
    else:
        return None

# 실시간으로 로그 저장
def tail_log_store():

    command = "tail -f " + log_path

    #filter_keywords = ["GET", "POST", "HEAD"]

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    line = []
    count = 0 #로그 개수를 저장할 변수
    # subprocess의 stdout에서 로그 라인을 읽어들여 처리
    while True:
        log_string = process.stdout.readline().decode()

        if not log_string:
            continue

        line.append(log_string) #로그 문자열을 리스트에 추가
        count += 1 #로그 개수 1증가

        if count == 50:
            break
    return line

# 매크로 탐지 패턴, 메인 함수
def tail_log_file():
    line = []
    line = tail_log_store() #실시간으로 저장한 로그를 문자열로 받아온다.
    ip_count = {} 

    if not line:
        print("no log")
    else:
        for log in line:
            match1 = re.search(r'^(\S+)', log)
            ip = match1.group(1)
            access_time = extract_time(log)

            if ip in ip_count:
                if ip_count[ip]['count'] >= 10 and access_time - ip_count[ip]['time'] < timedelta(seconds=5):
                    #print(access_time)
                    # block IP address
                    print(f"Blocking IP address: {ip}")
                    #a = access_time - ip_count[ip]['time']
                    #print(a)
                    block_thread = threading.Thread(target=block_ip_address, args=(ip, timedelta(minutes=10)))
                    block_thread.start()
                    break
                else:
                    ip_count[ip]['count'] += 1
            else:
                #firsttime = time.time()
                ip_count[ip] = {'count': 1, 'time': access_time}
                #print("first time is: {}".format(ip_count[ip]['time']))
        print("no problem")

while(1):
    tail_log_file()
