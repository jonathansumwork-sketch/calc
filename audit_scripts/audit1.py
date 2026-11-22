import numpy as np, glob, os
from PIL import Image
tr=np.loadtxt('symbols_training.csv',delimiter=',')
te=np.loadtxt('symbols_testing.csv',delimiter=',')
aug=np.loadtxt('symbols_training_augmented.csv',delimiter=',')
print('dtypes ok', tr.shape, te.shape, aug.shape)
for n,a in [('train',tr),('test',te),('aug',aug)]:
    p=a[:,1:]
    print(n,'min',p.min(),'max',p.max(),'mean %.2f'%p.mean(),'frac0 %.3f'%(p==0).mean(),'frac255 %.4f'%(p==255).mean(),'distinct',len(np.unique(np.round(p))),'frac non-integer %.3f'%(np.abs(p-np.round(p))>1e-9).mean(), 'frac strictly between 1..254 among nonzero %.3f'%(((p>0)&(p<255)).sum()/(p>0).sum()))
# map CSV rows to PNGs in each folder
pngs={}
for folder in ['input_images_auto_review','input_images_final','input_images_corrected']:
    d={}
    for f in sorted(glob.glob(folder+'/*.png')):
        d[os.path.basename(f)]=255-np.array(Image.open(f).convert('L')).reshape(-1)
    pngs[folder]=d
for folder,d in pngs.items():
    names=list(d); M=np.stack([d[n] for n in names]).astype(float)
    def match(rows):
        out=[];exact=0
        for r in rows:
            dist=np.abs(M-r[1:]).sum(axis=1); j=dist.argmin()
            out.append((names[j],dist[j]))
        return out
    mt=match(tr); me=match(te)
    print(folder,'train exact',sum(1 for _,x in mt if x==0),'/500; test exact',sum(1 for _,x in me if x==0),'/500')
    st=set(n for n,x in mt if x==0); se=set(n for n,x in me if x==0)
    print('  overlap exact train/test files:',len(st&se))
    # label consistency
    bad=[(n,r[0]) for (n,x),r in zip(mt,tr) if x==0 and int(n.split('_')[0])!=int(r[0])]
    print('  label mismatches train:',len(bad))
