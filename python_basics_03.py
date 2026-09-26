# %% 第一题
for i in range (1, 11):
    print(i)

# %% 第二题
for i in range(1, 21):
    if i % 2 == 0:
        print(i)
# %% 第三题
x = 0
for i in range(1, 101):
    x = x + i;
print(x)

# %% 第四题
n = int(input("请输入一个整数："))
for i in range(1, n + 1):
    print(i)
# %% 第五题
x = 0
n = int(input("请输入一个整数："))
for i in range(1, n + 1):
    x = x + i
print(x)
# %% 第六题
n = int(input("请输入一个整数："))
for i in range(1, n + 1):
    if i % 3 == 0:
        print(i)
# %% 练习题1
count = 0
n = int(input("请输入一个整数："))
for i in range(1, n + 1):
    if i % 2 == 0:
        count += 1
print(f"1到{n}之间偶数的个数是：{count}")
# %% 练习题2
totol = 0
n = int(input("请输入一个整数："))
for i in range(1, n + 1):
    if i % 2 == 0:
        totol += i
print(f"1到{n}之间偶数的和是：{totol}")
# %% 练习题3
multiple = 1
n = int(input("请输入一个整数："))
for i in range(1, n + 1):
    multiple *= i
print(f"1到{n}之间的乘积是：{multiple}")
# %% 练习题4
n = int(input("请输入一个整数："))
for i in range(1, 10):
    print(f"{n} * {i} = {n * i}")

# %%    练习题5
for i in range(1, 4):
    for j in range(1, 6):
        print("*", end=" ")
    print()

# %% 练习题6
for i in range(1, 6):
    for j in range(1, i + 1):
        print("*", end=" ")
    print()
# %% 第一题
for i in range(1, 5):
    for j in range(1, 5):
        print("*", end=" ")
    print()
# %% 第二题
for i in range(1, 6):
    for j in range(1, i + 1):
        print(j, end=" ")
    print()
# %% 第三题
for i in range(5, 0, -1):
    for j in range(1, i + 1):
        print("*", end=" ")
    print()
# %% 第四题
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j} * {i} = {i * j}", end="\t")
    print()


# %%  while循环的使用 第一题
i = 1
while i <= 10:
    print(i)
    i += 1

# %% 第二题
i = 1
while i <= 20:
    if i % 2 == 0:
        print(i)
    i += 1
# %% 第三题
total = 0
i = 1
while i <= 100:
    total += i
    i += 1
print(total)
# %% 第四题
n = int(input("请输入一个整数："))
i = 1
while i <= n:
    print(i)
    i += 1
# %% 第五题
password = input("请输入密码：")
while password != "123456":
    password = input("请输入密码：")
print("登陆成功")

# %% 第六题
n = 1
while n != 0:
    n = int(input("请输入一个整数："))
print("循环结束")

