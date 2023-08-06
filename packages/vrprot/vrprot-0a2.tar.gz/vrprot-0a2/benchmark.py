#! python3
from timeit import timeit
from main import main
from src.vrprot.argument_parser import argument_parser
import sys
import argparse


def benchmark_local():
    mode = [
        "local",
        "./processing_files/pdbs",
    ]
    run_benchmark(mode)


def benchmark_from_bulk():
    mode = [
        "bulk",
        "../../static/UP000000805_243232_METJA_v4_Kopie.tar",
    ]
    run_benchmark(mode)


def run_benchmark(mode):
    args = [
        "main.py",
        "-ll",
        "INFO",
    ]
    if "-pcc" in sys.argv:
        args += ["-pcc"]
    if "-parallel" in sys.argv or "-p" in sys.argv:
        args += ["-p"]
    if "-ow" in sys.argv:
        args += ["-ow"]
    args += mode
    sys.argv = args
    args = argument_parser().parse_args()
    main(args)


if __name__ == "__main__":
    func = {
        "local": benchmark_local,
        "bulk": benchmark_from_bulk,
    }
    if len(sys.argv) > 1:
        if sys.argv[1] in func:
            func = func[sys.argv[1]]
            n = 1
            runtime = timeit(func, number=n)
            print(f"{n} repetitions took", runtime, "seconds")
            print("Average time per repetition:", runtime / 10)
