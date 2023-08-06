# ----------------------------------------------------------------------------
# Description    : Cluster test script
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import pytest
import struct
from functools import partial

from tests import sequencer, qcm_qrm, instrument
from qblox_instruments import InstrumentClass, InstrumentType
from qblox_instruments import ClusterType
from qblox_instruments import Cluster
from qblox_instruments.qcodes_drivers.qcm_qrm import QcmQrm


# -- definitions -------------------------------------------------------------

DUMMY_CFG = {
    "1": ClusterType.CLUSTER_QCM,
    "3": ClusterType.CLUSTER_QCM,
    "4": ClusterType.CLUSTER_QCM_RF,
    "8": ClusterType.CLUSTER_QCM_RF,
    "10": ClusterType.CLUSTER_QRM,
    "15": ClusterType.CLUSTER_QRM,
    "16": ClusterType.CLUSTER_QRM_RF,
    "20": ClusterType.CLUSTER_QCM_RF,
}


def module(instrument: Cluster, dummy: ClusterType) -> QcmQrm:
    """
    Get dummy module index based on type.
    """

    for slot_idx in DUMMY_CFG:
        if DUMMY_CFG[slot_idx] == dummy:
            return instrument["module" + slot_idx]
    raise RuntimeError("Could not find dummy module ({}) in ".format(dummy) +
                       "dummy configuration.")


# -- fixtures ----------------------------------------------------------------

@pytest.fixture(name="cluster")
def make_dummy_cluster():
    clstr = Cluster("cluster", dummy_cfg=DUMMY_CFG)
    yield clstr

    # Clean up when done
    clstr.close()


# -- functions ---------------------------------------------------------------

def test_invalid_connection():
    """
    Test invalid connection scenarios.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """

    # Incompatible version with debug mode disabled.
    try:
        clstr = Cluster("cluster", debug=0, dummy_cfg={})
        clstr.close()
        raise AssertionError("Cluster instantiation should have failed.")
    except ConnectionError:
        pass

    # Connecting to non-CMM module.
    try:
        clstr = Cluster("cluster", dummy_cfg={"0": ClusterType.CLUSTER_QCM})
        clstr.close()
        raise AssertionError("Cluster instantiation should have failed.")
    except ConnectionError:
        pass


# ----------------------------------------------------------------------------
def test_type_specification(cluster):
    """
    Test type specification.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    assert cluster.instrument_class == InstrumentClass.CLUSTER
    assert cluster.instrument_type == InstrumentType.MM

    mod = module(cluster, ClusterType.CLUSTER_QCM)
    assert mod.module_type == InstrumentType.QCM
    assert mod.is_qcm_type is True
    assert mod.is_qrm_type is False
    assert mod.is_rf_type is False

    mod = module(cluster, ClusterType.CLUSTER_QRM)
    assert mod.module_type == InstrumentType.QRM
    assert mod.is_qcm_type is False
    assert mod.is_qrm_type is True
    assert mod.is_rf_type is False

    mod = module(cluster, ClusterType.CLUSTER_QCM_RF)
    assert mod.module_type == InstrumentType.QCM
    assert mod.is_qcm_type is True
    assert mod.is_qrm_type is False
    assert mod.is_rf_type is True

    mod = module(cluster, ClusterType.CLUSTER_QRM_RF)
    assert mod.module_type == InstrumentType.QRM
    assert mod.is_qcm_type is False
    assert mod.is_qrm_type is True
    assert mod.is_rf_type is True


# ----------------------------------------------------------------------------
def test_module_access(cluster):
    """
    Tests if modules can be accessed.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    assert len(cluster.modules) == 20
    for mod_idx, module in enumerate(cluster.modules):
        assert module.name == "{}_module{}".format(cluster.name, mod_idx + 1)
        assert module.name == cluster["module{}".format(mod_idx + 1)].name


# ----------------------------------------------------------------------------
def test_reset_cache_invalidation(cluster):
    """
    Tests if the call to reset also invalidates the caches on the qcodes
    parameters.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    instrument.test_reset_cache_invalidation(cluster)


# ----------------------------------------------------------------------------
def test_str(cluster):
    """
    Test string representation based in __str__

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    instrument.test_str(cluster, "Cluster", "cluster")


# ----------------------------------------------------------------------------
def test_get_scpi_commands(cluster):
    """
    Tests get SCPI commands function call. If no exceptions occur and the
    returned object matches the json schema the test passes.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    instrument.test_get_scpi_commands(cluster)


# ----------------------------------------------------------------------------
def test_get_idn(cluster):
    """
    Tests get IDN function call. If no exceptions occur and the returned
    object matches the json schema the test passes.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    instrument.test_get_idn(cluster)


# ----------------------------------------------------------------------------
def test_scpi_commands(cluster):
    """
    Tests remaining mandatory SCPI commands. If no exceptions occur the
    test passes.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    instrument.test_scpi_commands(cluster)


# ----------------------------------------------------------------------------
def test_get_system_state(cluster):
    """
    Tests get system state function call. If no exceptions occur the
    test passes.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    instrument.test_get_system_state(cluster)


# ----------------------------------------------------------------------------
def test_get_temp(cluster):
    """
    Tests temperature readout function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    instrument.test_get_temp(cluster)


# ----------------------------------------------------------------------------
def test_identify(cluster):
    """
    Tests test identify function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    instrument.test_identify(cluster)


# ----------------------------------------------------------------------------
def test_led_brightness(cluster):
    """
    Tests LED brightness setting and getting function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    instrument.test_led_brightness(cluster)


# ----------------------------------------------------------------------------
def test_ref_src(cluster):
    """
    Tests reference source setting and getting function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    instrument.test_ref_src(cluster)


# ----------------------------------------------------------------------------
def test_module_present(cluster):
    """
    Tests module present function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for slot_idx in range(1, 20):
        module = cluster.submodules["module{}".format(slot_idx)]
        assert module.present() == (str(slot_idx) in DUMMY_CFG)


# ----------------------------------------------------------------------------
def test_sequencer_access(cluster):
    """
    Tests if sequencers can be accessed.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in cluster.modules:
        if inst.present() == True:
            qcm_qrm.test_sequencer_access(inst)
        else:
            try:
                qcm_qrm.test_sequencer_access(inst)
                raise KeyError("Sequencers should not be accessible if "
                               "module is not present.")
            except AssertionError:
                pass


# ----------------------------------------------------------------------------
def test_lo_freq(cluster):
    """
    Tests LO frequency setting and getting function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM_RF),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst in modules:
        qcm_qrm.test_lo_freq(inst)

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QRM),
    ]
    for inst in modules:
        try:
            qcm_qrm.test_lo_freq(inst)
            raise AssertionError("LO parameters should not be "
                                 "available in baseband modules.")
        except KeyError:
            pass


# ----------------------------------------------------------------------------
def test_lo_enable(cluster):
    """
    Tests LO enable setting and getting function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM_RF),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst in modules:
        qcm_qrm.test_lo_enable(inst)

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QRM),
    ]
    for inst in modules:
        with pytest.raises(KeyError):
            qcm_qrm.test_lo_enable(inst)


# ----------------------------------------------------------------------------
def test_lo_pwr(cluster):
    """
    Tests LO power setting and getting function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QRM),
        module(cluster, ClusterType.CLUSTER_QCM_RF),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst in modules:
        qcm_qrm.test_lo_pwr(inst)


# ----------------------------------------------------------------------------
def test_in_amp_gain(cluster):
    """
    Tests input amplifier gain setting and getting function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    qcm_qrm.test_in_amp_gain(module(cluster, ClusterType.CLUSTER_QRM))

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QCM_RF),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst in modules:
        try:
            qcm_qrm.test_in_amp_gain(inst)
            raise AssertionError("Input amplifier parameters should "
                                 "only be available the baseband QRM.")
        except KeyError:
            pass


# ----------------------------------------------------------------------------
def test_out_amp_offset(cluster):
    """
    Tests output amplifier offset setting and getting function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM_RF),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst, num_out in zip(modules, [2, 1]):
        qcm_qrm.test_out_amp_offset(inst, num_out)

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QRM),
    ]
    for inst, num_out in zip(modules, [4, 2]):
        try:
            qcm_qrm.test_out_amp_offset(inst, num_out)
            raise AssertionError("Output amplifier offset parameters "
                                 "should only be available in RF "
                                 "modules.")
        except KeyError:
            pass


# ----------------------------------------------------------------------------
def test_out_dac_offset(cluster):
    """
    Tests output DAC offset setting and getting function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QRM),
    ]
    for inst, num_dac, max_offs in zip(modules, [4, 2], [2.5, 0.5]):
        qcm_qrm.test_out_dac_offset(inst, num_dac, max_offs)

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM_RF),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst, num_dac, max_offs in zip(modules, [4, 2], [2.5, 0.5]):
        try:
            qcm_qrm.test_out_dac_offset(inst, num_dac, max_offs)
            raise AssertionError("Output DAC offset parameters should "
                                 "only be available in baseband modules.")

        except KeyError:
            pass

# ----------------------------------------------------------------------------
def test_attenuation(cluster):
    """
    Tests attenuation setting and getting function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM_RF),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst, num_att, max_att in zip(modules, [0, 1], [30, 30]):
        qcm_qrm.test_attenuation(inst, True, num_att, max_att)
    for inst, num_att, max_att in zip(modules, [2, 1], [60, 60]):
        qcm_qrm.test_attenuation(inst, False, num_att, max_att)

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QRM),
    ]
    for inst, num_att, max_att in zip(modules, [2, 1], [60, 60]):
        with pytest.raises(KeyError):
            qcm_qrm.test_attenuation(inst, False, num_att, max_att)

    for inst, num_att, max_att in zip([modules[1]], [1], [30]):
        with pytest.raises(KeyError):
            qcm_qrm.test_attenuation(inst, True, num_att, max_att)


# ----------------------------------------------------------------------------
def test_scope_acquisition_control(cluster):
    """
    Tests scope acquisition control function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QRM),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst in modules:
        qcm_qrm.test_scope_acquisition_control(inst)

    modules =  [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QCM_RF),
    ]
    for inst in modules:
        try:
            qcm_qrm.test_scope_acquisition_control(inst)
            raise AssertionError("Acquisition functionality should "
                                 "only be supported by QRM modules.")
        except:
            pass


# ----------------------------------------------------------------------------
def test_channelmap(cluster):
    """
    Tests channel map setting and getting function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QRM),
        module(cluster, ClusterType.CLUSTER_QCM_RF),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst, num_dac in zip(modules, [4, 2, 4, 2]):
        for seq in inst.sequencers:
            sequencer.test_channelmap(seq, num_dac)


# ----------------------------------------------------------------------------
def test_waveform_weight_handling(cluster):
    """
    Tests waveform and weight handling (e.g. adding, deleting) function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture
    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QRM),
        module(cluster, ClusterType.CLUSTER_QCM_RF),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst in modules:
        for seq in inst.sequencers:
            sequencer.test_waveform_weight_handling(seq, "waveform")

    modules = [
        module(cluster, ClusterType.CLUSTER_QRM),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst in modules:
        for seq in inst.sequencers:
            sequencer.test_waveform_weight_handling(seq, "weight")

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QCM_RF),
    ]
    for inst in modules:
        for seq in inst.sequencers:
            try:
                sequencer.test_waveform_weight_handling(seq, "weight")
                raise AssertionError("Weight functionality should only be "
                                     "supported by QRM modules.")
            except NotImplementedError:
                pass

    # Test private methods
    waveform_length = 100
    waveforms = {
        "sawtooth": {
            "data": [(1.0 / (waveform_length)) * i for i in range(0, waveform_length)],
            "index": 2,
        }
    }
    sequence = {
        "waveforms": waveforms,
        "weights": waveforms,
        "acquisitions": {},
        "program": "stop",
    }
    mod = module(cluster, ClusterType.CLUSTER_QRM)
    mod.sequencer0.sequence(sequence)
    slot = mod.slot_idx

    for type in ["waveform", "weight"]:
        prefix = "awg" if type == "waveform" else "acq"
        get_wave_weight_data = getattr(
            cluster, "_get_{}_{}_data".format(prefix, type)
        )
        get_wave_weight_index = getattr(
            cluster, "_get_{}_{}_index".format(prefix, type)
        )
        get_wave_weight_length = getattr(
            cluster, "_get_{}_{}_length".format(prefix, type)
        )
        get_wave_weight_name = getattr(
            cluster, "_get_{}_{}_name".format(prefix, type)
        )
        get_num_wave_weights = getattr(
            cluster, "_get_{}_num_{}s".format(prefix, type)
        )

        waveform_name = "sawtooth"
        index = get_wave_weight_index(slot, 0, waveform_name)
        length = get_wave_weight_length(slot, 0, waveform_name)
        name = get_wave_weight_name(slot, 0, waveforms[waveform_name]["index"])
        num = get_num_wave_weights(slot, 0)
        data = get_wave_weight_data(slot, 0, waveform_name, 0, waveform_length)

        assert index == waveforms[waveform_name]["index"]
        assert length == waveform_length
        assert name == waveform_name
        assert num == len(waveforms)
        for sample0, sample1 in zip(waveforms[waveform_name]["data"], data):
            assert struct.unpack("f", struct.pack("f", sample0))[0] == sample1


# ----------------------------------------------------------------------------
def test_acquisition_handling(cluster):
    """
    Tests waveform handling (e.g. adding, deleting) function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QRM),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst in modules:
        for seq in inst.sequencers:
            sequencer.test_acquisition_handling(seq)

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QCM_RF),
    ]
    for inst in modules:
        for seq in inst.sequencers:
            try:
                sequencer.test_acquisition_handling(seq)
                raise AssertionError("Acquisition functionality should "
                                     "only be supported by QRM modules.")
            except NotImplementedError:
                pass

    # Test private methods
    sample_width = 12
    max_sample_value = 2 ** (sample_width - 1) - 1
    size = 2 ** 14
    scope_acq0 = struct.unpack(
        "i" * size,
        struct.pack(
            "i" * size,
            *[int(max_sample_value / size) * i for i in range(0, size)]
        ),
    )
    scope_acq1 = struct.unpack(
        "i" * size,
        struct.pack(
            "i" * size,
            *[max_sample_value - int(max_sample_value / size) * i for i in range(0, size)]
        ),
    )

    acquisitions = {"acq1": {"num_bins": 20, "index": 1}}
    sequence = {
        "waveforms": {},
        "weights": {},
        "acquisitions": acquisitions,
        "program": "stop",
    }
    mod = module(cluster, ClusterType.CLUSTER_QRM)
    slot = mod.slot_idx
    cluster.delete_dummy_binned_acquisition_data(slot)
    mod.sequencer0.sequence(sequence)
    mod.sequencer0.start_sequencer()

    acq_name = "acq1"
    index = cluster._get_acq_acquisition_index(slot, 0, acq_name)
    num_bins = cluster._get_acq_acquisition_num_bins(slot, 0, acq_name)
    name = cluster._get_acq_acquisition_name(slot, 0, acquisitions[acq_name]["index"])
    num_acq = cluster._get_acq_num_acquisitions(slot, 0)
    data = cluster._get_acq_acquisition_data(slot, 0, acq_name)

    assert index == acquisitions[acq_name]["index"]
    assert num_bins == 0
    assert name == acq_name
    assert num_acq == len(acquisitions)

    for sample0, sample1 in zip(scope_acq0, data["scope"]["path0"]["data"]):
        assert sample0 / max_sample_value == sample1
    for sample0, sample1 in zip(scope_acq1, data["scope"]["path1"]["data"]):
        assert sample0 / max_sample_value == sample1
    assert len(data["bins"]["integration"]["path0"]) == acquisitions[acq_name]["num_bins"]
    assert len(data["bins"]["integration"]["path1"]) == acquisitions[acq_name]["num_bins"]
    assert len(data["bins"]["threshold"]) == acquisitions[acq_name]["num_bins"]
    assert len(data["bins"]["avg_cnt"]) == acquisitions[acq_name]["num_bins"]


# ----------------------------------------------------------------------------
def test_program_handling(cluster, tmpdir):
    """
    Tests program handling function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture
    tmpdir
        Temporary directory

    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QRM),
        module(cluster, ClusterType.CLUSTER_QCM_RF),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst in modules:
        for seq in inst.sequencers:
            sequencer.test_program_handling(seq, tmpdir)


# ----------------------------------------------------------------------------
def test_sequencer_control(cluster):
    """
    Tests program handling function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QRM),
        module(cluster, ClusterType.CLUSTER_QCM_RF),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst in modules:
        for seq in inst.sequencers:
            sequencer.test_sequencer_control(seq, inst.is_qrm_type)


# ----------------------------------------------------------------------------
def test_dummy_binned_acquisition(cluster):
    """
    Tests dummy binned acquisition data mocking.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    qrm_module = module(cluster, ClusterType.CLUSTER_QRM)
    qrm_rf_module = module(cluster, ClusterType.CLUSTER_QRM_RF)

    def _set_dummy_fun_on_cluster(mod0, seq0, mod1, seq1):
        set_dummy_fun0 = partial(
                cluster.set_dummy_binned_acquisition_data,
                sequencer=seq0,
                slot_idx=mod0.slot_idx
        )
        set_dummy_fun1 = partial(
                cluster.set_dummy_binned_acquisition_data,
                sequencer=seq1,
                slot_idx=mod1.slot_idx
        )
        return set_dummy_fun0, set_dummy_fun1

    def _set_dummy_fun_on_module(mod0, seq0, mod1, seq1):
        module0 = getattr(cluster, f"module{mod0.slot_idx}")
        set_dummy_fun0 = partial(
                module0.set_dummy_binned_acquisition_data,
                sequencer=seq0
        )
        module1 = getattr(cluster, f"module{mod1.slot_idx}")
        set_dummy_fun1 = partial(
                module1.set_dummy_binned_acquisition_data,
                sequencer=seq1
        )
        return set_dummy_fun0, set_dummy_fun1

    def _set_dummy_fun_on_sequencer(mod0, seq0, mod1, seq1):
        module0 = getattr(cluster, f"module{mod0.slot_idx}")
        sequencer0 = getattr(module0, f"sequencer{seq0}")
        set_dummy_fun0 = sequencer0.set_dummy_binned_acquisition_data
        module1 = getattr(cluster, f"module{mod1.slot_idx}")
        sequencer1 = getattr(module1, f"sequencer{seq1}")
        set_dummy_fun1 = sequencer1.set_dummy_binned_acquisition_data
        return set_dummy_fun0, set_dummy_fun1


    for (mod0, seq0, mod1, seq1) in [(qrm_module, 2, qrm_rf_module, 3), (qrm_module, 3, qrm_rf_module, 2)]:
        # Testing multiple ways of setting the dummy data.
        set_dummy_fun0, set_dummy_fun1 = _set_dummy_fun_on_cluster(mod0, seq0, mod1, seq1)
        sequencer.test_dummy_binned_acquisition(seq0, seq1, mod0, mod1, set_dummy_fun0, set_dummy_fun1)

        set_dummy_fun0, set_dummy_fun1 = _set_dummy_fun_on_module(mod0, seq0, mod1, seq1)
        sequencer.test_dummy_binned_acquisition(seq0, seq1, mod0, mod1, set_dummy_fun0, set_dummy_fun1)

        set_dummy_fun0, set_dummy_fun1 = _set_dummy_fun_on_sequencer(mod0, seq0, mod1, seq1)
        sequencer.test_dummy_binned_acquisition(seq0, seq1, mod0, mod1, set_dummy_fun0, set_dummy_fun1)


# ----------------------------------------------------------------------------
def test_dummy_scope_acquisition(cluster):
    """
    Tests dummy scope acquisition data mocking.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    qrm_module = module(cluster, ClusterType.CLUSTER_QRM)
    qrm_rf_module = module(cluster, ClusterType.CLUSTER_QRM_RF)

    def _set_dummy_fun_on_cluster(mod, _):
        set_dummy_fun = partial(
                cluster.set_dummy_scope_acquisition_data,
                slot_idx=mod.slot_idx,
                sequencer=None
        )
        return set_dummy_fun

    def _set_dummy_fun_on_module(mod, _):
        module = getattr(cluster, f"module{mod.slot_idx}")
        set_dummy_fun = partial(
                module.set_dummy_scope_acquisition_data,
                sequencer=None
        )
        return set_dummy_fun

    def _set_dummy_fun_on_sequencer(mod, seq):
        module = getattr(cluster, f"module{mod.slot_idx}")
        sequencer = getattr(module, f"sequencer{seq}")
        set_dummy_fun = sequencer.set_dummy_scope_acquisition_data
        return set_dummy_fun

    for (mod, seq, test_dataset_index) in [(qrm_module, 0, 0), (qrm_rf_module, 1, 1)]:
        # Testing multiple ways of setting the dummy data.
        set_dummy_fun = _set_dummy_fun_on_cluster(mod, seq)
        sequencer.test_dummy_scope_acquisition(seq, mod, set_dummy_fun, test_dataset_index)

        set_dummy_fun = _set_dummy_fun_on_module(mod, seq)
        sequencer.test_dummy_scope_acquisition(seq, mod, set_dummy_fun, test_dataset_index)

        set_dummy_fun = _set_dummy_fun_on_sequencer(mod, seq)
        sequencer.test_dummy_scope_acquisition(seq, mod, set_dummy_fun, test_dataset_index)

# ----------------------------------------------------------------------------
def test_feedback(cluster):
    """
    Tests program handling function calls.

    Parameters
    ----------
    cluster: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    modules = [
        module(cluster, ClusterType.CLUSTER_QCM),
        module(cluster, ClusterType.CLUSTER_QRM),
        module(cluster, ClusterType.CLUSTER_QCM_RF),
        module(cluster, ClusterType.CLUSTER_QRM_RF),
    ]
    for inst in modules:
        for seq in inst.sequencers:
            sequencer.test_feedback_sequencer_param(seq, inst.is_qrm_type)
