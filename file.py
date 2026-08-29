import os


with open("demo.txt","w") as f:
    print(f.write("i am jyotir"))
    print(f.write("\ni am male"))
    print("file written")


with open("demo.txt","r") as f:
    print(f.read())
print("file read")



with open("demo.txt","r") as f:
    for line in f:
        print(line.strip())

with open("demo.txt","a") as f:
    f.write("\nkind to everyone")
with open ("demo.txt","r") as f:
    f.read()

lines=["python\n",
       "ml\n",
       "dl\n"
       ]

with open("demo.txt","w") as f:
    f.writelines(lines)

with open ("demo.txt","r") as f:
    data=f.read()
    words=data.split()
    print("words taken",words)

filename="demo.txt"
if os.path.exists(filename):
   os.remove(filename)
   print("file removed")
else:
    print("file not found")






