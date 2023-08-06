def test_configuration(client):
    r = client.get("/api/configuration")
    assert r.status_code == 200
    assert r.json == {
        "auth": {"enabled": False},
        "license": {
            "id": "etalab-2.0",
            "url": "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE",
        },
    }
