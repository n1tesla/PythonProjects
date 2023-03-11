import random
import string
from dataclasses import dataclass,field

def generate_id()->str:
    return "".join(random.choices(string.ascii_uppercase,k=12))


@dataclass(slots=True)
class Person:
    name:str
    address:str
    active:bool=True
    email_addresses:list[str]=field(default_factory=list)
    id:str = field(init=False,default_factory=generate_id) #by user cant initialize id value
    _search_string:str = field(init=False,repr=False)

    def __post_init__(self)->None:
        self._search_string=f"{self.name} {self.address}"

def main()->None:
    person=Person(name="Tuna",address="123 main st")

    print(person)
    print(person.__dict__["name"])
if __name__ == '__main__':
    main()



