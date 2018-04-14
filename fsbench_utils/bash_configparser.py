'''
Created on Jul 18, 2016

@author: roraoof
'''
separator = "="
keys = {}

def config_parser(path):
      
    with open(path) as f:
    
        for line in f:
            if separator in line:
    
                if line.startswith("#"):
                    continue
                name, value = line.split(separator, 1)
                value = (value.rstrip('\n').strip("\""))
                value = value.split(' ')
                
                if len(value) > 1:
                    keys[name.strip()] = value
                else:
                    keys[name.strip()] = value[0]
    
    return keys

if __name__ == "__main__":
    config_parser("/home/roraoof/workspace/Python/fsbench/config")