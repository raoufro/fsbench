'''
Created on Mar 2, 2018

@author: roraoof
'''
from benchmark.filesystem import Filesystem


class Benchmark(object):
    def __init__(self, config):
        self.config = config
        self.runs = int(config["runs"])
        self.result_dir = config["result_dir"]
        self.filesystems = []
        
        # add the names of filesystems
        self.__add_filesystems() 
        
    
    def __add_filesystems(self):
        filesystems_names = self.__get_filesystems()
        for filesystem_name in filesystems_names:
            new_filesystem = Filesystem(filesystem_name, self.result_dir, self.runs)
            self.filesystems.append(new_filesystem)
        
    def __get_filesystems(self):
        '''
        __get_filesystems returns the list of filesystems which are benchmarked.
        '''
        # FIX ME
        # extract the list of filesystems by looking at fs
        filesystems = ["f2fs"]
        return filesystems
    
    def show_benchmark_result(self):
        for filesystem in self.filesystems:
            result = filesystem.get_benchmark_result()
            
            benchmark_names = sorted(list(result.keys()))
            encryptions = [list(encryption.keys())[0] for encryption in result[benchmark_names[0]]]
            
            start = "%-50s"
            item = "%10s"
            macro_micro_string = start % ""
            meta_data_string = start % ""
            for encryption in encryptions:
                macro_micro_string += item % encryption
                meta_data_string += item % encryption
            macro_micro_string += "\n"
            meta_data_string += "\n"
                
            for benchmark_name in benchmark_names:
                if benchmark_name == "noop-metadata-fdtree":
                    metadata_result = result[benchmark_name]
                    metadata_result_list = [list(result.values())[0] for result in metadata_result]
                    
                    metadata_names = ["Directory Creation Rate", "File Creation Rate",
                                     "Directory Removal Rate", "File Removal Rate"]
                     
                    meta_data_string += "\n"
                    for idx_metadata_name in range(len(metadata_names)):
                        meta_data_string += start % (metadata_names[idx_metadata_name])
                        for idx in range(len(encryptions)):
                            meta_data_string += item % metadata_result_list[idx][idx_metadata_name]
                        meta_data_string += "\n"
                else:
                    macro_micro_string += "\n"
                    macro_micro_string += start % (benchmark_name)
                    for avg_bws in result[benchmark_name]:
                        for avg_bw in avg_bws.values():
                            macro_micro_string += item % avg_bw
                    macro_micro_string += "\n"

            print("#"*34 + " Macro/Micro-Benchmark " + "#"*34)
            print(macro_micro_string)

    def show_benchmark_result_normalized(self):
        for filesystem in self.filesystems:
            result = filesystem.get_benchmark_result()
            
            benchmark_names = sorted(list(result.keys()))
            encryptions = [list(encryption.keys())[0] for encryption in result[benchmark_names[0]]]
            
            start = "%-50s"
            item = "%10s"
            macro_micro_string = start % ""
            meta_data_string = start % ""
            for encryption in encryptions:
                macro_micro_string += item % encryption
                meta_data_string += item % encryption
            macro_micro_string += "\n"
            meta_data_string += "\n"
                
            for benchmark_name in benchmark_names:
                if benchmark_name == "noop-metadata-fdtree":
                    metadata_result = result[benchmark_name]
                    metadata_result_list = [list(result.values())[0] for result in metadata_result]
                    
                    metadata_names = ["Directory Creation Rate", "File Creation Rate",
                                     "Directory Removal Rate", "File Removal Rate"]
                     
                    meta_data_string += "\n"
                    for idx_metadata_name in range(len(metadata_names)):
                        meta_data_string += start % (metadata_names[idx_metadata_name])
                        for idx in range(len(encryptions)):
                            meta_data_string += item % metadata_result_list[idx][idx_metadata_name]
                        meta_data_string += "\n"
                else:
                    macro_micro_list = []
                    for avg_bws in result[benchmark_name]:
                        for avg_bw in avg_bws.values():
                            macro_micro_list.append(avg_bw)
                    macro_micro_list_normalized = []
                    for macro_micro_item in macro_micro_list:
                        if macro_micro_item != None:
                            macro_micro_item /= macro_micro_list[-1]
                        macro_micro_list_normalized.append(macro_micro_item)
                    
                    macro_micro_string += "\n"
                    macro_micro_string += start % (benchmark_name)
                    for macro_micro_item in macro_micro_list_normalized:
                        macro_micro_string += item % ("%.6s" % macro_micro_item) 
                    macro_micro_string += "\n"      

            print("#"*34 + " Macro/Micro-Benchmark " + "#"*34)
            print(macro_micro_string)
                        
            
if __name__ == '__main__':
    config= {'io_size_ratio': '"0.5"', 'logfile': '/home/user/Projects/fsbench/log/logfile', 'result_dir': '/home/roraoof/workspace/Python/fsbench/latest_fsbench_results', 'trans_num': '100', 'records_num': '1000', 'iosched_exclude': '"cfq deadline"', 'mount_dir': '/media/sdb5', 'sysbench_lua': '/home/user/Projects/fsbench/sysbench-lua', 'device': '/dev/sdb5', 'benchmark_exclude': '"macro-sysbench-mysql"', '#benchmark_exclude': '"macro-fio-grep macro-fio-untar macro-fio-compile macro-sysbench-mysql \\', 'runs': '3'}
    new_benchmark = Benchmark(config)
    new_benchmark.show_benchmark_result()
    new_benchmark.show_benchmark_result_normalized()
