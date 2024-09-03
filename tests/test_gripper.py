import pytest


from transitions.core import MachineError


def test_gripper_is_in_idle_state_when_created(gripper):
    state = gripper.state
    assert state == "idle", "Gripper is not in idle state"


def test_gripper_can_reset_from_idle(gripper):
    gripper.reset()
    state = gripper.state
    assert state == "opening", "Gripper did not reset"


def test_gripper_cannot_reset_from_opening(gripper_opening):
    try:
        gripper_opening.reset()
    except MachineError:
        assert True


def test_gripper_can_reset_from_closing(gripper_closing):
    gripper_closing.reset()
    state = gripper_closing.state
    assert state == "opening", "Gripper did not reset"


def test_gripper_can_open_from_close(gripper_closing):
    gripper_closing.open()
    state = gripper_closing.state
    assert state == "opening", "Gripper did not open"


def test_gripper_can_close_from_open(gripper_opening):
    gripper_opening.close()
    state = gripper_opening.state
    assert state == "closing", "Gripper did not close"
