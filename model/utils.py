class Position:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"Position({self.x}, {self.y}, {self.z})"


class Pose:
    def __init__(self, roll: float, pitch: float, yaw: float) -> None:
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def __str__(self) -> str:
        return f"Pose({self.roll}, {self.pitch}, {self.yaw})"


class Target:
    def __init__(self, postion: Position, pose: Pose) -> None:
        self.position = postion
        self.pose = pose

    @classmethod
    def from_floats(
        cls,
        pos_x: float,
        pos_y: float,
        pos_z: float,
        roll: float,
        pitch: float,
        yaw: float,
    ):
        return cls(Position(pos_x, pos_y, pos_z), Pose(roll, pitch, yaw))

    @classmethod
    def from_tuple_of_floats(
        cls,
        position: tuple[float, float, float],
        pose: tuple[float, float, float],
    ):
        return cls(Position(*position), Pose(*pose))

    def __str__(self) -> str:
        return f"Target({self.position}, {self.pose})"
