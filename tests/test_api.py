from app import app

def test_kvadrat():
    # Opprett en testklient
    client = app.test_client()

    # Send et GET-kall til API-et
    response = client.get("/api/kvadrat/4")

    # Hent JSON-data fra svaret
    data = response.get_json()

    # Sjekk at alt er riktig
    assert response.status_code == 200
    assert data["tall"] == 4
    assert data["kvadrat"] == 16


def test_version():
    # Opprett en testklient
    client = app.test_client()

    # Hent versjon
    response = client.get("/api/version")
    data = response.get_json()

    assert response.status_code == 200
    assert data["version"] == "1.0"

# Smidig IT-2 © TIP AS, 2026
