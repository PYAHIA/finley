"""
TO DO:
    
Add complete target handling (ignore hints,handle merges, and swaps)
"""
import re
import os

class Procedure():

    def __init__(self, file):
        with open(self.root_path+os.sep+file, 'r') as f:
            self.code = ' '.join(f.readlines())
            self.code = self.code.upper()
        self.parse_targets()
        self.parse_sources()

    def parse_targets(self):
        pattern = re.compile(r'INSERT\s+INTO\s+(.+\..+)')
        matches = re.findall(pattern, self.code)
        pattern2 = re.compile('CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(.+\..+)\s+AS')
        matches2 = re.findall(pattern2, self.code)
        targets = list(set(matches+matches2))

        self.targets = [target for target in targets if target.count('.') == 1]
        
    def parse_sources(self):
        pattern = re.compile(r'FROM\s+(\S+)\s+')
        matches = re.findall(pattern, self.code)
        pattern2 = re.compile(r'JOIN\s+(\S+)\s+')
        matches2 = re.findall(pattern2, self.code)
        sources = list(set(matches + matches2))
        
        self.sources = [source for source in sources if source.count('.') == 1]

    @property
    def root_path(self):
        if os.name == 'nt':
            return r"C:/Users/pyahia/git/airflow-docker/repos"
        else:
            return r"opt/airflow/repos"


if __name__ == "__main__":
    script = r"dvd-dw/film_pre.sql"
    d = Procedure(script)

    print(d.targets)







