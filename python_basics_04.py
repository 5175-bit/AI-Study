# %% break语句的使用 第一题
i = 1
while i <= 10:
    print(i)
    if i == 6:
        break
    i += 1
# %% 第二题
i = 1
while i <= 10:
    if i == 5:
        i += 1
        continue
    print(i)
    i += 1
# %% 第三题
while True:
    password = input("请输入密码：")
    if password == "123456":
        print("登录成功")
        break
# %% 第四题
while True:
    n = int(input("请输入一个整数："))
    if n > 0:
        print(f"{n}") 
    elif n < 0:
        continue
    else:
        print("程序结束")
        break
# %% 第五题
for i in range(1, 21):
    if i % 3 ==0:
        continue
    elif i > 15:
        break
    else:
        print(i)