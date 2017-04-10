#### Systemd

#### Usage

- start_unit(unit_name, mode="replace"), returns bool
- stop_unit(unit_name, mode="replace"), returns bool
- enable_unit(unit_name), returns bool
- disable_unit(unit_name), returns bool
- is_active(unit_name), returns bool

#### Example

```
from sysdmanager import SystemdManager

manager = SystemdManager()
print(manager.is_active("bluetooth.service"))
manager.start_unit("bluetooth.service")
```
