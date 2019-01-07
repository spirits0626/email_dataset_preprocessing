
# -*- coding: UTF-8 -*-

import os
import sys
import timeit
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer

##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    re_stopwords=re.compile('\u3000')#去除无用的'\u3000'字符
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    s=re_stopwords.sub('',s)
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s

##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',
                '':'Assigned to: ','':'=Enron',
                '':'Updated by','':'=Enron'}

    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr



# 英文标点集合
english_punctuations = {',', '.', ':', ';', "'", '`', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '>', '<','``','-','--','\"','~'}

start_str = ('x-','message-id:','date:','from:','mime-version:','content-type:','content-transfer-encoding:','cc:',
            'bcc:','to:', '  ','\t','subject:')
end_str=('enron.com,','enron.com,')

sr = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours',
      'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its',
      'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll",
      'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
      'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
      'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
      'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
      'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
      'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've",
      'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn',
      "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
      "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won',
      "won't", 'wouldn', "wouldn't","subject", "cn=jeff", "arnold/ou=gco/o=enron", "enron"}

def segment_file(src_file_path, dst_file_path):
    # 提取词干
    stemmer = LancasterStemmer()
    with open(src_file_path, 'r', encoding='iso-8859-1') as src_file:
        with open(dst_file_path, 'w', encoding='utf-8') as dst_file:
            for line in src_file:
                try:
                    line = line.rstrip().lower()
                    #print(line)
                    if line.strip()=='' or line.startswith(start_str) or line.endswith(end_str):
                        continue
                    tokens = nltk.word_tokenize(filter_tags(stemmer.stem(line)))
                    # 过滤掉标点
                    tokens = [token for token in tokens if token not in english_punctuations]
                    clean_tokens = tokens[:]
                    # 过滤掉停止词
                    for token in tokens:
                        if token in sr or len(token) < 6 or len(token)> 20 or token.isdigit() or bool(re.search(r'\d', token)) or "enron" in token or not bool(re.search('[a-z]', token)):
                            clean_tokens.remove(token)
                     # 提取词干
                    stem_tokens = []
                    for token in clean_tokens:
                        token = stemmer.stem(token).strip("[/='-]")
                        if len(token) >=  6 and token not in sr:
                            stem_tokens.append(token)
                    dst_file.write('\n'.join(stem_tokens))
                    if len(stem_tokens) > 0:
                        dst_file.write('\n')
                except Exception as ex:
                    print('\nError occurs when processing:', src_file_path)
                    print('Error line:', line)
                    print('Error:', ex)
                    return False
    return True


def segment_dir(root_dir_path):
    dst_root_dir_path = os.path.dirname(root_dir_path) + "/segment"
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
            dst_file_path = os.path.join(dst_dir_path, file_name + ".txt")

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
    # root_dir_path = 'C:/Users/Michael/Desktop/deleted_items'
    print('Start processing', root_dir_path)

    begin_time = timeit.default_timer()
    segment_dir(root_dir_path)
    end_time = timeit.default_timer()
    running_time = (end_time - begin_time) * 1000

    print('Completed! Running time is {:.3f} ms'.format(running_time))
