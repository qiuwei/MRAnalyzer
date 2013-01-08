#/usr/bin/python2
#-*-code:utf8 -*-
import re
import argparse
from collections import defaultdict
from lxml import etree

def parse(filename):
    '''parse all of the input file and extract all relations and store it into list'''
    with open(filename) as f:
        rel_data = defaultdict(list)
        sent_data = defaultdict(None)
        for line in f.readlines():
            #deal with each line
            if not re.match(r'^\s*$', line):
                # deal with relation line
                if line.endswith("||\n"):
                    t = line.split('|')
                    rel = t[8]
                    record = (t[0], t[3], t[10])
                    rel_data[rel].append(record)
                #deal with sentence line
                elif not line.endswith("-----\n"):
                    match = re.match(r'(.*?)\s(.*)', line)
                    if match:
                        sent = (match.group(1), match.group(2))
                        sent_data[sent[0]] = sent[1]

        #sort rel_data keys according to the length of its values
        root = etree.Element('relations')
        for i in sorted(rel_data.keys(), key=lambda k:len(rel_data[k])):
            relchild = etree.Element('relation',name=i, number=str(len(rel_data[i])))
            for t in rel_data[i]:
                inschild = etree.Element('sent', ID=t[0],rel1=t[1], rel2=t[2])
                inschild.text= sent_data[t[0]]
                relchild.append(inschild)
            root.insert(0,relchild)

        s = etree.tostring(root, pretty_print=True)
        print s

def check():
    '''check whether the relation extracted is right all not'''
    pass

def main():
    parser = argparse.ArgumentParser(description='Extract relations out from plain relation txt file')
    parser.add_argument("filename", help="path to the plain relation txt file")
    args = parser.parse_args()
    parse(args.filename)
    #parse("test1")

if __name__ == '__main__':
    main()
