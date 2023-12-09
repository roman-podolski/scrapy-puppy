/Users/romanpodolski/PycharmProjects/pythonProject/venv/bin/python /Users/romanpodolski/PycharmProjects/pythonProject/app/medium/medium_api.py 
# SQLAlchemy Mastery: Simplify Your Database Tasks and Do More with Less Code (Part 1)

SQLAlchemy is a really cool library for working with databases. Learning to write SQL queries with SQLAlchemy can be challenging because its not always straightforward. In this series, I want to show you how to approach common tasks that will help accelerate your learning of this awesome library.

![](https://miro.medium.com/0*0Orx_TiFLNZRg__Q.png)

If you need help connecting to your database, you can use Planetscale. Here is a tutorial that will help you set up everything you need.

[Tutorial link](https://blog.devops.dev/database-dreams-creating-a-robust-python-project-with-sqlalchemy-and-planetscale-fe1ee476e135)

### Note

I will omit `session.commit`, closing the database, and other related details, as we did in the previous tutorial. My primary focus will be on SQLAlchemy.

## 1. GROUP BY + HAVING

The `GROUP BY` clause is used to group rows from a table based on the values in one or more columns. The `HAVING` clause is used to filter the results of a `GROUP BY` . Its similar to `WHERE` but for `GROUP BY`.

### Query

```python
SELECT
    class
FROM
    courses
GROUP BY class
HAVING COUNT(DISTINCT student) >= 5;
```

### Data

```python
class Course(Base):
    __tablename__ = "courses"

    student_id = Column(Integer, primary_key=True)
    student = Column(Text, nullable=False)
    class_ = Column(Text, nullable=False)

new_courses = [
    Course(student="A", class_="Math"),
    Course(student="B", class_="English"),
    Course(student="C", class_="Math"),
    Course(student="D", class_="Biology"),
    Course(student="E", class_="Math"),
    Course(student="F", class_="Computer"),
    Course(student="G", class_="Math"),
    Course(student="H", class_="Math"),
    Course(student="HI", class_="Math"),
]
```

### Code

Most of the functionality is imported from the SQLAlchemy package. The `func` module contains a wide range of methods, including aggregate functions and much more. In this case, we can just chain the methods and put the condition to the having.

```python
from sqlalchemy import func, distinct

result = (
    session.query(Course.class_)
    .group_by(Course.class_)
    .having(func.count(distinct(Course.student)) >= 5)
)

for row in result:
    print(row)

# (Math,)
```

## 2. LEFT JOIN

### Query

```sql
SELECT
   p.project_id,
   ROUND(AVG(e.experience_years), 2) AS average_years
FROM project p
LEFT JOIN employee e USING(employee_id)
GROUP BY p.project_id;
```

### Data

```python
class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    experience_years = Column(Integer, nullable=False)


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, primary_key=True)

    __table_args__ = (
        UniqueConstraint("project_id", "employee_id", name="unique_project_id_employee_id"),
    )

new_employees = [
    Employee(name="Khaled", experience_years=3),
    Employee(name="Ali", experience_years=2),
    Employee(name="John", experience_years=1),
    Employee(name="Doe", experience_years=2),
]

new_projects = [
    Project(project_id=1, employee_id=1),
    Project(project_id=1, employee_id=2),
    Project(project_id=1, employee_id=3),
    Project(project_id=2, employee_id=1),
    Project(project_id=2, employee_id=4),
]
```

### Code

The `outerjoin` function, in this context, performs a LEFT OUTER JOIN, which is essentially the same as a LEFT JOIN. When using `outerjoin`, the first parameter indicates the table you want to join, and the second parameter defines the condition on which the columns should be used for joining the tables

```python
from sqlalchemy import func

result = (
    session.query(
        Project.project_id,
        func.round(func.avg(Employee.experience_years), 2).label("average_years"),
    ).outerjoin(Employee, Project.employee_id == Employee.employee_id)
    .group_by(Project.project_id)
)

for row in result:
    print(row)

# (1, Decimal(2.00))
# (2, Decimal(2.50))
```

## 3. NOT IN

### Query

```sql
SELECT student_id, student_name 
FROM students
WHERE department_id NOT IN (SELECT department_id from Departments);
```

### Data

```python
class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True)
    department_name = Column(Text, nullable=False)


class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True)
    student_name = Column(Text, nullable=False)
    department_id = Column(Integer, nullable=False)


create_tables_orm(engine)

new_departments = [
    Department(department_name="Electrical Engineering"),
    Department(department_name="Computer Engineering"),
    Department(department_name="Business Administration"),
]

new_students = [
    Student(student_name="Alice", department_id=1),
    Student(student_name="Bob", department_id=7),
    Student(student_name="Jennifer", department_id=13),
    Student(student_name="Jasmine", department_id=14),
    Student(student_name="Steve", department_id=77),
    Student(student_name="Luis", department_id=74),
    Student(student_name="Jonathan", department_id=1),
    Student(student_name="Daiana", department_id=7),
    Student(student_name="Madelynn", department_id=33),
    Student(student_name="John", department_id=1),
```

### Code

The subquery might be a bit confusing. In the `session.query`, we specify the columns we want to retrieve. In the `WHERE` clause, we indicate which column we want to compare with the subquery (not_in).

```python
from sqlalchemy import and_, func, desc


result = (
    session.query(Student.student_id, Student.student_name)
    .where(Student.department_id.not_in(session.query(Department.department_id)))
)

for row in result:
    print(row)

# (2, Bob)
# (3, Jennifer)
# (4, Jasmine)
# (5, Steve)
# (6, Luis)
# (8, Daiana)
# (9, Madelynn)
```

## 4. DISTINCT

### Query

```sql
SELECT activity_date AS "day",
COUNT(DISTINCT user_id) AS "active_users"
FROM activity
WHERE activity_date > 2019-06-27 AND activity_date <= 2019-07-27
GROUP BY activity_date;
```

### Data

```python
class Activity(Base):
    __tablename__ = "activity"

    activity_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    session_id = Column(Integer, nullable=False)
    activity_date = Column(Date, nullable=False)
    activity_type = Column(Text, nullable=False)


create_tables_orm(engine)

new_activities = [
    Activity(user_id=1, session_id=1, activity_date="2019-07-20", activity_type="open_session"),
    Activity(user_id=1, session_id=1, activity_date="2019-07-20", activity_type="scroll_down"),
    Activity(user_id=1, session_id=1, activity_date="2019-07-20", activity_type="end_session"),
    Activity(user_id=2, session_id=4, activity_date="2019-07-20", activity_type="open_session"),
    Activity(user_id=2, session_id=4, activity_date="2019-07-21", activity_type="send_message"),
    Activity(user_id=2, session_id=4, activity_date="2019-07-21", activity_type="end_session"),
    Activity(user_id=3, session_id=2, activity_date="2019-07-21", activity_type="open_session"),
    Activity(user_id=3, session_id=2, activity_date="2019-07-21", activity_type="send_message"),
    Activity(user_id=3, session_id=2, activity_date="2019-07-21", activity_type="end_session"),
    Activity(user_id=4, session_id=3, activity_date="2019-06-25", activity_type="open_session"),
    Activity(user_id=4, session_id=3, activity_date="2019-06-25", activity_type="end_session"),
]
```

### Code

Sometimes, instead of using `WHERE`, you might encounter `FILTER`, which serves the same purpose. Several important concepts come into play here.

When you see `.label`, it indicates an alias.

Initially, you can use `func.count` and include `distinct` within this method. Everything in this context is imported from SQLAlchemy. Pay special attention to `and_`, which has an underscore; it allows you to chain an infinite number of conditions together seamlessly.

```python
from sqlalchemy import func, and_, distinct


result = (
    session.query(
        Activity.activity_date.label("day"),
        func.count(distinct(Activity.user_id))
    ).where(and_(Activity.activity_date > "2019-06-27", Activity.activity_date <= "2019-07-27"))
    .group_by(Activity.activity_date)
)

for row in result:
    print(row)

# (datetime.date(2019, 7, 20), 2)
# (datetime.date(2019, 7, 21), 2)
```

---

**Thanks for reading my article!**

If you enjoyed the read and want to be part of our growing community, hit the follow button, and lets embark on a knowledge journey together.

Your feedback and comments are always welcome, so dont hold back!

## In Plain English

_Thank you for being a part of our community! Before you go:_

- _Be sure to **clap** and **follow** the writer! 👏_ 

- _You can find even more content at **[PlainEnglish.io](https://plainenglish.io/) 🚀**_ 

- _Sign up for our **[free weekly newsletter](http://newsletter.plainenglish.io/)**. 🗞 ️_

- _Follow us on **[Twitter](https://twitter.com/inPlainEngHQ)(X**_), _**[LinkedIn](https://www.linkedin.com/company/inplainenglish/)**_, _**[YouTube](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw)**_, and _**[Discord](https://discord.gg/XxRS92b2).**_

Process finished with exit code 0
