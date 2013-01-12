#/usr/bin/python2
#-*-code=utf8-*-

import os
import argparse
from lxml import etree
from collections import defaultdict


class RCFTbuilder:
    '''
    build rcft(relational context family) for erca from extracted relation xml file
    '''

    def __init__(self):
        self.emp = "   "
        self.dem = "|"
        self.mrk = "x"

    def build(self, filename, relname, src):
        with open(filename) as xmlfile:
            rel = etree.parse(xmlfile)
            self._build(rel, relname, src)

    def _build(self, rel, relname, src):
        tgt = "rel2" if src == "rel1" else "rel1"
        root = rel.getroot()
        print root.tag
        print len(root)
        r = rel.xpath("/relations/relation[@name=$rname]", rname=relname)
        src_concept = set()
        tgt_concept = set()
        relation = defaultdict()
        if r:
            for c in r[0]:
                print c.tag, c.get(src),"=" ,c.get(tgt)
                srcrel = c.get(src)
                tgtrel = c.get(tgt)
                src_concept.add(srcrel)
                tgt_concept.add(tgtrel)
                relation[(srcrel, tgtrel)] = True
            rcf = (list(src_concept), list(tgt_concept), relation)
        for i in relation.values():
            print i
        des = os.path.join("rcft", relname.lower())
        if not os.path.exists(des):
            os.makedirs(des)
        outputfilename = os.path.join(des, src + '.rcft')
        self._write(rcf, relname, outputfilename)

    def buildall(self, filename):
        '''
        build the rcft file for all of the relations
        '''
        def getrellist(rel):
                root = rel.getroot()
                for r in root:
                    yield r.get('name')

        with open(filename) as xmlfile:
            rel = etree.parse(xmlfile)
            for relname in getrellist(rel):
                self._build(rel, relname, "rel1")
                self._build(rel, relname, "rel2")

            #self._build(rel, relname, src)


    def _write(self, rcf, relname, rcftfilename):
        '''
        write rcf file to rcftfile
        '''
        with open(rcftfilename, 'w') as rcftfile:
            # first deal with binary context
            # then deal with relations
            rcftfile.write(self._build_src(rcf[0], "context1"))
            rcftfile.write(os.linesep)
            rcftfile.write(self._build_tgt(rcf[1], "context2"))
            rcftfile.write(os.linesep)
            rcftfile.write(self._build_rel(rcf, relname, "context1", "context2"))
            rcftfile.write(os.linesep)

    def _build_src(self, src, concept_name):
        '''
        build string for source formal concept
        '''
        content = "FormalContext "+ concept_name + os.linesep + self.dem + self.emp + self.dem + os.linesep
        for i in src:
            content += self.dem + i + self.dem + os.linesep
        return content

    def _build_tgt(self, tgt, concept_name):
        '''
        build string for target formal concept
        '''
        # build the header of the context
        content = "FormalContext "+ concept_name + os.linesep + self.dem + self.emp + self.dem
        for i in tgt:
            content += 'name :' + i + self.dem
        content += os.linesep
        for i in range(len(tgt)):
            content += self.dem + tgt[i] + self.dem + self.dem.join([self.mrk if j==i else self.emp for j in range(len(tgt)) ])
            content += self.dem + os.linesep
        return content

    def _build_rel(self, rcf, relname, srcname, tgtname):
        '''
        build string for relation concept
        '''
        content = "RelationalContext "+ relname + os.linesep
        content += "source " + srcname + os.linesep
        content += "target " + tgtname + os.linesep
        content += "scaling com.googlecode.erca.framework.algo.scaling.Wide" + os.linesep

        # build header
        content += self.dem + self.emp + self.dem
        for i in rcf[1]:
            content += i + self.dem
        content += os.linesep

        for i in rcf[0]:
            content += self.dem + i + self.dem + self.dem.join([self.mrk if rcf[2].get((i, rcf[1][j])) == True else self.emp for j in range(len(rcf[1]))])
            content += self.dem + os.linesep
        return content

def main():
    parser = argparse.ArgumentParser(description="Build rcft from extracted xml file which describes the relations")
    parser.add_argument("filename", help="the name of xml file")
    parser.add_argument("relname", help="the name of relation that needs to be built")
    parser.add_argument("--src", type=str, choices=["rel1", "rel2"], default="rel1", help="specify which context is the source")
    args = parser.parse_args()
    rcftbuilder = RCFTbuilder()
    rcftbuilder.build(args.filename, args.relname, args.src)
    rcftbuilder.buildall(args.filename)

if __name__ == '__main__':
    main()
