from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int
    city: str

new_student = {'name': 'ali', 'age': 32, 'city': 'peshawar'}


student = Person(**new_student)

print(student)