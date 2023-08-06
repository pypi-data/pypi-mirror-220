#!/usr/bin/env python
# coding: utf-8

# In[69]:


import numpy as np
import matplotlib.pyplot as plt
def plotKonrads(data, model=None, save_path=None):
    a = data.shape
    condi = int((a[1] + 1) ** 0.5)
    plt.subplots_adjust(hspace=0.5, wspace=0.5)  

    for i in range(a[1]):
        if condi < 11:
            plt.subplot(condi, condi, i + 2)
        else:
            plt.figure(int(i/condi) + 1)
            plt.subplot(condi, 1, (i % condi) + 1)
        
        plt.plot(data[0, i, :], 'b')
     
        plt.plot(data[1, i, :], 'r')
        plt.axis([0, a[2]-1, 0, 1])

    if model is not None:
        for i in range(a[1]):
            if condi < 11:
                plt.subplot(condi, condi, i+2)
            else:
                plt.figure(int(i/condi) + 1)
                plt.subplot(condi, 1, (i % condi) + 1)
            
           
            plt.plot(model[0, i, :], 'b-.')
            plt.plot(model[1, i, :], 'r-.')
            plt.axis([0, a[2]-1, 0, 1])
    
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    
    plt.show()

