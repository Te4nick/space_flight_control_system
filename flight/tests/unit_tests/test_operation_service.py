from uuid import uuid4
from django.test import TestCase

from flight.models import Operation
from flight.services import OperationService


class TestOperationService(TestCase):
    def setUp(self) -> None:
        self.service = OperationService()

    def test_get_operation_success(self):
        op_id = uuid4()
        op = Operation(op_id)

        self.service.operations[op_id] = op
        self.assertEqual(self.service.get_operation(op_id), op)

    def test_get_operation_not_found(self):
        op_id = uuid4()

        self.assertEqual(self.service.get_operation(op_id), None)

    def test_finish_operation_success(self):
        op_id = uuid4()
        op = Operation(op_id)

        self.service.operations[op_id] = op
        self.assertEqual(self.service.finish_operation(op_id, True), True)
        self.assertEqual(self.service.operations[op_id].result, True)

    def test_finish_operation_not_found(self):
        op_id = uuid4()

        self.assertEqual(self.service.finish_operation(op_id, True), False)

    def test_execute_operation_success(self):
        op_id = self.service.execute_operation(lambda x: x+1, args=(0,))
        op = Operation(op_id)

        self.assertEqual(self.service.operations.get(op_id), op)