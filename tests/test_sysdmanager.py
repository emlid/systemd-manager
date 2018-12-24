import dbus
import pytest

from sysdmanager import SystemdManager


@pytest.fixture()
def exec_status_properties():
    props = {
        'ExecMainStatus': 255,
        'Result': 'failed'
    }
    return props


class TestSystemdManager:
    def setup_method(self):
        self.sysdmanager = SystemdManager()
        self.unit_name = "test_service.service"

    def test_start_unit(self):
        start_status = self.sysdmanager.start_unit(self.unit_name)
        assert start_status

        active = self.sysdmanager.is_active(self.unit_name)
        assert active

    def test_stop_unit(self):
        stop_status = self.sysdmanager.stop_unit(self.unit_name)
        assert stop_status

        active = self.sysdmanager.is_active(self.unit_name)
        assert not active

    def test_restart_unit(self):
        # Confirm that an active unit, when restarted, stays active
        start_status = self.sysdmanager.start_unit(self.unit_name)
        assert start_status

        restart_status = self.sysdmanager.restart_unit(self.unit_name)
        assert restart_status

        active = self.sysdmanager.is_active(self.unit_name)
        assert active

        # Confirm that an inactive unit, when restarted, becomes active
        stop_status = self.sysdmanager.stop_unit(self.unit_name)
        assert stop_status

        restart_status = self.sysdmanager.restart_unit(self.unit_name)
        assert restart_status

        active = self.sysdmanager.is_active(self.unit_name)
        assert active

    def test_enable_unit(self):
        enable_status = self.sysdmanager.enable_unit(self.unit_name)
        assert enable_status

        unit_file_state = self.sysdmanager._get_unit_file_state(self.unit_name)
        assert unit_file_state == 'enabled'

    def test_disable_unit(self):
        disable_status = self.sysdmanager.disable_unit(self.unit_name)
        assert disable_status

        unit_file_state = self.sysdmanager._get_unit_file_state(self.unit_name)
        assert unit_file_state == 'disabled'

    def test_get_interface(self):
        iface = self.sysdmanager._get_interface()
        assert isinstance(iface, dbus.Interface)

    def test_get_active_state(self):
        self.sysdmanager.start_unit(self.unit_name)
        state = self.sysdmanager._get_active_state(self.unit_name)
        assert state == 'active'

    def test_is_active(self):
        active_state = self.sysdmanager.is_active(self.unit_name)
        assert active_state

    def test_is_failed(self):
        failed_state = self.sysdmanager.is_failed(self.unit_name)
        assert failed_state == False

    def test_get_exec_status(self, exec_status_properties):
        exec_status = self.sysdmanager._get_exec_status(exec_status_properties)
        assert exec_status == {'failed': 255}

    def test_get_unit_properties(self):
        props = self.sysdmanager._get_unit_properties(self.unit_name,
                                                      self.sysdmanager.SERVICE_UNIT_INTERFACE)
        assert isinstance(props, dbus.Dictionary)
