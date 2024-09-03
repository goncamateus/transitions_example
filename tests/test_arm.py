import pytest
from model.utils import Position, Pose


def test_arm_is_in_idle_state_when_created(arm):
    state = arm.state
    assert state == "idle", "Arm is not in idle state"


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param((None, None), False),
        pytest.param(
            (1, 2),
            True,
        ),
        pytest.param(
            (Pose(0.0, 0.0, 0.0), Position(1.0, 2.0, 3.0)),
            True,
        ),
    ],
)
def test_arm_dont_execute_position_arm_if_target_is_invalid(arm, input, expected):
    with pytest.raises(ValueError):
        arm.set_target(*input)
        executed = arm.position_arm()
        assert executed == expected, "Arm executed position_arm"


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param((None, None), "idle"),
        pytest.param((1, 2), "go_to_position"),
        pytest.param((Pose(0.0, 0.0, 0.0), Position(1.0, 2.0, 3.0)), "go_to_position"),
    ],
)
def test_arm_dont_change_state_if_target_is_invalid(arm, input, expected):
    with pytest.raises(ValueError):
        arm.set_target(*input)
        arm.position_arm()
        state = arm.state
        assert state == expected, "Arm changed state"


def test_arm_ends_on_finish(arm, target):
    arm.execute(*target)
    state = arm.state
    assert state == "finish", "Arm did not finish"


def test_arm_can_reach_two_sequential_targets(arm, targets):
    target0 = targets[0]
    target1 = targets[1]
    arm.execute(target0.position, target0.pose)
    arm.execute(target1.position, target1.pose)
    state = arm.state
    assert state == "finish", "Arm did not finish"
