import subprocess
s = subprocess.run(["python detector.py --test -f hehe.png"], shell=True, capture_output=True, text=True)
print(s.stdout)
# if s[0] == 0:
#     print(s[1])
# else:
#     print('Custom Error {}'.format(s[1]))