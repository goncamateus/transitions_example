import time

from transitions import Machine
from model.utils import Position, Pose


class Arm(object):
    """Class (sub-machine) of the Arm manipulator.
    The Arm has to go to a position and pose.
    """

    states = [
        {
            "name": "idle",
            "on_enter": [
                "current_state",
                "reset_attributes",
            ],
        },
        {
            "name": "go_to_position",
            "on_enter": [
                "current_state",
                "going_to_position",
            ],
        },
        {
            "name": "pose",
            "on_enter": [
                "current_state",
                "posing",
            ],
        },
        {
            "name": "finish",
            "on_enter": [
                "current_state",
                "stop_arm",
            ],
        },
        {
            "name": "reset",
            "on_enter": [
                "current_state",
            ],
        },
    ]

    transitions = [
        {
            "trigger": "position_arm",
            "source": "idle",
            "dest": "go_to_position",
            "conditions": ["is_target_valid"],
        },
        {
            "trigger": "pose_arm",
            "source": "go_to_position",
            "dest": "pose",
            "conditions": ["is_positioned"],
        },
        {
            "trigger": "finalize",
            "source": "pose",
            "dest": "finish",
            "conditions": ["is_posed"],
        },
        {
            "trigger": "reset_position",
            "source": "go_to_position",
            "dest": "reset",
        },
        {
            "trigger": "reset_pose",
            "source": "pose",
            "dest": "reset",
        },
        {
            "trigger": "reset_finish",
            "source": "finish",
            "dest": "reset",
        },
        {
            "trigger": "reset_system",
            "source": "reset",
            "dest": "idle",
        },
    ]

    def __init__(self) -> None:
        self.machine = Machine(
            model=self,
            states=Arm.states,
            transitions=Arm.transitions,
            initial="idle",
        )
        self._is_positioned = False
        self._is_posed = False

        self.current_position = None
        self.current_pose = None

        self.target_position = None
        self.target_pose = None

    @property
    def is_positioned(self) -> bool:
        return self._is_positioned

    @property
    def is_posed(self) -> bool:
        return self._is_posed

    def is_target_valid(self) -> bool:
        """Check if the target position and pose are valid.

        Returns:
            bool: validity of the target position and pose.
        """
        valid_position = isinstance(self.target_position, Position)
        valid_pose = isinstance(self.target_pose, Pose)
        validation = valid_position and valid_pose
        if not validation:
            raise ValueError(
                "Invalid target position or pose",
                self.target_position,
                self.target_pose,
            )
        return validation

    def reset_attributes(self) -> None:
        """Reset the attributes of the Arm."""
        self._is_positioned = False
        self._is_posed = False
        self.target_position = None
        self.target_pose = None

    def current_state(self) -> None:
        """
        Method to display the current state of the Machine.

        Returns:
            None
        """
        print(f"Machine Arm\nCurrent state: {self.state}")

    def set_target(self, position: Position, pose: Pose) -> None:
        """Set the target position and pose.

        Args:
            position (Position): Target position to be reached.
            pose (Pose): Target pose to be reached.
        """
        self.target_position = position
        self.target_pose = pose

    def going_to_position(self) -> None:
        """
        Method to move the robot to the target position.
        """
        time.sleep(1)
        self._is_positioned = True

    def posing(self) -> None:
        time.sleep(1)
        self._is_posed = True

    def stop_arm(self) -> None:
        print("Stopping the arm...")
        time.sleep(1)

    def execute_fsm(self) -> None:
        while self.state != "finish":
            available_transitions = self.machine.get_triggers(self.state)
            available_transitions = available_transitions[len(self.states) :]
            for current_transition in range(len(available_transitions)):
                method = getattr(self, available_transitions[current_transition])
                may_method = getattr(
                    self, "may_" + available_transitions[current_transition]
                )
                if may_method():
                    print(f"Executing: {available_transitions[current_transition]}")
                    method()

    def reset(self) -> None:
        while self.state != "idle":
            available_transitions = self.machine.get_triggers(self.state)
            available_transitions = available_transitions[len(self.states) :]
            for current_transition in range(len(available_transitions)):
                method = getattr(self, available_transitions[current_transition])
                may_method = getattr(
                    self, "may_" + available_transitions[current_transition]
                )
                if may_method():
                    print(f"Executing: {available_transitions[current_transition]}")
                    method()

    def execute(self, position: Position, pose: Pose) -> None:
        self.set_target(position, pose)
        self.execute_fsm()


if __name__ == "__main__":
    arm = Arm()
    position = Position(1.0, 2.0, 3.0)
    pose = Pose(0.0, 0.0, 0.0)
    arm.execute(position, pose)
    arm.reset()
