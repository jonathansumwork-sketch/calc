import numpy as np, scipy.ndimage as nd, scipy.special as sp, time, sys
tr=np.loadtxt('symbols_training.csv',delimiter=',')
te=np.loadtxt('symbols_testing.csv',delimiter=',')
aug=np.loadtxt('symbols_training_augmented.csv',delimiter=',')
print('train label order (first 60):',tr[:60,0].astype(int).tolist()[::5],'... sorted by class:',bool(np.all(np.diff(tr[:,0])>=0)))
print('aug label order (first 20):',aug[:20,0].astype(int).tolist(),' sorted:',bool(np.all(np.diff(aug[:,0])>=0)))
def rot(p,a): return nd.rotate(p.reshape(28,28),a,cval=0.01,order=1,reshape=False).reshape(-1)
def aug_set(angles):
    rows=[]
    for r in tr:
        for a in angles:
            rows.append(np.concatenate([[r[0]],rot(r[1:],a) if a!=0 else r[1:]]))
    return np.array(rows)
sets={}
sets['3x']=aug_set([0,10,20])
sets['4x_regen']=aug_set([-10,0,10,20])
def scale(x): return x/255.0*0.99+0.01
def run(data,epochs,seed,shuffle,hidden=200,lr=0.1):
    rs=np.random.RandomState(seed)
    wih=rs.normal(0,784**-0.5,(hidden,784)); who=rs.normal(0,hidden**-0.5,(10,hidden))
    X=scale(data[:,1:]); y=data[:,0].astype(int)
    T=np.full((len(y),10),0.01); T[np.arange(len(y)),y]=0.99
    for e in range(epochs):
        order=rs.permutation(len(y)) if shuffle else np.arange(len(y))
        for i in order:
            x=X[i][:,None]; t=T[i][:,None]
            h=sp.expit(wih@x); o=sp.expit(who@h)
            oe=t-o; he=who.T@oe
            who+=lr*(oe*o*(1-o))@h.T
            wih+=lr*(he*h*(1-h))@x.T
    h=sp.expit(wih@scale(te[:,1:]).T); o=sp.expit(who@h)
    pred=o.argmax(0); ok=(pred==te[:,0].astype(int))
    return ok.sum(), pred
seeds=range(int(sys.argv[1]))
conds=[('baseline 500, 10ep, class-ordered (as in file, no shuffle)',tr,10,False),
       ('baseline 500, 10ep, shuffled each epoch',tr,10,True),
       ('baseline 500, 40ep, shuffled (matched updates to 4x)',tr,40,True),
       ('3x 1500, 10ep, shuffled',sets['3x'],10,True),
       ('4x file as submitted 2000, 10ep, file order',aug,10,False),
       ('4x file as submitted 2000, 10ep, shuffled',aug,10,True)]
import json
res={}
t0=time.time()
for name,d,ep,sh in conds:
    c=[int(run(d,ep,s,sh)[0]) for s in seeds]
    res[name]=c
    print(f'{name}: correct/500 per seed {c} | mean {np.mean(c):.1f} ({np.mean(c)/5:.2f}%) min {min(c)} max {max(c)}  [{time.time()-t0:.0f}s]',flush=True)
