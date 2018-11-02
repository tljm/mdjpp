#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from jpp.options import default_options
from jpp.parse import JournalParserFilter

if __name__ == "__main__":

    import argparse

    description = '''MarkDown Journal PreProcessor'''

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    for option in (o for o in dir(default_options) if o.startswith('jpp_')):
        name = option[4:].replace("_","-")
        if isinstance(getattr(default_options,option),bool):
            parser.add_argument("--%s" % name,
                                action="store_true",
                                dest=name,
                                required=False)
        elif name.endswith('-tag'):
            parser.add_argument("--%s" % name,
                                action="append",
                                dest=name,
                                required=False,
                                default=list(),
                                type=str)
        else:
            parser.add_argument("--%s" % name,
                                action="store",
                                dest=name,
                                required=False,
                                default=getattr(default_options,option),
                                type=type(getattr(default_options,option)))
    
    args,jfiles = parser.parse_known_args()

    # change default options
    for option in (o for o in dir(default_options) if o.startswith('jpp_')):
        name = option[4:].replace("_","-")
        setattr(default_options,option,getattr(args,name))
    
    default_options.reparse_options()
    
    # detect index
    for jf in jfiles:
        if jf.endswith('index.mdj'):
            jfiles = [jfiles.pop(jfiles.index(jf))] + jfiles
            break

    jp = JournalParserFilter()
    
    for jfile_name in jfiles:
        with open(jfile_name) as jfile:
            jp.proceed(jfile)
        
    jp.finalize() # explicit call
    
