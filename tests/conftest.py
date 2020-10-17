import pytest

@pytest.fixture
def get_ios_test_data_int_brief():
    with open(r'tests/data/ios_show_ip_interface_brief.txt', 'r') as file:
        file_data = file.read()

    return file_data


@pytest.fixture
def get_ios_test_data_int_g_0_1():
    with open(r'tests/data/ios_show_interfaces_g0-1.txt', 'r') as file:
        file_data = file.read()

    return file_data
