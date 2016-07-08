#!/usr/bin/python 
import sys
import re
import json

def extract_fdtree_json_output(fdtree_output):
    match = re.search(r'for a total of (\w+) directories', fdtree_output)
    if match:
        dirs_num = match.group(1)
    
    match = re.search(r'for a total of (\w+) files and (\w+)', fdtree_output)
    if match:
        files_num = match.group(1)
    
    match = re.search(r'Directory creates per second =  (\d+)', fdtree_output)
    if match:
        dirs_create_per_sec = match.group(1)
    
    match = re.search(r'File creates per second      =  (\d+)', fdtree_output)
    if match:
        files_create_per_sec = match.group(1)
        
    match = re.search(r'File removals per second     =  (\d+)', fdtree_output)
    if match:
        files_removal_per_sec = match.group(1)
    
    match = re.search(r'Directory removals per second =  (\d+)', fdtree_output)
    if match:
        dirs_removal_per_sec = match.group(1)
    
    metadata_json = { 'dirs': {
                                 'dirs_num': dirs_num, 
                                 'dirs_create_per_sec':dirs_create_per_sec,
                                 'dirs_removal_per_sec':dirs_removal_per_sec}
                       ,'files':{
                                 'files_num':files_num,
                                 'files_create_per_sec': files_create_per_sec,
                                 'files_removal_per_sec': files_removal_per_sec
                                }
                       }
                                    
                                 
    json_string = json.dumps(metadata_json, sort_keys=True, indent=4)+"\n"
    return json_string
    
if __name__ == "__main__":
    fdtree_output = sys.stdin.read()
    fdtree_json_output = extract_fdtree_json_output(fdtree_output)
    fdtree_output_file = open(sys.argv[1], "w+")
    fdtree_output_file.write(fdtree_json_output)
    fdtree_output_file.close()
    
    
