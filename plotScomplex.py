#sample output plot file.  Using the list of objects in 'names' below,
#make a joint plot of all results and lit data files

import matplotlib.pyplot as plt
import numpy
import PolFit


color={'u':'m','b':'b','v':'g','r':'r','i':'#ff8000','J':'#ff66b2','H':'k'}
marker={'u':'o','b':'^','v':'s','r':'*','i':'>','J':'p','H':'<'}
#marker={'u':'.','b':'.','v':'.','r':'.','i':'.','J':'.','H':'.'}
#ms={'u':4,'b':5,'v':6,'r':7,'i':8,'J':9,'H':10}
ms={'u':4,'b':4,'v':4,'r':4,'i':4,'J':9,'H':9}
z={'u':4,'b':5,'v':6,'r':7,'i':8,'J':9,'H':10}

ast={}

lit=open("s_complex_lit_new.dat")
for line in lit.readlines():
    if line[0]=='#':
        continue
    if line.rstrip()=='':
        continue
    dat=line.rstrip().split()
    band=dat[0]

    if band=="G":
        band='v'
    elif band=="U":
        band='u'
    elif band=="B":
        band='b'
    elif band=="V":
        band='v'
    elif band=="I":
        band='i'
    elif band=="R2":
        band='r'
    elif band=="R":
        band='r'
    elif band=="O":
        band='r'
    
    phase=float(dat[1])
    pol=float(dat[2])
    pol_err=float(dat[3])
    if band not in ast:
        ast[band]={}
        ast[band]['phase']=[]
        ast[band]['pol']=[]
        ast[band]['err']=[]
    ast[band]['phase'].append(phase)
    ast[band]['pol'].append(pol)
    ast[band]['err'].append(pol_err)


#names=["eunomia","juno","iris","massalia","phocaea"] Phocaea is being weird. 
names=["juno","iris","eunomia","massalia"]
for name in names:
    
    res=open(name+"_results.dat")
    for line in res.readlines():
        if line[0]=='#':
            continue
        if line.rstrip()=='':
            continue
        dat=line.rstrip().split()
        band=dat[0]
        phase=float(dat[1])
        pol=float(dat[2])
        pol_err=float(dat[3])
        if band not in ast:
            ast[band]={}
            ast[band]['phase']=[]
            ast[band]['pol']=[]
            ast[band]['err']=[]
        ast[band]['phase'].append(phase)
        ast[band]['pol'].append(pol)
        ast[band]['err'].append(pol_err)

#res=open("juno_results.dat")
#for line in res.readlines():
#    if line[0]=='#':
#        continue
#    if line.rstrip()=='':
#        continue
#    dat=line.rstrip().split()
#    band=dat[0]
#    phase=float(dat[1])
#    pol=float(dat[2])
#    pol_err=float(dat[3])
#    if band not in ast:
#        ast[band]={}
#        ast[band]['phase']=[]
#        ast[band]['pol']=[]
#        ast[band]['err']=[]
#    ast[band]['phase'].append(phase)
#    ast[band]['pol'].append(pol)
#    ast[band]['err'].append(pol_err)
#
#res=open("iris_results.dat")
#for line in res.readlines():
#    if line[0]=='#':
#        continue
#    if line.rstrip()=='':
#        continue
#    dat=line.rstrip().split()
#    band=dat[0]
#    phase=float(dat[1])
#    pol=float(dat[2])
#    pol_err=float(dat[3])
#    if band not in ast:
#        ast[band]={}
#        ast[band]['phase']=[]
#        ast[band]['pol']=[]
#        ast[band]['err']=[]
#    ast[band]['phase'].append(phase)
#    ast[band]['pol'].append(pol)
#    ast[band]['err'].append(pol_err)
    

plt.figure()
for b in ['H','J','r','v','b','u']:
    if b not in ast:
        continue
    plt.errorbar(ast[b]['phase'],ast[b]['pol'],yerr=ast[b]['err'],ms=ms[b],color=color[b],ls='None',marker=marker[b],label=b,zorder=z[b])

allp=numpy.arange(0,80,0.1)
plt.plot(allp,[0 for xx in allp],'k:')

print("U bands")
gophase=ast['u']['phase']
gopol=ast['u']['pol']
pout,params=PolFit.PolPhase(gophase,gopol,p0=[4.6,0.19,10])
yout=[PolFit.ppcurve(pout,xx) for xx in allp]
plt.plot(allp,yout,ls='dashed',color=color['u'])

print("B bands")
gophase=ast['b']['phase']
gopol=ast['b']['pol']
pout,params=PolFit.PolPhase(gophase,gopol,p0=[4.6,0.19,10])
yout=[PolFit.ppcurve(pout,xx) for xx in allp]
plt.plot(allp,yout,ls='dashed',color=color['b'])

print("V bands")
gophase=ast['v']['phase']
gopol=ast['v']['pol']
pout,params=PolFit.PolPhase(gophase,gopol,p0=[4.6,0.19,10])
yout=[PolFit.ppcurve(pout,xx) for xx in allp]
plt.plot(allp,yout,ls='dashed',color=color['v'])

print("R bands")
gophase=ast['r']['phase']
gopol=ast['r']['pol']
pout,params=PolFit.PolPhase(gophase,gopol,p0=[4.6,0.19,10])
yout=[PolFit.ppcurve(pout,xx) for xx in allp]
plt.plot(allp,yout,ls='dashed',color=color['r'])



##eq from muninone09, constants are assumed here
#p_a=3.1  #amplitude param
#p_k=0.13 #slope param
#p_b=-1  #assumed to ensure P=0 at alpha=0
#p_d=10.  #width of negative branch
#
#pout=p_a * (numpy.e**(-allp/p_d) + p_b) + p_k*allp
#plt.plot(allp,pout,ls='dashed',color=color['v'])


print("J band")
gophase=ast['J']['phase']
gopol=ast['J']['pol']
pout,params=PolFit.PolPhase(gophase,gopol,p0=[4.5,0.2,10])
yout=[PolFit.ppcurve(pout,xx) for xx in allp]
plt.plot(allp,yout,ls='dashed',color=color['J'])



#p_a=4.55  #amplitude param
#p_k=0.19 #slope param
#p_b=-1  #assumed to ensure P=0 at alpha=0
#p_d=10.  #width of negative branch
#
#pout=p_a * (numpy.e**(-allp/p_d) + p_b) + p_k*allp
#plt.plot(allp,pout,ls='dashed',color=color['J'])

print("H band")
gophase=ast['H']['phase']
gopol=ast['H']['pol']
pout,params=PolFit.PolPhase(gophase,gopol,p0=[4.5,0.2,10])
yout=[PolFit.ppcurve(pout,xx) for xx in allp]
plt.plot(allp,yout,ls='dashed',color=color['H'])


tline=""
for name in names:
    tline=tline+name.capitalize()+" + "

tline=tline[:-3]  #to remove the trailing + 
    
plt.title(tline)
plt.xlim(0,35)
plt.ylim(-1.2,1.2)
plt.legend()
plt.xlabel("Phase (deg)")
plt.ylabel("Polarization (%, wrt scattering plane)")
plt.savefig("Scomplex_phase_pol.png")
