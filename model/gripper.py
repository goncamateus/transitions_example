import time

from transitions import Machine


class Gripper(object):
    """Class (sub-machine) of the gripper manipulator.
    The gripper only has to open and close.
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
            "name": "opening",
            "on_enter": [
                "current_state",
                "opening_gripper",
            ],
        },
        {
            "name": "closing",
            "on_enter": [
                "current_state",
                "closing_gripper",
            ],
        },
    ]

    transitions = [
        {
            "trigger": "reset",
            "source": ["idle", "opening", "closing"],
            "dest": "opening",
        },
        {
            "trigger": "close",
            "source": "opening",
            "dest": "closing",
            "conditions": ["opened"],
        },
        {
            "trigger": "open",
            "source": "closing",
            "dest": "opening",
            "conditions": ["closed"],
        },
    ]

    def __init__(self) -> None:
        self.machine = Machine(
            model=self,
            states=Gripper.states,
            transitions=Gripper.transitions,
            initial="idle",
        )

        self._gripper_state = 0

    def opened(self) -> bool:
        """
        Returns:
            bool: True if the gripper is opened, False otherwise.
        """
        return self._gripper_state == 0

    def closed(self) -> bool:
        """
        Returns:
            bool: True if the gripper is closed, False otherwise.
        """
        return self._gripper_state == 1

    def reset_attributes(self) -> None:
        """Reset the gripper attributes"""
        self._gripper_state = 0

    def current_state(self):
        """
        Method to display the current state of the Machine.

        Returns:
            None
        """
        print(f"\nMachine Gripper\nCurrent State: {self.state}")

    def opening_gripper(self):
        """Method to open the gripper.

        Returns:
            None
        """
        print("Opening Gripper...\n")
        time.sleep(1)
        self._gripper_state = 0

    def closing_gripper(self):
        """Method to close the gripper.

        Returns:
            None
        """
        print("Closing Gripper...\n")
        time.sleep(1)
        self._gripper_state = 1


if __name__ == "__main__":
    from transitions.core import MachineError

    gripper = Gripper()
    gripper.reset()
    try:
        gripper.open()
    except MachineError as e:
        print("raised error:", e, "as expected")
    gripper.close()
    try:
        gripper.close()
    except MachineError as e:
        print("raised error:", e, "as expected")
    gripper.open()
    assert gripper.opened(), "Gripper should be opened"
