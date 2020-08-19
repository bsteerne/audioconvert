import os
import sys
import shutil
from dataclasses import dataclass, field
from enum import Enum



@dataclass
class Converter:
    input_dir : str = r'M:\Music\ConvertedMusic'
    input_ext : list = field(default_factory=lambda: ['.flac', '.acc', '.ogg', '.m4a', '.M4A', '.wav', '.mp3'])
    inplace : bool = True
    output_dir : str = r'M:\Music\ConvertedMusic'
    output_ext : str  = '.mp3' 
    convert_cmd : str = r'.\ffmpeg.exe -i "{0}" -codec:a libmp3lame -qscale:a 0 "{1}"'


    
    def generate_file_list(self):
        print('Generating list: {}'.format(self.input_dir))
        for root, subdirs, files in os.walk(self.input_dir):   
            for filename in files:
                file_path = os.path.join(root, filename)
                ext = os.path.splitext(file_path)[1]

                if not ext in self.input_ext:
                    if not ext in self.found_ext:
                        self.found_ext[ext] = 0
                    
                    
                    self.found_ext[ext] += 1
                    continue
                
                new_file_path = os.path.splitext(file_path.replace(self.input_dir, self.output_dir) if not self.inplace else file_path)[0] + self.output_ext

                if ext == self.output_ext:
                    action = Actions.nothing if self.inplace else Actions.copy
                elif self.inplace:
                    action = Actions.convert_and_delete
                else:
                    action = Actions.convert

                self.file_list.append((file_path, new_file_path, action))

    def execute(self):
        if len(self.file_list) == 0:
            self.generate_file_list()


        for (inp, outp, action) in self.file_list:
            inp_enc = inp.replace('"', '""')
            outp_enc = outp.replace('"', '""')
            folder = os.path.split(outp)[0] 
            
            if not os.path.exists(folder):
                print("Creating folder: {}".format(folder))
                os.makedirs(folder)
            
            if action == Actions.convert:
                print("Convert: '{}'".format(inp))
                # str = self.convert_cmd.format(inp_enc, outp_enc)
                # print(str)
                # os.system(str)
            elif action == Actions.convert_and_delete:
                pass
                print("Convert: '{}'".format(inp))
                str = self.convert_cmd.format(inp_enc, outp_enc)
                os.system(str)
                print("Removing: {}".format(inp)) 
                os.remove(inp) 
            elif action == Actions.copy:
                print("Copy: '{}".format(inp))
                shutil.copy(inp, outp)
            else:
                pass
                

                


    def __post_init__(self):
        self.found_ext = {}
        self.file_list = []
    

class Actions(Enum):
    nothing = 1
    copy = 2
    convert = 3
    convert_and_delete = 4

if __name__ == "__main__":
    c = Converter()
    c.execute()

    print('Found the following non processed extentions: {}'.format(c.found_ext))

