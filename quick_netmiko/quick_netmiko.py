"""
This is a simple class to get command from Cisco devices

"""
import ipaddress
import socket
from netmiko import ConnectHandler
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2020, Benjamin P. Trachtenberg"
__credits__ = None
__license__ = 'The MIT License (MIT)'
__status__ = 'prod'
__version_info__ = (1, 0, 1)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'


class FailedDnsLookup(Exception):
    """
    Exception for DNS Exceptions
    """

    def __init__(self, value):
        super().__init__(value)
        self.value = '{}'.format(value)

    def __str__(self):  # pragma: no cover
        return repr(self.value)


class QuickNetmiko:
    """
    Class to run commands and get output

    :type device_ip_name: String
    :param device_ip_name: The device name or ip address
    :type device_type: String
    :param device_type: One of the following {'cisco_nxos_ssh', 'cisco_ios', 'cisco_iosxr'}
    :type username: String
    :param username: The username to use
    :type password: String
    :param password: The password to use

    :rtype: None
    :returns: None

    :raises AttributeError: If device_types is not one of these {'cisco_nxos_ssh', 'cisco_ios', 'cisco_iosxr'}
    :raises FailedDnsLookup: If a hostname is not able to be looked up via DNS
    :raises FailedDnsLookup: If there is a timeout when looking up a hostname

    """

    def __init__(self, device_ip_name, device_type, username, password):
        device_types = {'cisco_nxos_ssh', 'cisco_ios', 'cisco_iosxr'}

        if device_type not in device_types:
            raise AttributeError('device_type must be one of the following {}'.format(device_types))

        try:
            self.device_ip = str(ipaddress.ip_address(device_ip_name))

        except ValueError:
            try:
                self.device_ip = socket.gethostbyname(device_ip_name)

            except socket.gaierror as e:
                raise FailedDnsLookup('DNS lookup failed while looking up {}'.format(device_ip_name)) from e

            except socket.timeout as e:
                raise FailedDnsLookup('DNS timed out while looking up {}'.format(device_ip_name)) from e

        self.device_type = device_type
        self.username = username
        self.password = password
        self.device_ip_name = device_ip_name

    def __str__(self):  # pragma: no cover
        return '{} device_name = {}'.format(type(self), self.device_ip_name)

    def __get_params(self):
        """
        Private method to get the Netmiko connection parameters

        :rtype: Dict
        :returns: A dictionary of connection params

        """
        params = {'device_type': self.device_type,
                  'host': self.device_ip,
                  'username': self.username,
                  'password': self.password}

        return params

    @staticmethod
    def __send_single_command(net_con, command):
        """
        Private method to send a command to a device and get the results

        :type net_con: <class 'netmiko.ConnectHandler'>
        :param net_con: The netmiko connection handler object
        :type command: String
        :param command: The command to get data for

        :rtype: String
        :returns: The results from the command

        """
        data = str()

        data += net_con.send_command(command)
        net_con.disconnect()

        return data

    def __send_list_of_commands(self, net_con, commands):
        """
        Private method to send a list of commands to a device and get the results

        :type net_con: <class 'netmiko.ConnectHandler'>
        :param net_con: The netmiko connection handler object
        :type commands: List
        :param commands: The list of commands to get data for

        :rtype: String
        :returns: The results from the command

        """
        data = str()
        for command in commands:
            data += self.__send_single_command(net_con, command)

        return data

    def send_commands(self, commands):
        """
        Method to send a list of commands or single command to a device and get the results

        :type commands: List or String
        :param commands: The list of commands or single command to get data for

        :rtype: String
        :returns: The results from the commands

        :raises TypeError: If commands is not a list or string

        """
        net_con = ConnectHandler(**self.__get_params())

        data = str()

        if isinstance(commands, list):
            data += self.__send_list_of_commands(net_con, commands)

        elif isinstance(commands, str):
            data += self.__send_single_command(net_con, commands)

        else:
            raise TypeError('commands must be a list, or a string but received a {}'.format(type(commands)))

        return data
