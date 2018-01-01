from Saver import saves
N_PHI = 9*2;N_save = 9*2
fc = 1; wd = 1080/fc; ht = 1080/fc

lgt = ht #1.575       # initial length
lgtx = .5           # length multiplier
sep = ht/2**.5        # separation
sepx = .5           # separation multiplier
iterations = 9
steps = 1           # steps per iteration
parts = 4           # split into how many parts
ang = TWO_PI/parts  # angle between parts
huei = .85            # initial hue
hueshift = .2

nscale = 1e0

def settings():
    size(wd,ht)

def setup():
    global F, saving
    colorMode(HSB,1.)
    rectMode(CENTER)
    noStroke()
    background(0)
    # frameRate(1)
    noiseSeed(220)
    saving = saves(N_PHI,N_save)
    saving.onClick()
    ###
    F = fractal(lgt,lgtx,sep,sepx,iterations,steps,parts,hueshift)

def draw():
    background(0)
    translate(width/2,height/2)
    # rotate(TWO_PI/12)
    F.evolve()
    print F.steps, F.iters
    saving.save_frame()

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
            fill(self.c)
            rect(0,0,self.L,self.L)
    
    def update(self,nL,npos,nrot,nc):
        self.L = nL; self.c = nc
        self.pos = npos; self.rot = nrot

class fractal():
    def __init__(self,L,Lmult,R,Rmult,niter,nstep,npart,hshift):
        self.iters = 0; self.steps = self.nstep = nstep
        self.ni = niter; self.np = npart; self.hs = hshift
        self.L = L; self.Lmult = Lmult
        self.R = R; self.Rmult = Rmult
        self.p = [particle((L,L),(PVector(0,0),PVector(0,0)),
                           (0,0),(color(huei,1,1),color(huei,1,1)))]
        self.p[0].show()
        self.growing = True
    
    def divide(self):
        pp = []
        self.L *= self.Lmult  # new length
        self.R *= self.Rmult  # new separation
        for i in xrange(len(self.p)):
            nL = (self.p[i].L,self.L)
            opos = self.p[i].pos
            orot = self.p[i].rot
            oc = self.p[i].c
            for j in xrange(self.np):
                h = hue(oc) + self.hs*(map(j,0,self.np,-.5,.5) +
                                       map(noise(i*nscale,j*nscale),
                                           0,.8,-.5,.5))
                # h = hue(oc) + \
                #     self.hs*map(noise(i*nscale,j*nscale,self.iters*nscale),
                #                 0,.8,-.5,.5)
                nc = color(hloop(h),1,1) # new color
                # new rotation
                # nrot = self.p[i].rot + map(j,0,self.np,0,TWO_PI)
                nrot = map(j,0,self.np,-PI,PI)
                nang = (j%self.np)*ang+PI/4
                npos = PVector(self.R*cos(nang),
                               self.R*sin(nang)) # new pos
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
            self.steps += 1; self.grow() 
        else: 
            self.iters += 1
            if self.iters > self.ni: 
                noLoop(); print 'finished'
                self.show()
                return
            self.divide()
            self.steps = 0; self.grow()
        self.show()
        

###
def hloop(h):
    if not(0<=h<1): return h - floor(h)
    else: return h

def keyPressed():
    if key == 's': saver.onClick()