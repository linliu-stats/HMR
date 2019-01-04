#!/usr/bin/env python

# ------------------------------------
# Python Modual
# ------------------------------------

import os
import sys
import string
import time
# --------------------------
# custom package
# --------------------------

### tool function
from HMRpipe.Utility      import (sp,
                                   pdf_name,
                                   raise_error,
                                   wlog,
                                   ewlog,
                                   rwlog,
                                   CMD,
                                   bwsigAve,
                                   createDIR
                                   )
# --------------------------
# main 
# --------------------------

def step1_generate_matrix(conf_dict,logfile):
    '''
    generate expression matrix file 
    main data processing step, including mapping, generate expression matrix and QC matrix which is used in next step
    for fastq format : 
        STAR/bowtie2 mapping
        q30 filter, 
    for sam format:
        q30 filter     
    ''' 
    #t= time.time()
    ### generate TF overlap matrix using bed tools
    wlog("generate TF overlap matrix",logfile)
    init = 0
    for f in conf_dict['General']['peakfilenames']:
        if init == 0:
            cmd = 'intersectBed -a %s -b %s -c '%(conf_dict['General']['HMRpeak'],conf_dict['General']['peakFolder'] + f + ".bed")
            init = 1
        else:
            cmd += '| intersectBed -a - -b %s -c '%(conf_dict['General']['peakFolder'] + f + ".bed")
    
    cmd += '> %s'%(conf_dict['General']['outname']+"_peakov.bed")
    rwlog(cmd,logfile)

    ### generate HMsig

    wlog("generate HMsignal matrix",logfile)
    inf = open(conf_dict['General']['HMRpeak'])
    outf = open(conf_dict['General']['outname']+"_HMsig.bed",'w')
    for line in inf:
        ll = line.split()
        addsig = bwsigAve(conf_dict['General']['signal'],
                          ll[0],ll[1],ll[2],conf_dict['General']['software'])
        newll = ll + [addsig]
        outf.write("\t".join(map(str,newll))+"\n")
    inf.close()
    outf.close()

    #s1time = time.time() -t
    #wlog("time for Step1: %s"%(s1time),logfile)
    #conf_dict['results'] = {}
    #conf_dict['results']['expmat'] = conf_dict['Step2_ExpMat']['expmat']
    #conf_dict['results']['qcmat'] = conf_dict['Step2_ExpMat']['qcmat']
    
    return conf_dict
