# This program is placed under the GPL license.
# Copyright (c) 2016, Emlid Limited
# All rights reserved.

# If you are interested in using this program as a part of a
# closed source project, please contact Emlid Limited (info@emlid.com).

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import dbus


class SystemdManager(object):

    def __init__(self):
        self.__bus = dbus.SystemBus()

    def start_unit(self, unit_name, mode="replace"):
        interface = self._get_interface()

        if interface is None:
            return False

        try:
            interface.StartUnit(unit_name, mode)
            return True
        except dbus.exceptions.DBusException as error:
            print(error)
            return False

    def stop_unit(self, unit_name, mode="replace"):
        interface = self._get_interface()

        if interface is None:
            return False

        try:
            interface.StopUnit(unit_name, mode)
            return True
        except dbus.exceptions.DBusException as error:
            print(error)
            return False

    def enable_unit(self, unit_name):
        interface = self._get_interface()

        if interface is None:
            return False

        try:
            interface.EnableUnitFiles([unit_name], 
                dbus.Boolean(False), dbus.Boolean(True))
            return True
        except dbus.exceptions.DBusException as error:
            print(error)
            return False

    def disable_unit(self, unit_name):
        interface = self._get_interface()

        if interface is None:
            return False

        try:
            interface.DisableUnitFiles([unit_name], 
                dbus.Boolean(False))
            return True
        except dbus.exceptions.DBusException as error:
            print(error)
            return False

    def _get_interface(self):
        try:
            obj = self.__bus.get_object("org.freedesktop.systemd1",
                "/org/freedesktop/systemd1")
            return dbus.Interface(obj,
                "org.freedesktop.systemd1.Manager")
        except dbus.exceptions.DBusException as error:
            print(error)
            return None

    def is_active(self, unit_name):
        properties = self._get_unit_properties(unit_name)

        if properties is None:
            return False

        try:
            return "active" ==\
                properties["ActiveState"].encode("utf-8")
        except KeyError:
            return False

    def _get_unit_properties(self, unit_name):
        interface = self._get_interface()

        if interface is None:
            return None

        try:
            unit_path = interface.LoadUnit(unit_name)

            obj = self.__bus.get_object(
                "org.freedesktop.systemd1", unit_path)

            properties_interface = dbus.Interface(
                obj, "org.freedesktop.DBus.Properties")

            return properties_interface.GetAll(
                "org.freedesktop.systemd1.Unit")
        except dbus.exceptions.DBusException as error:
            print(error)
            return None



if __name__ == "__main__":

    unit_name = "bluetooth.service"
    manager = SystemdManager()

    print("stop: " + str(manager.stop_unit(unit_name)))
    print("is active: " + str(manager.is_active(unit_name)))

    print("start: " + str(manager.start_unit(unit_name)))
    print("is active: " + str(manager.is_active(unit_name)))

    print("enable: " + str(manager.enable_unit(unit_name)))
    #print("disable: " + str(manager.disable_unit(unit_name)))

