import random

from transitions import Machine

from model.arm import Arm
from model.gripper import Gripper
from model.utils import Target


class PickAndPlaceRobot(object):

    states = [
        {
            "name": "idle",
            "on_enter": [
                "current_state",
                "reset_attributes",
                "set_pick_target",
            ],
        },
        {
            "name": "pick",
            "on_enter": [
                "current_state",
                "open_gripper",
                "moving_to_pick_position",
                "close_gripper",
                "set_place_target",
            ],
        },
        {
            "name": "error",
            "on_enter": [
                "current_state",
                "add_try",
            ],
        },
        {
            "name": "retry",
            "on_enter": [
                "current_state",
            ],
        },
        {
            "name": "place",
            "on_enter": [
                "current_state",
                "moving_to_place_position",
                "open_gripper",
            ],
        },
        {
            "name": "finished",
            "on_enter": [
                "current_state",
            ],
        },
        {
            "name": "abort",
            "on_enter": [
                "current_state",
            ],
        },
    ]

    transitions = [
        {
            "trigger": "start",
            "source": "idle",
            "dest": "pick",
            "conditions": ["no_errors_occurred"],
        },
        {
            "trigger": "fail",
            "source": "pick",
            "dest": "error",
            "conditions": ["picking_error"],
        },
        {
            "trigger": "retry_pick",
            "source": "error",
            "dest": "retry",
            "conditions": ["can_retry"],
        },
        {
            "trigger": "retry_decision",
            "source": "retry",
            "dest": "pick",
            "conditions": ["can_retry"],
        },
        {
            "trigger": "abort_retry",
            "source": "retry",
            "dest": "abort",
        },
        {
            "trigger": "success",
            "source": "pick",
            "dest": "place",
            "conditions": ["object_picked"],
        },
        {
            "trigger": "place_success",
            "source": "place",
            "dest": "finished",
            "conditions": ["object_placed"],
        },
        {
            "trigger": "reset",
            "source": ["idle", "pick", "place", "error", "retry", "abort", "finished"],
            "dest": "idle",
            "conditions": ["errors_occurred"],
        },
    ]

    def __init__(self, pick_target: Target, place_target: Target) -> None:
        self.machine = Machine(
            model=self,
            states=PickAndPlaceRobot.states,
            transitions=PickAndPlaceRobot.transitions,
            initial="idle",
        )

        self.gripper = Gripper()
        self.arm = Arm()

        self._tries = None
        self._can_retry = None
        self._no_errors_occured = None
        self._errors_occured = None
        self._picking_error = None
        self._object_picked = None
        self._object_placed = None

        self.reset_attributes()

        self._pick_target = pick_target
        self._place_target = place_target

    def current_state(self) -> None:
        """
        Method to display the current state of the Machine.

        Returns:
            None
        """
        print(f"Current state: {self.state}")

    def reset_attributes(self) -> None:
        """Reset the attributes of the PickAndPlaceRobot."""
        self.gripper.reset()
        self.arm.reset()
        self._tries = 0
        self._can_retry = True
        self._no_errors_occured = True
        self._picking_error = False
        self._object_picked = False
        self._object_placed = False

    @property
    def pick_target(self) -> Target:
        return self._pick_target

    @property
    def place_target(self) -> Target:
        return self._place_target

    @property
    def tries(self) -> int:
        return self._tries

    @property
    def can_retry(self) -> bool:
        return self._can_retry

    @property
    def errors_occurred(self) -> bool:
        return self._errors_occured

    @property
    def no_errors_occurred(self) -> bool:
        return not self._errors_occured

    @property
    def picking_error(self) -> bool:
        return self._picking_error

    @property
    def object_picked(self) -> bool:
        return self._object_picked

    @property
    def object_placed(self) -> bool:
        return self._object_placed

    def set_pick_target(self) -> None:
        self.arm.set_target(self.pick_target.position, self.pick_target.pose)

    def set_place_target(self) -> None:
        self.arm.set_target(self.place_target.position, self.place_target.pose)

    def add_try(self) -> None:
        self._tries += 1

    def open_gripper(self) -> None:
        self.gripper.reset()
        self._object_picked = False
        if self.arm.is_posed and self.arm.target_position == self.place_target.position:
            chance = random.randint(0, 1)
            if chance < 0.8:
                self._object_placed = True
            else:
                self._object_placed = False
                self._errors_occurred = True

    def close_gripper(self) -> None:
        self.gripper.close()
        if self.arm.is_posed and self.arm.target_position == self.pick_target.position:
            self._object_placed = False
            chance = random.randint(0, 1)
            if chance < 0.8:
                self._object_picked = True
            else:
                self._object_picked = False
                self._picking_error = True
                self._errors_occurred = True

    def moving_to_pick_position(self) -> None:
        self.arm.execute(self.pick_target.position, self.pick_target.pose)

    def moving_to_place_position(self) -> None:
        self.arm.execute(self.place_target.position, self.place_target.pose)

    def execute_fsm(self) -> None:
        while self.state != "finished":
            available_transitions = self.machine.get_triggers(self.state)
            available_transitions = available_transitions[len(self.states) :]
            for current_transition in range(len(available_transitions)):
                method = getattr(self, available_transitions[current_transition])
                may_method = getattr(
                    self, "may_" + available_transitions[current_transition]
                )
                if may_method():
                    print(
                        f"Machine PickAndPlace--------\nExecuting: {available_transitions[current_transition]}"
                    )
                    method()
