'''
Created on Mar 2, 2018

@author: roraoof
'''
from benchmark.encryption import Encryption
import os
import re

class Filesystem(object):
    def __init__(self, fs_name, result_dir, runs):
        self.fs_name = fs_name
        self.result_dir = os.path.join(result_dir, fs_name)
        self.runs = runs
        self.benchmark_names = []
        self.encryptions = []
        
        self.__add_encryptions()
    
    def __extract_benchmark_filenames(self):
        '''
        __extract_benchmark_filenames returns the names of files which are located in the 
        result_dir for a specific filesystem. What is returned is sorted list
        that contains only single name of duplicated names.
        '''
        result_dir = self.result_dir
        files_list = []
        run_list = os.listdir(result_dir)
        for run in run_list:
            run_dir = os.path.join(result_dir, run)
            if os.path.isfile(run_dir):
                continue      
            files_list.extend(os.listdir(run_dir))
    
        # Remove duplicated filenames
        files_list = list(set(files_list))
        return sorted(files_list)
    
    def __add_encryptions(self):
        benchmark_filenames = self.__extract_benchmark_filenames()
        benchmark_names = []
        encryption_types = []
        assigned_files = {}
        pattern = r"(\w+)-(.*)"
        for benchmark in benchmark_filenames:
            match = re.search(pattern, benchmark)
            if match:
                encryption_types.append(match.group(1))
                benchmark_names.append(match.group(2))
                
        encryption_types = sorted(list(set(encryption_types)))
        self.benchmark_names = sorted(list(set(benchmark_names)))
        
        for encryption_type in encryption_types:
            pattern = r"%s-(.*)" % encryption_type
            selected_files = [benchmark for benchmark in benchmark_filenames if re.search(pattern, benchmark)]
            assigned_files[encryption_type] = sorted(selected_files)
            
            new_encryption = Encryption(encryption_type, assigned_files[encryption_type], self.result_dir, self.runs)
            self.encryptions.append(new_encryption)  
    
    def get_benchmark_result(self):
        results = {}
        for benchmark_name in self.benchmark_names:
            tmp = []
            for encryption in self.encryptions:
                encryption_type = encryption.get_type()
                benchmark_result = encryption.get_benchmark_result(encryption_type + '-' +benchmark_name)
                tmp.append({encryption_type:benchmark_result})
            results[benchmark_name]=tmp
        return results
    
                

if __name__ == '__main__':
    result_dir = "/home/roraoof/workspace/Python/fsbench/fsbench_results"
    runs = 3
    fss = Filesystem("f2fs", result_dir, runs)
    print(fss.get_benchmark_result(), len(fss.get_benchmark_result()))
