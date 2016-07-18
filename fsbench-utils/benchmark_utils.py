'''
@author: roraoof
'''
import os
import re 

def get_result_filenames(result_dir):
    """
    get_result_filenames returns the names of files which are located in the 
    result_dir. What is returned is sorted list that contains only single name 
    of duplicated names.
    
    result_dir: the directory that contains the result of benchmark
    """
    files_list = []
    dir_list = os.listdir(result_dir)
    for dir_item in dir_list:
        if os.path.isfile(dir_item):
            continue      
        path = "%s/%s" % (result_dir, dir_item)
        files = os.listdir(path)
        files_list.extend(files)

    files_list = list(set(files_list))
    return sorted(files_list)

def set_files(filenames, microbench, macrobench, metabench):
    """
    set_files sets each filenames to the appropriate benchmark type and returns 
    a hash contains the benchmark type as a key and related filenames as a value.
    
    filenames: the list of unique filenames in result directory
    microbench: the list of micro-benchmarks
    macrobench: the list of macro-benchmarks
    matabench: the list of metadata-benchmarks   
    """
    assigned_files = {}
    for micro in microbench:
        pattern = r".*-%s-.*" % micro
        selected_files = [file for file in filenames if re.search(pattern, file )]
        assigned_files[micro] = selected_files
        [filenames.remove(file) for file in selected_files]
    for macro in macrobench:
        pattern = r".*-%s.*" % macro
        selected_files = [file for file in filenames if re.search(pattern, file )]
        assigned_files[macro] = selected_files
        [filenames.remove(file) for file in selected_files]
    for metadata in metabench:
        pattern = r".*-%s.*" % metadata
        selected_files = [file for file in filenames if re.search(pattern, file )]
        assigned_files[metadata] = selected_files
        [filenames.remove(file) for file in selected_files]
    return assigned_files
   
if __name__ == '__main__':
    result_dir = "/home/roraoof/fsbench/result"
    files = get_result_filenames(result_dir)
    print files, len(files)
    

