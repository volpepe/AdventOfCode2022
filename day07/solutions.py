from typing import List, Tuple

from aocd import get_data
from dotenv import load_dotenv

class File():
    '''
    Represents a file, with a name and a size.
    '''
    def __init__(self, name:str, size:int) -> None:
        self.name = name
        self.size = size

    def get_size(self):
        return self.size

    def get_name(self):
        return self.name


class Folder():
    '''
    Represents a folder, with a name, a parent folder and a list of files and folders it contains.
    Files and folders can be added to these lists as they are discovered.
    Its size can be computed recursively summing the size of files that are directly contained by the 
    folder with the size of files contained in children folders.
    '''
    def __init__(self, name:str, filelist:List, childlist:List, parent_dir=None) -> None:
        self.name = name
        self.parent_dir = parent_dir
        self.filelist = filelist
        self.childlist  = childlist
        self.size = None

    def get_name(self):
        return self.name

    def get_filelist(self):
        return self.filelist

    def get_dirlist(self):
        return self.childlist
    
    def get_parent_dir(self):
        return self.parent_dir

    def add_file(self, file):
        self.filelist.append(file)

    def add_children(self, folder):
        self.childlist.append(folder)

    def get_size(self):
        # Only compute size once, since structure doesn't change after initialization
        if self.size is None:
            # Sum of elements of current folder + sum of elements of contained folders
            self.size = sum(map(lambda f: f.get_size(), self.filelist)) + \
                        sum(map(lambda d: d.get_size(), self.childlist))
        return self.size


def create_filesystem(instructions:List[str]) -> Tuple[Folder, List[Folder]]:
    root_dir = Folder(name='/', filelist=[], childlist=[], parent_dir=None)
    current_dir = root_dir
    found_directories = [root_dir]
    for inst in instructions:
        if inst.startswith('$'):
            # COMMANDS
            # We only need to deal with cd, because ls just starts a sequence
            # of lines in the input where files and directories are discovered
            # and not dealt with here.
            if inst.startswith('$ cd'):
                # cd: change current directory
                # It makes the assumption that the directory we want to move
                # to has been discovered with ls first.
                dirname = inst.split(' ')[-1]
                # Is it cd .. or cd dirname or cd /?
                if dirname == '..': current_dir = current_dir.get_parent_dir() 
                elif dirname == '/': current_dir = root_dir
                else:
                    for child in current_dir.get_dirlist():
                        if child.name == dirname:
                            current_dir = child
                            break
        elif inst.startswith('dir'):
            # DIRECTORY DISCOVERY
            # Instantiate the directory and add it to the found ones
            dirname = inst.split(' ')[-1]
            dir = Folder(dirname, filelist=[], childlist=[], parent_dir=current_dir)
            found_directories.append(dir)
            # Also add this folder to the parent's childlist
            current_dir.add_children(dir)
        else:
            # FILE DISCOVERY
            # Add the file to the current directory's filelist
            size, filename = inst.split(' ')
            size = int(size)
            current_dir.add_file(File(filename, size))
    return root_dir, found_directories


if __name__ == '__main__':
    load_dotenv()
    lines = get_data(day=7, year=2022).splitlines()
    filesystem, found_directories = create_filesystem(lines)

    # Problem 1
    under_100000_sum = 0
    for dir in found_directories:
        dir_size = dir.get_size()
        if dir_size <= 100000:
            under_100000_sum += dir_size
    print(f'The sum of sizes of directories occupying at most 100000 is: {under_100000_sum}')
    
    # Problem 2
    total_space = 70000000
    needed_space = 30000000
    occupied_space = filesystem.get_size()
    delete_at_least = occupied_space - (total_space - needed_space)
    print(f"We need to delete at least {delete_at_least} from the device")
    sorted_dirs = sorted(found_directories, key=lambda dir: dir.get_size())
    for dir in sorted_dirs:
        dir_size = dir.get_size()
        if dir_size >= delete_at_least:
            break
    print(f"This can be achieved by removing dir {dir.get_name()}, occupying {dir.get_size()} of space")

            
    
    
    