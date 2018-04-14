'''
@author: roraouf
'''
import re
from benchmark.benchmark_tools import Fio, Fdtree

# Different types of benchmarking in file systems  
benchmark_categories = ["micro", "macro", "metadata"]

# Different types of micro-benchmark_tools implemented in this program
micro_benchmarks = ["micro_fio_sync"]

# Different types of macro-benchmark_tools implemented in this program
macro_benchmarks = ["macro_fio"]

# Different types of metadata-benchmark_tools implemented in this program
metadata_benchmarks = ["metadata_fdtree"]

# Implemented micro-benchmark_tools based on Fio synchronous IO
micro_fio_sync = ["micro-fio-sync-read", "micro-fio-sync-write",
                  "micro-fio-sync-randread", "micro-fio-sync-randwrite"]

# Implemented macro-benchmark_tools based on Fio
macro_fio = ["macro-fio-grep", "macro-fio-untar", "macro-fio-compile"]

# Implemented benchmark_tools based on metadata operations
metadata_fdtree = ["metadata-fdtree"]

class BenchmarkCategory(object):
    def __init__(self, benchmark_type, benchmark_names, result_dir, runs):
        self.benchmark_type = benchmark_type
        self.benchmark_names = benchmark_names 
        self.result_dir = result_dir
        self.runs = runs
        
        self.benchmark_categories = []
        self.__add_benchmarks()
    
    def __add_benchmarks(self):
        
        if self.benchmark_type == "micro":
            for micro_benchmark in micro_benchmarks:
                for benchmark in eval(micro_benchmark):
                    pattern = r".*-%s-.*" % benchmark
                    selected_benchmarks = [name for name in self.benchmark_names if re.search(pattern, name)]
                    
                    # FIX ME - Make it work with all benchmark_tools 
                    new_benchmark = Fio(benchmark, selected_benchmarks, self.result_dir, self.runs )
                    self.benchmark_categories.append(new_benchmark)
                    
        elif self.benchmark_type == "macro":
            for macro_benchmark in macro_benchmarks:
                for benchmark in eval(macro_benchmark):
                    pattern = r".*-%s" % benchmark
                    selected_benchmarks = [name for name in self.benchmark_names if re.search(pattern, name)]
                    
                    # FIX ME - Make it work with all benchmark_tools 
                    new_benchmark = Fio(benchmark, selected_benchmarks, self.result_dir, self.runs)
                    self.benchmark_categories.append(new_benchmark)
                    
        elif self.benchmark_type == "metadata":
            for metadata_benchmark in metadata_benchmarks:
                for benchmark in eval(metadata_benchmark):
                    pattern = r".*-%s" % benchmark
                    selected_benchmarks = [name for name in self.benchmark_names if re.search(pattern, name)]
                    
                    # FIX ME
                    new_benchmark = Fdtree(benchmark, selected_benchmarks, self.result_dir, self.runs)
                    self.benchmark_categories.append(new_benchmark)
            
    def get_benchmark_result(self, benchmark_name):
        if benchmark_name in self.benchmark_names:
            for benchmark in self.benchmark_categories:
                benchmark_result = benchmark.get_benchmark_result(benchmark_name)
                if benchmark_result == None:
                    continue
                else:
                    return benchmark_result
        else:
            return None



if __name__ == '__main__':
    result_dir = "/home/roraoof/workspace/Python/fsbench/fsbench_results/f2fs"
    runs = 3
    micro_benchmak = BenchmarkCategory("micro", 
                                ['dmcrypt-noop-micro-fio-sync-randread-buffered-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-randread-buffered-0.5-4096', 'dmcrypt-noop-micro-fio-sync-randread-direct-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-randread-direct-0.5-4096', 'dmcrypt-noop-micro-fio-sync-randwrite-buffered-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-randwrite-buffered-0.5-4096', 'dmcrypt-noop-micro-fio-sync-randwrite-direct-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-randwrite-direct-0.5-4096', 'dmcrypt-noop-micro-fio-sync-read-buffered-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-read-buffered-0.5-4096', 'dmcrypt-noop-micro-fio-sync-read-direct-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-read-direct-0.5-4096', 'dmcrypt-noop-micro-fio-sync-write-buffered-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-write-buffered-0.5-4096', 'dmcrypt-noop-micro-fio-sync-write-direct-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-write-direct-0.5-4096'],
                                result_dir, runs)
      
    macro_benchmark = BenchmarkCategory("macro", 
                                ['dmcrypt-noop-macro-fio-compile', 'dmcrypt-noop-macro-fio-grep', 'dmcrypt-noop-macro-fio-untar'],
                                result_dir, runs)
  
    metadata_benchmark = BenchmarkCategory("metadata", 
                                ['dmcrypt-noop-metadata-fdtree'],
                                result_dir, runs)
    
    print(micro_benchmak.get_benchmark_result('dmcrypt-noop-micro-fio-sync-randread-buffered-0.5-2097152'))
    print(macro_benchmark.get_benchmark_result('dmcrypt-noop-macro-fio-grep'))
    print(metadata_benchmark.get_benchmark_result('dmcrypt-noop-metadata-fdtree'))
