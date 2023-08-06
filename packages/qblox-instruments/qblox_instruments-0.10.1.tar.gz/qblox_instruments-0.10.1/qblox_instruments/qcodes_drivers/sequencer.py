# ----------------------------------------------------------------------------
# Description    : Sequencer QCoDeS interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

from typing import List, Union, Tuple, NoReturn
from functools import partial
from qcodes import validators as vals
from qcodes import Instrument, InstrumentChannel


# -- class -------------------------------------------------------------------

class Sequencer(InstrumentChannel):
    """
    This class represents a single sequencer. It combines all sequencer
    specific parameters and functions into a single QCoDes InstrumentChannel.
    """

    # ------------------------------------------------------------------------
    def __init__(
        self,
        parent: Union[Instrument, InstrumentChannel],
        name: str,
        seq_idx: int,
    ):
        """
        Creates a sequencer class and adds all relevant parameters for the
        sequencer.

        Parameters
        ----------
        parent : Union[Instrument, InstrumentChannel]
            The QCoDeS class to which this sequencer belongs.
        name : str
            Name of this sequencer channel
        seq_idx : int
            The index of this sequencer in the parent instrument, representing
            which sequencer is controlled by this class.

        Returns
        ----------

        Raises
        ----------
        """

        # Initialize instrument channel
        super().__init__(parent, name)

        # Store sequencer index
        self._seq_idx = seq_idx

        # Add required parent attributes for the QCoDeS parameters to function
        for attr_name in Sequencer._get_required_parent_attr_names():
            self._register(attr_name)

        # Add parameters
        # -- Channel map (All modules) ---------------------------------------
        self.add_parameter(
            "channel_map_path0_out0_en",
            label="Sequencer path 0 output 0 enable",
            docstring="Sets/gets sequencer channel map enable of path 0 to "
                      "output 0.",
            unit="",
            vals=vals.Bool(),
            set_parser=bool,
            get_parser=bool,
            set_cmd=partial(self._set_sequencer_channel_map, 0),
            get_cmd=partial(self._get_sequencer_channel_map, 0),
        )

        self.add_parameter(
            "channel_map_path1_out1_en",
            label="Sequencer path 1 output 1 enable",
            docstring="Sets/gets sequencer channel map enable of path 1 to "
                      "output 1.",
            unit="",
            vals=vals.Bool(),
            set_parser=bool,
            get_parser=bool,
            set_cmd=partial(self._set_sequencer_channel_map, 1),
            get_cmd=partial(self._get_sequencer_channel_map, 1),
        )

        if self.parent.is_qcm_type:
            self.add_parameter(
                "channel_map_path0_out2_en",
                label="Sequencer path 0 output 2 enable.",
                docstring="Sets/gets sequencer channel map enable of path 0 "
                          "to output 2.",
                unit="",
                vals=vals.Bool(),
                set_parser=bool,
                get_parser=bool,
                set_cmd=partial(self._set_sequencer_channel_map, 2),
                get_cmd=partial(self._get_sequencer_channel_map, 2),
            )

            self.add_parameter(
                "channel_map_path1_out3_en",
                label="Sequencer path 1 output 3 enable.",
                docstring="Sets/gets sequencer channel map enable of path 1 "
                          "to output 3.",
                unit="",
                vals=vals.Bool(),
                set_parser=bool,
                get_parser=bool,
                set_cmd=partial(self._set_sequencer_channel_map, 3),
                get_cmd=partial(self._get_sequencer_channel_map, 3),
            )

        # -- Sequencer (All modules) -----------------------------------------
        self.add_parameter(
            "sync_en",
            label="Sequencer synchronization enable",
            docstring="Sets/gets sequencer synchronization enable which "
                      "enables party-line synchronization.",
            unit="",
            vals=vals.Bool(),
            set_parser=bool,
            get_parser=bool,
            set_cmd=partial(
                self._set_sequencer_config_val,
                ["seq_proc","sync_en"]
            ),
            get_cmd=partial(
                self._get_sequencer_config_val,
                ["seq_proc","sync_en"]
            ),
        )

        self.add_parameter(
            "nco_freq",
            label="Sequencer NCO frequency",
            docstring="Sets/gets sequencer NCO frequency in Hz with a "
                    "resolution of 0.25 Hz. Be aware that the outputs "
                    "have low-pass filters with a cut-off frequency of "
                    "{} MHz".format("300" if self.parent.is_rf_type else "350"),
            unit="Hz",
            vals=vals.Numbers(-500e6, 500e6),
            set_parser=float,
            get_parser=float,
            set_cmd=partial(
                self._set_sequencer_config_val,
                ["awg", "nco", "freq_hz"]
            ),
            get_cmd=partial(
                self._get_sequencer_config_val,
                ["awg", "nco", "freq_hz"]
            ),
        )

        self.add_parameter(
            "nco_phase_offs",
            label="Sequencer NCO phase offset",
            docstring="Sets/gets sequencer NCO phase offset in degrees with "
                      "a resolution of 3.6e-7 degrees.",
            unit="Degrees",
            vals=vals.Numbers(0, 360),
            set_parser=float,
            get_parser=float,
            set_cmd=partial(
                self._set_sequencer_config_val,
                ["awg", "nco", "po"]
            ),
            get_cmd=partial(
                self._get_sequencer_config_val,
                ["awg", "nco", "po"]
            ),
        )

        self.add_parameter(
            "nco_prop_delay_comp",
            label="Sequencer NCO propagation delay compensation",
            docstring="Sets/gets a delay that compensates the NCO phase "
                        "to the input path with respect to the instrument's "
                        "combined output and input propagation delay. This "
                        "delay is applied on top of a default delay of 146 ns.",
            unit="ns",
            vals=vals.Numbers(-50, 50),
            set_parser=int,
            get_parser=int,
            set_cmd=partial(
                self._set_sequencer_config_val,
                ["awg", "nco", "delay_comp"]
            ),
            get_cmd=partial(
                self._get_sequencer_config_val,
                ["awg", "nco", "delay_comp"]
            ),
        )

        self.add_parameter(
            "nco_prop_delay_comp_en",
            label="Sequencer NCO propagation delay compensation enable",
            docstring="Sets/gets the enable for a delay that compensates "
                        "the NCO phase to the input path with respect to the "
                        "instrument's combined output and input propagation "
                        "delay. This delays the frequency update as well.",
            unit="ns",
            vals=vals.Bool(),
            set_parser=bool,
            get_parser=bool,
            set_cmd=partial(
                self._set_sequencer_config_val,
                ["awg", "nco", "delay_comp_en"]
            ),
            get_cmd=partial(
                self._get_sequencer_config_val,
                ["awg", "nco", "delay_comp_en"]
            ),
        )

        self.add_parameter(
            "marker_ovr_en",
            label="Sequencer marker override enable",
            docstring="Sets/gets sequencer marker override enable.",
            unit="",
            vals=vals.Bool(),
            set_parser=bool,
            get_parser=bool,
            set_cmd=partial(
                self._set_sequencer_config_val,
                ["awg", "marker_ovr", "en"]
            ),
            get_cmd=partial(
                self._get_sequencer_config_val,
                ["awg", "marker_ovr", "en"]
            ),
        )

        self.add_parameter(
            "marker_ovr_value",
            label="Sequencer marker override value",
            docstring="Sets/gets sequencer marker override value. Bit index "
                      "corresponds to marker channel index.",
            unit="",
            vals=vals.Numbers(0, 15),
            set_parser=int,
            get_parser=int,
            set_cmd=partial(
                self._set_sequencer_config_val,
                ["awg", "marker_ovr", "val"]
            ),
            get_cmd=partial(
                self._get_sequencer_config_val,
                ["awg", "marker_ovr", "val"]
            ),
        )

        self.add_parameter(
            "sequence",
            label="Sequence",
            docstring="Sets sequencer's AWG waveforms, acquistion weights, "
                      "acquisitions and Q1ASM program. Valid input is a "
                      "string representing the JSON filename or a JSON "
                      "compatible dictionary.",
            vals=vals.MultiType(vals.Strings(), vals.Dict()),
            set_cmd=self._set_sequence,
            get_cmd=Sequencer._get_sequence_raise,
            snapshot_exclude=True,
        )

        for x in range(1, 16):
            self.add_parameter(
                "trigger{}_count_threshold".format(x),
                label="Counter threshold for trigger address T{}".format(x),
                docstring="Sets/gets threshold for counter on trigger "
                        "address T{}. Thresholding condition used: "
                        "greater than or equal.".format(x),
                unit="",
                vals=vals.Numbers(0, 65535),
                set_parser=int,
                get_parser=int,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["seq_proc", "trg", x-1, "count_threshold"]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["seq_proc", "trg", x-1, "count_threshold"]
                ),
            )

            self.add_parameter(
                "trigger{}_threshold_invert".format(x),
                label="Comparison result inversion for trigger address {}".format(x),
                docstring="Sets/gets comparison result inversion for trigger"
                        "address {}.".format(x),
                unit="",
                vals=vals.Bool(),
                set_parser=bool,
                get_parser=bool,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["seq_proc", "trg", x-1, "threshold_invert"]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["seq_proc", "trg", x-1, "threshold_invert"]
                ),
            )

        # -- AWG settings (All modules) --------------------------------------
        for x in range(0, 2):
            self.add_parameter(
                "cont_mode_en_awg_path{}".format(x),
                label="Sequencer continous waveform mode enable for AWG path 0",
                docstring="Sets/gets sequencer continous waveform mode enable "
                        "for AWG path {}.".format(x),
                unit="",
                vals=vals.Bool(),
                set_parser=bool,
                get_parser=bool,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["awg", "cont_mode", "en_path", x]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["awg", "cont_mode", "en_path", x]
                ),
            )

            self.add_parameter(
                "cont_mode_waveform_idx_awg_path{}".format(x),
                label="Sequencer continous waveform mode waveform index for "
                    "AWG path {}".format(x),
                docstring="Sets/gets sequencer continous waveform mode waveform "
                        "index or AWG path {}.".format(x),
                unit="",
                vals=vals.Numbers(0, 2 ** 10 - 1),
                set_parser=int,
                get_parser=int,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["awg", "cont_mode", "wave_idx_path", x]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["awg", "cont_mode", "wave_idx_path", x]
                ),
            )

            self.add_parameter(
                "upsample_rate_awg_path{}".format(x),
                label="Sequencer upsample rate for AWG path {}".format(x),
                docstring="Sets/gets sequencer upsample rate for AWG path {}.".format(x),
                unit="",
                vals=vals.Numbers(0, 2 ** 16 - 1),
                set_parser=int,
                get_parser=int,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["awg", "upsample_rate_path", x]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["awg", "upsample_rate_path", x]
                ),
            )

            self.add_parameter(
                "gain_awg_path{}".format(x),
                label="Sequencer gain for AWG path 0",
                docstring="Sets/gets sequencer gain for AWG path 0.",
                unit="",
                vals=vals.Numbers(-1.0, 1.0),
                set_parser=float,
                get_parser=float,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["awg", "gain_path", x]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["awg", "gain_path", x]
                ),
            )

            self.add_parameter(
                "offset_awg_path{}".format(x),
                label="Sequencer offset for AWG path {}".format(x),
                docstring="Sets/gets sequencer offset for AWG path {}.".format(x),
                unit="",
                vals=vals.Numbers(-1.0, 1.0),
                set_parser=float,
                get_parser=float,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["awg", "offs_path", x]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["awg", "offs_path", x]
                ),
            )

        self.add_parameter(
            "mixer_corr_phase_offset_degree",
            label="Sequencer mixer phase imbalance correction",
            docstring="Sets/gets sequencer mixer phase imbalance correction "
                      "for AWG; applied to AWG path 1 relative to AWG path 0 "
                      "and measured in degrees",
            unit="",
            vals=vals.Numbers(-45.0, 45.0),
            set_parser=float,
            get_parser=float,
            set_cmd=partial(
                self._set_sequencer_config_val,
                ["awg", "mixer", "corr_phase_offset_degree"]
            ),
            get_cmd=partial(
                self._get_sequencer_config_val,
                ["awg", "mixer", "corr_phase_offset_degree"]
            ),
        )

        self.add_parameter(
            "mixer_corr_gain_ratio",
            label="Sequencer mixer gain imbalance correction",
            docstring="Sets/gets sequencer mixer gain imbalance correction "
                      "for AWG; equal to AWG path 1 amplitude divided by "
                      "AWG path 0 amplitude.",
            unit="",
            vals=vals.Numbers(0.5, 2.0),
            set_parser=float,
            get_parser=float,
            set_cmd=partial(
                self._set_sequencer_config_val,
                ["awg", "mixer", "corr_gain_ratio"]

            ),
            get_cmd=partial(
                self._get_sequencer_config_val,
                ["awg", "mixer", "corr_gain_ratio"]
            ),
        )

        self.add_parameter(
            "mod_en_awg",
            label="Sequencer modulation enable",
            docstring="Sets/gets sequencer modulation enable for AWG.",
            unit="",
            vals=vals.Bool(),
            set_parser=bool,
            get_parser=bool,
            set_cmd=partial(
                self._set_sequencer_config_val,
                ["awg", "mixer", "en"]
            ),
            get_cmd=partial(
                self._get_sequencer_config_val,
                ["awg", "mixer", "en"]
            ),
        )

        # -- Acquisition settings (QRM modules only) -------------------------
        if self.parent.is_qrm_type:
            self.add_parameter(
                "demod_en_acq",
                label="Sequencer demodulation enable",
                docstring="Sets/gets sequencer demodulation enable for "
                          "acquisition.",
                unit="",
                vals=vals.Bool(),
                set_parser=bool,
                get_parser=bool,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["acq", "demod_en"]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["acq", "demod_en"]
                ),
            )

            self.add_parameter(
                "integration_length_acq",
                label="Sequencer integration length",
                docstring="Sets/gets sequencer integration length in number "
                          "of samples for non-weighed acquisitions on paths "
                          "0 and 1. Must be a multiple of 4",
                unit="",
                vals=vals.Numbers(4, 2 ** 24 - 4),
                set_parser=int,
                get_parser=int,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["acq", "th_acq", "non_weighed_integration_len"]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["acq", "th_acq", "non_weighed_integration_len"]
                ),
            )


            self.add_parameter(
                "thresholded_acq_rotation",
                label="Sequencer integration result phase rotation",
                docstring="Sets/gets sequencer integration result phase "
                          "rotation in degrees.",
                unit="Degrees",
                vals=vals.Numbers(0, 360),
                set_parser=float,
                get_parser=float,
                set_cmd=self._set_sequencer_config_rotation_matrix,
                get_cmd=self._get_sequencer_config_rotation_matrix,
            )

            self.add_parameter(
                "thresholded_acq_threshold",
                label="Sequencer discretization threshold",
                docstring="Sets/gets sequencer discretization threshold for "
                          "discretizing the phase rotation result. "
                          "Discretization is done by comparing the threshold "
                          "to the rotated integration result of path 0. "
                          "This comparison is applied before normalization "
                          "(i.e. division) of the rotated value with the "
                          "integration length and therefore the threshold "
                          "needs to be compensated (i.e. multiplied) with "
                          "this length for the discretization to function "
                          "properly.",
                unit="",
                vals=vals.Numbers(-1.0 * (2 ** 24 - 4), 1.0 * (2 ** 24 - 4)),
                set_parser=float,
                get_parser=float,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["acq", "th_acq", "discr_threshold"]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["acq", "th_acq", "discr_threshold"]
                ),
            )

            self.add_parameter(
                "thresholded_acq_marker_en",
                label="Thresholded acquisition marker enable",
                docstring="Enable mapping of thresholded acquisition result to markers.",
                unit="",
                vals=vals.Bool(),
                set_parser=bool,
                get_parser=bool,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["acq", "th_acq_mrk_map", "en"]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["acq", "th_acq_mrk_map", "en"]
                ),
            )

            self.add_parameter(
                "thresholded_acq_marker_address",
                label="Marker mask which maps the thresholded acquisition result to the "
                        "markers",
                docstring="Sets/gets the marker mask which maps the thresholded acquisition "
                        "result to the markers (M1 to M4).",
                unit="",
                vals=vals.Numbers(0, 15) if not parent.is_rf_type else vals.Numbers(0,3),
                set_parser=int,
                get_parser=int,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["acq", "th_acq_mrk_map", "addr"]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["acq", "th_acq_mrk_map", "addr"]
                ),
            )

            self.add_parameter(
                "thresholded_acq_marker_invert",
                label="Inversion of the thresholded acquistion result before it is masked "
                        "onto the markers",
                docstring="Sets/gets inversion of the thresholded acquistion result before "
                        "it is masked onto the markers.",
                unit="",
                vals=vals.Bool(),
                set_parser=bool,
                get_parser=bool,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["acq", "th_acq_mrk_map", "inv"]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["acq", "th_acq_mrk_map", "inv"]
                ),
            )

            self.add_parameter(
                "thresholded_acq_trigger_en",
                label="Thresholded acquistion result enable",
                docstring="Sets/gets mapping of thresholded acquisition result to trigger network.",
                unit="",
                vals=vals.Bool(),
                set_parser=bool,
                get_parser=bool,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["acq", "th_acq_trg_map", "en"]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["acq", "th_acq_trg_map", "en"]
                ),
            )

            self.add_parameter(
                "thresholded_acq_trigger_address",
                label="Trigger address to which the thresholded acquisition result is mapped to "
                      "the trigger network",
                docstring="Sets/gets the trigger address to which the thresholded "
                        "acquisition result is mapped to the trigger network (T1 to T15)",
                unit="",
                vals=vals.Numbers(1, 15),
                set_parser=int,
                get_parser=int,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["acq", "th_acq_trg_map", "addr"]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["acq", "th_acq_trg_map", "addr"]
                ),
            )

            self.add_parameter(
                "thresholded_acq_trigger_invert",
                label="Inversion of the thresholded acquistion result before it is masked "
                        "onto the trigger network node",
                docstring="Sets/gets the inversion of the thresholded acquistion result "
                        "before it is mapped to the trigger network.",
                unit="",
                vals=vals.Bool(),
                set_parser=bool,
                get_parser=bool,
                set_cmd=partial(
                    self._set_sequencer_config_val,
                    ["acq", "th_acq_trg_map", "inv"]
                ),
                get_cmd=partial(
                    self._get_sequencer_config_val,
                    ["acq", "th_acq_trg_map", "inv"]
                ),
            )

            if not self.parent.is_rf_type:
                self.add_parameter(
                        "ttl_acq_auto_bin_incr_en",
                        label="TTL trigger acquisition automatic bin increase.",
                        docstring="Sets/gets whether the bin index is automatically "
                                  "incremented when acquiring multiple triggers. "
                                  "Disabling the TTL trigger acquisition path "
                                  "resets the bin index.",
                        unit="",
                        vals= vals.Bool(),
                        set_parser=bool,
                        get_parser=bool,
                        set_cmd=partial(
                            self._set_sequencer_config_val,
                            ["acq", "ttl", "auto_bin_incr_en"]
                        ),
                        get_cmd=partial(
                            self._get_sequencer_config_val,
                            ["acq", "ttl", "auto_bin_incr_en"]
                        ),
                    )

                self.add_parameter(
                    "ttl_acq_threshold",
                    label="TTL trigger acquisition threshold",
                    docstring="Sets/gets the threshold value with which to compare "
                              "the input ADC values of the selected input path.",
                    unit="",
                    vals= vals.Numbers(-1.0,1.0),
                    set_parser=float,
                    get_parser=float,
                    set_cmd=partial(
                        self._set_sequencer_config_val,
                        ["acq", "ttl", "threshold"]
                    ),
                    get_cmd=partial(
                        self._get_sequencer_config_val,
                        ["acq", "ttl", "threshold"]
                    ),
                )

                self.add_parameter(
                    "ttl_acq_input_select",
                    label="TTL trigger acquisition input",
                    docstring="Sets/gets the input used to compare against "
                              "the threshold value in the TTL trigger acquisition "
                              "path.",
                    unit="",
                    vals= vals.Numbers(0,1),
                    set_parser=int,
                    get_parser=int,
                    set_cmd=partial(
                        self._set_sequencer_config_val,
                        ["acq", "ttl", "in"]
                    ),
                    get_cmd=partial(
                        self._get_sequencer_config_val,
                        ["acq", "ttl", "in"]
                    ),
                )

    # ------------------------------------------------------------------------
    @property
    def seq_idx(self) -> int:
        """
        Get sequencer index.

        Parameters
        ----------

        Returns
        ----------
        int
            Sequencer index

        Raises
        ----------
        """

        return self._seq_idx

    # ------------------------------------------------------------------------
    @staticmethod
    def _get_required_parent_attr_names() -> List:
        """
        Return list of parent attribute names that are required for the QCoDeS
        parameters to function, so that the can be registered to this object
        using the _register method.

        Parameters
        ----------

        Returns
        ----------
        List
            List of parent attribute names to register.

        Raises
        ----------
        """

        # Sequencer attributes
        attr_names = []
        for operation in ["set", "get"]:
            attr_names.append("_{}_sequencer_channel_map".format(operation))
            attr_names.append("_{}_sequencer_config".format(operation))
            attr_names.append("_{}_sequencer_config_val".format(operation))
            attr_names.append("_{}_sequencer_config_rotation_matrix".format(operation))
        attr_names.append("_set_sequencer_program")
        attr_names.append("_set_sequence")
        attr_names.append("arm_sequencer")
        attr_names.append("start_sequencer")
        attr_names.append("stop_sequencer")
        attr_names.append("get_sequencer_state")

        # Dummy acquisition data attributes
        attr_names.append("set_dummy_binned_acquisition_data")
        attr_names.append("delete_dummy_binned_acquisition_data")
        attr_names.append("set_dummy_scope_acquisition_data")
        attr_names.append("delete_dummy_scope_acquisition_data")

        # Waveform, weight and acquisition attributes
        for component in ["waveform", "weight", "acquisition"]:
            attr_names.append("_add_{}s".format(component))
            attr_names.append("_delete_{}".format(component))
            attr_names.append("get_{}s".format(component))
        attr_names.append("store_scope_acquisition")
        attr_names.append("_get_acq_acquisition_data")
        attr_names.append("delete_acquisition_data")
        attr_names.append("get_acquisition_state")

        return attr_names

    # ------------------------------------------------------------------------
    def _register(self, attr_name: str) -> None:
        """
        Register parent attribute to this sequencer using functools.partial
        to pre-select the sequencer index. If the attribute does not exist in
        the parent class, a method that raises a `NotImplementedError`
        exception is registered instead. The docstring of the parent attribute
        is also copied to the registered attribute.

        Parameters
        ----------
        attr_name : str
            Attribute name of parent to register.

        Returns
        ----------

        Raises
        ----------
        """

        if hasattr(self.parent, attr_name):
            parent_attr = getattr(self.parent, attr_name)
            partial_func = partial(parent_attr, self.seq_idx)
            partial_func.__doc__ = (
                "Important:\n" +
                "This method calls {0} using functools.partial to set the " +
                "sequencer index. The following docstring is of {1}.{0}:\n\n"
            ).format(attr_name, type(self.parent).__name__)
            partial_func.__doc__ += parent_attr.__doc__
            setattr(self, attr_name, partial_func)
        else:
            def raise_not_implemented_error(*args, **kwargs) -> None:
                raise NotImplementedError(
                    '{} does not have "{}" attribute.'.format(self.parent.name, attr_name)
                )
            setattr(self, attr_name, raise_not_implemented_error)

    # ------------------------------------------------------------------------
    def _invalidate_qcodes_parameter_cache(self) -> None:
        """
        Marks the cache of all QCoDeS parameters on this sequencer as invalid.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        for param in self.parameters.values():
            param.cache.invalidate()

    # ------------------------------------------------------------------------
    @staticmethod
    def _get_sequence_raise() -> NoReturn:
        raise RuntimeError(
            "The `sequence` parameter cannot be queried from the instrument. "
            "Use `sequencer.sequence.cache()` instead. "
            "If this exception was raised by `sequencer.sequence.cache()`, "
            "then the cache was invalid and the instrument state is unknown "
            "(after startup or reset)."
        )

    # ----------------------------------------------------------------------------
    def set_trigger_thresholding(self, address: int, count: int, invert: bool) -> None:
        """
        Sets threshold for designated trigger address counter, together with the inversion condition.
        Thresholding condition used: greater than or equal.

        Parameters
        ----------
        address: int
            Trigger address to which the settings are applied
        count: int
            Threshold
        invert: bool
            Comparison result inversion

        Returns
        ----------

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """

        self.set("trigger{}_count_threshold".format(address), count)
        self.set("trigger{}_threshold_invert".format(address), invert)

    # ----------------------------------------------------------------------------
    def get_trigger_thresholding(self, address: int) -> Tuple:
        """
        Gets threshold for designated trigger address counter, together with the inversion condition.
        Thresholding condition used: greater than or equal.

        Parameters
        ----------
        address: int
            Trigger address to which the settings are applied

        Returns
        ----------
        int
            Threshold
        bool
            Comparison result inversion

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """

        count = self.get("trigger{}_count_threshold".format(address))
        invert = self.get("trigger{}_threshold_invert".format(address))
        return (count, invert)

    # ----------------------------------------------------------------------------
    def reset_trigger_thresholding(self) -> None:
        """
        Resets trigger thresholds for all trigger address counters (T1 to T15) back to 0.
        Also resets inversion back to false.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """

        for x in range(1, 16):
            self.set("trigger{}_count_threshold".format(x), 1)
            self.set("trigger{}_threshold_invert".format(x), False)
