import numpy as np, scipy.ndimage as nd, scipy.special as sp, time
tr=np.loadtxt('symbols_training.csv',delimiter=',')
te=np.loadtxt('symbols_testing.csv',delimiter=',')
aug=np.loadtxt('symbols_training_augmented.csv',delimiter=',')
def scale(x): return x/255.0*0.99+0.01
def train(data,epochs,seed,shuffle,hidden=200,lr=0.1,wihdiv=784):
    rs=np.random.RandomState(seed)
    wih=rs.normal(0,wihdiv**-0.5,(hidden,784)); who=rs.normal(0,hidden**-0.5,(10,hidden))
    X=scale(data[:,1:]); y=data[:,0].astype(int)
    T=np.full((len(y),10),0.01); T[np.arange(len(y)),y]=0.99
    for e in range(epochs):
        order=rs.permutation(len(y)) if shuffle else np.arange(len(y))
        for i in order:
            x=X[i][:,None]; t=T[i][:,None]
            h=sp.expit(wih@x); o=sp.expit(who@h); oe=t-o; he=who.T@oe
            who+=lr*(oe*o*(1-o))@h.T; wih+=lr*(he*h*(1-h))@x.T
    return wih,who
def acc(net,rows):
    wih,who=net; o=sp.expit(who@sp.expit(wih@scale(rows[:,1:]).T)); return int((o.argmax(0)==rows[:,0].astype(int)).sum())
print('--- which baseline settings give ~98.2% (491/500)? (3 seeds each)')
for hid in (100,200):
    for ep in (1,2,3,4,5,10):
        for sh in (True,False):
            c=[acc(train(tr,ep,s,sh,hid),te) for s in range(3)]
            print(f'hidden {hid} epochs {ep:2d} shuffle {sh!s:5}: {c}')
print('--- robustness: rotated TEST copies (analysis only), baseline(shuffled) vs 4x(shuffled), 4 seeds')
def rot_rows(rows,a): 
    out=rows.copy()
    for i,r in enumerate(rows): out[i,1:]=nd.rotate(r[1:].reshape(28,28),a,cval=0,order=1,reshape=False).reshape(-1)
    return out
angles=[-30,-20,-10,0,10,20,30]
tests={a:rot_rows(te,a) for a in angles}
B=[train(tr,10,s,True) for s in range(4)]
A=[train(aug,10,s,True) for s in range(4)]
for a in angles:
    b=np.mean([acc(n,tests[a]) for n in B]); g=np.mean([acc(n,tests[a]) for n in A])
    print(f'test rotated {a:+3d}: baseline {b/5:.1f}%  4x-augmented {g/5:.1f}%')
