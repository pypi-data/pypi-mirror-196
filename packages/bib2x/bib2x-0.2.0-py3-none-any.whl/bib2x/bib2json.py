from __future__ import print_function
# ===================================================================
# bib2x - A BibTex to HTML (and JSON) converter.
# Version 2.0.
#
# Main module
#
# (c) Daniel Krajzewicz 2011-2014, 2023
# - daniel@krajzewicz.de
# - http://www.krajzewicz.de
# - https://github.com/dkrajzew/degrotesque
# - http://www.krajzewicz.de/blog/degrotesque.php
# 
# Available under the BSD license.
# ===================================================================


# --- imports -------------------------------------------------------
import os
import sys
import re
import sqlite3


# --- debugging options ---------------------------------------------
DEBUG_SPECIAL_RECOGNITION = False
DEBUG_SPECIAL_CODING = False
DEBUG_UNKNOWN_CMD = False


# --- functions -----------------------------------------------------
def _lengthSorter(a, b):
    return len(a)-len(b)


# --- classes -------------------------------------------------------
class TeXfile:
    def __init__(self):
        self._stringMap = {}
        self._stringMapKeys = []
        DB = os.path.join(os.path.dirname(__file__), 'tex.db')
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute('SELECT * FROM styles')
        self._tex_styles = cur.fetchall()
        cur.execute('SELECT * FROM stylesp')
        self._tex_styles_pref = cur.fetchall()
        cur.execute('SELECT * FROM conv')
        self._tex_conv = cur.fetchall()
        cur.execute('SELECT * FROM repl')
        self._tex_repl = cur.fetchall()

    def _decodeCommand(self, cmd, optArgs, content, ret):
        if DEBUG_SPECIAL_RECOGNITION: print "decode: '" + cmd + "/" + content + "'"
        if cmd=='\\':
            if DEBUG_SPECIAL_RECOGNITION: print ">!3"
            return content, False
        for t in self._tex_styles:
            if cmd == t[0]:
                r = str(t[1])
                r = r.replace("%s", content)
                r = r.replace("%a", optArgs)
                if DEBUG_SPECIAL_RECOGNITION: print ">" + r
                return r, False
        for t in self._tex_styles_pref:
            if cmd == t[0]:
                if DEBUG_SPECIAL_RECOGNITION: print ">!1"
                ret["pref"] = True
                return "", False
        for t in self._tex_conv:
            if cmd.startswith(t[0]):
                r = str(t[1].strip())
                if DEBUG_SPECIAL_RECOGNITION: print ">" + r + cmd[len(t[0]):]
                removeSpaces = t[0][1].isalpha()
                return r + cmd[len(t[0]):], removeSpaces
        cmd2 = cmd + content
        for t in self._tex_conv:
            if cmd2.startswith(t[0]):
                r = str(t[1].strip())
                if DEBUG_SPECIAL_RECOGNITION: print ">" + r + cmd2[len(t[0]):]
                return r + cmd2[len(t[0]):], False
        ret["unfound"] = True
        if DEBUG_UNKNOWN_CMD: print "Unknown cmd '%s'" % cmd
        if cmd[0]=='\\':
            return cmd[1:], False
        return cmd, False

    def _decodeCommand2(self, cmd, optArgs, content, w, beg, end, currPos):
        ret = {}
        r, s = self._decodeCommand(cmd, optArgs, content, ret)
        if "pref" in ret:
            for i in self._tex_styles_pref:
                if cmd==i[0]:
                    beg = beg + len(cmd)
                    while w[beg]==' ' or w[beg]=='\n':
                        beg = beg + 1
                    r, e = self._tex2html(w, beg, end)
                    if DEBUG_SPECIAL_RECOGNITION: print "> " + str(i[1]) + r + str(i[2])
                    return str(i[1]) + r + str(i[2]), end
        if "unfound" in ret and currPos<end-1 and w[currPos]=='\\':
            cmd = cmd + w[currPos+1:currPos+2]
            r, s = self._decodeCommand(cmd, optArgs, "", ret)
            currPos += 2
        if s:
            if DEBUG_SPECIAL_RECOGNITION: print "here's s"
            currPos = self._skipSpaces(w, currPos)
        return r, currPos
    
    def _findMatchingBracket(self, w, beg, o="{", c="}"):
        i = beg
        l = 0
        while i<len(w):
            if w[i]==o:
                l = l + 1
            if w[i]==c:
                l = l - 1
                if l==0:
                    return i
            i = i + 1
        print "error: Missing closing bracket '%s'" % w[beg:]
        return len(w)
        
    def _skipSpaces(self, w, i):
        while i<len(w) and w[i].isspace():
            i = i + 1
        return i

    def _tex2html(self, w, beg=0, end=-1):
        #print "%s %s %s" % (w, beg, end)
        i = beg
        if end<0:
            end = len(w)
        else:
            end = min(len(w), end)
        r = ""
        while i<end:
            if w[i]=='\\':
                procB = i
                cmdEnd = -1
                optArgs = ""
                i = i + 1
                e1 = False
                while i<end and not e1:
                    if not e1 and w[i]=='[':
                        # optional parameter
                        cmdEnd = i
                        q = self._findMatchingBracket(w, i, "[", "]")
                        optArgs = ", " + w[i+1:q]
                        if DEBUG_SPECIAL_CODING: print "2a: %s %s %s" % (procB, i, optArgs)
                        i = q + 1
                    if not e1 and w[i]=='{':
                        # escaped command, with a bracketed parameter
                        if DEBUG_SPECIAL_CODING: print "2: %s %s %s" % (procB, i, w)
                        q = self._findMatchingBracket(w, i)
                        dec, e = self._tex2html(w, i+1, q)
                        if cmdEnd<0: cmdEnd = i
                        t1, i = self._decodeCommand2(w[procB:cmdEnd].strip(), optArgs, dec, w, beg, end, i)
                        r = r + t1
                        i = q + 1
                        e1 = True                    
                    if not e1 and w[i]=='|':
                        # escaped command, with a bracketed parameter
                        if DEBUG_SPECIAL_CODING: print "2b: %s %s %s" % (procB, i, w)
                        q = w.find('|', i+1)
                        dec, e = self._tex2html(w, i+1, q)
                        if cmdEnd<0: cmdEnd = i
                        t1, i = self._decodeCommand2(w[procB:cmdEnd].strip(), optArgs, dec, w, beg, end, i)
                        r = r + t1
                        i = q + 1
                        e1 = True
                    if not e1 and w[i]=='\\' and i==procB+1:
                        if DEBUG_SPECIAL_CODING: print "1b: %s %s %s %s %s" % (procB, i, w, len(w), end)
                        r = r + "<br/>"
                        i = self._skipSpaces(w, i + 1)
                        e1 = True 
                    if not e1 and (w[i]==' ' or w[i]=='\\' or (i>=procB+2 and not w[i].isalpha() and w[procB+1].isalpha())):
                        # escaped command, closed by a trailing blank
                        if DEBUG_SPECIAL_CODING: print "1: %s %s %s %s %s" % (procB, i, w, len(w), end)
                        t1, i = self._decodeCommand2(w[procB:i].strip(), optArgs, "", w, beg, end, i)
                        r = r + t1
                        e1 = True
                    if not e1:
                        i = i + 1
                if i==end and not e1:
                    if DEBUG_SPECIAL_CODING: print "3: %s %s %s %s %s" % (procB, i, w, len(w), end)
                    t1, i = self._decodeCommand2(w[procB:i].strip(), optArgs, "", w, beg, end, i)
                    r = r + t1
            elif w[i]=='{':
                q = self._findMatchingBracket(w, i)
                if DEBUG_SPECIAL_CODING: print "4: %s %s %s" % (i, q, w[i+1:q])
                dec, i = self._tex2html(w, i+1, q)
                if DEBUG_SPECIAL_CODING: print "t1: %s %s %s %s" % ("hallo", i, w[i-2:i+2], dec)
                r = r + dec
                i = q + 1
                if DEBUG_SPECIAL_CODING: print "t2: %s %s %s %s %s" % ("hallo", i, w[i-2:i+2], end, r)
            elif w[i]=='$':
                q = w.find('$', i+1)
                if q<0:
                    print "unclosed special character $"
                    q = i
                if DEBUG_SPECIAL_CODING: print "5: %s %s %s" % (i, q, w[i+1:q])
                dec, i = self._tex2html(w, i+1, q)
                r = r + dec
                i = q + 1
            else:
                if w[i]=='\n':
                    r = r + ' '
                else:
                    r = r + w[i]                    
                i = i + 1
        for t in self._tex_repl:
            r = r.replace(str(t[0]), str(t[1]))
        r2 = ""
        html = False
        for j in range(0, len(r)):
            if r[j]=='<':
                html = True
            elif r[j]=='>':
                html = False
            if r[j]=='"' and not html:
                r2 = r2 + "&quot;"
            elif r[j]=="'" and not html:
                r2 = r2 + "&rsquo;"
            else:
                r2 = r2 + r[j]
        r = r2            
        r = re.sub("\s+" , " ", r)
        return r, i    
                

    def _splitHTMLaware(self, what):
        """Splits the given string at ';' and ',', assuring that a split
             is not done if the occured ';' belongs to a HTML-encoded special
             character"""
        ret = []
        b = 0
        isHTML = False
        for i in range(0, len(what)):
            if what[i]=='&':
                isHTML = True
            if what[i]==',' or (what[i]==';' and not isHTML):
                ret.append(what[b:i].strip())
                b = i+1
            if what[i]==';':
                isHTML = False
        ret.append(what[b:].strip())
        return ret
                    

    def _convValue(self, value, lastItem):
        # this may be the document ending bracket
        if lastItem and value[-1]=="}":
            value = value[:-1]
        if value in self._stringMap:
            value = self._stringMap[value]
        else:
            value, e = self._tex2html(value)
            value = value.replace('"', "\\\"")
            b = value.find("\\")
            while b>=0:
                if b<len(value)-1 and value[b+1:b+2]!='\\' and value[b+1:b+2]!='"':
                    value = value[:b] + '\\' + value[b:]
                    b = value.find("\\", b+2)
                else:
                    b = value.find("\\", b+1)
        return value
    
    def _escaped(self, src, i):
        if i==0:
            return False
        return src[i-1]=='\\'

    def _getNext(self, src, i):
        i1 = src.find("=", i)
        if i1<0:
            return "", "", -1, False
        key = src[i:i1].strip().lower();
        i1 += 1
        i2 = i1
        no = 0
        odelim = ""
        cdelim = ""
        completeValue = ""
        while True:
            if not src[i2:i2+1].isspace():
                if no==0 and odelim=="":
                    i1 = i2
                    if src[i2:i2+1]=="{":
                        odelim = "{"
                        cdelim = "}"
                    elif src[i2:i2+1]=='"':
                        odelim = '"'
                        cdelim = '"'
                        i2 += 1
                    else:
                        odelim = ","
                        cdelim = ","
                        i1 = i1 - 1
                if src[i2:i2+1]==odelim and (i2==0 or src[i2-1:i2]!="\\"):
                    no = no + 1
            if (src[i2:i2+1]=='#' and no==0 and not self._escaped(src, i2)):
                if DEBUG_SPECIAL_CODING: print "%s %s %s" % (src[i2-2:i2+2], src[i2-1:i2], self._escaped(src, i2))
                value = src[i1+1:i2].strip()
                completeValue = completeValue + self._convValue(value, cdelim=="," and len(src)==i2)
                i1 = i2 + 1
                i2 = i2 + 1
                if i2>=len(src):
                    return key, completeValue, i2+1, True
                no = 0
                odelim = ""
                cdelim = ""
            elif len(src)==i2 or (src[i2:i2+1]==cdelim and (i2==0 or src[i2-1:i2]!="\\")):
                no = no - 1
                if len(src)==i2 or no==0:
                    value = src[i1+1:i2]#.strip()
                    if odelim=='{':
                        value = value.strip()
                    #print "        %s %s" % (value, len(src))
                    completeValue = completeValue + self._convValue(value, cdelim=="," and len(src)==i2)
                    while i2<len(src):
                        i2 = i2 + 1
                        if src[i2-1]=='#':
                            break
                        if src[i2-1]==',' or src[i2-1]=='}':
                            return key, completeValue, i2+1, True    
                    if i2==len(src):
                        return key, completeValue, i2+1, True
                    no = 0
                    odelim = ""
                    cdelim = ""
            i2 += 1



    def read2string(self, file, skipComments=True, convertSpaces=True):
        fdi = open(file)
        c = []
        for l in fdi.readlines():
            if skipComments:
                if len(l)>0 and l[0]=='%':
                    continue
            c.append(l)
        fdi.close()
        c = " ".join(c)
        if convertSpaces:
            c = c.replace("\t", " ")
        return c



    def parse(self, c, handler):
        b1 = 0
        while b1<len(c):
            b1 = c.find("@", b1)
            if b1<0:
                break;
            i1 = c.find("{", b1+1)
            if i1<0:
                break;
            e1 = self._findMatchingBracket(c, i1)
            e = c[b1+1:e1+1]
            i1 = e.find("{")
            b1 = e1
            entryType = e[:i1].strip()
            if entryType.lower()=="string" or entryType.lower()=="comment":
                t = e[i1+1:-1]
                b = t.find("=")
                key = t[:b].strip()
                value = t[b+1:].strip()
                if value[0]=='"' and value[-1]=='"':
                    value = value[1:-1]
                v, e = self._tex2html(value)
            if entryType.lower()=="string":
                handler.addStringDefinition(key, v)
                self._stringMap[key], e = self._tex2html(value)
                self._stringMapKeys.append(key)
                self._stringMapKeys.sort(_lengthSorter)
                self._stringMapKeys.reverse()
                continue
            if entryType.lower()=="comment":
                handler.addComment(key, value)
                continue
            i2 = e.find(",", i1)
            entryID = e[i1+1:i2]
            print "%s %s" % (entryID, i1)
            handler.startEntry(entryID)
            handler.addField(entryID, "bibtex-type", entryType)
            #entry = entry + '    "%s":{\n' % id
            #entry = entry + '     "bibtex-type":"%s"' % entryType
            haveNext = True
            #hadOne = True
            i2 += 1
            while haveNext:
                key, value, i2, haveNext = self._getNext(e, i2)
                if haveNext:
#                    if hadOne:
#                        entry = entry + ",\n"
                    hadOne = True
                    if key=="keywords":
                        w = self._splitHTMLaware(value)
                        w = filter(len, w)
                        #entry = entry + '     "%s":%s' % (key, w)
                        handler.addField(entryID, key, w)
                    elif key=="author" or key=="editor":            
                        value = value.replace(" AND ", " and ")
                        if value.find(" and ")>=0:
                            w = value.split(" and ")
                        else:
                            w = [ value ]
                        #entry = entry + '     "%s":%s' % (key, w)
                        handler.addField(entryID, key, w)
                    elif key=="file":
                        value = value.replace("http//", "http://").replace("http\\:", "http:").replace("http\\\\:", "http:")
                        a1 = value.find(':')
                        a2 = value.rfind(':')            
                        w = [ value[:a1], value[a1+1:a2], value[a2+1:] ]
                        #print w
                        if len(w)==3 and len(w[1])!=0:# and w[2].lower()=="url":
                            #entry = entry + '     "%s":{"name":"%s","url":"%s"}' % (key, w[0], w[1])
                            pairs = []
                            pairs.append(["name", w[0]])                        
                            pairs.append(["url", w[1]])                        
                            handler.addField2(entryID, key, pairs)
                        else:
                            hadOne = False
                    elif key=="year":
                        a1 = value.find('.')
                        if a1>=0: value = value[value.rfind(".")+1:]
                        a1 = value.find('-')
                        if a1>=0: value = value[:a1]
                        a1 = value.find('&') # ndash/mdash - should maybe be split so that the information is preserved, but sorting is possible
                        if a1>=0: value = value[:a1]
                        year = 0
                        try: year = int(value)
                        except: pass
#                     entry = entry + '     "%s":%s' % (key, year)                                
                        handler.addField(entryID, key, year)
                    elif key=="pages":
                        value = value.replace("--", "&ndash;")
                        value = value.replace("-", "&ndash;")
                        value = value.replace(" ", "")
#                        entry = entry + '     "%s":"%s"' % (key, value)
                        handler.addField(entryID, key, value)
                    else:
                        handler.addField(entryID, key, value)
#                        entry = entry + '     "%s":"%s"' % (key, value)
                    if e[i2:i2+1]==",":
                        i2 += 1
#            if not firstEntry:
#                entry = ",\n" + entry
#                pass
#            else:
#                firstEntry = False
#            entry = entry + "\n    }" 
            handler.closeEntry(entryID)
        #    fdo.write(entry) 

class TeXhandler:
    def __init__(self):
        pass
        
    def addStringDefinition(self, key, v):
        pass
        
    def addComment(self, key, v):
        pass
        
    def startEntry(self, entryID):
        pass

    def addField(self, entryID, key, v):
        pass

    def addField2(self, entryID, ukey, key, v):
        pass

    def closeEntry(self, entryID):
        pass



class JSONexportingTeXhandler(TeXhandler):
    def __init__(self, fdo):
        self._entry = ""
        self._firstEntry = True
        self._fdo = fdo
        self._hadOne = False
        fdo.write("var bib={\n \"entries\":{\n")

    def addStringDefinition(self, key, v):
        pass
        
    def addComment(self, key, v):
        pass
        
    def startEntry(self, entryID):
        self._hadOne = False
        self._entry = ""
        self._entry = self._entry + '    "%s":{\n' % entryID

    def addField(self, entryID, key, v):
        if self._hadOne:
            self._entry = self._entry + ",\n"
        if isinstance(v, int):
            self._entry = self._entry + '     "%s":%s' % (key, v)
        elif isinstance(v, list):
            self._entry = self._entry + '     "%s":%s' % (key, v)
        else:
            self._entry = self._entry + '     "%s":"%s"' % (key, v)
        self._hadOne = True

    def addField2(self, entryID, key, pairs):
        if self._hadOne:
            self._entry = self._entry + ",\n"
        self._entry = self._entry + '     "%s":{' % (key)
        r = []
        for p in pairs:
                r.append('"%s":"%s"' % (p[0], p[1]))
        self._entry = self._entry + ",".join(r)
        self._entry = self._entry + '}'
        self._hadOne = True

    def closeEntry(self, entryID):
        if not self._firstEntry:
            self._entry = ",\n" + self._entry
        else:
            self._firstEntry = False
        self._entry = self._entry + "\n    }" 
        self._fdo.write(self._entry) 




class StoringTeXhandler:
    def __init__(self):
        self._entries = {}
        self._entryIDs = []
        self._stringMap = {}
        self._stringMapKeys = []
        
        self._groupNames = []
        self._groups = {}

        
    def addStringDefinition(self, key, v):
        self._stringMap[key] = v
        self._stringMapKeys.append(key)
        
    def addComment(self, key, v):
        # !!! only for JabRef
        if not v.strip().startswith("jabref-meta: groupstree"):
            return
        v = v[v.find("0"):]
        lines = v.split("\n")
        c = ""
        tree = []
        lastLevel = 0
        for l in lines:
            c = c + l.strip()
            i = c.rfind(";")
            #print "%s %s %s %s" % (i, len(c)-1, c[i-2], c[i-2-5:])
            if i==len(c)-1 and len(c)>2 and c[i-1]!='\\':
                d = c[:c.find("\\;")].strip()
                level = int(d[:d.find(" ")])
                name = d[d.find(":")+1:]
                if level<=lastLevel:
                    tree = tree[:-(lastLevel - level + 1)]
                lastLevel = level
                tree.append(name)
                
                if level!=0:
                    d = c[c.find(";")+1:].strip()
                    d = d[d.find(";")+1:d.rfind(";")]
                    items = filter(None, d.split("\;"))
                    gName = "/".join(tree)
                    if gName not in self._groupNames:
                        self._groupNames.append(gName)
                    if gName not in self._groups:
                        self._groups[gName] = []
                    self._groups[gName].extend(items)
                #print "------------\n" + c[:20]
                c = ""
#        for g in self._groups:
#            print g
#            for i in self._groups[g]:
#                print " " + i
        
    def startEntry(self, entryID):
        self._entries[entryID] = {}
        self._entryIDs.append(entryID)

    def addField(self, entryID, key, v):
        self._entries[entryID][key] = v

    def addField2(self, entryID, ukey, key, v):
        if ukey not in self._entries[entryID]:
            self._entries[entryID][ukey] = {}
        self._entries[entryID][ukey][key] = v

    def closeEntry(self, entryID):
        pass





# --- main
def main(argv):
        texF = TeXfile()
        c = texF.read2string(argv[1])
        fdo = open(argv[2], "w")
        h = JSONexportingTeXhandler(fdo)
        texF.parse(c, h)
        fdo.write("\n }\n};\n")


# -- main check
if __name__ == '__main__':
        main(sys.argv)
