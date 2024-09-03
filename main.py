from model.pick_and_place import PickAndPlaceRobot
from model.utils import Target


def main():
    robot = PickAndPlaceRobot(
        Target.from_tuple_of_floats((1.0, 2.0, 3.0), (0.0, 0.0, 0.0)),
        Target.from_tuple_of_floats((4.0, 5.0, 6.0), (1.0, 2.0, 3.0)),
    )
    robot.execute_fsm()


if __name__ == "__main__":
    main()
