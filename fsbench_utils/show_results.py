#!/usr/bin/env python

from bash_configparser import config_parser
import sys
from benchmark.benchmarking import Benchmark

if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        config = config_parser(config_file)
        new_benchmark = Benchmark(config)
        new_benchmark.show_benchmark_result_normalized()
    else:
        print("You must provide config file for further process.")
        exit(-1)
        
