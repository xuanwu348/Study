import os

base_path = os.path.dirname(os.path.abspath(__file__))
whitelist = []
with open("whitelist.txt", 'rt') as f:
    line = f.readlines()
    if line:
        whitelist.extend(map(lambda x:x.strip(),line))

for dirname, _, filenames in os.walk(base_path):
    for name in filenames:
        if name in whitelist:
            continue
        else:
            os.remove(os.path.join(dirname, name))
print(base_path,whitelist)

