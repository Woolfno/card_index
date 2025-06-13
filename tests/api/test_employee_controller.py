import uuid
from datetime import datetime
from decimal import Decimal

import pytest
from litestar.status_codes import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT)
from litestar.testing import AsyncTestClient

from models.models import Employee
from schemas.employee import EmployeeShort


@pytest.fixture(scope="function")
def employee(db):
    emp = EmployeeShort(id=uuid.uuid4(), first_name="Ivanov", middle_name="Ivan", last_name="Ivanovich", 
                                start_date=datetime.now().date(), position_id=10, salary=Decimal(2500))    
      
    with db.cursor() as cursor:
        query = "INSERT INTO public.employee (id, first_name, middle_name, last_name, start_date, position_id, salary) " \
        "VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s) RETURNING id;"
        cursor.execute(query, (emp.first_name, emp.middle_name, emp.last_name, emp.start_date, emp.position_id, emp.salary))
        db.commit()
        emp.id=uuid.UUID(cursor.fetchone()[0])
        
        yield emp
        
        cursor.execute("DELETE FROM public.employee WHERE id=%s;", (str(emp.id),))
        db.commit()

@pytest.fixture
def boss(db):
    emp = EmployeeShort(id=uuid.uuid4(), first_name="Petrov", middle_name="Petr", last_name="Petrovich", 
                                start_date=datetime.now().date(), position_id=11, salary=Decimal(3500))
      
    with db.cursor() as cursor:
        query = "INSERT INTO public.employee (id, first_name, middle_name, last_name, start_date, position_id, salary) " \
        "VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s) RETURNING id;"
        cursor.execute(query, (emp.first_name, emp.middle_name, emp.last_name, emp.start_date, emp.position_id, emp.salary))
        db.commit()
        emp.id=uuid.UUID(cursor.fetchone()[0])
        
        yield emp
        
        cursor.execute("DELETE FROM public.employee WHERE id=%s;", (str(emp.id),))
        db.commit()

@pytest.mark.asyncio
async def test_get_employee_list(client:AsyncTestClient):
    response = await client.get(f'/api/employee')
    assert response.status_code == HTTP_200_OK
    assert len(response.text) > len('[]')

@pytest.mark.asyncio
async def test_get_employee_by_id(employee:EmployeeShort, client:AsyncTestClient):
    response = await client.get(f'/api/employee/{str(employee.id)}')
    assert response.status_code == HTTP_200_OK

@pytest.mark.asyncio
async def test_employee_create(client:AsyncTestClient, db):
    payload = {"first_name":"Ivanov", "middle_name": "Ivan", "last_name": "Ivanovich", 
                            "start_date":datetime.now().date().strftime("%Y-%m-%d"), 
                            "position_id":20, "salary":2500}
    response = await client.post('/api/employee/', 
                            json=payload,
                            )
    assert response.status_code==HTTP_201_CREATED
    employee = EmployeeShort.model_validate(response.json())
    assert employee.id != ''
    with db.cursor() as cursor:
        cursor.execute("SELECT id FROM public.employee WHERE id=%s;", (str(employee.id),))
        result = cursor.fetchone()
        
        assert result is not None

        cursor.execute("DELETE FROM public.employee WHERE id=%s;", (str(employee.id),))
        db.commit()    

@pytest.mark.asyncio
async def test_employee_update(employee:EmployeeShort, client:AsyncTestClient, db):
    payload = {"first_name":"new first name"}
    response = await client.patch(f"/api/employee/{str(employee.id)}", json=payload)
    assert response.status_code == HTTP_200_OK
    response_emp = response.json()
    assert str(employee.id )== response_emp['id']
    assert employee.first_name != response_emp['first_name']
    assert employee.middle_name == response_emp['middle_name']

    with db.cursor() as cursor:
        cursor.execute("SELECT first_name FROM public.employee WHERE id=%s;", (str(employee.id),))
        result = cursor.fetchone()
        
        assert result is not None
        assert result[0] == response_emp['first_name']

@pytest.mark.asyncio
async def test_employee_remove(employee:EmployeeShort, client:AsyncTestClient, db):
    response = await client.delete(f"/api/employee/{str(employee.id)}")
    assert response.status_code == HTTP_204_NO_CONTENT

    with db.cursor() as cursor:
        cursor.execute("SELECT id FROM public.employee WHERE id=%s;", (str(employee.id),))
        result = cursor.fetchone()
        assert result is None

@pytest.mark.asyncio
async def test_employee_change_boss(employee:Employee, boss:Employee, client:AsyncTestClient, db):
    response = await client.put(f"/api/employee/{str(employee.id)}/boss", json={"id":str(boss.id)})
    assert response.status_code == HTTP_200_OK
    
    with db.cursor() as cursor:
        cursor.execute("SELECT boss_id FROM public.employee WHERE id=%s;", (str(employee.id),))
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == str(boss.id)