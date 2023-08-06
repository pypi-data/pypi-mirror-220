#!/usr/bin/env python
# coding: utf-8

# In[1]:


def fragment_compound_space(compounds=None, fragments=None, metric='euclidean', distance_matrix=True, new_space=False, input_dist_matrix=None):
    import numpy as np
    from scipy.spatial import distance # Distance similarity
    from master_strange_mol_rep import mol_rep as strange
    
    # MS part

    if distance_matrix == True and new_space== False:
        array_1= compounds
        array_2= fragments
        a='Green light!!!'
        if array_1.shape[1] > array_2.shape[1]:
            array_2=strange.zero_pad_two_ndarrays(array_1,array_2)
        else:
            array_1=strange.zero_pad_two_ndarrays(array_2,array_1)
        total_similarity=[]
        for i in array_1:
            similarity=[]
            for u in array_2:
                if metric == 'euclidean':
                    similarity.append(distance.euclidean(u,i))
                elif metric == 'cosine':
                    similarity.append(distance.cosine(u,i))
                elif metric == 'canberra':
                    similarity.append(distance.canberra(u,i))
                elif metric == 'manhattan':
                    similarity.append(distance.cityblock(u,i))
                else:
                    a='This distance metric is not available!!!'
            total_similarity.append(similarity)
        return np.array(total_similarity)
        
    
    elif distance_matrix == True and new_space== True:
        array_1= compounds
        array_2= fragments
        a='Green light!!!'
        if array_1.shape[1] > array_2.shape[1]:
            array_2=strange.zero_pad_two_ndarrays(array_1,array_2)
        else:
            array_1=strange.zero_pad_two_ndarrays(array_2,array_1)
        total_similarity=[]
        for i in array_1:
            similarity=[]
            for u in array_2:
                if metric == 'euclidean':
                    similarity.append(distance.euclidean(u,i))
                elif metric == 'cosine':
                    similarity.append(distance.cosine(u,i))
                elif metric == 'canberra':
                    similarity.append(distance.canberra(u,i))
                elif metric == 'manhattan':
                    similarity.append(distance.cityblock(u,i))
                else:
                    a='This distance metric is not available!!!'
            total_similarity.append(similarity)

    # Fragment space part    
        
        rep_cs=np.array(total_similarity)
        bb_a=np.zeros((rep_cs.shape[1],rep_cs.shape[1]))
        bb_a[np.diag_indices_from(bb_a)] = 1
        relative_rep=[]
        if metric == 'euclidean':
            asd=[]
            bb_array=pd.DataFrame(bb_a)
            for i in range(bb_a.shape[0]):
                asd.append((bb_a[0]-bb_a[i])*-2)
            asd.append((bb_a[1]-bb_a[2])*-2)
                  
            bb_mat=pd.DataFrame(asd)
            rep=pd.DataFrame(rep_cs)

            for i in range(rep.shape[0]):
                A = np.array(pd.DataFrame(np.array(bb_mat)))
                b = np.array(rep.iloc[i])
        
                qas=[]
                for t in range(len(b)):
                    qas.append(b[0]**2-b[t]**2)
                qas.append(b[1]**2-b[2]**2)
        
                x=np.linalg.solve(A[1:]+0.001,qas[1:])
                relative_rep.append(x)    
    
        elif metric == 'canberra':
            asdf=[]
            bb_a=np.zeros((9,9))
            bb_a[np.diag_indices_from(bb_a)] = 1
            bb_array=pd.DataFrame(bb_a)
            dist=rep.iloc[i]
            A=np.array(bb_array*(dist-4))
            b=2-dist
            for t in np.linalg.solve(A,pd.DataFrame(b)):
                asdf.append(float(t))
            relative_rep.append(asdf)
        return np.array(total_similarity),np.array(relative_rep)
    
    elif distance_matrix == False and new_space== True:
        rep_cs=np.array(input_dist_matrix)
        bb_a=np.zeros((rep_cs.shape[1],rep_cs.shape[1]))
        bb_a[np.diag_indices_from(bb_a)] = 1
        relative_rep=[]
        rep=pd.DataFrame(rep_cs)
        if metric == 'euclidean':
            asd=[]
            bb_array=pd.DataFrame(bb_a)
            for i in range(bb_a.shape[0]):
                asd.append((bb_a[0]-bb_a[i])*-2)
            asd.append((bb_a[1]-bb_a[2])*-2)
                  
            bb_mat=pd.DataFrame(asd)

            for i in range(rep.shape[0]):
                A = np.array(pd.DataFrame(np.array(bb_mat)))
                b = np.array(rep.iloc[i])
        
                qas=[]
                for t in range(len(b)):
                    qas.append(b[0]**2-b[t]**2)
                qas.append(b[1]**2-b[2]**2)
        
                x=np.linalg.solve(A[1:]+0.001,qas[1:])
                relative_rep.append(x)    
    
        elif metric == 'canberra':
            for i in range(rep.shape[0]):
                asdf=[]
                bb_a=np.zeros((rep_cs.shape[1],rep_cs.shape[1]))
                bb_a[np.diag_indices_from(bb_a)] = 1
                bb_array=pd.DataFrame(bb_a)
                dist=rep.iloc[i]
                A=np.array(bb_array*(dist-4))
                b=2-dist
                for t in np.linalg.solve(A,pd.DataFrame(b)):
                    asdf.append(float(t))
                relative_rep.append(asdf)
        return np.array(relative_rep)


# In[ ]:




