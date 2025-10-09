import pytest


def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1
    
def test_is_instance():
    assert isinstance('Eslam' , str)
    assert not isinstance("10" , int)

def test_boolean():
    validated = True 
    assert validated is True 
    assert ('hello' == 'world') is False

def test_type():
    assert type('Hello' is str)
    assert type('world' is not int)
    
def test_greater_or_less_than():
    assert 10 < 20 
    assert 20 > 10

def test_list():
    num_list = [1,2,3,4,5]
    any_list = [False , False]
    assert 1 in num_list 
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)
    
    
class Student:
    def __init__(self , first_name:str , last_name:str , major:str , years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return  Student('Eslam' , 'Kamel' , 'Computer Science' , 5)
        
def test_person_initialization(): # manual instantiation
    p = Student('Eslam' , 'Kamel' , 'Computer Science' , 5)
    assert p.first_name == 'Eslam' , 'first name should be Eslam'
    assert p.last_name == 'Kamel' , 'last name should be Kamel'
    assert p.major == 'Computer Science'
    assert p.years == 5
    
def test_person_initialization2(default_employee:Student): # automatic instantiation
    assert default_employee.first_name == 'Eslam' , 'first name should be Eslam'
    assert default_employee.last_name == 'Kamel' , 'last name should be Kamel'
    assert default_employee.major == 'Computer Science'
    assert default_employee.years == 5