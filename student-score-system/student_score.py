def input_students():
    students = []
    while True:
        name = input("请输入学生名字：")
        score = float(input("请输入学生成绩："))
        student = {
            "name": name,
            "score": score
        }
        students.append(student)
        choice = input("是否继续录入？y/n：")
        if choice.lower() == "n":
            break
    return students
def get_score(student):
    return student["score"]
def show_statistics(students):
    scores = []
    pass_count = 0
    for student in students:
        score = student["score"]
        scores.append(score)
        if score >= 60:
            pass_count += 1
    if len(scores) == 0:
        print("没有学生成绩")
        return
    print(f"学生人数为：{len(scores)}")
    print(f"学生的最高分为：{max(scores)}")
    print(f"学生的最低分为：{min(scores)}")
    print(f"学生的平均分为：{sum(scores) / len(scores):.2f}")
    print(f"及格学生人数为：{pass_count}")
def show_ranking(students):
    sorted_students = sorted(
        students,
        key=get_score,
        reverse=True
    )
    print("成绩排名")
    for sorted_student in sorted_students:
        print(sorted_student["name"], sorted_student["score"])
students = input_students()
show_statistics(students)
show_ranking(students)