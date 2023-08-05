import argparse

arg1 = argparse.ArgumentParser()
arg1.add_argument("file", type=str, help="Path to the Python file to run")
arg1.add_argument("--a", type=int, default=1)
arg1.add_argument("--b", type=int, default=2)

args = arg1.parse_args()
print(args)
print("a + b = ", args.a + args.b)
