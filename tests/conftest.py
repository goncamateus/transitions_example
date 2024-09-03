import pytest


from model.arm import Arm
from model.gripper import Gripper
from model.utils import Position, Pose, Target


@pytest.fixture(scope="function")
def arm():
    yield Arm()


@pytest.fixture(scope="function")
def target():
    yield (Position(1.0, 2.0, 3.0), Pose(0.0, 0.0, 0.0))


@pytest.fixture(scope="function")
def gripper():
    yield Gripper()


@pytest.fixture(scope="function")
def gripper_opening(gripper):
    gripper.reset()
    yield gripper


@pytest.fixture(scope="function")
def gripper_closing(gripper):
    gripper.reset()
    gripper.close()
    yield gripper


@pytest.fixture(scope="function")
def targets():
    target0 = Target(Position(1.0, 2.0, 3.0), Pose(0.0, 0.0, 0.0))
    target1 = Target(Position(4.0, 5.0, 6.0), Pose(1.0, 2.0, 3.0))
    yield (target0, target1)
