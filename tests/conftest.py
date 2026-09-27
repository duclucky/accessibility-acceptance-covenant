from __future__ import annotations

import os
import tempfile


_WINDOWS_MESSAGE_FILES: list[str] = []


def _windows_inject_message_to_fd0(vm) -> None:
    """Compatibility guard for gltest 0.30.0rc2 on Windows.

    Windows cannot unlink the temporary message file while fd 0 still refers to
    it. Upstream unlinks immediately; retain it until pytest session teardown.
    """
    from gltest.direct.sdk_compat import import_address, import_calldata

    calldata = import_calldata()
    address_type = import_address()

    def address(value):
        return address_type(value) if isinstance(value, bytes) else value

    message_data = {
        "contract_address": address(vm._contract_address),
        "sender_address": address(vm.sender),
        "origin_address": address(vm.origin),
        "stack": [],
        "value": vm._value,
        "datetime": vm._datetime,
        "is_init": False,
        "chain_id": vm._chain_id,
        "entry_kind": 0,
        "entry_data": b"",
        "entry_stage_data": None,
    }
    encoded = calldata.encode(message_data)
    fd, path = tempfile.mkstemp(prefix="gltest-message-")
    os.write(fd, encoded)
    os.lseek(fd, 0, os.SEEK_SET)
    vm._original_stdin_fd = os.dup(0)
    os.dup2(fd, 0)
    os.close(fd)
    _WINDOWS_MESSAGE_FILES.append(path)


def pytest_configure(config) -> None:
    if os.name == "nt":
        import gltest.direct.loader as loader

        loader._inject_message_to_fd0 = _windows_inject_message_to_fd0


def pytest_sessionfinish(session, exitstatus) -> None:
    for path in _WINDOWS_MESSAGE_FILES:
        try:
            os.unlink(path)
        except OSError:
            pass
