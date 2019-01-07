
# -*- coding: UTF-8 -*-

import os
import sys
import timeit
import re

'''
只使用与较小的文件，比较大的文件运行时间长
'''
def segment_file(src_file_path,dst_file_path):

    infopen = open(src_file_path,'r',encoding='utf-8')
    outopen = open(dst_file_path,'w',encoding='utf-8')
    lines = infopen.readlines()
    list_1 = set()
    for line in lines:
        try:
            if line not in list_1:
                list_1.add(line)
                outopen.write(line)
        except Exception as ex:
            print('\nError occurs when processing:', src_file_path)
            print('Error line:', line)
            print('Error:', ex)
            return False
    return True



def segment_dir(root_dir_path):
    dst_root_dir_path = os.path.dirname(root_dir_path) + "/remove"
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
            result = segment_file(src_file_path, dst_file_path)
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

    print('Start processing', root_dir_path)

    begin_time = timeit.default_timer()
    
    segment_dir(root_dir_path)
    
    end_time = timeit.default_timer()
    running_time = (end_time - begin_time) * 1000

    print('Completed! Running time is {:.3f} ms'.format(running_time))
