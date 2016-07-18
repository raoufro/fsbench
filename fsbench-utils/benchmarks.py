'''
@author: roraouf
'''
import os
import json

class Benchmark(object):
    def __init__(self, name, filesystems, result_dir):
        self.name = name
        self.filesystems = filesystems
        self.result_dir = result_dir
        self.benchmarks_files = []
        self.benchmarks = []
        
    def get_benchmark_list(self):
        return self.benchmarks_files
    
    def get_benchmarks(self):
        return self.benchmarks

class MicroBenchmark(Benchmark):
    def __init__(self, name, filesystems, result_dir):
        super(MicroBenchmark, self).__init__(name, filesystems, result_dir)
        benchmark_type = "micro"
        
    def add_benchmarks(self, benchmarks_files):
        self.benchmarks_files.extend(benchmarks_files)
        for benchmark_file in benchmarks_files:
            new_benchmark = FioBenchmark(self.filesystems, 'sync', self.result_dir, benchmark_file)
            self.benchmarks.append(new_benchmark)
    
    def show_avg_bw(self):
        start = "%-50s"
        item = "%10s"
        string = start % "" 
        for fs in self.filesystems:
            string += item % fs
        string += "\n"
        for benchmark in self.benchmarks:
            string += start % (benchmark.get_name())
            for avg_bw in benchmark.get_avg_bw():
                string += item % avg_bw
            string += "\n"
        print string
    
class MacroBenchmark(Benchmark):
    def __init__(self, name, filesystems, result_dir):
        super(MacroBenchmark, self).__init__(name, filesystems, result_dir)
        benchmark_type = "macro"
    
    def add_benchmarks(self, benchmarks_files):
        self.benchmarks_files.extend(benchmarks_files)
        for benchmark_file in benchmarks_files:
            new_benchmark = FioBenchmark(self.filesystems, 'sync', self.result_dir, benchmark_file)
            self.benchmarks.append(new_benchmark)
    
    def show_avg_bw(self):
        start = "%-50s"
        item = "%10s"
        string = start % "" 
        for fs in self.filesystems:
            string += item % fs
        string += "\n"
        for benchmark in self.benchmarks:
            string += start % (benchmark.get_name())
            for avg_bw in benchmark.get_avg_bw():
                string += item % avg_bw
            string += "\n"
        print string
    
 
class MetadataBenchmark(Benchmark):
    def __init__(self, name, filesystems, result_dir):
        super(MetadataBenchmark, self).__init__(name, filesystems, result_dir)
        benchmark_type = "metadata"
    
    def add_benchmarks(self, benchmarks_files):
        self.benchmarks_files.extend(benchmarks_files)
        for benchmark_file in benchmarks_files:
            new_benchmark = FdtreeBenchmark(self.filesystems, self.result_dir, benchmark_file)
            self.benchmarks.append(new_benchmark)
    
    def show_result(self):
        start = "%-50s"
        item = "%10s"
        metadata_names = ["Directory Creation Rate", "File Creation Rate",
                         "Directory Removal Rate", "File Removal Rate"]
        result = self.benchmarks[0].get_result()
        string = start % "" 
        for fs in self.filesystems:
            string += item % fs
        string += "\n"
        for idx_metadata_name in range(len(metadata_names)):
            string += start % (metadata_names[idx_metadata_name])
            for idx in range(len(self.filesystems)):
                string += item % result[idx][idx_metadata_name]
            string += "\n"
        print string

class FioBenchmark():
    def __init__(self, filesystems, ioengine, result_dir, name):
        self.filesystems = filesystems
        self.ioengine = ioengine
        self.result_dir = result_dir
        self.name = name
    def get_name(self):
        return self.name
    def get_avg_bw(self):
        result = []
        for fs in self.filesystems:
            try:
                file = os.path.join(self.result_dir, fs, self.name)
                fb = open(file,'r')
                js = fb.read()
                js_content = json.loads(js)
                result.append(str(js_content["jobs"][0]["mixed"]["bw"]))
            except:
                result.append('-')
            else:
                fb.close()
        return result
                
    
class FdtreeBenchmark():
    def __init__(self, filesystems, result_dir, name):
        self.filesystems = filesystems
        self.result_dir = result_dir
        self.name = name
    def get_name(self):
        return self.name
    def __get_file_creation_rate(self, js_content):
        return js_content["files"]["files_create_per_sec"]
    def __get_dir_creation_rate(self, js_content):
        return js_content["dirs"]["dirs_create_per_sec"]
    def __get_file_removal_rate(self, js_content):
        return js_content["files"]["files_removal_per_sec"]
    def __get_dir_removal_rate(self, js_content):
        return js_content["dirs"]["dirs_removal_per_sec"]
    def get_result(self):
        result = []
        for fs in self.filesystems:
            try:
                result_set =[]
                file = os.path.join(self.result_dir, fs, self.name)
                fb = open(file,'r')
                js = fb.read()
                js_content = json.loads(js)
                result_set.append(self.__get_dir_creation_rate(js_content))
                result_set.append(self.__get_file_creation_rate(js_content))
                result_set.append(self.__get_dir_removal_rate(js_content))
                result_set.append(self.__get_file_removal_rate(js_content))
                result.append(result_set)
            except:
                result.append(['-','-','-','-'])
            else:
                fb.close()
        return result
    
if __name__ == "__main__":
    filesystems = ["ext4", "f2fs", "nilfs2"]
    micro = MicroBenchmark("test", filesystems, "here")
    print str(micro)