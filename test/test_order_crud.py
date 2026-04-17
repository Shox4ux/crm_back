import pytest
from httpx import AsyncClient
from fastapi import status



BASE_URL = "/orders"



@pytest.mark.asyncio
async def test_get_all_orders(client: AsyncClient):
    response = await client.get(f"{BASE_URL}/create")
    assert response.status_code == status.HTTP_200_OK

# BASE_URL = "/aspects"
# payload = {"name": "Focus", "max_value": 0.5}
# changed_data = {"name": "Changed", "max_value": 0.5}
# multi_payload = [
#     {"name": "Focus", "max_value": 0.5},
#     {"name": "Read", "max_value": 0.5},
#     {"name": "Write", "max_value": 0.5},
# ]


# @pytest.mark.asyncio
# async def test_get_all_aspects(client: AsyncClient):
#     for obj in multi_payload:
#         response = await client.post(f"{BASE_URL}/", json=obj)
#         assert response.status_code == status.HTTP_200_OK

#     response = await client.get(f"{BASE_URL}/")
#     assert response.status_code == status.HTTP_200_OK
#     data = [AspectRead(**item) for item in response.json()]
#     assert len(data) == 3


# @pytest.mark.asyncio
# async def test_create_aspect(client: AsyncClient):
#     response = await client.post(f"{BASE_URL}/", json=payload)
#     assert response.status_code == status.HTTP_200_OK
#     data = AspectRead(**response.json())
#     assert data.name == "Focus"


# @pytest.mark.asyncio
# async def test_get_one_aspect(client: AsyncClient):
#     response = await client.post(f"{BASE_URL}/", json=payload)

#     assert response.status_code == status.HTTP_200_OK
#     data = AspectRead(**response.json())

#     response = await client.get(f"{BASE_URL}/{data.id}")
#     assert response.status_code == status.HTTP_200_OK


# @pytest.mark.asyncio
# async def test_get_one_aspect_not_found(client: AsyncClient):
#     non_existent_id = 99999
#     with pytest.raises(ItemNotFound) as exc_info:
#         await client.get(f"{BASE_URL}/{non_existent_id}")

#     assert exc_info.value.status_code == 404


# @pytest.mark.asyncio
# async def test_delete_aspect(client: AsyncClient):
#     response = await client.post(f"{BASE_URL}/", json=payload)

#     assert response.status_code == status.HTTP_200_OK
#     data = AspectRead(**response.json())

#     response = await client.delete(f"{BASE_URL}/{data.id}")
#     assert response.status_code == status.HTTP_200_OK


# @pytest.mark.asyncio
# async def test_update_aspect(client: AsyncClient):
#     response = await client.post(f"{BASE_URL}/", json=payload)

#     assert response.status_code == status.HTTP_200_OK
#     data = AspectRead(**response.json())
#     response = await client.patch(f"{BASE_URL}/{data.id}", json=changed_data)
#     assert response.status_code == status.HTTP_200_OK
