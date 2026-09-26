# %% 
scores = [90, 85, 78, 92, 66]
print("成绩列表：", scores)
scores.append(88)
print("添加88后的成绩列表：", scores)
scores.remove(78)
print("删除78后的成绩列表：", scores)
# %% 习题1
scores = [78, 92, 85, 66, 100]
print(scores[0], scores[2], scores[-1])

# %% 习题2
scores[1] = 95
print(scores)
# %% 习题3
scores.append(88)
print(scores)

# %% 习题4
print(sum(scores), max(scores), min(scores), sum(scores) / len(scores))
# %% 习题5
for score in scores:
    print(score)

# %% 习题6
count = 0
for score in  scores:
    if score >= 60:
        count += 1
print(count)

# %% 切片,insert, sort, pop 习题1
numbers = [10, 20, 30, 40, 50, 60]
print(numbers[1:4])
# %% 习题2
print(numbers[-3:])
# %% 习题3
numbers.insert(2,25)
print(numbers)
# %% 习题4
numbers.remove(40)
print(numbers)
# %% 习题5
removed = numbers.pop(1)
print(removed)
# %% 习题6
numbers.sort()
print(numbers)
numbers.sort(reverse=True)
print(numbers)
sorted(numbers)
print(numbers)
# %% tuple 习题1
student = ("Bob", 24, "应用数学", "大连理工大学")
print(student[0], student[2], student[-1])

# %% 习题2
numbers = (10, 20, 30, 40, 50, 60)
numbers[1:4]
# %% 习题3
for Numbers in numbers:
    print(Numbers)
# %% 习题4
point = (3, 5)
x, y = point
print(x)
print(y)
# %% 习题5
a = (10)
b = (10,)
print(type(a))
print(type(b))

