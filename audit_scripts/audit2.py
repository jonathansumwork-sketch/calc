import numpy as np, scipy.ndimage as nd
tr=np.loadtxt('symbols_training.csv',delimiter=',')
te=np.loadtxt('symbols_testing.csv',delimiter=',')
aug=np.loadtxt('symbols_training_augmented.csv',delimiter=',')
big=np.loadtxt('bigger_set.csv',delimiter=',')
def rot(p,a,cval=0.01):
    return nd.rotate(p.reshape(28,28),a,cval=cval,order=1,reshape=False).reshape(-1)
# which transform produced each augmented row?
def key(r): return tuple(np.round(r).astype(int))
augidx={}
for i,r in enumerate(aug): augidx.setdefault(key(r[1:]),[]).append(i)
print('aug unique rows',len(augidx),'of',len(aug))
found={a:0 for a in (-10,0,10,20)}; foundcl={a:0 for a in found}
for i,r in enumerate(tr):
    for a in found:
        for cv in (0.01,0):
            k=key(rot(r[1:],a,cv))
            if k in augidx:
                found[a]+=1; 
                if all(aug[j,0]==r[0] for j in augidx[k]): foundcl[a]+=1
                break
print('training rows whose rotation (cval .01 or 0) is found in aug file:',found,'label ok:',foundcl)
# any test image (or rotation of a test image) in aug file?
leak=0; 
for r in te:
    for a in (-10,0,10,20):
        if key(rot(r[1:],a)) in augidx or key(rot(r[1:],a,0)) in augidx: leak+=1
print('test images (or their rotations) found in augmented training file:',leak)
print('aug equals bigger_set as multiset:', sorted(map(key,[r[1:] for r in aug]))==sorted(map(key,[r[1:] for r in big])))
# rotation direction check: rotate a vertical bar by +20 and see which way it leans
img=np.zeros((28,28)); img[4:24,14]=255
r=nd.rotate(img,20,order=1,reshape=False)
ys,xs=np.where(r>50); top=xs[ys==ys.min()].mean(); bot=xs[ys==ys.max()].mean()
print('+20 deg: top x=%.1f bottom x=%.1f ->'%(top,bot),'top leans LEFT (anticlockwise visually)' if top<bot else 'top leans RIGHT (clockwise visually)')
# nearest-neighbour distances: test->train vs test->test
from numpy.linalg import norm
D=np.sqrt(((te[:,None,1:]-tr[None,:,1:])**2).sum(-1))
same=(te[:,0][:,None]==tr[:,0][None,:])
nn_same=np.where(same,D,1e9).min(1); nn_other=np.where(~same,D,1e9).min(1)
print('NN same-class dist: median %.0f min %.0f; NN other-class median %.0f; test imgs where nearest train img is other class: %d'%(np.median(nn_same),nn_same.min(),np.median(nn_other),(nn_other<nn_same).sum()))
# within-train near-duplicates
Dt=np.sqrt(((tr[:,None,1:]-tr[None,:,1:])**2).sum(-1)); np.fill_diagonal(Dt,1e9)
print('closest train-train pair distance %.0f ; closest test->train %.0f'%(Dt.min(),D.min()))
