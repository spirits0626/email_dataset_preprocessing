
# -*- coding: UTF-8 -*-

import os
import sys
import timeit
import re

def readfile(filename):
    with open(filename, 'r', encoding='iso-8859-1') as src_file:
        aa=set()
        for line in src_file:
            aa.add(line.strip('\n'))
        print(aa) #2.x请将此行改为 print aa
        return aa



def segment_file(src_file_path, dst_file_path, linelist):
    with open(src_file_path, 'r', encoding='iso-8859-1') as src_file:
        with open(dst_file_path, 'w', encoding='utf-8') as dst_file:
            for line in src_file:
                try:
                    if line.strip('\n') in linelist or line == "":
                        #print(line.strip('\n'))
                        continue
                    dst_file.write(line)
                except Exception as ex:
                    print('\nError occurs when processing:', src_file_path)
                    print('Error line:', line)
                    print('Error:', ex)
                    return False
    return True


def segment_dir(root_dir_path, linelist):
    dst_root_dir_path = os.path.dirname(root_dir_path) + "/filter"
    if not os.path.exists(dst_root_dir_path):
        os.mkdir(dst_root_dir_path)

    files_count = count_files(root_dir_path)
    processed_count = 0

    for dir_path, dir_names, file_names in os.walk(root_dir_path):

        for file_name in file_names:
            rel_dir_path = dir_path.replace(root_dir_path, '')
            if rel_dir_path.startswith('/') or rel_dir_path.startswith('\\'):
                rel_dir_path = rel_dir_path[1:]

            dst_dir_path = os.path.join(dst_root_dir_path, rel_dir_path)
            if not os.path.exists(dst_dir_path):
                os.makedirs(dst_dir_path)

            src_file_path = os.path.join(dir_path, file_name)
            dst_file_path = os.path.join(dst_dir_path, file_name)

            print('\r{}/{}'.format(processed_count, files_count), end='')
            # 对每个文件分词
            result = segment_file(src_file_path, dst_file_path, linelist)
            if not result:
                return

            processed_count += 1

    print('\r{}/{}'.format(processed_count, files_count))


def count_files(root_dir_path):
    count = 0

    for dir_path, dir_names, file_names in os.walk(root_dir_path):
        count += len(file_names)

    return count


if __name__ == '__main__':

    root_dir_path = sys.argv[1]
    word_fre_path = sys.argv[2]
    print('Start processing', root_dir_path)

    begin_time = timeit.default_timer()
    
    linelist = readfile(word_fre_path)
    segment_dir(root_dir_path, linelist)
    
    end_time = timeit.default_timer()
    running_time = (end_time - begin_time) * 1000

    print('Completed! Running time is {:.3f} ms'.format(running_time))
