# ----------------------------------------------------------------------------
# Description    : Pulsar test script
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import pytest
import struct
from functools import partial

from tests import sequencer, qcm_qrm, instrument
from qblox_instruments import InstrumentClass, InstrumentType
from qblox_instruments import PulsarType, ClusterType
from qblox_instruments import Pulsar
from qblox_instruments import DummyBinnedAcquisitionData

# -- fixtures ----------------------------------------------------------------


@pytest.fixture(name="pulsar_qcm")
def make_dummy_qcm():
    plsr = Pulsar("pulsar_qcm", dummy_type=PulsarType.PULSAR_QCM)
    yield plsr

    # Clean up when done
    plsr.close()


@pytest.fixture(name="pulsar_qcm_rf")
def make_dummy_qcm_rf():
    plsr = Pulsar("pulsar_qcm_rf", dummy_type=PulsarType._PULSAR_QCM_RF)
    yield plsr

    # Clean up when done
    plsr.close()


@pytest.fixture(name="pulsar_qrm")
def make_dummy_qrm():
    plsr = Pulsar("pulsar_qrm", dummy_type=PulsarType.PULSAR_QRM)
    yield plsr

    # Clean up when done
    plsr.close()


@pytest.fixture(name="pulsar_qrm_rf")
def make_dummy_qrm_rf():
    plsr = Pulsar("pulsar_qrm_rf", dummy_type=PulsarType._PULSAR_QRM_RF)
    yield plsr

    # Clean up when done
    plsr.close()


# -- functions -----------------------------------------------------------------


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
    def test_incompatible_version(dummy_type: PulsarType):
        try:
            plsr = Pulsar("pulsar", debug=0, dummy_type=dummy_type)
            plsr.close()
            raise AssertionError("Pulsar instantiation should have failed.")
        except ConnectionError:
            pass

    test_incompatible_version(PulsarType.PULSAR_QCM)
    test_incompatible_version(PulsarType.PULSAR_QRM)

    # Connecting to non-QCM/QRM module.
    try:
        plsr = Pulsar("pulsar", dummy_type=ClusterType._CLUSTER_MM)
        plsr.close()
        raise AssertionError("Pulsar instantiation should have failed.")
    except ConnectionError:
        pass


# ----------------------------------------------------------------------------
def test_type_specification(pulsar_qcm,
                            pulsar_qrm,
                            pulsar_qcm_rf,
                            pulsar_qrm_rf):
    """
    Test type specification.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    assert pulsar_qcm.instrument_class == InstrumentClass.PULSAR
    assert pulsar_qcm.instrument_type == InstrumentType.QCM
    assert pulsar_qcm.is_qcm_type is True
    assert pulsar_qcm.is_qrm_type is False
    assert pulsar_qcm.is_rf_type is False

    assert pulsar_qrm.instrument_class == InstrumentClass.PULSAR
    assert pulsar_qrm.instrument_type == InstrumentType.QRM
    assert pulsar_qrm.is_qcm_type is False
    assert pulsar_qrm.is_qrm_type is True
    assert pulsar_qrm.is_rf_type is False

    assert pulsar_qcm_rf.instrument_class == InstrumentClass.PULSAR
    assert pulsar_qcm_rf.instrument_type == InstrumentType.QCM
    assert pulsar_qcm_rf.is_qcm_type is True
    assert pulsar_qcm_rf.is_qrm_type is False
    assert pulsar_qcm_rf.is_rf_type is True

    assert pulsar_qrm_rf.instrument_class == InstrumentClass.PULSAR
    assert pulsar_qrm_rf.instrument_type == InstrumentType.QRM
    assert pulsar_qrm_rf.is_qcm_type is False
    assert pulsar_qrm_rf.is_qrm_type is True
    assert pulsar_qrm_rf.is_rf_type is True


# ----------------------------------------------------------------------------
def test_reset_cache_invalidation(pulsar_qcm,
                                  pulsar_qrm,
                                  pulsar_qcm_rf,
                                  pulsar_qrm_rf):
    """
    Tests if the call to reset also invalidates the caches on the qcodes parameters.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        instrument.test_reset_cache_invalidation(inst)


# ----------------------------------------------------------------------------
def test_str(pulsar_qcm,
             pulsar_qrm,
             pulsar_qcm_rf,
             pulsar_qrm_rf):
    """
    Test string representation based in __str__

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst, name in zip(
        [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf],
        ["pulsar_qcm", "pulsar_qrm", "pulsar_qcm_rf", "pulsar_qrm_rf"],
    ):
        instrument.test_str(inst, "Pulsar", name)


# ----------------------------------------------------------------------------
def test_get_scpi_commands(pulsar_qcm,
                           pulsar_qrm,
                           pulsar_qcm_rf,
                           pulsar_qrm_rf):
    """
    Tests get SCPI commands function call. If no exceptions occur and the returned object matches
    the json schema the test passes.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        instrument.test_get_scpi_commands(inst)


# ----------------------------------------------------------------------------
def test_get_idn(pulsar_qcm,
                 pulsar_qrm,
                 pulsar_qcm_rf,
                 pulsar_qrm_rf):
    """
    Tests get IDN function call. If no exceptions occur and the returned object matches
    the json schema the test passes.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        instrument.test_get_idn(inst)


# ----------------------------------------------------------------------------
def test_scpi_commands(pulsar_qcm,
                       pulsar_qrm,
                       pulsar_qcm_rf,
                       pulsar_qrm_rf):
    """
    Tests remaining mandatory SCPI commands. If no exceptions occur the test passes.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        instrument.test_scpi_commands(inst)


# ----------------------------------------------------------------------------
def test_get_system_state(pulsar_qcm,
                          pulsar_qrm,
                          pulsar_qcm_rf,
                          pulsar_qrm_rf):
    """
    Tests get system state function call. If no exceptions occur the test passes.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        instrument.test_get_system_state(inst)


# ----------------------------------------------------------------------------
def test_get_temp(pulsar_qcm,
                  pulsar_qrm,
                  pulsar_qcm_rf,
                  pulsar_qrm_rf):
    """
    Tests temperature readout function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        instrument.test_get_temp(inst)


# ----------------------------------------------------------------------------
def test_identify(pulsar_qcm,
                  pulsar_qrm,
                  pulsar_qcm_rf,
                  pulsar_qrm_rf):
    """
    Tests test identify function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        instrument.test_identify(inst)


# ----------------------------------------------------------------------------
def test_led_brightness(pulsar_qcm,
                  pulsar_qrm,
                  pulsar_qcm_rf,
                  pulsar_qrm_rf):
    """
    Tests LED brightness setting and getting function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        instrument.test_led_brightness(inst)


# ----------------------------------------------------------------------------
def test_ref_src(pulsar_qcm,
                 pulsar_qrm,
                 pulsar_qcm_rf,
                 pulsar_qrm_rf):
    """
    Tests reference source setting and getting function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        instrument.test_ref_src(inst)


# ----------------------------------------------------------------------------
def test_sequencer_access(pulsar_qcm,
                          pulsar_qrm,
                          pulsar_qcm_rf,
                          pulsar_qrm_rf):
    """
    Tests if sequencers can be accessed.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        qcm_qrm.test_sequencer_access(inst)


# ----------------------------------------------------------------------------
def test_lo_freq(pulsar_qcm,
                 pulsar_qrm,
                 pulsar_qcm_rf,
                 pulsar_qrm_rf):
    """
    Tests LO frequency setting and getting function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm_rf, pulsar_qrm_rf]:
        qcm_qrm.test_lo_freq(inst)

    for inst in [pulsar_qcm, pulsar_qrm]:
        try:
            qcm_qrm.test_lo_freq(inst)
            raise AssertionError("LO parameters should not be available "
                                 "in baseband modules.")
        except KeyError:
            pass


# ----------------------------------------------------------------------------
def test_lo_enable(pulsar_qcm,
                     pulsar_qrm,
                     pulsar_qcm_rf,
                     pulsar_qrm_rf):
    """
    Tests LO enable setting and getting function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm_rf, pulsar_qrm_rf]:
        qcm_qrm.test_lo_enable(inst)

    for inst in [pulsar_qcm, pulsar_qrm]:
        with pytest.raises(KeyError):
            qcm_qrm.test_lo_enable(inst)


# ----------------------------------------------------------------------------
def test_lo_pwr(pulsar_qcm,
                pulsar_qrm,
                pulsar_qcm_rf,
                pulsar_qrm_rf):
    """
    Tests LO power setting and getting function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        qcm_qrm.test_lo_pwr(inst)


# ----------------------------------------------------------------------------
def test_in_amp_gain(pulsar_qcm,
                     pulsar_qrm,
                     pulsar_qcm_rf,
                     pulsar_qrm_rf):
    """
    Tests input amplifier gain setting and getting function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    qcm_qrm.test_in_amp_gain(pulsar_qrm)

    for inst in [pulsar_qcm, pulsar_qcm_rf, pulsar_qrm_rf]:
        try:
            qcm_qrm.test_in_amp_gain(inst)
            raise AssertionError("Input amplifier parameters should only "
                                 "be available the baseband QRM.")
        except KeyError:
            pass


# ----------------------------------------------------------------------------
def test_out_amp_offset(pulsar_qcm,
                        pulsar_qrm,
                        pulsar_qcm_rf,
                        pulsar_qrm_rf):
    """
    Tests output amplifier offset setting and getting function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst, num_out in zip([pulsar_qcm_rf, pulsar_qrm_rf], [2, 1]):
        qcm_qrm.test_out_amp_offset(inst, num_out)

    for inst, num_out in zip([pulsar_qcm, pulsar_qrm], [4, 2]):
        try:
            qcm_qrm.test_out_amp_offset(inst, num_out)
            raise AssertionError("Output amplifier offset parameters "
                                 "should only be available in RF modules.")
        except KeyError:
            pass


# ----------------------------------------------------------------------------
def test_out_dac_offset(pulsar_qcm,
                        pulsar_qrm,
                        pulsar_qcm_rf,
                        pulsar_qrm_rf):
    """
    Tests output DAC offset setting and getting function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst, num_dac, max_offs in zip(
        [pulsar_qcm, pulsar_qrm],
        [4, 2],
        [2.5, 0.5]
    ):
        qcm_qrm.test_out_dac_offset(inst, num_dac, max_offs)

    for inst, num_dac, max_offs in zip(
        [pulsar_qcm_rf, pulsar_qrm_rf],
        [4, 2],
        [2.5, 0.5]
    ):
        try:
            qcm_qrm.test_out_dac_offset(inst, num_dac, max_offs)
            raise AssertionError("Output DAC offset parameters should "
                                 "only be available in baseband modules.")
        except KeyError:
            pass

# ----------------------------------------------------------------------------
def test_attenuation(pulsar_qcm,
                     pulsar_qrm,
                     pulsar_qcm_rf,
                     pulsar_qrm_rf):
    """
    Tests attenuation setting and getting function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst, num_att, max_att in zip([pulsar_qcm_rf, pulsar_qrm_rf], [0, 1], [30, 30]):
        qcm_qrm.test_attenuation(inst, True, num_att, max_att)
    for inst, num_att, max_att in zip([pulsar_qcm_rf, pulsar_qrm_rf], [2, 1], [60, 60]):
        qcm_qrm.test_attenuation(inst, False, num_att, max_att)

    for inst, num_att, max_att in zip([pulsar_qcm, pulsar_qrm], [2, 1], [60, 60]):
        with pytest.raises(KeyError):
            qcm_qrm.test_attenuation(inst, False, num_att, max_att)

    for inst, num_att, max_att in zip([pulsar_qrm], [1], [30]):
        with pytest.raises(KeyError):
            qcm_qrm.test_attenuation(inst, True, num_att, max_att)


# ----------------------------------------------------------------------------
def test_scope_acquisition_control(pulsar_qcm,
                                   pulsar_qrm,
                                   pulsar_qcm_rf,
                                   pulsar_qrm_rf):
    """
    Tests scope acquisition control function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qrm, pulsar_qrm_rf]:
        qcm_qrm.test_scope_acquisition_control(inst)

    for inst in [pulsar_qcm, pulsar_qcm_rf]:
        try:
            qcm_qrm.test_scope_acquisition_control(inst)
            raise AssertionError("Acquisition functionality should only "
                                 "be supported by QRM modules.")
        except:
            pass


# ----------------------------------------------------------------------------
def test_channelmap(pulsar_qcm,
                    pulsar_qrm,
                    pulsar_qcm_rf,
                    pulsar_qrm_rf):
    """
    Tests channel map setting and getting function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst, num_dac in zip(
        [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf],
        [4, 2, 4, 2]
    ):
        for seq in inst.sequencers:
            sequencer.test_channelmap(seq, num_dac)


# ----------------------------------------------------------------------------
def test_waveform_weight_handling(pulsar_qcm,
                                  pulsar_qrm,
                                  pulsar_qcm_rf,
                                  pulsar_qrm_rf):
    """
    Tests waveform and weight handling (e.g. adding, deleting) function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        for seq in inst.sequencers:
            sequencer.test_waveform_weight_handling(seq, "waveform")

    for inst in [pulsar_qrm, pulsar_qrm_rf]:
        for seq in inst.sequencers:
            sequencer.test_waveform_weight_handling(seq, "weight")

    for inst in [pulsar_qcm, pulsar_qcm_rf]:
        for seq in inst.sequencers:
            try:
                sequencer.test_waveform_weight_handling(seq, "weight")
                raise AssertionError("Weight functionality should only "
                                     "be supported by QRM modules.")
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

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        inst.sequencer0.sequence(sequence)

        for type in ["waveform", "weight"]:
            if type == "waveform" or (type == "weight" and inst.is_qrm_type):
                prefix = "awg" if type == "waveform" else "acq"
                get_wave_weight_data = getattr(
                    inst, "_get_{}_{}_data".format(prefix, type)
                )
                get_wave_weight_index = getattr(
                    inst, "_get_{}_{}_index".format(prefix, type)
                )
                get_wave_weight_length = getattr(
                    inst, "_get_{}_{}_length".format(prefix, type)
                )
                get_wave_weight_name = getattr(
                    inst, "_get_{}_{}_name".format(prefix, type)
                )
                get_num_wave_weights = getattr(
                    inst, "_get_{}_num_{}s".format(prefix, type)
                )

                waveform_name = "sawtooth"
                index = get_wave_weight_index(0, waveform_name)
                length = get_wave_weight_length(0, waveform_name)
                name = get_wave_weight_name(0, waveforms[waveform_name]["index"])
                num = get_num_wave_weights(0)
                data = get_wave_weight_data(0, waveform_name, 0, waveform_length)

                assert index == waveforms[waveform_name]["index"]
                assert length == waveform_length
                assert name == waveform_name
                assert num == len(waveforms)
                for sample0, sample1 in zip(waveforms[waveform_name]["data"], data):
                    assert struct.unpack("f", struct.pack("f", sample0))[0] == sample1


# ----------------------------------------------------------------------------
def test_acquisition_handling(pulsar_qcm,
                              pulsar_qrm,
                              pulsar_qcm_rf,
                              pulsar_qrm_rf):
    """
    Tests waveform handling (e.g. adding, deleting) function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qrm, pulsar_qrm_rf]:
        for seq in inst.sequencers:
            sequencer.test_acquisition_handling(seq)

    for inst in [pulsar_qcm, pulsar_qcm_rf]:
        for seq in inst.sequencers:
            try:
                sequencer.test_acquisition_handling(seq)
                raise AssertionError("Acquisition functionality should only "
                                     "be supported by QRM modules.")
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

    for inst in [pulsar_qrm, pulsar_qrm_rf]:
        inst.sequencer0.sequence(sequence)
        inst.sequencer0.start_sequencer()

        acq_name = "acq1"
        index = inst._get_acq_acquisition_index(0, acq_name)
        num_bins = inst._get_acq_acquisition_num_bins(0, acq_name)
        name = inst._get_acq_acquisition_name(0, acquisitions[acq_name]["index"])
        num_acq = inst._get_acq_num_acquisitions(0)
        data = inst._get_acq_acquisition_data(0, acq_name)

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
def test_program_handling(pulsar_qcm,
                          pulsar_qrm,
                          pulsar_qcm_rf,
                          pulsar_qrm_rf,
                          tmpdir):
    """
    Tests program handling function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture
    tmpdir
        Temporary directory

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        for seq in inst.sequencers:
            sequencer.test_program_handling(seq, tmpdir)


# ----------------------------------------------------------------------------
def test_sequencer_control(pulsar_qcm,
                           pulsar_qrm,
                           pulsar_qcm_rf,
                           pulsar_qrm_rf):
    """
    Tests program handling function calls.

    Parameters
    ----------
    pulsar_qcm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qcm_rf: test_fixture
        Dummy RF Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        for seq in inst.sequencers:
            sequencer.test_sequencer_control(seq, inst.is_qrm_type)


# ----------------------------------------------------------------------------
def test_dummy_binned_acquisition(pulsar_qrm, pulsar_qrm_rf):
    """
    Tests dummy binned acquisition data mocking.

    Parameters
    ----------
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    def _set_dummy_fun_on_pulsar(inst, seq0, seq1):
        set_dummy_fun0 = partial(
                inst.set_dummy_binned_acquisition_data,
                sequencer=seq0
        )
        set_dummy_fun1 = partial(
                inst.set_dummy_binned_acquisition_data,
                sequencer=seq1
        )
        return set_dummy_fun0, set_dummy_fun1

    def _set_dummy_fun_on_sequencer(inst, seq0, seq1):
        sequencer0 = getattr(inst, f"sequencer{seq0}")
        set_dummy_fun0 = sequencer0.set_dummy_binned_acquisition_data
        sequencer1 = getattr(inst, f"sequencer{seq1}")
        set_dummy_fun1 = sequencer1.set_dummy_binned_acquisition_data
        return set_dummy_fun0, set_dummy_fun1

    for inst in [pulsar_qrm, pulsar_qrm_rf]:
        for (seq0, seq1) in [(0, 1), (1, 0)]:
            # Testing multiple ways of setting the dummy data.
            set_dummy_fun0, set_dummy_fun1 = _set_dummy_fun_on_pulsar(inst, seq0, seq1)
            sequencer.test_dummy_binned_acquisition(seq0, seq1, inst, inst, set_dummy_fun0, set_dummy_fun1)

            set_dummy_fun0, set_dummy_fun1 = _set_dummy_fun_on_sequencer(inst, seq0, seq1)
            sequencer.test_dummy_binned_acquisition(seq0, seq1, inst, inst, set_dummy_fun0, set_dummy_fun1)

# ----------------------------------------------------------------------------
def test_dummy_scope_acquisition(pulsar_qrm, pulsar_qrm_rf):
    """
    Tests dummy scope acquisition data mocking.

    Parameters
    ----------
    pulsar_qrm: test_fixture
        Dummy Pulsar test fixture
    pulsar_qrm_rf: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    def _set_dummy_fun_on_pulsar(inst, _):
        set_dummy_fun = partial(
                inst.set_dummy_scope_acquisition_data,
                sequencer=None
        )
        return set_dummy_fun

    def _set_dummy_fun_on_sequencer(inst, seq):
        sequencer = getattr(inst, f"sequencer{seq}")
        set_dummy_fun = sequencer.set_dummy_scope_acquisition_data
        return set_dummy_fun

    for inst in [pulsar_qrm, pulsar_qrm_rf]:
        for (seq, test_dataset_index) in [(0, 0), (1, 1)]:
            # Testing multiple ways of setting the dummy data.

            set_dummy_fun = _set_dummy_fun_on_pulsar(inst, seq)
            sequencer.test_dummy_scope_acquisition(seq, inst, set_dummy_fun, test_dataset_index)

            set_dummy_fun = _set_dummy_fun_on_sequencer(inst, seq)
            sequencer.test_dummy_scope_acquisition(seq, inst, set_dummy_fun, test_dataset_index)

# ----------------------------------------------------------------------------
def test_feedback(pulsar_qcm,
                       pulsar_qrm,
                       pulsar_qcm_rf,
                       pulsar_qrm_rf):
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

    for inst in [pulsar_qcm, pulsar_qrm, pulsar_qcm_rf, pulsar_qrm_rf]:
        for seq in inst.sequencers:
            sequencer.test_feedback_sequencer_param(seq, inst.is_qrm_type)
