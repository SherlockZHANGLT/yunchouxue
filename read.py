import numpy as np
baselen=np.load('baselen.npy')  #加载文件
dlist_test=np.load('dlist_test.npy')  #加载文件
dlist_train=np.load('dlist_train.npy')  #加载文件
IDL=np.load('IDL.npy')  #加载文件
xinlist_test=np.load('xinlist_test.npy')  #加载文件
xinlist_train=np.load('xinlist_train.npy')  #加载文件
print('baselen:')
print(baselen)
print('dlist_test:')
print(dlist_test)
print('dlist_train:')
print(dlist_train)
print('IDL:')
print(IDL)
print('xinlist_test:')
print(xinlist_test)
print('xinlist_train:')
print(xinlist_train)