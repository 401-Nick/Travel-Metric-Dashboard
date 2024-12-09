# Unauthenticated user should be redirected to login page when trying to access dashboard
def test_dashboard_unauthenticated_route(client):
    resp = client.get("/dashboard")
    assert resp.status_code == 308


def test_logged_in_dashboard_route(logged_in_client):
    resp = logged_in_client.get("/dashboard", follow_redirects=True)
    assert resp.status_code == 200
