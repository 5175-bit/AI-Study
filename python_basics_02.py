a = 10
b = 5
print(a > b)
print(a < b)
print(a == b)
print(a != b)
print(a >= b)
print(a <= b)
age = 20
if age >=18:
    print("你已经成年了")

score = 58
if score >=60:
    print("及格")
else:
    print("不及格")

score = 85
if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else: 
    print("不及格")   

score = float(input("请输入你的成绩："))
if score >= 60:
    print("及格")
else:
    print("不及格")

x = int(input("请输入一个整数："))
if x > 0:
    print("正数")
elif x < 0:
    print("负数")
else:
    print("零")

a = int(input("请输入第一个整数："))
if a % 2 == 0:
    print("偶数")
else:
    print("奇数")

a = int(input("请输入第一个整数："))
b = int(input("请输入第二个整数："))
if a >= b:
    print(a)
else:
    print(b)

score = int(input("请输入你的成绩："))
if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")

# %%
age = int(input("请输入你的年龄："))
if age < 18:
    print("未成年")
elif age < 60:
    print("成年人")
else:
    print("老年人")

# %%
x = int(input("请输入一个整数："))
if x % 2 == 0 and x % 3 == 0:
    print("能同时被2和3整除")
else:
    print("不能同时被2和3整除")
# %%
age = int(input("请输入你的年龄："))
if age < 0 or age > 120:
    print("年龄输入不合理")
else:
    print("年龄输入合理")


# %%
score = int(input("请输入你的成绩："))
if score < 0 or score > 100:
    print("成绩输入错误")
else:
    if score >= 90:
        print("优秀")
    elif score >= 80:
        print("良好")
    elif score >= 60:
        print("及格")
    else:
        print("不及格")

# %%
username = input("请输入用户名：")
password = input("请输入密码：")
if username == "admin" and password == "123456":
    print("登录成功") 
else:
    print("登录失败")

# %%
is_raining = False
if not is_raining:
    print("可以出去散步")
else:
    print("最好不要出门")

# %% for循环的使用
for i in range (1, 11):
    print(i)

# %%
for i in range(1, 21):
    if i % 2 == 0:
        print(i)
# %%
x = 0
for i in range(1, 101):
    x = x + i;
print(x)

# %%
n = int(input("请输入一个整数："))
for i in range(1, n + 1):
    print(i)
# %%
x = 0
n = int(input("请输入一个整数："))
for i in range(1, n + 1):
    x = x + i
print(x)
# %%
n = int(input("请输入一个整数："))
for i in range(1, n + 1):
    if i % 3 == 0:
        print(i)
# %%
