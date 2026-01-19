import pytest
def test_equal_or_not_equal():
    assert 3==3

def test_is_instance():
    assert isinstance('this is a sstring',str)

class Student:
    def __init__(self,first_name:str,last_name:str,major:str,years:int):
        self.first_name=first_name
        self.last_name=last_name
        self.major=major
        self.years=years

@pytest.fixture
def default_employee():
    return Student('John','Doe','Computer Science',3)

def test_person_initialization(default_employee):
    assert default_employee.first_name=="John",'First name should be john'
    assert default_employee.last_name == "Doe", 'Last name should be doe'
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 3