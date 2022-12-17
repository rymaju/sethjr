import argparse
from interbotix_xs_modules.arm import InterbotixManipulatorXS


def move_the_thing(x: float, z: float) -> None:
    bot = InterbotixManipulatorXS("rx200", "arm", "gripper")
    bot.arm.set_ee_cartesian_trajectory(x=x, z=z)
    bot.arm.go_to_sleep_pose()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make the thingy do the movement.")
    parser.add_argument('-x', type=float, help = "the x value", default=0)
    parser.add_argument('-z', type=float, help = "the z value", default=0)
    args = parser.parse_args()
    bot = InterbotixManipulatorXS("rx200", "arm", "gripper")
    bot.arm.set_ee_cartesian_trajectory(x=x, z=z)
    bot.arm.go_to_sleep_pose()

if __name__ == "__main__":  move_the_thing(args.x, args.z)
