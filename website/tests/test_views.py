import pytest
from django.urls import reverse

@pytest.mark.asyncio
async def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_institution_list_view_with_mock(client, mock_fetch_data):
    # Setup mock return value
    mock_fetch_data.return_value = {
        "institutions": [
            {"cnpj": "123", "name": "Mock Inst", "verified": True, "state": "SP", "region": "Sudeste"}
        ]
    }
    
    response = client.get(reverse('institutions'))
    assert response.status_code == 200
    assert b"Mock Inst" in response.content

@pytest.mark.asyncio
async def test_detail_institution_view_with_mock(client, mock_fetch_data):
    # Setup mock return value
    mock_fetch_data.return_value = {
        "cnpj": "123",
        "name": "Mock Details",
        "about": "Advanced testing",
        "verified": True
    }
    
    response = client.get(reverse('detail_institution', kwargs={'cnpj': '123'}))
    assert response.status_code == 200
    assert b"Mock Details" in response.content
