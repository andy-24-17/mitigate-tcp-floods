import subprocess

def add_iptables_rate_limit():
    # This drops incoming packets from the same IP that sends >10 packets/sec
    rules = [
        "iptables -F",
        "iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 20 -j DROP",
        "iptables -A INPUT -p tcp --dport 80 -m recent --name badguy --rcheck --seconds 10 -j DROP",
        "iptables -A INPUT -p tcp --dport 80 -m recent --name badguy --set",
        "iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/sec --limit-burst 100 -j ACCEPT"
    ]

    for rule in rules:
        subprocess.run(rule.split())

if __name__ == "__main__":
    print("Applying iptables rate-limiting rules...")
    add_iptables_rate_limit()
    print("Rate-limiting rules applied.")
