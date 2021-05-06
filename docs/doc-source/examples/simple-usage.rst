Simple Usage
============

.. code-block:: python

   from quick_netmiko import QuickNetmiko

   command_obj = QuickNetmiko('10.0.0.100', 'cisco_ios', 'fake', 'fake-pass')

   out = command_obj.send_commands('show version')

   print(out)
