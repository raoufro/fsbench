from benchmarks import *
import  benchmark_utils
import bash_configparser
import sys


micro_fio_sync = ["micro-fio-sync-read", "micro-fio-sync-write",
                  "micro-fio-sync-randread", "micro-fio-sync-randwrite"]

macro_fio = ["macro-fio-grep", "macro-fio-untar", "macro-fio-compile"]

metadata_fdtree = ["metadata-fdtree"]


if __name__ == '__main__':
    config_file = sys.argv[1]
    config = bash_configparser.config_parser(config_file)
    filesystems = "ext4 f2fs nilfs2"
    result_dir = config["result_dir"]
    
    micro_benchmarks = []
    macro_benchmarks = []
    metadata_benchmarks= []
    
    filenames = benchmark_utils.get_result_filenames(result_dir)
    benchmarks_files = benchmark_utils.set_files(filenames, micro_fio_sync, 
                                                macro_fio, metadata_fdtree)
    
    del(filenames)
    filesystems = filesystems.split()
       
    # Create Micro-benchmark Objects with their files
    for microbench_name in micro_fio_sync:
        if len(benchmarks_files[microbench_name]):
            new_micro_benchmark = MicroBenchmark(microbench_name, filesystems, result_dir)
            new_micro_benchmark.add_benchmarks(benchmarks_files[microbench_name])
            micro_benchmarks.append(new_micro_benchmark)
        
    # Create Macro-benchmark Objects with their files
    for macrobench_name in macro_fio:
        if len(benchmarks_files[macrobench_name]):
            new_macro_benchmark = MacroBenchmark(macrobench_name, filesystems, result_dir)
            new_macro_benchmark.add_benchmarks(benchmarks_files[macrobench_name])
            macro_benchmarks.append(new_macro_benchmark)
         
    # Create Metadata-benchmark Object with its files
    for metabench_name in metadata_fdtree:
        if len(benchmarks_files[metabench_name]):
            new_meta_benchmark = MetadataBenchmark(metabench_name, filesystems, result_dir)
            new_meta_benchmark.add_benchmarks(benchmarks_files[metabench_name])
            metadata_benchmarks.append(new_meta_benchmark)
    
    print "#"*32, "Micro-Benchmark", "#"*32    
    for micro_benchmark in micro_benchmarks:
        micro_benchmark.show_avg_bw()

    print "#"*32, "Macro-Benchmark", "#"*32
    for macro_benchmark in macro_benchmarks:
        macro_benchmark.show_avg_bw()
    
    print "#"*31, "Metadata-Benchmark", "#"*31   
    for metadata_benchmark in metadata_benchmarks:
        metadata_benchmark.show_result()
