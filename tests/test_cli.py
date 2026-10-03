from unittest.mock import patch, Mock
import cli
 
 
def fake_response(data, ok=True):
    return Mock(ok=ok, json=lambda: data)
 
 
def run(argv):
    
    args = cli.build_parser().parse_args(argv)
    args.func(args)
 
 
ITEM = {"id": 1, "name": "Milk", "brand": "Silk", "price": 3.5, "stock": 10}

@patch("cli.requests.request")
def test_list_items(mock_request, capsys):
    mock_request.return_value = fake_response([ITEM])
    run(["list"])
    assert "Milk" in capsys.readouterr().out
 
 
@patch("cli.requests.request")
def test_view_item(mock_request, capsys):
    mock_request.return_value = fake_response(ITEM)
    run(["view", "1"])
    assert "name: Milk" in capsys.readouterr().out
 
 
@patch("cli.requests.request")
def test_add_item(mock_request, capsys):
    mock_request.return_value = fake_response(ITEM)
    run(["add", "Milk", "--price", "3.5", "--stock", "10"])
    assert "Added" in capsys.readouterr().out


@patch("cli.requests.request")
def test_update_item(mock_request, capsys):
    mock_request.return_value = fake_response(ITEM)
    run(["update", "1", "--price", "3.5"])
    assert "Updated" in capsys.readouterr().out
 
 
def test_update_without_values(capsys):
    run(["update", "1"])
    assert "Error" in capsys.readouterr().out
 
 
@patch("cli.requests.request")
def test_delete_item(mock_request, capsys):
    mock_request.return_value = fake_response({"message": "Item deleted successfully"})
    run(["delete", "1"])
    assert "Item deleted" in capsys.readouterr().out
 
 
@patch("cli.requests.request")
def test_api_error_message(mock_request, capsys):
    mock_request.return_value = fake_response({"error": "Item not found"}, ok=False)
    run(["view", "999"])
    assert "Item not found" in capsys.readouterr().out


@patch("cli.requests.request", side_effect=cli.requests.exceptions.ConnectionError)
def test_connection_error(mock_request, capsys):
    run(["list"])
    assert "cannot connect" in capsys.readouterr().out
 
 
@patch("cli.requests.request")
def test_find_by_name(mock_request, capsys):
    mock_request.return_value = fake_response([{"barcode": "1", "name": "Nutella", "brand": "Ferrero"}])
    run(["find", "--name", "nutella"])
    assert "Nutella" in capsys.readouterr().out
 
 
def test_find_without_values(capsys):
    run(["find"])
    assert "Error" in capsys.readouterr().out
 
 