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
 