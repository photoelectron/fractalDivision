fc = 2; wd = ht = 1080/fc

def settings():
    size(wd,ht)

def setup():
    global F
    colorMode(HSB,1.)
    rectMode(CENTER)
    noFill()
    background(0)
    ###
    F = fractal(width/2,.25,width/4,10,240,4,.333)

def draw():
    background(0)
    translate(width/2,height/2)
    F.evolve()

###

class particle():
    def __init__(self,Lr,posr,rotr,cr):
        # init values
        self.L = Lr[0]; self.c = cr[0]
        self.pos = PVector(0,0); self.rot = 0
        # value ranges
        self.Lr = Lr; self.cr = cr
        self.posr = posr; self.rotr = rotr

    def show(self):
        with pushMatrix():
            translate(self.pos.x,self.pos.y)
            rotate(self.rot)
            stroke(self.c)
            rect(0,0,self.L,self.L)
    
    def update(self,nL,npos,nrot,nc):
        self.L = nL; self.c = nc
        self.pos = npos; self.rot = nrot

class fractal():
    def __init__(self,L,Lmult,R,niter,nstep,npart,hshift):
        self.iters = 0; self.steps = self.nstep = nstep
        self.ni = niter; self.np = npart
        self.L = L; self.Lmult = Lmult
        self.R = R; self.hs = hshift
        self.p = [particle((L,L),(PVector(0,0),PVector(0,0)),
                           (0,0),(color(.5,1,1),color(.5,1,1)))]
        self.p[0].show()
        self.growing = True
    
    def divide(self):
        pp = []
        self.L *= self.Lmult  # new length
        for i in xrange(len(self.p)):
            nL = (self.p[i].L,self.L)
            r = self.R/self.iters  # new position radius
            opos = self.p[i].pos
            orot = self.p[i].rot
            oc = self.p[i].c
            for j in xrange(self.np):
                h = hue(oc) + self.hs*map(j,0,self.np,-.5,.5)
                nc = color(hloop(h),1,1) # new color
                # new rotation
                nrot = self.p[i].rot + map(j,0,self.np,-PI,PI)
                npos = PVector(r*cos(nrot),r*sin(nrot)) # new pos
                P = particle(nL,(opos,opos+npos),(orot,nrot),(oc,nc))
                pp.append(P)
        self.p = pp[:]
    
    def grow(self):
        for i in xrange(len(self.p)):
            pct = map(self.steps,0,self.nstep,0,1)
            mL = lerp(self.p[i].Lr[0],self.p[i].Lr[1],pct)
            mpos = PVector.lerp(self.p[i].posr[0],self.p[i].posr[1],pct)
            mrot = lerp(self.p[i].rotr[0],self.p[i].rotr[1],pct)
            h = lerp(hue(self.p[i].cr[0]),hue(self.p[i].cr[1]),pct)
            mc = color(h,1,1)
            self.p[i].update(mL,mpos,mrot,mc)
    
    def show(self):
        for i in xrange(len(self.p)):
            self.p[i].show()
    
    def evolve(self):
        if self.steps < self.nstep: 
            self.grow(); self.steps += 1
        else: 
            self.iters += 1
            if self.iters > self.ni: noLoop()
            self.divide(); self.steps = 0
        self.show()

###
def hloop(h):
    if not(0<=h<1): return h - floor(h)
    else: return h