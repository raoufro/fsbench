'''
Created on Mar 2, 2018

@author: roraoof
'''

import re 
from benchmark.benchmark_types import BenchmarkCategory, benchmark_categories

class Encryption():
    def __init__(self, encrypt_type, benchmark_names, result_dir, runs):
        self.encrypt_type = encrypt_type
        self.benchmark_names = benchmark_names
        self.result_dir = result_dir
        self.runs = runs
        
        self.benchmark_categories = []
        self.__add_benchmark_categories()
        
    def __add_benchmark_categories(self):
        assigned_files = {}
        
        for benchmark_category in benchmark_categories:
            pattern = r".*-%s-.*" % benchmark_category
            selected_benchmarks = [name for name in self.benchmark_names if re.search(pattern, name)]
            assigned_files[benchmark_category] = sorted(selected_benchmarks)
            
            new_benchmark = BenchmarkCategory(benchmark_category, assigned_files[benchmark_category], self.result_dir, self.runs)
            self.benchmark_categories.append(new_benchmark)

    
    def get_benchmark_result(self, benchmark_name):
        if benchmark_name in self.benchmark_names:
            for benchmark_category in self.benchmark_categories:
                benchmark_result = benchmark_category.get_benchmark_result(benchmark_name)
                if benchmark_result == None:
                    continue
                else:
                    return benchmark_result
        else:
            return None
        
    def get_type(self):
        return self.encrypt_type
        

if __name__ == '__main__':
    result_dir = "/home/roraoof/workspace/Python/fsbench/fsbench_results/f2fs"
    runs = 3
    new_encryption = Encryption("dmcrypt", 
                                ['dmcrypt-noop-macro-fio-compile', 'dmcrypt-noop-macro-fio-grep', 'dmcrypt-noop-macro-fio-untar', 'dmcrypt-noop-metadata-fdtree', 'dmcrypt-noop-micro-fio-sync-randread-buffered-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-randread-buffered-0.5-4096', 'dmcrypt-noop-micro-fio-sync-randread-direct-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-randread-direct-0.5-4096', 'dmcrypt-noop-micro-fio-sync-randwrite-buffered-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-randwrite-buffered-0.5-4096', 'dmcrypt-noop-micro-fio-sync-randwrite-direct-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-randwrite-direct-0.5-4096', 'dmcrypt-noop-micro-fio-sync-read-buffered-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-read-buffered-0.5-4096', 'dmcrypt-noop-micro-fio-sync-read-direct-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-read-direct-0.5-4096', 'dmcrypt-noop-micro-fio-sync-write-buffered-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-write-buffered-0.5-4096', 'dmcrypt-noop-micro-fio-sync-write-direct-0.5-2097152', 'dmcrypt-noop-micro-fio-sync-write-direct-0.5-4096'],
                                result_dir, runs)
    print(new_encryption.get_benchmark_result('dmcrypt-noop-macro-fio-grep'))
    print(new_encryption.get_benchmark_result('dmcrypt-noop-micro-fio-sync-randread-buffered-0.5-4096'))
    print(new_encryption.get_benchmark_result('dmcrypt-noop-metadata-fdtree'))

    
    
