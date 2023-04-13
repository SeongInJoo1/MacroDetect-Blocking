import time
import subprocess

access_log_file = "/var/log/apache2/access.log"
blocked_js_file = "/var/log/apache2/blocked_js.log"
ip_count = {}
BLOCK_THRESHOLD = 5
#BLOCK_TIME = 60 #1분뒤에 차단 해제

def block_ip(ip):
    subprocess.call(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
    with open(blocked_js_file, "a") as f:
        f.write(ip + "\n")

def check_logs():
    with open(access_log_file, 'r') as f:
        for line in f:
            if "js" in line:
                ip = line.split()[0]
                if ip not in ip_count:
                    ip_count[ip] = 1
                else:
                    ip_count[ip] += 1
                if ip_count[ip] >= BLOCK_THRESHOLD:
                    block_ip(ip)
                    del ip_count[ip]

#while True:
#   check_logs()
#   time.sleep(10)
