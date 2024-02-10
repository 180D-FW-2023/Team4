import os
def ping_test(ip):
    num = 5
    response = os.popen(f"ping -c {num} {ip} ").read()
    print(response)
    count = response.count("Request timeout") + response.count("Request timed out.")
    print(count)
    if count >= num-1:
        return False
    return True

print(ping_test("192.168.1.50"))
