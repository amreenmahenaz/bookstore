import pytest
from unittest.mock import patch, MagicMock
from legacySystsModel import shutdown


@pytest.fixture
def mock_memory():
    """Fixture to mock memory structure."""
    return {
        "region": {
            "systs_list": ["sys1", "sys2"],
            "pkr_list": ["pkr1", "pkr2"],
            "entityMapping": {
                "entity1": "task1.task2",
                "entity2": "task3.task4",
            },
            "accountsToBeSynchronized": ["acct1", "acct2"],
        }
    }


@patch("legacySystsModel.subprocess.call")
@patch("legacySystsModel._legacy_refresh")
@patch("legacySystsModel.memory", create=True)
def test_shutdown(mock_memory_patch, mock_legacy_refresh, mock_subprocess, mock_memory):
    """Test the shutdown function."""
    mock_memory_patch.__getitem__.side_effect = mock_memory.__getitem__
    
    config = {"server": "test_server"}
    acct_mapping = {"acct1": "entity1", "acct2": "entity2"}
    region = "region"

    try:
        shutdown(config, acct_mapping, region)
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")

    # Check if _legacy_refresh is called for each system in systs_list
    assert mock_legacy_refresh.call_count == len(mock_memory["region"]["systs_list"])

    # Check if subprocess.call is triggered for PKRouter refresh
    assert mock_subprocess.call_count > 0
    mock_subprocess.assert_any_call(
        f"netAdminCmd -t 60 pkr1 PKRouter reload", shell=True
    )
    mock_subprocess.assert_any_call(
        f"netAdminCmd -t 60 pkr2 PKRouter reload", shell=True
    )

    # Check if subprocess.call is triggered for entityMapping refresh
    mock_subprocess.assert_any_call(
        f"netAdminCmd task1 reloadAcctInfo", shell=True
    )
    mock_subprocess.assert_any_call(
        f"netAdminCmd task3 reloadAcctInfo", shell=True
    )

    # Check if subprocess.call is triggered for account synchronization
    mock_subprocess.assert_any_call(
        f"netAdminCmd task1 synchronizeAccount acct1", shell=True
    )
    mock_subprocess.assert_any_call(
        f"netAdminCmd task3 synchronizeAccount acct2", shell=True
    )
