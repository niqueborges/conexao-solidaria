import pytest
from django.urls import reverse

@pytest.mark.asyncio
async def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
