import pytest
from litestar.testing import AsyncTestClient
from litestar.status_codes import HTTP_200_OK
from datetime import datetime


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