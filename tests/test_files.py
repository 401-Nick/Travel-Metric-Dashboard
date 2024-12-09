def test_files_route(logged_in_client):
    resp = logged_in_client.get("/files")
    if resp.status_code == 308:
        resp = logged_in_client.get("/files/")
    assert resp.status_code == 200


def test_files_upload_route(logged_in_client):
    resp = logged_in_client.post(
        "/files/upload", data={"file": (b"dummy content", "dummyfile.txt")}
    )
    assert resp.status_code in [200, 302]


def test_files_download_route(logged_in_client):
    resp = logged_in_client.get("/files/download/1/test.txt")
    assert resp.status_code in [200, 404]


def test_files_delete_route(logged_in_client):
    resp = logged_in_client.post("/files/delete/1", follow_redirects=True)
    assert resp.status_code in [200, 404]


def test_files_rename_file_route(logged_in_client):
    resp = logged_in_client.post(
        "/files/rename_file/1", data={"new_name": "newname.txt"}, follow_redirects=True
    )
    assert resp.status_code in [200, 404]
