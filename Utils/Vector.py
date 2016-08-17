"""
Vector Tuple @ Utils
Functions used for Vector Tuples
"""

def multVec3ByScalar(v,s):
    return (v[0]*s, v[1]*s,v[2]*s)

def divVec3ByScalar(v,s):
    return (v[0]/s, v[1]/s,v[2]/s)
    
def addVec3ByScalar(v,s):
    return (v[0]+s, v[1]+s,v[2]+s)
    
def subVec3ByScalar(v,s):
    return (v[0]-s, v[1]-s,v[2]-s)
    
def addVec3toVec3(v1,v2):
    return (v1[0]+v2[0],
            v1[1]+v2[1],
            v1[2]+v2[2])
    
def subVec3toVec3(v1,v2):
    return (v1[0]-v2[0],
            v1[1]-v2[1],
            v1[2]-v2[2])