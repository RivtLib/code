#!

from __future__ import division
from __future__ import print_function
from collections import OrderedDict
import os
from numpy import *
from once.calcheck import ModCheck
import once.config as cfg

__version__ = "0.9.0"
__author__ = 'rholland'

class ModDict(object):
    """Return an ordered dictionary of model operations.
    
     methods:
        get_mdict()
        _build_mdict()  # model operations dictionary
        _build_mdict
        _tag_e
        _tag_i
        _tag_lt
        _tag_r
        _tag_s
        _tag_t
        _tag_v    
    """
    def __init__(self):
        """Assemble dictionaries from models and sub-models
    
        """
        self.vbos = cfg.verboseflag
        self.el = ModCheck()
        self.mdict = OrderedDict()
        self.mfile = cfg.mfile
        self.mpath = cfg.mpath
        self.ppath = cfg.ppath
        self.mpathfile = os.path.join(self.mpath, self.mfile)
        with open(self.mpathfile, 'r') as modfile:
            self.model = modfile.readlines()
        if self.model[0][0:2]== '#-':
            self.model = self.model[1:]
        #print(self.model)
        self.mtags = ['#- ', '[r]', '[i]', '[v]', '[e]','[t]', '[s]']
        self.cnt = 0
        self.snum = self.snumchk = self.enum = 0
        self.dec1 = cfg.defaultdec                                                                                   
        try:                                             # set calc number                                                                                        
            self.cnum = int(self.mfile[1:5])
            self.calcnum = str(self.cnum)
            self.divcnum = str(self.calcnum)[0:2]
            self.modnum = str(self.calcnum)[2:4]
        except:
            self.calcnum = '0101'
            self.divnum = '01'
            self.modnum = '01'
        
    def get_mdict(self):
        """return model dictionary
    
        """
        return self.mdict
    
        
    def _build_mdict(self):
        """Build model dictionary.
        1[s]
         
         Each dictionary entry is processed in order. Unique keys 
         are generated by appending the model line number to the once tag. 
         A dictionary entry contains parameters delineated by
         commas, | or #- in the model file. Python comments that start
         at the beginning of a line are not stored.
    
        Operation keys, number of parameters and tags:
            _r + line number - 6 - [r] run 
            _i + line number - 6 - [i] insert
            _v + line number - 4 - [v] value            
            _e + line number - 8 - [e] equation
            _t + line number - 8 - [t] table
            _s + line number - 3 - [s] sections
            _y + line number - 2 - value heading
            _~ + line number - 1 - blank line
            _#               - 1 - control line
            _x + line number - 2 - pass-through text
            _lt              - 2 - license text [licensetext]
    
    
            [r]  p0   |   p1     |   p2    |   p3   |    p4   |   p5    
                'os'     command     arg1      arg2      arg3     arg4 
                'py'     script      arg1      arg2      arg3     arg4     
                 
            [i]  p0   |   p1      |  p2         |   p4      |   p5         
                'fig'   fig file    caption       size        location
                'fun'   mod file    func 1       func 2       func 3  
                'txt'  text file    wrap/literal   b,i        indent
                'csv'    csv        rst / doc      len          
                'mod'    model      rivets  
                'dat'    file       var name      rows       cols   
                        
            [v] p0   |  p1    |    p2     |    p3              
                var    expr     statemnt     descrip 
    
            [e] p0  |  p1   |  p2   |   p3    |  p4 | p5   |  p6  |  p7       
                var    expr   statemt  descrip  dec1  dec2   unit   eqnum
 
            
            [t] p0 |  p1   |  p2    |  p3  |  p4     |   p5   | p6   | p7 
                var  state1  state2   desc   outfile    dec1   un1    un2
            
            [s] p0     | p1        |  p2                 
                title   calc num     sect num           
        """
        il = ' '  # current line in model
        ip = ' '  # accumulator for multi-line operations
        pend = ' '
        pendlist = [ 'v', 'e']
        mtag = ' '
        for il in self.model:
            self.cnt += 1
            ils = il.strip()
            #print('ils',ils, len(ils))
            if len(ils) == 0:  mtag = '_~'              # blank line           
            elif '# ' in ils[0:3]:
                continue     # comment
            elif ils[:3] in self.mtags: mtag = ils[:3]  # registered tag
            else: mtag = '_x'                           # text                                          
            if pend in pendlist:
                if mtag == '_~':   # end accumulator
                    if pend == 'v': self._tag_v(ip)
                    if pend == 'e': self._tag_e(ip)
                    #if pend == 't': self._tag_t(ip)
                    ip = ' '                            # reset accumulator
                    pend = ' '
                    mkey = '_~' + str(self.cnt)
                    self.mdict[mkey] = ' '
                    continue
                else:                                   # accumulate multi-line
                    ip += il
                    continue
            #print('mtag', mtag, ils)                   # debug-tags

            if mtag in self.mtags:
                #print ('tag #-', il)
                if mtag == '#- ':
                    mkey = '_#' + str(self.cnt)
                    self.mdict[mkey] = il.rstrip('\n')
                    continue
                elif mtag == '[r]':
                    self._tag_r(il)
                elif mtag == '[i]':
                    self._tag_i(il)
                elif mtag == '[v]':
                    ip += il
                    pend = 'v'
                elif mtag == '[e]':
                    ip += il
                    pend = 'e'
                elif mtag == '[t]':
                    ip += il
                    pend = 't'
                elif mtag == '[s]':
                    self._tag_s(il)
                continue  
            if mtag == '_~':
                mkey = '_~' + str(self.cnt)
                self.mdict[mkey] = ' '
                continue
            elif mtag == '_x':                      # pass through text
                mkey = '_x' + str(self.cnt)         
                self.mdict[mkey] = [il]
            else: pass
        #for il in self.mdict: print(self.mdict[il])
    
    def _tag_r(self, block):
        """Add [r] run
        1[s]
    
         key:
         values:
            [r]   p0 |   p1   |   p2     |   p3    |   p4   |    p5   |   p6    
                        'os'     command     arg1      arg2      arg3     arg4 
                        'py'     script      arg1      arg2      arg3     arg4        
        """
        self.enum += 1
        if self.snum > self.snumchk:
            self.enum = 1
            self.snumchk = self.snum
        enumb = ' [' + str(self.snum) + '.' + str(self.enum) + ']'
    
        ivect = block.splitlines()
        fname = ivect[1].split('|')[0]
        var2 = ivect[1].split('|')[1].strip()
        ref = ivect[0].strip()
    
        # set dictionary values
        mkey = '_f' + str(self.cnt)
        self.mdict[mkey] = ['[f]', fname, var2, ref, enumb]
    
    def _tag_i(self, linep):
        """Add [i] insert
        1[s]

            key: _i           
            Dictionary Value:
                 p0    |  p1    |   p2     |  p3     |   p4            
                'fig'     figure   caption   size   location
                'tex'     text     
                'mod'     model
                'fun'     function   var name   reference 
                'rea'     file       var name   vector or table
                'wri'     file       var nam             
        """
        # set dictionary values
        lp = (linep.strip())[3:].split('|')
        #print('lp',lp)
        lp0 = lp[0].strip()
        lp1 = lp[1].strip()
        lp2 = lp[2].strip()
        lp3 = lp[3].strip()
        lp4 = lp[4].strip()
        mkey = '_i' + str(self.cnt)
        self.mdict[mkey] = [lp0, lp1, lp2, lp3, lp4]    
    
    def _tag_v(self, block):
        """add [v] values

        1[s]
    
            arg1: block description 
            arg2: var = value   #- description
            
            key: values    
            _y :  p0                | p1
                 block description    eqnum

            _v :   p0  |   p1  |  p2      |    p3            
                 var    expr     statemnt   descrip     
        
        """
        linev = block.splitlines()        # break block into list of lines 
        #print(linev)
        self.enum += 1                   # reset eq number if new section
        if self.snum > self.snumchk:
            self.enum = 1
            self.snumchk = self.snum
        eqnum = ' [' + str(self.snum) + '.' + str(self.enum) + ']'
        key1 = '_y' + str(self.cnt)     # write block description
        blkdesc = linev[0].split('[v]')
        self.mdict[key1] = [ blkdesc[1], eqnum ]
        for valx in linev[1:]:
            if len(valx) > 0:
                self.cnt += 1    
                key2 = '_v' + str(self.cnt)
                state1, ref1 = valx.split('|')
                var1 = state1.split("=")[0].strip()
                expr1 = state1.split("=")[1].strip()
                self.mdict[key2] = [var1, expr1, state1.strip(), ref1.strip()]
    
    def _tag_e(self, block):
        """add [e] equation
    
        1[s]
        
            key : _e + line number  
            value:  p0  |  p1   |  p2   |   p3    |  p4 | p5   |  p6  |  p7       
                var    expr   statemt  descrip  dec1  dec2  unit  eqnum
        """
        #print('eblock',block)
        self.enum += 1                   # reset equation number at new section
        if self.snum > self.snumchk:
            self.enum = 1
            self.snumchk = self.snum
        eqnum = ' [' + str(self.snum) + '.' + str(self.enum) + ']'
        linev = block.splitlines()        # break lines into list 
        line1 = linev[0].split("|")
        ref = line1[0].split('[e]')[1]
        try:
            decs = line1[1].strip()
        except:
            decs = cfg.defaultdec
        dec1, dec2 = decs.split(',')    
        try:
            unit = line1[2].strip()
        except:
            unit = ' '
        state1 = linev[1].strip()
        expr1 = state1.split("=")[1].strip()
        var1 = state1.split("=")[0].strip()
        ref1 = ref.strip()
        key1 = '_e' + str(self.cnt)
        self.mdict[key1] = [var1, expr1, state1, ref1, dec1, dec2, unit, eqnum]
      
    def _tag_t(self, block):
        """ add [t] table
        
        1[s]
        
            key: 
            values: 
            [t]   p0 |  p1  |  p2  |  p3  |  p4    |   p5   | p6   | p7  | p8
                 00var  state1  desc   range1   range2   dec1   un1   un2
        """
        # reset equation number at new section
        self.enum += 1
        if self.snum > self.snumchk:
            self.enum = 1
            self.snumchk = self.snum
        ivect = block.strip().splitlines()
        # read format
        try:
            ref, fnum = ivect[0][3:].split("#-")
            fnum = str(self.modnum) + fnum.strip()
        except:
            ref = ivect[0][3:]
            fnum = str(self.modnum) + '01'
        decs, unts, opt = self.fdict[fnum]
        try:
            decs.split(',')
        except:
            decs = self.fdict['default'][1]
        enumb = ' [' + str(self.snum) + '.' + str(self.enum) + '] '
        ref = ref.strip()
        rng1 = rng2 = state = expr = ''
        mkey = '_a' + str(self.cnt)
        arrayblock = ivect[1:]
        # imported table
        if '=' not in arrayblock[0]:
            state = arrayblock[0].strip()
        # explicit table
        elif '=' in arrayblock[0] and '=' not in arrayblock[1]:
            _k = ''
            state1 = [_i.strip()[:] + _k for _i in arrayblock]
            state2 = ''.join(state1)
            expr = state2.split("=")[1].strip()
            state = state2
        # vector from range
        elif len(arrayblock) == 2:
            rng1 = arrayblock[0]
            state = arrayblock[1]
            expr = state.split("=")[1].strip()
        # table from ranges
        elif len(arrayblock) == 3:
            rng1 = arrayblock[0]
            rng2 = arrayblock[1]
            state = arrayblock[2]
            expr = state.split("=")[1].strip()
        # set dictionary values
        self.mdict[mkey] = ['[a]', state, expr, rng1, rng2, ref,
                          decs, unts, opt, '[' + self.modnum + ']', enumb]
        #print(state)
    
    def _tag_s(self, line):
        """Add [s] section
        1[s]
    
            arg: section description
    
            key : value            
            _s :    p0         |       p1      |   p2     
                  left string    calc number     sect num   
    
        """
        stitle = line[3:].strip()
        tocflg = 0
        sleft  =  stitle
        #print('tocflg', tocflg)
        self.snum += 1
        snum1 = '[' + str(self.snum) + ']'
        cnum1 = '['+str(self.calcnum)+']'
        mkey = '_s' + str(self.cnt)
        self.mdict[mkey] = [sleft,cnum1,snum1]
    
    def _tag_lt(self):
        """  _lt add public domain license to dict
        
        """   
        mkey = '_lt'
        self.mdict[mkey] = \
"""____________________________________________________________________________

This document (the calc) is generated from a on-c-e public domain template.
The calc is licensed under the CCO 1.0 Public Domain Dedication
at http://creativecommons.org/publicdomain/zero/1.0/
The calc is not a structural design calculation. The calc user
assumes sole responsibility for all inputs and results.
"""
