"""
String @ Utils
Functions used for manipulating strings
"""

import pymel.core as pc
import maya.cmds as mc

alphabet = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',
                11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',
                20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}

def removeSuffix(string):
    s = string.split('_')

    if len(s) < 2:
        return string

    suffix = '_' + s[-1]
    r = string[:-len(suffix)]
    return r

def add_(string = ''):
    """
    Add an _ if string is not empty
    """
    s = ''
    if string:
        s = string + '_'

    return s
    
def combineWith_(string):
    """
    combine all strings given with _
    """
    
    if len(string) == 0:
        return ''
                   
    s = string[0]
    for item in string[1:-1]:
        if item == '':
            continue
        s = s + '_' + item
        
    if not s == '' and not string[-1] == '':
        s = s + '_' + string[-1]
        
    return s
    
def intToAlpha(v):
    s = ''
    
    div = v / 26
    mod = v % 26
    
    if div >= 1:
        s = s + convertToAlpha(int(div))        
            
    if mod >= 1:
        s = s + alphabet[mod]
        
    return s

# TODO: remove all usage of this as python has string search and replace built in
def strSearchReplace(str,search,replace):
    retstr = str
    
    # sanity check please
    if search == '':
        return str

    if str == '':
        return str

    retstr = retstr.replace(search,replace)

    return retstr

def strChop(str):
    ret = ''
    cnt = len(str)
    if cnt <= 1:
        return ret

    ret = str[1:cnt-1]

    return ret

def strUpperIdx(str,index):
    cnt = len(str)
    if index < 1 or index > cnt:
        return str

    pre = ""
    post = ""
    mid = ""

    if index > 1:
        pre = str[1:index-1]
    if index < cnt:
        post = str[index+1:cnt]
    mid = str[index:index]
    mid = mid.upper()

    ret = pre + mid + post
    return ret

def strLowerIdx(str,index):
    cnt = len(str)
    if index < 1 or index > cnt:
        return str

    pre = ""
    post = ""
    mid = ""

    if index > 1:
        pre = str[1:index-1]
    if index < cnt:
        post = str[index+1:cnt]
    mid = str[index:index]
    mid = mid.lower()

    ret = pre + mid + post
    return ret

def intToStr(i,padding):
    s = str(i)
    while len(s) < padding:
        s = ('0'+s)

    return s

def floatToStr(f,prePad,decPad):
    s = str(f)

    parts = s.split('.')
    while len(parts[0]) < prePad:
        parts[0] = ('0' + parts[0])

    while len(parts[1]) < decPad:
        parts[1] = (parts[1] + '0')

    if decPad >= 1:
        parts[1] = parts[1][1:decPad]
        s = parts[0] + '.' + parts[1]
    else:
        s = parts[0]

    return s

def objShortName(obj):
    ret = ''
    if obj == '':
        return ret
    parts = obj.split('|')
    cnt = len(parts)

    if cnt <= 0:
        ret = obj
    else:
        ret = parts[cnt-1]

    return ret

def objGetPrefix(obj):
    ret = ''
    if obj == '':
        return ret

    obj = objShortName(obj)
    
    parts = obj.split('_')
    cnt = len(parts)

    if cnt <= 1:
        ret = ''
    else:
        for i in range(cnt-1):
            if i > 0:
                ret += '_'
            ret += parts[i]

    return ret