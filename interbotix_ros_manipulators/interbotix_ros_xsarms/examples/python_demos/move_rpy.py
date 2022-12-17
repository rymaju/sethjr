import argparse
from interbotix_xs_modules.arm import InterbotixManipulatorXS


def move_the_thing(x,y,z,r: float, p: float, yw: float) -> None:
    bot = InterbotixManipulatorXS("rx200", "arm", "gripper")
    #bot.arm.go_to_home_pose()
    bot.arm.set_ee_pose_components(x=x, y=y, z=z, roll = r, pitch = p, yaw = yw)
    print("hello")
    bot.arm.go_to_home_pose()
    bot.arm.go_to_sleep_pose()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make the thingy do the movement.")
    parser.add_argument('-x', type=float, help = "the x value", default=0)
    parser.add_argument('-y', type=float, help = "the y value", default=0)
    parser.add_argument('-z', type=float, help = "the z value", default=0)
    parser.add_argument('-r', type=float, help = "the roll value", default=0)
    parser.add_argument('-p', type=float, help = "the pitch value", default=0)
    parser.add_argument('-yw', type=float, help = "the yam value", default=0)
    args = parser.parse_args()
    move_the_thing(args.x, args.y, args.z, args.r, args.p, args.yw)
