#_*_ coding:utf-8 _*_

def lines(file):
    #生成器， 文本最后加一空行
    for line in file:
        yield  line
        yield  '\n'

def blocks(file):
    #生成器， 生成单独的文本块
    block = []
    for line in lines(file):
        #strip() 方法用于移除字符串头尾指定的字符（默认为空格）
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
