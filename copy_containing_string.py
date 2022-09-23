import os

source_dir = 'C:\\pycharm_workspaces\\pycharm_projects\\FF7R'
string_to_search = 'aerith'
target_dir = 'C:\\temp'

def run_fast_scandir(dir):
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            with open(f.path, 'rb') as file:
                # read all content of a file and search string
                file_contents = file.read()
                if str.encode(string_to_search) in file_contents:
                    # print('string found in file', f.path)
                    files.append(f.path)
                    target_file = target_dir+files[-1].replace(source_dir,'')
                    # print(target_file)
                    os.makedirs('\\'.join(target_file.split('\\')[:-1]), exist_ok=True)
                    with open(target_file, 'wb') as file_writer:
                        file_writer.write(file_contents)


    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir)
        subfolders.extend(sf)
        files.extend(f)

    return subfolders, files


subfolders, files = run_fast_scandir(source_dir)