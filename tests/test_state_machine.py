import unittest
from lexer.state_machine import StateMachine, State


def are_states_equal(m_state, state) -> bool:
    if m_state == state:
        return True
    return False


class TestStateMachine(unittest.TestCase):
    def test_machine_reset(self):
        machine = StateMachine("reset_test_machine", {})
        machine.state = State.undefined
        machine.prevState = State.undefined
        machine.reset_state()
        self.assertTrue(are_states_equal(machine.prevState, State.begin))
        self.assertTrue(are_states_equal(machine.state, State.begin))

    def test_machine_default_state(self):
        machine = StateMachine("default_state_test_machine", {})
        self.assertTrue(are_states_equal(machine.prevState, State.begin))
        self.assertTrue(are_states_equal(machine.state, State.begin))

    def test_machine_change_state(self):
        def rule(obj):
            if obj == 1:
                return State.num
            return State.undefined

        machine = StateMachine("change_state_test_machine", {
            State.begin: rule
        })

        machine.process_object(1)
        self.assertTrue(are_states_equal(machine.state, State.num))


if __name__ == '__main__':
    unittest.main()
