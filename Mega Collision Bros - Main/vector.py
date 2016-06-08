import math

class Vect2D:
    """Basic vector class"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mag(self):
        return math.hypot(self.x, self.y)    

    def __add__(self, v):        
        return Vect2D(self.x + v.x, self.y + v.y)       

    def __mul__(self, v):
        if type(v) is int or type(v) is float:
            #scalar multiplication(return vector)
            return Vect2D(self.x * v, self.y * v)            
        else:
            #dot product(return scalar)
            return (self.x * v.x + self.y * v.y)    
            
    def __div__(self, a):
       return Vect2D(float(self.x)/a, float(self.y)/a)

    def __sub__(self, v):
        return self + (v * -1)

    def __neg__(self):
        return self * - 1

    def __str__(self):
        return "Vector(%d, %d)"%(self.xy())

    def xy(self):
        return self.x, self.y

    def angle(self, v):
        return math.degrees(math.acos(self * v))

    def normalise(self):
        return self / self.mag()
    
    def tangent(self, d):
        return Vect2D(self.y * d, self.x * -d)

def vectorCollision(v1, v2, pos1, pos2):
    """Takes 2 velocity and 2 position vectors and returns 2 new velocity
    vectors"""
    #find normal and tangent collision unit vectors
    n = Vect2D(pos2.x - pos1.x, pos2.y - pos1.y)
    n = n.normalise()
    t = n.tangent(-1)
    #resolve velocity vectors into normal and tangential components(scalar)
    v1_n = n * v1
    v1_t = t * v1
    v2_n = n * v2
    v2_t = t * v2
    #find new normal velocities(scalar)
    #v1' = v1n(m1 - m2) + 2(m2 * v2n)/m1+m2
    #v2' = v2n(m2 - m1) + 2(m1 * v2n)/m1+m2
    #TODO: MASS(both 1 atm)
    v1_np = 2 * v2_n / 2
    v2_np = 2 * v1_n / 2
    #convert scalar velocities above into vectors
    v1_np = n * v1_np
    v1_tp = t * v1_t
    v2_np = n * v2_np
    v2_tp = t * v2_t
    #add tangent and normal components of both new velocities and return them
    return v1_np + v1_tp, v2_np + v2_tp
    

    
    
    
    
    
    
    
    
        
    
        
