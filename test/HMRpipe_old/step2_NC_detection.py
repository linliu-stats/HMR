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
                                   createDIR)
# --------------------------
# main 
# --------------------------
def step2_NC_detection(conf_dict,logfile):
    '''
    analysis part
    mainly Rscript
    '''   
    # start
    # create section for 
    # Rscript detectNonCanonical.r outname signalname usePQ cutoff alpha lambdachoice topN tmpRpackgeDIR
    createDIR(conf_dict['General']['startdir']+"tmpPackage/")
    cmd = "Rscript %s %s %s %s %s %s %s"%(conf_dict['rscript']+"detectNonCanonical.r",
                         conf_dict['General']['outname'],
                         conf_dict['General']['signalname'],
                         conf_dict['options']['Pvalue'],
                         conf_dict['options']['Alpha'],
                         conf_dict['options']['Lambda'],
                         conf_dict['options']['TopNcofactors'],
                         conf_dict['General']['startdir']+"tmpPackage/")
    #rwlog(cmd,logfile)
    os.system('echo "[CMD] %s " >> %s'%(cmd,logfile))
    tmpobj = sp(cmd)

    return conf_dict


