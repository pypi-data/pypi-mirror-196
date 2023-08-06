from copy import copy
import doctest
from pathlib import Path

import numpy as np


def read_mdfile(md_file: Path):
    '''
    读取.md文件内容，转换为“目录”列表

    >>> md_file = Path('./folder.md')
    >>> folders =  read_mdfile(md_file)
    '''
    lines = md_file.read_text(encoding='utf-8')
    folders = [i.strip() for i in lines.split('\n') if i.strip() != ""]
    return folders


def count_sharp(item: str):
    '''
    count the aoumnt of "#" in "item"

    >>> item = "## b1"
    >>> count_sharp(item)
    2
    '''
    import re
    pat = re.compile('^#+')

    mat = pat.match(item)
    if mat:
        return len(mat.group())


def retrive_folder(item: str):
    '''
    提取出目录名称

    >>> item = "### c1"
    >>> retrive_folder(item)
    'c1'
    '''
    import re
    pat = re.compile('[^#\s].*')
    return pat.findall(item)[0]


def get_index(num: list):
    '''

    >>> num = [1, 2, 2, 3, 1, 2, 3, 2]
    >>> get_index(num)
    [[0], [0, 1], [0, 2], [0, 2, 3], [4], [4, 5], [4, 5, 6], [4, 7]]
    '''
    stack = []
    rst = []
    _rst = []
    for n, i in enumerate(num):
        if len(stack) == 0 or stack[-1] < i:
            stack.append(i)
            _rst.append(n)
        else:
            while(len(stack) > 0 and i <= stack[-1]):
                stack.pop()
                _rst.pop()
            stack.append(i)
            _rst.append(n)
        rst.append(copy(_rst))
    return rst


def main(argv=None):
    '''

    >>> md_file = './folder.md'
    >>> project_name = "sample_project"
    >>> main(md_file, project_name)
    '''
    import argparse
    parser = argparse.ArgumentParser(prog='create_porject_directories')
    parser.add_argument('--md_file', help='目录.md')
    parser.add_argument('--project_name', help='项目名称')
    args = parser.parse_args(argv)

    md_file = args.md_file
    project_name = args.project_name

    md_path = Path(md_file)
    project_path = Path(project_name)
    items = read_mdfile(md_path)
    num = [count_sharp(i) for i in items]
    folders = np.array([retrive_folder(i) for i in items])

    idx = get_index(num)

    for i in idx:
        fd = project_path / "/".join(folders[i])
        fd.mkdir(parents=True)


if __name__ == "__main__":

    main()
