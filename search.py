import numpy as np

def search(Y:np.ndarray)->np.ndarray:
    n=2500#数组大小
    V_=-0.1#小于V_的才会进入峰的判断 记为能量判据
    dur=30#间隔小于此不记为一个峰 记为间隔判据
    tesp=20#原图相连 tesp 个点视为一个点 处理相近的数据
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

    i=1
    while i<n:
        while i<n and p[i][1]>V_:#能量判据
            i=i+1
        if i>n :
            break
        '''
        这里以下是凸包的主体
        '''
        top=0
        st[top]=i-1
        top=top+1
        st[top]=i
        fg=0
        cnt=0#间隔判据
        while i<n and p[i][1]<V_:
            while top>1 and np.cross(p[st[top]]-p[st[top-1]],p[i]-p[st[top]])<=0:
                top=top-1
            if (not fg) and p[i][1]-p[st[top]][1]>0:
                fg=top#找到了峰
            cnt=cnt+1
            top=top+1
            st[top]=i
            i=i+1
        if fg and cnt>=dur:#间隔判据
            while fg<=top and p[st[fg]][0]<p[i][0]-tesp:
                ans[0]=ans[0]+1
                ans[ans[0]]=st[fg]
                fg=fg+1
        st[top+1]=0
        i=i+1

    # print(ans)
    i=1
    while i<=ans[0]:
        bias=0
        fg=i
        maxn=p[ans[i]][1]
        while i<=ans[0] and p[ans[i]][0]<p[ans[fg]][0]+tesp:
            maxn=min(maxn,p[ans[i]][1])
            bias=i
            i=i+1
        aans[0]=aans[0]+1
        aans[aans[0]]=ans[bias]
    return aans