'''
Created on Jul 18, 2016

@author: roraoof
'''
import ConfigParser

class FakeSecHead(object):
    def __init__(self, fp):
        self.fp = fp
        self.sechead = '[asection]\n'

    def readline(self):
        if self.sechead:
            try: 
                return self.sechead
            finally: 
                self.sechead = None
        else: 
            return self.fp.readline()
        

def config_parser(path):
    cp = ConfigParser.SafeConfigParser()
    cp.readfp(FakeSecHead(open(path, 'r')))
    config = dict((x,y) for x,y in  cp.items('asection'))
    return config