"""This test module verifies all circuit qudit methods."""
from __future__ import annotations

from typing import Any

import numpy as np
import pytest
from hypothesis import given
from hypothesis.strategies import integers

from bqskit.ir.circuit import Circuit
from bqskit.ir.gates import CNOTGate
from bqskit.ir.gates import ConstantUnitaryGate
from bqskit.ir.gates import HGate
from bqskit.utils.test.strategies import radixes
from bqskit.utils.test.types import invalid_type_test
from bqskit.utils.test.types import valid_type_test


class TestAppendQudit:
    """This tests `circuit.append_qudit`."""

    @valid_type_test(Circuit(2).append_qudit)
    def test_valid_type(self) -> None:
        pass

    @invalid_type_test(Circuit(2).append_qudit)
    def test_invalid_type(self) -> None:
        pass

    @given(integers(max_value=1))
    def test_invalid_value(self, val: int) -> None:
        with pytest.raises(ValueError):
            Circuit(2).append_qudit(val)

    def test_default(self) -> None:
        circuit = Circuit(1)
        assert circuit.num_qudits == 1
        assert circuit.dim == 2
        assert len(circuit.radixes) == 1
        circuit.append_qudit()
        assert circuit.num_qudits == 2
        assert circuit.dim == 4
        assert len(circuit.radixes) == 2
        circuit.append_qudit()
        assert circuit.num_qudits == 3
        assert circuit.dim == 8
        assert len(circuit.radixes) == 3

    def test_qutrit(self) -> None:
        circuit = Circuit(1, [3])
        assert circuit.num_qudits == 1
        assert circuit.dim == 3
        assert len(circuit.radixes) == 1
        circuit.append_qudit(3)
        assert circuit.num_qudits == 2
        assert circuit.dim == 9
        assert len(circuit.radixes) == 2
        circuit.append_qudit(3)
        assert circuit.num_qudits == 3
        assert circuit.dim == 27
        assert len(circuit.radixes) == 3

    def test_hybrid(self) -> None:
        circuit = Circuit(1)
        assert circuit.num_qudits == 1
        assert circuit.dim == 2
        assert len(circuit.radixes) == 1
        circuit.append_qudit(4)
        assert circuit.num_qudits == 2
        assert circuit.dim == 8
        assert len(circuit.radixes) == 2
        assert circuit.radixes[0] == 2
        assert circuit.radixes[1] == 4
        circuit.append_qudit(3)
        assert circuit.num_qudits == 3
        assert circuit.dim == 24
        assert len(circuit.radixes) == 3
        assert circuit.radixes[0] == 2
        assert circuit.radixes[1] == 4
        assert circuit.radixes[2] == 3

    def test_append_gate(self) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.append_qudit()
        circuit.append_gate(CNOTGate(), [3, 4])
        assert circuit.num_qudits == 5
        assert circuit[3, 4].gate == CNOTGate()


class TestExtendQudits:
    """This tests `circuit.extend_qudits`."""

    @valid_type_test(Circuit(2).extend_qudits)
    def test_valid_type(self) -> None:
        pass

    @invalid_type_test(Circuit(2).extend_qudits)
    def test_invalid_type(self) -> None:
        pass

    @given(radixes())
    def test_invalid(self, radixes: tuple[int, ...]) -> None:
        radixes = (-1,) + radixes
        with pytest.raises(ValueError):
            Circuit(1).extend_qudits(radixes)

    @given(radixes())
    def test_valid(self, radixes: tuple[int, ...]) -> None:
        circ = Circuit(1)
        circ.extend_qudits(radixes)
        assert circ.radixes == (2,) + radixes
        assert circ.num_qudits == len(radixes) + 1

    def test_qubits(self) -> None:
        circuit = Circuit(1, [2])
        assert circuit.num_qudits == 1
        assert circuit.dim == 2
        assert len(circuit.radixes) == 1
        circuit.extend_qudits([2, 2])
        assert circuit.num_qudits == 3
        assert circuit.dim == 8
        assert len(circuit.radixes) == 3
        circuit.extend_qudits([2, 2])
        assert circuit.num_qudits == 5
        assert circuit.dim == 32
        assert len(circuit.radixes) == 5

    def test_qutrits(self) -> None:
        circuit = Circuit(1, [3])
        assert circuit.num_qudits == 1
        assert circuit.dim == 3
        assert len(circuit.radixes) == 1
        circuit.extend_qudits([3, 3])
        assert circuit.num_qudits == 3
        assert circuit.dim == 27
        assert len(circuit.radixes) == 3
        circuit.extend_qudits([3, 3])
        assert circuit.num_qudits == 5
        assert circuit.dim == 243
        assert len(circuit.radixes) == 5

    def test_hybrid(self) -> None:
        circuit = Circuit(1)
        assert circuit.num_qudits == 1
        assert circuit.dim == 2
        assert len(circuit.radixes) == 1
        circuit.extend_qudits([3, 4])
        assert circuit.num_qudits == 3
        assert circuit.dim == 24
        assert len(circuit.radixes) == 3
        assert circuit.radixes[0] == 2
        assert circuit.radixes[1] == 3
        assert circuit.radixes[2] == 4
        circuit.extend_qudits([3, 2])
        assert circuit.num_qudits == 5
        assert circuit.dim == 144
        assert len(circuit.radixes) == 5
        assert circuit.radixes[0] == 2
        assert circuit.radixes[1] == 3
        assert circuit.radixes[2] == 4
        assert circuit.radixes[3] == 3
        assert circuit.radixes[4] == 2

    def test_append_gate(self) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.extend_qudits([2, 2])
        circuit.append_gate(CNOTGate(), [3, 4])
        circuit.append_gate(CNOTGate(), [4, 5])
        assert circuit.num_qudits == 6
        assert circuit[3, 4].gate == CNOTGate()
        assert circuit[4, 5].gate == CNOTGate()


class TestInsertQudit:
    """This tests `circuit.insert_qudit`."""

    @valid_type_test(Circuit(2).insert_qudit)
    def test_valid_type(self) -> None:
        pass

    @invalid_type_test(Circuit(2).insert_qudit)
    def test_invalid_type(self) -> None:
        pass

    @given(integers(max_value=1))
    def test_invalid(self, val: int) -> None:
        with pytest.raises(ValueError):
            Circuit(1).insert_qudit(0, val)

    def test_default(self) -> None:
        circuit = Circuit(1)
        assert circuit.num_qudits == 1
        assert circuit.dim == 2
        assert len(circuit.radixes) == 1
        circuit.insert_qudit(0)
        assert circuit.num_qudits == 2
        assert circuit.dim == 4
        assert len(circuit.radixes) == 2
        circuit.insert_qudit(0)
        assert circuit.num_qudits == 3
        assert circuit.dim == 8
        assert len(circuit.radixes) == 3

    def test_qutrit(self) -> None:
        circuit = Circuit(1, [3])
        assert circuit.num_qudits == 1
        assert circuit.dim == 3
        assert len(circuit.radixes) == 1
        circuit.insert_qudit(0, 3)
        assert circuit.num_qudits == 2
        assert circuit.dim == 9
        assert len(circuit.radixes) == 2
        circuit.insert_qudit(0, 3)
        assert circuit.num_qudits == 3
        assert circuit.dim == 27
        assert len(circuit.radixes) == 3

    def test_hybrid(self) -> None:
        circuit = Circuit(1)
        assert circuit.num_qudits == 1
        assert circuit.dim == 2
        assert len(circuit.radixes) == 1
        circuit.insert_qudit(0, 4)
        assert circuit.num_qudits == 2
        assert circuit.dim == 8
        assert len(circuit.radixes) == 2
        assert circuit.radixes[0] == 4
        assert circuit.radixes[1] == 2
        circuit.insert_qudit(-1, 3)
        assert circuit.num_qudits == 3
        assert circuit.dim == 24
        assert len(circuit.radixes) == 3
        assert circuit.radixes[0] == 4
        assert circuit.radixes[1] == 3
        assert circuit.radixes[2] == 2

    def test_append_gate_1(self) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.insert_qudit(0)
        circuit.append_gate(CNOTGate(), [0, 3])
        assert circuit.num_qudits == 5
        assert len(circuit.radixes) == 5
        assert circuit.radixes.count(2) == 5
        assert circuit[3, 0].gate == CNOTGate()
        assert circuit[3, 0].location == (0, 3)
        assert circuit[0, 1].gate == CNOTGate()
        assert circuit[0, 1].location == (1, 2)
        assert circuit[1, 2].gate == CNOTGate()
        assert circuit[1, 2].location == (2, 3)
        assert circuit[2, 3].gate == CNOTGate()
        assert circuit[2, 3].location == (3, 4)

    def test_append_gate_2(self) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.insert_qudit(1)
        circuit.append_gate(CNOTGate(), [0, 3])
        assert circuit.num_qudits == 5
        assert len(circuit.radixes) == 5
        assert circuit.radixes.count(2) == 5
        assert circuit[3, 0].gate == CNOTGate()
        assert circuit[3, 0].location == (0, 3)
        assert circuit[0, 0].gate == CNOTGate()
        assert circuit[0, 0].location == (0, 2)
        assert circuit[1, 2].gate == CNOTGate()
        assert circuit[1, 2].location == (2, 3)
        assert circuit[2, 3].gate == CNOTGate()
        assert circuit[2, 3].location == (3, 4)

    def test_append_gate_3(self) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.insert_qudit(2)
        circuit.append_gate(CNOTGate(), [0, 3])
        assert circuit.num_qudits == 5
        assert len(circuit.radixes) == 5
        assert circuit.radixes.count(2) == 5
        assert circuit[3, 0].gate == CNOTGate()
        assert circuit[3, 0].location == (0, 3)
        assert circuit[0, 0].gate == CNOTGate()
        assert circuit[0, 0].location == (0, 1)
        assert circuit[1, 1].gate == CNOTGate()
        assert circuit[1, 1].location == (1, 3)
        assert circuit[2, 3].gate == CNOTGate()
        assert circuit[2, 3].location == (3, 4)

    def test_append_gate_4(self) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.insert_qudit(3)
        circuit.append_gate(CNOTGate(), [0, 3])
        assert circuit.num_qudits == 5
        assert len(circuit.radixes) == 5
        assert circuit.radixes.count(2) == 5
        assert circuit[1, 0].gate == CNOTGate()
        assert circuit[1, 0].location == (0, 3)
        assert circuit[0, 0].gate == CNOTGate()
        assert circuit[0, 0].location == (0, 1)
        assert circuit[1, 1].gate == CNOTGate()
        assert circuit[1, 1].location == (1, 2)
        assert circuit[2, 2].gate == CNOTGate()
        assert circuit[2, 2].location == (2, 4)

    def test_append_gate_5(self) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.insert_qudit(4)
        circuit.append_gate(CNOTGate(), [0, 3])
        assert circuit.num_qudits == 5
        assert len(circuit.radixes) == 5
        assert circuit.radixes.count(2) == 5
        assert circuit[3, 0].gate == CNOTGate()
        assert circuit[3, 0].location == (0, 3)
        assert circuit[0, 1].gate == CNOTGate()
        assert circuit[0, 1].location == (0, 1)
        assert circuit[1, 2].gate == CNOTGate()
        assert circuit[1, 2].location == (1, 2)
        assert circuit[2, 3].gate == CNOTGate()
        assert circuit[2, 3].location == (2, 3)
        assert circuit[3, 3].gate == CNOTGate()
        assert circuit[3, 3].location == (0, 3)
        assert circuit[0, 0].gate == CNOTGate()
        assert circuit[0, 0].location == (0, 1)
        assert circuit[1, 1].gate == CNOTGate()
        assert circuit[1, 1].location == (1, 2)
        assert circuit[2, 2].gate == CNOTGate()
        assert circuit[2, 2].location == (2, 3)

    def test_append_gate_6(self) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.insert_qudit(-3)
        circuit.append_gate(CNOTGate(), [0, 3])
        assert circuit.num_qudits == 5
        assert len(circuit.radixes) == 5
        assert circuit.radixes.count(2) == 5
        assert circuit[3, 0].gate == CNOTGate()
        assert circuit[3, 0].location == (0, 3)
        assert circuit[0, 0].gate == CNOTGate()
        assert circuit[0, 0].location == (0, 2)
        assert circuit[1, 2].gate == CNOTGate()
        assert circuit[1, 2].location == (2, 3)
        assert circuit[2, 3].gate == CNOTGate()
        assert circuit[2, 3].location == (3, 4)

    def test_append_gate_7(self) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.insert_qudit(-6)
        circuit.append_gate(CNOTGate(), [0, 3])
        assert circuit.num_qudits == 5
        assert len(circuit.radixes) == 5
        assert circuit.radixes.count(2) == 5
        assert circuit[3, 0].gate == CNOTGate()
        assert circuit[3, 0].location == (0, 3)
        assert circuit[0, 1].gate == CNOTGate()
        assert circuit[0, 1].location == (1, 2)
        assert circuit[1, 2].gate == CNOTGate()
        assert circuit[1, 2].location == (2, 3)
        assert circuit[2, 3].gate == CNOTGate()
        assert circuit[2, 3].location == (3, 4)

    def test_append_gate_8(self) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.insert_qudit(25)
        circuit.append_gate(CNOTGate(), [0, 3])
        assert circuit.num_qudits == 5
        assert len(circuit.radixes) == 5
        assert circuit.radixes.count(2) == 5
        assert circuit[3, 0].gate == CNOTGate()
        assert circuit[3, 0].location == (0, 3)
        assert circuit[0, 1].gate == CNOTGate()
        assert circuit[0, 1].location == (0, 1)
        assert circuit[1, 2].gate == CNOTGate()
        assert circuit[1, 2].location == (1, 2)
        assert circuit[2, 3].gate == CNOTGate()
        assert circuit[2, 3].location == (2, 3)

    def test_multi_gate_1(self, gen_random_utry_np: Any) -> None:
        circuit = Circuit(4)
        three_qubit_gate = ConstantUnitaryGate(gen_random_utry_np(8))
        circuit.append_gate(three_qubit_gate, [1, 2, 3])
        circuit.append_gate(three_qubit_gate, [0, 2, 3])
        circuit.append_gate(three_qubit_gate, [0, 1, 3])
        circuit.append_gate(three_qubit_gate, [0, 1, 2])
        circuit.insert_qudit(0)
        assert circuit.num_qudits == 5
        assert len(circuit.radixes) == 5
        assert circuit.radixes.count(2) == 5
        assert circuit[0, 2].gate == three_qubit_gate
        assert circuit[0, 2].location == (2, 3, 4)
        assert circuit[1, 1].gate == three_qubit_gate
        assert circuit[1, 1].location == (1, 3, 4)
        assert circuit[2, 1].gate == three_qubit_gate
        assert circuit[2, 1].location == (1, 2, 4)
        assert circuit[3, 1].gate == three_qubit_gate
        assert circuit[3, 1].location == (1, 2, 3)

    def test_multi_gate_2(self, gen_random_utry_np: Any) -> None:
        circuit = Circuit(4, [2, 2, 3, 3])
        three_qubit_gate = ConstantUnitaryGate(
            gen_random_utry_np(12), [2, 2, 3],
        )
        circuit.append_gate(three_qubit_gate, [0, 1, 3])
        circuit.append_gate(three_qubit_gate, [0, 1, 2])
        circuit.insert_qudit(2)
        assert circuit.num_qudits == 5
        assert len(circuit.radixes) == 5
        assert circuit.radixes[0] == 2
        assert circuit.radixes[1] == 2
        assert circuit.radixes[2] == 2
        assert circuit.radixes[3] == 3
        assert circuit.radixes[4] == 3
        assert circuit[0, 1].gate == three_qubit_gate
        assert circuit[0, 1].location == (0, 1, 4)
        assert circuit[1, 1].gate == three_qubit_gate
        assert circuit[1, 1].location == (0, 1, 3)

    def test_multi_gate_3(self, gen_random_utry_np: Any) -> None:
        circuit = Circuit(4)
        three_qubit_gate = ConstantUnitaryGate(
            gen_random_utry_np(12), [2, 2, 3],
        )
        circuit.insert_qudit(2, 3)
        assert circuit.num_qudits == 5
        assert len(circuit.radixes) == 5
        assert circuit.radixes[0] == 2
        assert circuit.radixes[1] == 2
        assert circuit.radixes[2] == 3
        assert circuit.radixes[3] == 2
        assert circuit.radixes[4] == 2
        circuit.append_gate(three_qubit_gate, [0, 1, 2])
        assert circuit[0, 0].gate == three_qubit_gate
        assert circuit[0, 0].location == (0, 1, 2)


class TestPopQudit:
    """This tests `circuit.pop_qudit`."""

    @valid_type_test(Circuit(2).pop_qudit)
    def test_valid_type(self) -> None:
        pass

    @invalid_type_test(Circuit(2).pop_qudit)
    def test_invalid_type(self) -> None:
        pass

    def test_index_invalid1(self) -> None:
        circuit = Circuit(1)
        try:
            circuit.pop_qudit(-5)
        except IndexError:
            return
        except BaseException:
            assert False, 'Unexpected Exception.'

    def test_index_invalid2(self) -> None:
        circuit = Circuit(1)
        try:
            circuit.pop_qudit(5)
        except IndexError:
            return
        except BaseException:
            assert False, 'Unexpected Exception.'

    def test_index_invalid3(self) -> None:
        circuit = Circuit(4, [2, 2, 3, 3])
        try:
            circuit.pop_qudit(5)
        except IndexError:
            return
        except BaseException:
            assert False, 'Unexpected Exception.'

    def test_index_invalid_empty(self) -> None:
        circuit = Circuit(1)
        assert circuit.num_qudits == 1
        try:
            circuit.pop_qudit(0)
        except ValueError:
            return
        except BaseException:
            assert False, 'Unexpected Exception.'

    @pytest.mark.parametrize('qudit_index', [-4, -1, 0, 3])
    def test_append_gate_1(self, qudit_index: int) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.pop_qudit(qudit_index)
        assert circuit.num_qudits == 3
        assert len(circuit.radixes) == 3
        assert circuit.radixes.count(2) == 3
        assert circuit.num_operations == 2
        assert circuit[0, 0].gate == CNOTGate()
        assert circuit[0, 0].location == (0, 1)
        assert circuit[1, 1].gate == CNOTGate()
        assert circuit[1, 1].location == (1, 2)
        assert circuit[0, 1].gate == CNOTGate()
        assert circuit[0, 1].location == (0, 1)
        assert circuit[1, 2].gate == CNOTGate()
        assert circuit[1, 2].location == (1, 2)

    @pytest.mark.parametrize('qudit_index', [-3, 1])
    def test_append_gate_2(self, qudit_index: int) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.pop_qudit(qudit_index)
        assert circuit.num_qudits == 3
        assert len(circuit.radixes) == 3
        assert circuit.radixes.count(2) == 3
        assert circuit.num_operations == 1
        assert circuit[0, 1].gate == CNOTGate()
        assert circuit[0, 1].location == (1, 2)
        assert circuit[0, 2].gate == CNOTGate()
        assert circuit[0, 2].location == (1, 2)

    @pytest.mark.parametrize('qudit_index', [-2, 2])
    def test_append_gate_3(self, qudit_index: int) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.pop_qudit(qudit_index)
        assert circuit.num_qudits == 3
        assert len(circuit.radixes) == 3
        assert circuit.radixes.count(2) == 3
        assert circuit.num_operations == 1
        assert circuit[0, 0].gate == CNOTGate()
        assert circuit[0, 0].location == (0, 1)
        assert circuit[0, 1].gate == CNOTGate()
        assert circuit[0, 1].location == (0, 1)

    @pytest.mark.parametrize('qudit_index', [-4, -1, 0, 3])
    def test_append_gate_4(self, qudit_index: int) -> None:
        circuit = Circuit(4)
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.append_gate(CNOTGate(), [0, 1])
        circuit.append_gate(CNOTGate(), [1, 2])
        circuit.append_gate(CNOTGate(), [2, 3])
        circuit.pop_qudit(qudit_index)
        assert circuit.num_qudits == 3
        assert len(circuit.radixes) == 3
        assert circuit.radixes.count(2) == 3
        assert circuit.num_operations == 6
        assert circuit[0, 0].gate == CNOTGate()
        assert circuit[0, 0].location == (0, 1)
        assert circuit[1, 1].gate == CNOTGate()
        assert circuit[1, 1].location == (1, 2)
        assert circuit[2, 0].gate == CNOTGate()
        assert circuit[2, 0].location == (0, 1)
        assert circuit[3, 1].gate == CNOTGate()
        assert circuit[3, 1].location == (1, 2)
        assert circuit[4, 0].gate == CNOTGate()
        assert circuit[4, 0].location == (0, 1)
        assert circuit[5, 1].gate == CNOTGate()
        assert circuit[5, 1].location == (1, 2)

    @pytest.mark.parametrize('qudit_index', [-4, -3, -2, -1, 0, 1, 2, 3])
    def test_multi_gate_1(
            self, qudit_index: int, gen_random_utry_np: Any,
    ) -> None:
        circuit = Circuit(4)
        three_qubit_gate = ConstantUnitaryGate(gen_random_utry_np(8))
        circuit.append_gate(three_qubit_gate, [1, 2, 3])
        circuit.append_gate(three_qubit_gate, [0, 2, 3])
        circuit.append_gate(three_qubit_gate, [0, 1, 3])
        circuit.append_gate(three_qubit_gate, [0, 1, 2])
        circuit.pop_qudit(qudit_index)
        assert circuit.num_qudits == 3
        assert len(circuit.radixes) == 3
        assert circuit.radixes.count(2) == 3
        assert circuit.num_operations == 1
        assert circuit.num_cycles == 1
        assert circuit[0, 0].gate == three_qubit_gate
        assert circuit[0, 0].location == (0, 1, 2)
        assert circuit[0, 1].gate == three_qubit_gate
        assert circuit[0, 1].location == (0, 1, 2)
        assert circuit[0, 2].gate == three_qubit_gate
        assert circuit[0, 2].location == (0, 1, 2)

    @pytest.mark.parametrize('qudit_index', [-2, -1, 2, 3])
    def test_multi_gate_2(
            self, qudit_index: int, gen_random_utry_np: Any,
    ) -> None:
        circuit = Circuit(4, [2, 2, 3, 3])
        three_qubit_gate = ConstantUnitaryGate(
            gen_random_utry_np(12), [2, 2, 3],
        )
        circuit.append_gate(three_qubit_gate, [0, 1, 3])
        circuit.append_gate(three_qubit_gate, [0, 1, 2])
        circuit.pop_qudit(qudit_index)
        assert circuit.num_qudits == 3
        assert len(circuit.radixes) == 3
        assert circuit.num_operations == 1
        assert circuit.num_cycles == 1
        assert circuit.radixes[0] == 2
        assert circuit.radixes[1] == 2
        assert circuit.radixes[2] == 3
        assert circuit[0, 0].gate == three_qubit_gate
        assert circuit[0, 0].location == (0, 1, 2)
        assert circuit[0, 1].gate == three_qubit_gate
        assert circuit[0, 1].location == (0, 1, 2)
        assert circuit[0, 2].gate == three_qubit_gate
        assert circuit[0, 2].location == (0, 1, 2)


class TestIsQuditInRange:
    """This tests `circuit.is_qudit_in_range`."""

    @valid_type_test(Circuit(2).is_qudit_in_range)
    def test_valid_type(self) -> None:
        pass

    @invalid_type_test(Circuit(2).is_qudit_in_range)
    def test_invalid_type(self) -> None:
        pass

    @given(integers())
    def test_return_type(self, an_int: int) -> None:
        circuit = Circuit(4, [2, 2, 3, 3])
        assert isinstance(circuit.is_qudit_in_range(an_int), (bool, np.bool_))

    @pytest.mark.parametrize('test_value', [-5, -4, -3, -2, -1])
    def test_true_neg(self, test_value: int) -> None:
        circuit = Circuit(5)
        assert circuit.is_qudit_in_range(test_value)

    @pytest.mark.parametrize('test_value', [0, 1, 2, 3, 4])
    def test_true_pos(self, test_value: int) -> None:
        circuit = Circuit(5)
        assert circuit.is_qudit_in_range(test_value)

    @pytest.mark.parametrize('test_value', [-1000, -100, -8, -6])
    def test_false_neg(self, test_value: int) -> None:
        circuit = Circuit(5)
        assert not circuit.is_qudit_in_range(test_value)

    @pytest.mark.parametrize('test_value', [5, 6, 8, 100, 1000])
    def test_false_pos(self, test_value: int) -> None:
        circuit = Circuit(5)
        assert not circuit.is_qudit_in_range(test_value)


class TestIsQuditIdle:
    """This tests `circuit.is_qudit_idle`."""

    @valid_type_test(Circuit(2).is_qudit_idle)
    def test_valid_type(self) -> None:
        pass

    @invalid_type_test(Circuit(2).is_qudit_idle)
    def test_invalid_type(self) -> None:
        pass

    def test_return_type(
            self, r6_qudit_circuit: Circuit,
    ) -> None:
        for i in range(6):
            assert isinstance(r6_qudit_circuit.is_qudit_idle(i), bool)

    def test_single(self) -> None:
        circuit = Circuit(4, [2, 2, 2, 2])
        assert circuit.is_qudit_idle(0)
        assert circuit.is_qudit_idle(1)
        assert circuit.is_qudit_idle(2)
        assert circuit.is_qudit_idle(3)

        circuit.append_gate(HGate(), [0])
        assert not circuit.is_qudit_idle(0)
        assert circuit.is_qudit_idle(1)
        assert circuit.is_qudit_idle(2)
        assert circuit.is_qudit_idle(3)

        circuit.append_gate(HGate(), [1])
        assert not circuit.is_qudit_idle(0)
        assert not circuit.is_qudit_idle(1)
        assert circuit.is_qudit_idle(2)
        assert circuit.is_qudit_idle(3)

        circuit.append_gate(HGate(), [2])
        assert not circuit.is_qudit_idle(0)
        assert not circuit.is_qudit_idle(1)
        assert not circuit.is_qudit_idle(2)
        assert circuit.is_qudit_idle(3)

        circuit.append_gate(HGate(), [3])
        assert not circuit.is_qudit_idle(0)
        assert not circuit.is_qudit_idle(1)
        assert not circuit.is_qudit_idle(2)
        assert not circuit.is_qudit_idle(3)

        circuit.pop((0, 0))
        assert circuit.is_qudit_idle(0)
        assert not circuit.is_qudit_idle(1)
        assert not circuit.is_qudit_idle(2)
        assert not circuit.is_qudit_idle(3)

        circuit.pop((0, 1))
        assert circuit.is_qudit_idle(0)
        assert circuit.is_qudit_idle(1)
        assert not circuit.is_qudit_idle(2)
        assert not circuit.is_qudit_idle(3)

        circuit.pop((0, 2))
        assert circuit.is_qudit_idle(0)
        assert circuit.is_qudit_idle(1)
        assert circuit.is_qudit_idle(2)
        assert not circuit.is_qudit_idle(3)

        circuit.pop((0, 3))
        assert circuit.is_qudit_idle(0)
        assert circuit.is_qudit_idle(1)
        assert circuit.is_qudit_idle(2)
        assert circuit.is_qudit_idle(3)
