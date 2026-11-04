
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase


# --------------------------------------------------
# 1. FastAPI application
# --------------------------------------------------

app = FastAPI(title="Student Management API")

# from fastapi import FastAPI 
# app = FastAPI() 

# @app.get("/")
# def home():
#     return {"message":"fastAPI is running"}
# --------------------------------------------------
# 2. Neo4j connection
# --------------------------------------------------

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "MyFirstInstance"

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


# --------------------------------------------------
# 3. Request model
# --------------------------------------------------

class Student(BaseModel):
    name: str
    age: int
    email: str
    course: str


# --------------------------------------------------
# 4. GET all students
#
# Example:
# GET /students
# GET /students?course=Python
# --------------------------------------------------

@app.get("/students")
def get_students(course: str | None = None):

    try:
        with driver.session() as session:

            if course:
                query = """
                MATCH (s:Student)
                WHERE s.course = $course
                RETURN s
                ORDER BY s.id
                """

                result = session.run(
                    query,
                    course=course
                )

            else:
                query = """
                MATCH (s:Student)
                RETURN s
                ORDER BY s.id
                """

                result = session.run(query)

            students = []

            for record in result:
                student = record["s"]

                students.append(dict(student))

            return {
                "count": len(students),
                "students": students
            }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while getting students"
        )


# --------------------------------------------------
# 5. GET one student
#
# Path parameter:
# GET /students/1
# --------------------------------------------------

@app.get("/students/{student_id}")
def get_student(student_id: int):

    try:
        with driver.session() as session:

            query = """
            MATCH (s:Student {id: $student_id})
            RETURN s
            """

            result = session.run(
                query,
                student_id=student_id
            )

            record = result.single()

            if record is None:
                raise HTTPException(
                    status_code=404,
                    detail="Student not found"
                )

            return dict(record["s"])

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while getting the student"
        )

# --------------------------------------------------
# 6. CREATE student
#
# POST /students
#
# JSON body:
# {
#     "name": "Rahul",
#     "age": 21,
#     "email": "rahul@gmail.com",
#     "course": "Python"
# }
# --------------------------------------------------

@app.post("/students")
def create_student(student: Student):

    try:
        with driver.session() as session:

            # Generate next ID
            id_query = """
            MATCH (s:Student)
            RETURN coalesce(max(s.id), 0) + 1 AS next_id
            """

            id_result = session.run(id_query)

            next_id = id_result.single()["next_id"]

            # Create student
            query = """
            CREATE (s:Student {
                id: $id,
                name: $name,
                age: $age,
                email: $email,
                course: $course
            })
            RETURN s
            """

            result = session.run(
                query,
                id=next_id,
                name=student.name,
                age=student.age,
                email=student.email,
                course=student.course
            )

            created_student = result.single()["s"]

            return {
                "message": "Student created successfully",
                "student": dict(created_student)
            }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while creating student"
        )


# --------------------------------------------------
# 7. UPDATE student
#
# PUT /students/1
#
# JSON body:
# {
#     "name": "Rahul Kumar",
#     "age": 22,
#     "email": "rahul@gmail.com",
#     "course": "FastAPI"
# }
# --------------------------------------------------

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: Student
):

    try:
        with driver.session() as session:

            query = """
            MATCH (s:Student {id: $student_id})

            SET
                s.name = $name,
                s.age = $age,
                s.email = $email,
                s.course = $course

            RETURN s
            """

            result = session.run(
                query,
                student_id=student_id,
                name=student.name,
                age=student.age,
                email=student.email,
                course=student.course
            )

            record = result.single()

            if record is None:
                raise HTTPException(
                    status_code=404,
                    detail="Student not found"
                )

            return {
                "message": "Student updated successfully",
                "student": dict(record["s"])
            }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while updating student"
        )


# --------------------------------------------------
# 8. DELETE student
#
# DELETE /students/1
# --------------------------------------------------

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    try:
        with driver.session() as session:

            query = """
            MATCH (s:Student {id: $student_id})

            DELETE s

            RETURN count(s) AS deleted_count
            """

            result = session.run(
                query,
                student_id=student_id
            )

            deleted_count = result.single()["deleted_count"]

            if deleted_count == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Student not found"
                )

            return {
                "message": "Student deleted successfully"
            }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while deleting student"
        )


# --------------------------------------------------
# 9. Application shutdown
# --------------------------------------------------

@app.on_event("shutdown")
def shutdown():

    driver.close()
