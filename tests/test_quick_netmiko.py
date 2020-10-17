import pytest
import os
import sys
import socket
from netmiko.cisco.cisco_ios import CiscoIosBase
from netmiko.cisco import CiscoIosSSH
from netmiko import ConnectHandler
base_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
sys.path.append(os.path.join(base_path))
from quick_netmiko import QuickNetmiko
from quick_netmiko.quick_netmiko import FailedDnsLookup


def test_quick_netmiko_bad_device_type():
    with pytest.raises(AttributeError):
        QuickNetmiko('10.0.0.100', 'unknown', 'temp', 'temp')


def test_quick_netmiko_fail_dns_timeout(monkeypatch):
    def socket_timeout(*args):
        raise socket.timeout

    monkeypatch.setattr(socket, 'gethostbyname', socket_timeout)

    with pytest.raises(FailedDnsLookup):
        QuickNetmiko('test_name', 'cisco_ios', 'temp', 'temp')


def test_quick_netmiko_fail_dns_socket_gaierror(monkeypatch):
    def socket_gaierror(*args):
        raise socket.gaierror

    monkeypatch.setattr(socket, 'gethostbyname', socket_gaierror)

    with pytest.raises(FailedDnsLookup):
        QuickNetmiko('test_name', 'cisco_ios', 'temp', 'temp')


def test_send_single_command_no_lookup(monkeypatch, get_ios_test_data_int_brief):
    def mock_init(*args, **kwargs):
        return None

    def mock_command_get(*args, **kwargs):
        return get_ios_test_data_int_brief

    def mock_connection_disco(*args, **kwargs):
        return True

    monkeypatch.setattr(ConnectHandler, '__init__', mock_init)
    monkeypatch.setattr(CiscoIosBase, '__init__', mock_init)
    monkeypatch.setattr(CiscoIosSSH, 'send_command', mock_command_get)
    monkeypatch.setattr(CiscoIosSSH, 'disconnect', mock_connection_disco)

    nm_obj = QuickNetmiko('10.0.0.100', 'cisco_ios', 'temp', 'temp')

    returned_data = nm_obj.send_commands('show ip interface brief')

    assert returned_data == get_ios_test_data_int_brief


def test_send_list_commands_no_lookup(monkeypatch, get_ios_test_data_int_brief, get_ios_test_data_int_g_0_1):
    def mock_init(*args, **kwargs):
        return None

    def mock_command_get(*args, **kwargs):
        temp_data = get_ios_test_data_int_brief + get_ios_test_data_int_g_0_1
        return temp_data

    def mock_connection_disco(*args, **kwargs):
        return True

    monkeypatch.setattr(ConnectHandler, '__init__', mock_init)
    monkeypatch.setattr(CiscoIosBase, '__init__', mock_init)
    monkeypatch.setattr(CiscoIosSSH, 'send_command', mock_command_get)
    monkeypatch.setattr(CiscoIosSSH, 'disconnect', mock_connection_disco)

    nm_obj = QuickNetmiko('10.0.0.100', 'cisco_ios', 'temp', 'temp')

    returned_data = nm_obj.send_commands(['show ip interface brief', 'show interfaces GigabitEthernet 0/1'])

    expected_data = get_ios_test_data_int_brief + get_ios_test_data_int_g_0_1

    side_effect = expected_data + expected_data

    assert returned_data == side_effect


def test_send_single_command_lookup(monkeypatch, get_ios_test_data_int_brief):
    def mock_init(*args, **kwargs):
        return None

    def mock_command_get(*args, **kwargs):
        return get_ios_test_data_int_brief

    def mock_connection_disco(*args, **kwargs):
        return True

    def socket_lookup(*args, **kwargs):
        return '10.0.0.100'

    monkeypatch.setattr(socket, 'gethostbyname', socket_lookup)
    monkeypatch.setattr(ConnectHandler, '__init__', mock_init)
    monkeypatch.setattr(CiscoIosBase, '__init__', mock_init)
    monkeypatch.setattr(CiscoIosSSH, 'send_command', mock_command_get)
    monkeypatch.setattr(CiscoIosSSH, 'disconnect', mock_connection_disco)

    nm_obj = QuickNetmiko('FAKE-DEVICE', 'cisco_ios', 'temp', 'temp')

    returned_data = nm_obj.send_commands('show ip interface brief')

    assert returned_data == get_ios_test_data_int_brief


def test_send_single_command_no_lookup_bad_command_data(monkeypatch, get_ios_test_data_int_brief):
    def mock_init(*args, **kwargs):
        return None

    def mock_command_get(*args, **kwargs):
        return get_ios_test_data_int_brief

    def mock_connection_disco(*args, **kwargs):
        return True

    monkeypatch.setattr(ConnectHandler, '__init__', mock_init)
    monkeypatch.setattr(CiscoIosBase, '__init__', mock_init)
    monkeypatch.setattr(CiscoIosSSH, 'send_command', mock_command_get)
    monkeypatch.setattr(CiscoIosSSH, 'disconnect', mock_connection_disco)

    nm_obj = QuickNetmiko('10.0.0.100', 'cisco_ios', 'temp', 'temp')

    with pytest.raises(TypeError):
        nm_obj.send_commands(1)
