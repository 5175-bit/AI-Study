# %% dict 习题1
student = {
    "name": "Bob",
    "age": 24, 
    "major": "应用数学",
    "school": "大连理工大学"
}
print(student["name"], student["major"])

# %% 习题2
student["age"]=25
print(student)
# %% 习题3
student["score"]=90
print(student)
# %% 习题4
student.pop("school")
print(student)
# %% 习题5
if "major" in student:
    print("major存在")
# %% 习题6
for key, value in student.items():
    print(key, value)
# %% 习题1
student = {
    "name": "Bob",
    "age": 24
}
print(student.get("name"))
# %% 习题2
print(student.get("score", 0))

# %% 习题3
print(student.keys())
print(student.values())
print(student.items())
# %% 习题4
students = [
    {"name": "Alice", "score": 92},
    {"name": "Bob", "score": 78},
    {"name": "Tom", "score": 85}
]
print(students[1])
# %% 习题5
for student in students:
    print(student["name"], student["score"])

# %% 习题6
count = 0
for student in students:
    if student["score"] >= 80:
        count += 1
print(count)

# %% set 习题1
numbers = {1, 2, 3, 3, 4, 4, 5}
print(numbers)
# %% 习题2
numbers.add(6)
print(numbers)
# %% 习题3
numbers.remove(2)
print(numbers)
# %% 习题4
if 5 in numbers:
    print(f"{5}在集合中")
# %%
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a | b)
print(a & b)
print(a - b)
# %% 字符串 习题1
text = "Python"
print(text[0], text[-1], text[1:4])
# %% 习题2
print(text[::-1])
# %% 3
name = " Bob "
print(name.strip())
# %% 4
text = "hello python"
print(text.upper())
# %% 5
text = "I like Java"
print(text.replace("Java", "Python"))
# %% 6
text = "Alice,Bob,Tom,Jack"
list = text.split(",") 
for name in list:
    print(name)
# %% 1
text = "Python is easy, Python is powerful"
print(text.find("Python"))
# %% 2
print(text.count("Python"))
# %% 3
filename = "data.csv"
print(filename.startswith("data"))
# %% 4
print(filename.endswith(".csv"))
# %% 5
str = input()
if str.isdigit():
    print("纯数字")
else:
    print("不是纯数字")
# %% 6
username = input()
if username.isalnum() :
    print("用户名格式正确")
else:
    print("用户名格式错误")
# %%
