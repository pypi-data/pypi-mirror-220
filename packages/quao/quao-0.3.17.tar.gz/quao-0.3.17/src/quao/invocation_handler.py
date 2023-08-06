"""
    QuaO Project invocation_handler.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from .backend import Backend
from .data.request.request_data import RequestData
from .util.response_utils import ResponseUtils


class InvocationHandler:
    def __init__(self, event):
        self.event = event

    def invoke(self, circuit_preparation, post_processing):
        """

        @param post_processing:
        @param circuit_preparation:
        @return:
        """

        request_data = RequestData(self.event)
        backend = Backend(request_data)

        circuit = circuit_preparation(request_data.input)

        job = backend.submit_job(circuit, post_processing)

        response = ResponseUtils.generate_response(job)

        return response
