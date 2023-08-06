# ----------------------------------------------------------------------------
# Description    : Transport layer (abstract, IP, file, dummy)
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

from qblox_instruments import PulsarType
from qblox_instruments.ieee488_2 import QcmQrmDummyTransport


# -- class -------------------------------------------------------------------

class PulsarDummyTransport(QcmQrmDummyTransport):
    """
    Class to replace Pulsar device with dummy device to support software
    stack testing without hardware. The class implements all mandatory,
    required and Pulsar specific SCPI calls. Call reponses are largely
    artifically constructed to be inline with the call's functionality
    (e.g. `*IDN?` returns valid, but artificial IDN data.) To assist
    development, the Q1ASM assembler has been completely implemented. Please
    have a look at the call's implentation to know what to expect from its
    response.
    """

    # ------------------------------------------------------------------------
    def __init__(
        self,
        dummy_type: PulsarType
    ):
        """
        Create Pulsar dummy transport class.

        Parameters
        ----------
        dummy_type : PulsarType
            Dummy module type (e.g. Pulsar QCM, Pulsar QRM)

        Returns
        ----------

        Raises
        ----------
        """

        # Initialize base class
        super().__init__(dummy_type)

        # Set command list
        self._cmds["STATus:QUEStionable:LED:BRIGHTness?"] = self._get_led_brightness

    # ------------------------------------------------------------------------
    def _get_led_brightness(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get LED brightness

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = "HIGH"
