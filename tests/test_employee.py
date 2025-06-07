from datetime import datetime
import uuid
import pytest
import pytest_asyncio
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

from models.models import Employee
from app import app

app.debug = True


@pytest.fixture(scope="function")
def employee(db):
    emp = Employee(first_name="Ivanov", middle_name="Ivan", last_name="Ivanovich", 
                                start_date=datetime.now().date(), position_id=10, salary=2500)    
    
    with db.cursor() as cursor:
        query = "INSERT INTO public.employee (id, first_name, middle_name, last_name, start_date, position_id, salary) " \
        "VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s) RETURNING id;"
        cursor.execute(query, (emp.first_name, emp.middle_name, emp.last_name, emp.start_date, 10, emp.salary))
        db.commit()
        emp.id=uuid.UUID(cursor.fetchone()[0])
        
        yield emp
        
        cursor.execute("DELETE FROM public.employee WHERE id=%s;", (str(emp.id),))
        db.commit()

@pytest.mark.asyncio
async def test_get_employee_by_id(employee:Employee):
    async with AsyncTestClient(app=app) as client:
        response = await client.get(f'/api/employee/{str(employee.id)}')
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_without_photo(client:AsyncTestClient, db):
    payload = {"first_name":"Ivanov", "middle_name": "Ivan", "last_name": "Ivanovich", 
                            "start_date":datetime.now().date().strftime("%Y-%m-%d"), 
                            "position_id":20, "salary":2500}
    response = await client.post('/employee/create', 
                            data=payload, 
                            files={'photo_file':open('tests/test_photo.jpg', 'rb')}
                            )
    assert response.status_code==HTTP_200_OK
    id = response.url.path.split('/')[-1]
    assert id != ''
    with db.cursor() as cursor:
        cursor.execute("SELECT id FROM public.employee WHERE id=%s;", (str(id),))
        result = cursor.fetchone()
        
        assert result is not None

        cursor.execute("DELETE FROM public.employee WHERE id=%s;", (str(id),))
        db.commit()