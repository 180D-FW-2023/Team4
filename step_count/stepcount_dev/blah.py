import numpy as np

f = open("P03_wrist100.csv", "r")
lines = f.readlines()
f.close()

new_lines = []

# for i in lines:
#     new_line = i.replace(",", " ", 1)
#     new_lines.append(new_line)

for i in lines:
    new_line = i.split(",")
    new_line.pop()
    new_line = ",".join(new_line)
    new_lines.append(new_line+"\n")

f = open("blahblah.csv", "w")
f.writelines(new_lines)
f.close()