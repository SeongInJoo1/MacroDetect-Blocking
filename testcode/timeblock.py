

def unblock_ip(ip):
    with open(BLOCKED_IPS_FILE, "r") as f:
        ips = f.readlines()
    with open(BLOCKED_IPS_FILE, "w") as f:
        for blocked_ip in ips:
            if blocked_ip.strip() != ip:
                f.write(blocked_ip)



def block_ip(ip):
    subprocess.call(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
    with open(BLOCKED_IPS_FILE, "a") as f:
        f.write(ip + "\n")
    time.sleep(BLOCK_TIME)
    subprocess.call(["iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"])
    unblock_ip(ip)

