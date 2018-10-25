from jpp.tags import istag, maketag
from jpp.tags import Tag,Date,Verbatim,NoTag
from jpp.render import HTML

class JournalParser(object):
    
    def __init__(self):
        
        self.open_tags = [NoTag()]
        self.metastable_tag = None
        
        self.engine = HTML()
    
    def __del__(self):
        self.finalize()
    
    def printable(self,tag=None):
        return True
    
    def print(self,line):
        self.open_tags[-1].print(line)
        #print(line)
        
    def open_tag(self,tag):
        self.open_tags.append(tag)
        # print tag opening if current state is printable
        if self.printable(tag):
            self.print(self.engine.tag_opener(tag))
            self.print(self.engine.tag(tag))
            #self.print("OPEN: %s" % tag)
        
    def close_tag(self,tag):
        # check is tag closes last tag(s)
        #closed = []
        if self.open_tags:
            if isinstance(tag,type(self.open_tags[-1])):
                #closed.append(self.open_tags.pop(-1))
                closed_tag = self.open_tags.pop(-1)
                self.print(closed_tag)
                self.print(self.engine.tag_closer(closed_tag))
            elif isinstance(tag,Date) and Date in list(map(type,self.open_tags)):
                while True:
                    #closed.append(self.open_tags.pop(-1))
                    closed_tag = self.open_tags.pop(-1)
                    self.print(closed_tag)
                    self.print(self.engine.tag_closer(closed_tag))
                    #if isinstance(closed[-1],Date):
                    if isinstance(closed_tag,Date):
                        break
        if False:#closed:
            for tag in closed:
                if self.printable(tag):
                    self.print(self.engine.tag_closer(tag))
                    #self.print("CLOSE: %s" % tag)
        
    def proceed(self,source):
        """
        Proceed with source.
        """
        for line in source:
            line = line.rstrip()
            # not a tag!
            if not istag(line) and self.printable():
                if self.metastable_tag:
                    # open metastable tag
                    self.open_tag(self.metastable_tag)
                    self.metastable_tag = None
                # print line
                self.print(line)
            # tag!
            else:
                this_tag = maketag(line)
                # no metastable tag
                if not self.metastable_tag:
                    # make new metastable tag
                    self.metastable_tag = this_tag
                    # does new tag close last tag?
                    self.close_tag(this_tag)
                # metastable tag present
                else:
                    # is metastable tag or this tag of Date type?
                    if isinstance(self.metastable_tag,Date) or isinstance(this_tag,Date):
                        # open metastable tag
                        self.open_tag(self.metastable_tag)
                        # recreate metastable tag with new tag
                        self.metastable_tag = this_tag
                        # does new tag close last tag?
                        self.close_tag(this_tag)
                    else:
                        # add new tag to metastable tag
                        self.metastable_tag.append(this_tag)
    
    def finalize(self):
        for tag in self.open_tags[:0:-1]:
            self.close_tag(tag)
        if self.open_tags:
            # final tag left
            final_tag = self.open_tags.pop()
            self.final_printout(final_tag)
    
    def final_printout(self,tag):
        for line in tag.body:
            if isinstance(line,Tag):
                self.final_printout(line)
            else:
                print(line)

            
            
                
