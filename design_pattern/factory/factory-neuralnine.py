from abc import ABCMeta, abstractstaticmethod

#ABCMeta= cant create instance of the class
class IPerson(metaclass=ABCMeta):
    @abstractstaticmethod
    def person_method():
        """ Interface Method"""

# p1=IPerson() #It wont work. Cant instantiate
# p1.person_method()


class Student(IPerson):
    def __init__(self):
        self.name="Basic Student Name"
    def person_method(self):
        print("I am a student")

class Teacher(IPerson):
    def __init__(self):
        self.name="Basic Teacher Name"

    def person_method(self):
        print("I am a teacher")

s1=Student()
s1.person_method()

t1=Teacher()
t1.person_method()


"""we know that we want to create person object
but we dont know if this object shall be a student or a teacher
we want to decide that dynamically during run time """


class PersonFactory:
    @staticmethod
    def build_person(person_type):
        if person_type=="Student":
            return Student()
        if person_type=="Teacher":
            return Teacher()
        print("Invalid Type")
        return -1

if __name__=="__main__":
    choice=input("What type of person do you want to create?\n")
    person=PersonFactory.build_person(choice)
    person.person_method()
    