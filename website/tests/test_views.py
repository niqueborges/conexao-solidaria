import pytest
from django.urls import reverse

@pytest.mark.asyncio
async def test_home_view(async_client):
    response = await async_client.get(reverse('home'))
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_institution_list_view_with_mock(async_client, mock_fetch_data):
    # Setup mock return value
    mock_fetch_data.return_value = {
        "institutions": [
            {"cnpj": "123", "name": "Mock Inst", "verified": True, "state": "SP", "region": "Sudeste"}
        ]
    }
    
    response = await async_client.get(reverse('institutions'))
    assert response.status_code == 200
    assert b"Mock Inst" in response.content

@pytest.mark.asyncio
async def test_detail_institution_view_with_mock(async_client, mock_fetch_data):
    # Setup mock return value
    mock_fetch_data.return_value = {
        "cnpj": "123",
        "name": "Mock Details",
        "about": "Advanced testing",
        "verified": True
    }
    
    response = await async_client.get(reverse('institution', kwargs={'cnpj': '123'}))
    assert response.status_code == 200
    assert b"Mock Details" in response.content
