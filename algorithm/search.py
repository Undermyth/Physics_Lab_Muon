import numpy as np

def search(Y:np.ndarray,n=2500,V_=-0.8,tV_=-2,zV_=-2,dur=3,tesp=4,stesp=2)->np.ndarray:
    # n=2500#数组大小
    # V_=-0.1#小于V_的才会进入峰的判断 记为能量判据
    # tV_=-0.2#次峰的门限
    # zV_=-0.8
    # dur=80#间隔小于此不记为一个峰 记为间隔判据
    # tesp=100#原图相连 tesp 个点视为一个点 处理相近的数据
    # stesp=50#寻找次峰的间隔
    '''
    数组初始化
    '''
    # with open("./py.txt","r") as f:
    #     p=f.readlines()
    # tY=[]
    # for i in p:
    #     tY.append(float(i))
    # Y=np.asarray(tY)
    X=np.arange(0,n,1)
    p=np.stack((X,Y),axis=1)#坐标数组
    st=np.zeros((n+10,),dtype=int)#索引的栈
    ans=np.zeros((n+10,),dtype=int)#一产输出
    aans=np.zeros((n+10,),dtype=int)#二产输出
    # aans=np.empty()
    
    i=1
    while i<n:
        while i<n and p[i][1]>zV_:#能量判据
            i=i+1
        if i>n :
            break
        '''
        这里以下是凸包的主体
        '''
        # top=0
        # st[top]=i-1
        # top=top+1
        # st[top]=i
        top=1
        st[top]=i-1
        fg=0
        cnt=0#间隔判据
        ans[0]=0
        # print(i)
        while i<n and p[i][1]<V_:
            while top>1 and np.cross(p[st[top]]-p[st[top-1]],p[i]-p[st[top]])<=0:
                top=top-1
            if (not fg) and top>1 and p[i][1]-p[st[top]][1]>=0:
                fg=top+1#找到了峰
                # print(fg,st[:top+1])
                # if i+tesp//3<n and p[i][1]==np.amin(Y[i:i+tesp//3]) and p[i][1]==np.amax(Y[i:i+tesp//3]):
                if p[i][1]==p[i-1][1] and i<n-1 and p[i][1]==p[i+1][1]:
                    ans[0]=ans[0]+1
                    ans[ans[0]]=i
                    while p[i][1]==p[i+1][1]:
                        i=i+1
                    st[top]=i-1
                    # print("ping")
                bias=st[top]
                maxn=p[i][1]
                while i<=st[top]+tesp and i<n and p[i][1]<V_  and p[i][0]<p[st[top]][0]+tesp:
                    if maxn>p[i][1]:
                        maxn=p[i][1]
                        bias=i
                        # print(maxn,bias)
                    cnt=cnt+1
                    i=i+1
                if i==n:
                    break
                ans[0]=ans[0]+1
                ans[ans[0]]=bias
                i=bias
                # print(ans[:ans[0]+1])
                # i=i+tesp
                # print(i,top)
            if fg and top+1<fg:
                fg=top
                # print(1)
            cnt=cnt+1
            top=top+1
            st[top]=i
            # print(st[:top+1])
            i=i+1
        # print(ans[:ans[0]+1],cnt,fg)
        if fg and cnt>=dur:#间隔判据
            # print(fg,st[:top+1])
            # print(ans[:ans[0]+1])
            fg=fg+1
            while fg<=top and p[ans[ans[0]]][0]+tesp>=p[st[fg]][0]:
                fg=fg+1
            while fg<=top and (p[st[fg]][0]<p[i][0]-tesp if i<n else st[fg]!=i-1):
                ans[0]=ans[0]+1
                ans[ans[0]]=st[fg]
                bias=fg
                # print(fg)
                maxn=p[st[fg]][1]
                while fg<=top and p[st[fg]][0]<p[ans[ans[0]]][0]+tesp:
                    if maxn>p[st[fg]][1]:
                        maxn=p[st[fg]][1]
                        bias=fg
                        # print(maxn,bias)
                    # maxn=min(maxn,p[ans[i]][1])
                    fg=fg+1
                ans[ans[0]]=st[bias]
                if p[st[bias]][0]+tesp>p[n-1][0]:
                    ans[0]=ans[0]-1
            # print(ans[:ans[0]+1])
            aans=np.vstack((aans,ans))
        st[top+1]=0
        i=i+1
    # print(aans)
    if len(aans.shape)==2:
        mx,_ =aans.shape 
    else :
        mx=1
    for i in range(1,mx):
        l=aans[i][aans[i][0]]
        r=aans[i+1][1] if i+1<mx else n-1
        tmp=np.argmin(Y[l:r+1])
        # print(l,r,tmp)
        while tmp<=stesp or r-l-stesp<=tmp:
            if r-l<=dur or Y[l+tmp]>=tV_:
                break
            if r-l-stesp<=tmp:
                r=r-1
            elif tmp<=stesp:
                l=l+1
            else:
                break
            tmp=np.argmin(Y[l:r+1])
            # print(l,r,tmp,Y[l+tmp])
        if r-l>dur and Y[l+tmp]<tV_:
            # print("abab")
            aans[i][aans[i][0]+1]=l+tmp
            aans[i][0]=aans[i][0]+1
    return aans[1:]