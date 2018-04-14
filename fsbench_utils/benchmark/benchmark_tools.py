'''
Created on Mar 4, 2018

@author: roraoof
'''
from benchmark.benchmark_tools_specific import FioBenchmark, FdtreeBenchmark 

class BenchmarkTool(object):
    def __init__(self, name, benchmark_names, result_dir, runs):
        self.name = name
        self.benchmark_names = benchmark_names
        self.result_dir = result_dir
        self.runs = runs
        self.benchmark_categories = []
        
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

class Fio(BenchmarkTool):
    def __init__(self, name, benchmark_filenames, result_dir, runs):
        super().__init__(name, benchmark_filenames, result_dir, runs)
        self.__add_benchmarks()
    
    def __add_benchmarks(self):
        for benchmark_filename in self.benchmark_names:
            new_fiobenchmark = FioBenchmark(benchmark_filename, self.result_dir, self.runs)
            self.benchmark_categories.append(new_fiobenchmark)
    
    
class Fdtree(BenchmarkTool):
    def __init__(self, name, benchmark_filenames, result_dir, runs):
        super().__init__(name, benchmark_filenames, result_dir, runs)
        self.__add_fdtreebenchmarks()
        
    def __add_fdtreebenchmarks(self):
        for benchmark_filename in self.benchmark_names:
            new_fdtree_benchmark = FdtreeBenchmark(benchmark_filename, self.result_dir, self.runs)
            self.benchmark_categories.append(new_fdtree_benchmark)



if __name__ == '__main__':
    result_dir = "/home/roraoof/workspace/Python/fsbench/fsbench_results/f2fs"
    runs = 3
    new_fio = Fio('micro-fio-sync-read',
                  ['dmcrypt-noop-micro-fio-sync-read-buffered-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-read-buffered-0.5-4096', 'dmcrypt-noop-micro-fio-sync-read-direct-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-read-direct-0.5-4096'],
                  result_dir,
                  runs)
    new_fdtree = Fdtree('metadata-fdtree',
                  ['ecryptfs-noop-metadata-fdtree'],
                  result_dir,
                  runs)
    print(new_fio.get_benchmark_result('dmcrypt-noop-micro-fio-sync-read-buffered-0.5-2097152'))
    print(new_fdtree.get_benchmark_result('ecryptfs-noop-metadata-fdtree'))
