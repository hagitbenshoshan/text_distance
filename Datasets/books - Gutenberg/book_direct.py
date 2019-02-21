import urllib
import re
from urllib2 import Request
url = "https://www.gutenberg.org/files/11/11-0.txt"
response = urllib.urlopen(url)
raw = response.read().decode('utf8')
token = 'CHAPTER'
chunks = []
current_chunk = []

for line in raw:
   if line.startswith(token) and current_chunk:
      # if line starts with token and the current chunk is not empty
      chunks.append(current_chunk[:]) #  add not empty chunk to chunks
      current_chunk = [] #  make current chunk blank
   # just append a line to the current chunk on each iteration
   current_chunk.append(line)

chunks.append(current_chunk)  #  append the last chunk outside the loop
print chunks
"""x = raw.split('CHAPTER')[2]
y = x.split('End of Project Gutenberg')[0]
print y

files = x.split('CHAPTER')
names = ['file'+ str(num) for num in range(len(files))]
for num,file in enumerate(files):
    open(names[num],'w').write(file)
 
from itertools import count
output_file = open('c1.txt', 'wb')

chapter_number = count(1)
for line in x:
    if 'CHAPTER' in line:
        output_file.close()
        output_file = open('{:03}-chapter'.format(next(chapter_number)), 'wb')
    output_file.write(line)
output_file.close()


 for line in   raw.splitlines():
    if re.match("^CHAPTER+$", line):
        if f:
            f.close()
        f = open(line + '.txt', 'w')

    else:
        f.write(line + "\n")
"""