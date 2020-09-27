
def test_webhook(request_client):

    client = request_client(json=True)

    response = client.get('/dialogs/some/')
    # not allowed method
    assert response.status_code == 405

    response = client.post('/dialogs/some/')
    # unknown dialog
    assert response.status_code == 404

    # known dialog. bogus data.
    response = request_client().post('/dialogs/dione/')
    assert response.status_code == 400

    # known dialog. valid data.
    response = client.post('/dialogs/dione/', {})
    assert response.status_code == 200
    assert response.json() == {}

    # known dialog. bogus implementation
    response = client.post('/dialogs/ditwo/', {})
    assert response.status_code == 500
