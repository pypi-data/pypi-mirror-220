"""
    QuaO Project ibm_quantum_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from qiskit import transpile

from ...model.device.qiskit_device import QiskitDevice
from ...util.json_parser_util import JsonParserUtils
from ...config.logging_config import *


class IbmQuantumDevice(QiskitDevice):

    def _is_simulator(self) -> bool:
        return self.device.configuration().simulator

    def _create_job(self, circuit, shots):
        logger.debug('Create Ibm Quantum job with {0} shots'.format(shots))
        transpile_circuit = transpile(circuit, self.device)

        return self.device.run(transpile_circuit, shots=shots)
