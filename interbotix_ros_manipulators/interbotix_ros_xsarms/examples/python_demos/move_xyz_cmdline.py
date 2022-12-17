import argparse
from interbotix_xs_modules.arm import InterbotixManipulatorXS


def move_the_thing(x: float, z: float) -> None:
    bot = InterbotixManipulatorXS("rx200", "arm", "gripper")
    bot.arm.set_ee_cartesian_trajectory(x=x, z=z)
    bot.arm.go_to_sleep_pose()

if __name__ == "__main__":
    while True:
        x,z = input('x z: ').split()
        move_the_thing(float(x), float(z))
