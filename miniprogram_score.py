class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def update_score(self, new_score):
        self.score = new_score
    def is_passed(self):
        return self.score >= 60
students = []
while True:

    print("===== 学生管理系统 =====")
    print("1. 添加学生")
    print("2. 查询学生")
    print("3. 修改成绩")
    print("4. 删除学生")
    print("5. 显示全部学生")
    print("0. 退出")

    choice = input("请输入操作编号：")
    
    if choice == "1":
        name = input("请输入学生姓名：")
        score = float(input("请输入学生成绩："))

        found = False
        for student in students:
            if student.name == name:
                found = True
                break
        if not found:
            student_append = Student(name, score)
            students.append(student_append)
            print("添加成功")
        else:
            print("学生已存在")

    elif choice == "2":
        name = input("请输入查询学生姓名：")

        found = False
        for student in students:
            if student.name == name:
                found = True
                if student.is_passed():
                    print(f"姓名：{student.name}\n成绩：{student.score}\n状态：及格")
                else:
                    print(f"姓名：{student.name}\n成绩：{student.score}\n状态：未及格")
                break
        if not found:
            print("没有找到该学生")

    elif choice == "3":
        try:
            name = input("请输入学生姓名：")
            new_score = float(input("请输入学生成绩："))

            found = False

            for student in students:
                if student.name == name:
                    student.update_score(new_score)
                    found = True
                    print("修改完成")
                    break

            if not found:
                print("没有找到该学生")

        except ValueError:
            print("输入成绩有误，请重新输入")

    elif choice == "4":
        remove_name = input("请输入要删除学生的姓名：")

        found = False
        for student in students:
            if student.name == remove_name:
                remove_student = student
                found = True
                break
        if found:
            students.remove(remove_student)
            print("已删除该学生")
        else:
            print("没有找到该学生")
    
    elif choice == "5":

        if not students:
            print("列表中没有学生")

        else:
            for student in students:
                if student.is_passed():
                    print(
                        f"姓名：{student.name}\n"
                        f"成绩：{student.score}\n"
                        f"状态：及格"
                    )
                else:
                    print(
                        f"姓名：{student.name}\n"
                        f"成绩：{student.score}\n"
                        f"状态：未及格"
                    )
    elif choice == "0":
            print("程序结束")
            break
    
    else:
        print("输入有误，请重新输入")

