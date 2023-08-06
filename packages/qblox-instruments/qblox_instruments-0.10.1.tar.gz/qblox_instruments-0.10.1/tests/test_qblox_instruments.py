# ----------------------------------------------------------------------------
# Description    : Qblox Instruments test script
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import pytest
import fastjsonschema

from datetime import datetime
from qblox_instruments import Pulsar
from qblox_instruments import DeviceInfo, BuildInfo, get_build_info, __version__
from qblox_instruments import InstrumentClass, InstrumentType, PulsarType, ClusterType
from qblox_instruments import SystemState, SystemStatus, SystemStatusFlags, SystemStatusSlotFlags
from qblox_instruments import SequencerState, SequencerStatus, SequencerStatusFlags


# -- fixtures ----------------------------------------------------------------

@pytest.fixture(name="pulsar_qcm")
def make_dummy_qcm():
    plsr = Pulsar("pulsar_qcm", dummy_type=PulsarType.PULSAR_QCM)
    yield plsr

    # Clean up when done
    plsr.close()


# -- functions ---------------------------------------------------------------

def test_device_info(pulsar_qcm):
    """
    Tests DeviceInfo object methods.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """

    # Create device info from dummy
    device_info = DeviceInfo.from_idn(pulsar_qcm._get_idn())

    # Check device info contents
    assert device_info.manufacturer == "qblox"
    assert device_info.model == "pulsar_qcm"
    assert device_info.serial == "whatever"

    assert "fw" in device_info
    assert "kmod" in device_info
    assert "sw" in device_info
    assert ("cfg_man" in device_info) is False

    # Replace build timestamps for conversion to unix timestamp to work.
    # The dummy timestamps are before 1970 and so will fail.
    timestamp = datetime.strptime("01/01/2000-00:00:00", "%d/%m/%Y-%H:%M:%S")
    device_info._fw_build._build = timestamp
    device_info._kmod_build._build = timestamp
    device_info.sw_build._build = timestamp

    # Get build info objects
    fw_build_info = device_info.fw_build
    assert fw_build_info is not None
    kmod_build_info = device_info.kmod_build
    assert kmod_build_info is not None
    sw_build_info = device_info.sw_build
    assert sw_build_info is not None
    cfg_man_build_info = device_info.cfg_man_build
    assert cfg_man_build_info is None

    # Check device info IDN string
    assert device_info.to_idn() == "{},{},{},{} {} {}".format(
        device_info.manufacturer,
        device_info.model,
        device_info.serial,
        sw_build_info.to_idn("sw"),
        fw_build_info.to_idn("fw"),
        kmod_build_info.to_idn("kmod"),
    )

    # Check device info IDN dict
    device_info_dict = {
        "manufacturer": device_info.manufacturer,
        "model": device_info.model,
        "ser": device_info.serial,
        "fw": fw_build_info.to_dict(),
        "kmod": kmod_build_info.to_dict(),
        "sw": sw_build_info.to_dict(),
    }
    assert device_info.to_dict() == device_info_dict
    assert device_info == DeviceInfo.from_dict(device_info_dict)

    # Check device info IDN tuple
    assert device_info.to_tuple() == (
        device_info.manufacturer,
        device_info.model,
        device_info.serial,
        sw_build_info.to_tuple(),
        fw_build_info.to_tuple(),
        kmod_build_info.to_tuple(),
        None,
    )


# ----------------------------------------------------------------------------
def test_build_info(pulsar_qcm):
    """
    Tests BuildInfo object methods.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """

    # Create device info from dummy
    build_info = DeviceInfo.from_idn(pulsar_qcm._get_idn()).fw_build

    # Replace build timestamp for conversion to unix timestamp to work.
    # The dummy timestamps are before 1970 and so will fail.
    timestamp = datetime.strptime("01/01/2000-00:00:00", "%d/%m/%Y-%H:%M:%S")
    build_info._build = timestamp

    # Check build info contents
    assert build_info.version == (0, 0, 0)
    assert build_info.build == timestamp
    assert build_info.build_iso == timestamp.isoformat()
    assert build_info.build_unix == timestamp.timestamp()
    assert build_info.hash == int("0xDEADBEAF", 16)
    assert build_info.hash_str == "DEADBEAF".lower()
    assert build_info.dirty is False
    assert build_info.dirty_str == "0"

    # Check build info IDN string
    assert (
        build_info.to_idn()
        == "Version={0} Build={1} Hash=0x{2:08X} Dirty={3}".format(
            build_info.version_str,
            build_info.build_str,
            build_info.hash,
            build_info.dirty_str,
        )
    )

    # Check build info dict
    build_info_dict = {
        "version": build_info.version,
        "build": build_info.build_unix,
        "hash": build_info.hash,
        "dirty": build_info.dirty,
    }
    assert build_info.to_dict() == build_info_dict
    assert build_info == BuildInfo.from_dict(build_info_dict)

    # Check build info tuple
    assert build_info.to_tuple() == (
        build_info.version,
        build_info.build_unix,
        build_info.hash,
        build_info.dirty,
    )


# ----------------------------------------------------------------------------
def test_get_build_info():
    """
    Tests get build info function and checks if the returned dictionary has the
    correct format. If not, the test fails.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """

    # Build info
    build_info = get_build_info()

    # Check build info
    build_info_schema = {
        "title": "Build information container.",
        "description": "Contains build information.",
        "required": ["version", "build", "hash", "dirty"],
        "properties": {
            "version": {
                "description": "Version string",
                "type": "string"
            },
            "build": {
                "description": "Build date",
                "type": "string"
            },
            "hash": {
                "description": "Git hash",
                "type": "string"
            },
            "dirty": {
                "description": "Git dirty indication",
                "type": "boolean"
            },
        },
    }

    validate_build_info = fastjsonschema.compile(build_info_schema)
    validate_build_info(build_info.to_idn_dict())


# ----------------------------------------------------------------------------
def test_version():
    """
    Test if __version__ matches version in the build information else fail.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """

    # Test version
    assert __version__ == get_build_info().version_str


# ----------------------------------------------------------------------------
def test_instrument_types():
    """
    Test instrument type string representations.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """

    assert repr(InstrumentClass.PULSAR) == "<InstrumentClass.PULSAR>"
    assert str(InstrumentClass.PULSAR) == "Pulsar"
    assert InstrumentClass.PULSAR == "Pulsar"
    assert not InstrumentClass.PULSAR != "Pulsar"
    assert list({InstrumentClass.PULSAR: ""}.keys()) == ["Pulsar"]

    assert repr(InstrumentType.QCM) == "<InstrumentType.QCM>"
    assert str(InstrumentType.QCM) == "QCM"
    assert InstrumentType.QCM == "QCM"
    assert not InstrumentType.QCM != "QCM"
    assert list({InstrumentType.QCM: ""}.keys()) == ["QCM"]

    assert repr(PulsarType.PULSAR_QCM) == "<PulsarType.PULSAR_QCM>"
    assert str(PulsarType.PULSAR_QCM) == "Pulsar QCM"
    assert PulsarType.PULSAR_QCM == "Pulsar QCM"
    assert not PulsarType.PULSAR_QCM != "Pulsar QCM"
    assert list({PulsarType.PULSAR_QCM: ""}.keys()) == ["Pulsar QCM"]

    assert repr(ClusterType.CLUSTER_QRM_RF) == "<ClusterType.CLUSTER_QRM_RF>"
    assert str(ClusterType.CLUSTER_QRM_RF) == "Cluster QRM-RF"
    assert ClusterType.CLUSTER_QRM_RF == "Cluster QRM-RF"
    assert not ClusterType.CLUSTER_QRM_RF != "Cluster QRM-RF"
    assert list({ClusterType.CLUSTER_QRM_RF: ""}.keys()) == ["Cluster QRM-RF"]


# ----------------------------------------------------------------------------
def test_system_state():
    """
    Test system state string representations.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """

    # Test system state string representations
    state = SystemState(
        SystemStatus.OKAY,
        [],
        SystemStatusSlotFlags()
    )
    assert repr(state) == "SystemState(status=<SystemStatus.OKAY>, flags=[], slot_flags=SystemStatusSlotFlags())"
    assert str(state) == "Status: OKAY, Flags: NONE, Slot flags: NONE"

    state = SystemState(
        SystemStatus.OKAY,
        [
            SystemStatusFlags.CARRIER_PLL_UNLOCKED,
            SystemStatusFlags.FPGA_PLL_UNLOCKED,
        ],
        SystemStatusSlotFlags({
            "slot1": [
                SystemStatusFlags.CARRIER_PLL_UNLOCKED,
                SystemStatusFlags.FPGA_PLL_UNLOCKED,
            ],
            "slot20": [
                SystemStatusFlags.CARRIER_PLL_UNLOCKED,
                SystemStatusFlags.FPGA_PLL_UNLOCKED
            ],
    }))
    assert repr(state) == (
        "SystemState(status=<SystemStatus.OKAY>, "
        "flags=[<SystemStatusFlags.CARRIER_PLL_UNLOCKED>, <SystemStatusFlags.FPGA_PLL_UNLOCKED>], "
        "slot_flags=SystemStatusSlotFlags("
        "slot1=[<SystemStatusFlags.CARRIER_PLL_UNLOCKED>, <SystemStatusFlags.FPGA_PLL_UNLOCKED>], "
        "slot20=[<SystemStatusFlags.CARRIER_PLL_UNLOCKED>, <SystemStatusFlags.FPGA_PLL_UNLOCKED>]))"
    )
    assert str(state) == (
        "Status: OKAY, "
        "Flags: CARRIER_PLL_UNLOCKED, FPGA_PLL_UNLOCKED, "
        "Slot flags: SLOT1_CARRIER_PLL_UNLOCKED, SLOT1_FPGA_PLL_UNLOCKED, "
        "SLOT20_CARRIER_PLL_UNLOCKED, SLOT20_FPGA_PLL_UNLOCKED"
    )

    assert SystemStatus.OKAY == "OKAY"
    assert not SystemStatus.OKAY != "OKAY"
    assert list({SystemStatus.OKAY: True}.keys()) == ["OKAY"]

    assert SystemStatusFlags.CARRIER_PLL_UNLOCKED == "CARRIER_PLL_UNLOCKED"
    assert not SystemStatusFlags.CARRIER_PLL_UNLOCKED != "CARRIER_PLL_UNLOCKED"
    assert list({SystemStatusFlags.CARRIER_PLL_UNLOCKED: ""}.keys()) == ["CARRIER_PLL_UNLOCKED"]


# ----------------------------------------------------------------------------
def test_sequencer_state():
    """
    Test sequencer state string representations.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """

    # Test sequencer state string representations
    state = SequencerState(SequencerStatus.IDLE, [])
    assert repr(state) == "SequencerState(status=<SequencerStatus.IDLE>, flags=[])"
    assert str(state) == "Status: IDLE, Flags: NONE"

    state = SequencerState(SequencerStatus.IDLE, [
        SequencerStatusFlags.FORCED_STOP,
        SequencerStatusFlags.ACQ_BINNING_DONE,
    ])
    assert repr(state) == (
        "SequencerState(status=<SequencerStatus.IDLE>, "
        "flags=[<SequencerStatusFlags.FORCED_STOP>, <SequencerStatusFlags.ACQ_BINNING_DONE>])"
    )
    assert str(state) == "Status: IDLE, Flags: FORCED_STOP, ACQ_BINNING_DONE"

    assert SequencerStatus.IDLE == "IDLE"
    assert not SequencerStatus.IDLE != "IDLE"
    assert list({SequencerStatus.IDLE: ""}.keys()) == ["IDLE"]

    assert SequencerStatusFlags.FORCED_STOP == "FORCED_STOP"
    assert not SequencerStatusFlags.FORCED_STOP != "FORCED_STOP"
    assert list({SequencerStatusFlags.FORCED_STOP: ""}.keys()) == ["FORCED_STOP"]
