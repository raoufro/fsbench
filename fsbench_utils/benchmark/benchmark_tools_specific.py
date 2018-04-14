'''
Created on Mar 4, 2018

@author: roraoof
'''
import os, json

class SpecificBenchmarkTool(object):
    def __init__(self, filename, result_dir, runs):
        self.filename = filename
        self.result_dir = result_dir
        self.runs = runs
    
        self.files = []
        self.__add_files()
        
    def __add_files(self):
        for run in range(1,self.runs+1):
            actual_filename = os.path.join(self.result_dir, str(run), self.filename)
            self.files.append(actual_filename)

class FioBenchmark(SpecificBenchmarkTool):
    def __init__(self, filename, result_dir, runs):
        super().__init__(filename, result_dir, runs)
    
    def get_benchmark_result(self, benchmark_name):
        results = []
        if benchmark_name == self.filename:
            for file in self.files:
#                 print(file, self.__get_avg_bw(file))
                results.append(self.__get_avg_bw(file))
            return int((sum(results)) / max(len(results), 1))
        else:
            return None
    
    def __get_avg_bw(self, filename):
        result = 0
        try:
            fb = open(filename,'r')
            js = fb.read()
            js_content = json.loads(js)
            result = js_content["jobs"][0]["mixed"]["bw"]
        except:
            result = None
            print(filename)
        else:
            fb.close()
        return result
                    
class FdtreeBenchmark(SpecificBenchmarkTool):
    def __init__(self, filename, result_dir, runs):
        super().__init__(filename, result_dir, runs)
 
    def get_benchmark_result(self, benchmark_name):
        results = []
        if benchmark_name == self.filename:
            for file in self.files:
                results.append(self.__get_metadata_fdtree(file))
            avg_result = []
            for j in range (len(results[1])):
                col_list = []
                for i in range(len(results)):
                    col_list.append(int(results[i][j]))
                avg_result.append(int(sum(col_list)/max(len(col_list),1)))
            return avg_result
        else:
            return None
        
    def __get_file_creation_rate(self, js_content):
        return js_content["files"]["files_create_per_sec"]
    def __get_dir_creation_rate(self, js_content):
        return js_content["dirs"]["dirs_create_per_sec"]
    def __get_file_removal_rate(self, js_content):
        return js_content["files"]["files_removal_per_sec"]
    def __get_dir_removal_rate(self, js_content):
        return js_content["dirs"]["dirs_removal_per_sec"]
    
    def __get_metadata_fdtree(self, filename):
        try:
            result_set =[]
            fb = open(filename,'r')
            js = fb.read()
            js_content = json.loads(js)
            result_set.append(self.__get_dir_creation_rate(js_content))
            result_set.append(self.__get_file_creation_rate(js_content))
            result_set.append(self.__get_dir_removal_rate(js_content))
            result_set.append(self.__get_file_removal_rate(js_content))
        except:
            result_set = None
            print(filename)
        else:
            fb.close()
        return result_set
