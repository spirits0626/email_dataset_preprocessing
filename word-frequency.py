# -*- coding: UTF-8 -*-

import os
import sys
import timeit
import re
from collections import Counter
from functools import reduce
from operator import add
from pathlib import Path

def word_frequency(root_dir_path):

        ps = Path(root_dir_path).rglob('*.txt')
        
        #for p in ps:
        # print(p)
        c = reduce(add, [Counter(p.read_text().split()) for p in ps])
        result = c.most_common()
        return result;

def write_to_file(result, dst_file_path, threshold):

    with open(dst_file_path, 'w', encoding='utf-8') as dst_file:
        for res in result:
            if res[1] > int(threshold):
                dst_file.write(str(res[0]) + '\n')
            #print(res)

    
if __name__ == '__main__':


    
    begin_time = timeit.default_timer()
    print('Start processing\n')
    root_dir_path = sys.argv[1]
    result = word_frequency(root_dir_path)

    # 将出现频率超过阈值的单词写入文件中
    threshold1 = sys.argv[2]
    dst_file_path1 = os.path.join(root_dir_path, "word_frequency1.txt")
    write_to_file(result, dst_file_path1, threshold1)

    threshold2 = sys.argv[3]
    dst_file_path2 = os.path.join(root_dir_path, "word_frequency2.txt")
    write_to_file(result, dst_file_path2, threshold2)

    threshold3 = sys.argv[4]
    dst_file_path3 = os.path.join(root_dir_path, "word_frequency3.txt")
    write_to_file(result, dst_file_path3, threshold3)
    
    end_time = timeit.default_timer()
    running_time = (end_time - begin_time) * 1000

    print('Completed! Running time is {:.3f} ms'.format(running_time))

