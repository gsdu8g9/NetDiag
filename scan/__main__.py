import argparse

from core import Scanner


def parse_arguments():
    """Parse arguments"""
    parser = argparse.ArgumentParser(
        description="Ping sweep for hosts and help determining subnets.")
    parser.add_argument(
        "--subnets",
        required=True,
        nargs="+",
        help="Subnet blocks that you would like to scan.")
    parser.add_argument(
        "--threads",
        type=int,
        default=20,
        help="Count of threads that you would like to use.")
    parser.add_argument(
        "--nmap-args",
        default='-T4 -F',
        help="arguments to be passed to nmap. Default=[-T4 -F]")
    return parser.parse_args()


def main():
    """Main function"""
    args = parse_arguments()
    sweep = Scanner(
        subnets=args.subnets,
        threads=args.threads)
    sweep.start()


if __name__ == "__main__":
    main()
