import sys

def print(*args):
    sys.stdout.write(" ".join(map(str, args)) + "\n")

x = 10
y = 3.14
z = True
s = "Hello, A!"
c = 'A'

def add(a, b):
    return a + b

if x > 5:
    print("x is greater than 5")
else:
    print("x is less than or equal to 5")

for i in range(10):
    print(i)

if __name__ == "__main__":
    result = add(5, 3)
    print("add(5, 3) =", result)