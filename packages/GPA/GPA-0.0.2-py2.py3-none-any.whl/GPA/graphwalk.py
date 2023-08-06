import numpy as np
import scipy.sparse as sp

def GraphWalk(nodes, edges, mask, step=1, direction='forward', contained=False):
    # get node id dict.
    nodeIDs = dict((nID, idx) for idx, nID in enumerate(nodes.T[0]))
    # get the adjency matrix.
    nodesOut = [nodeIDs[n] for n in edges.T[0]]
    nodesIn = [nodeIDs[n] for n in edges.T[1]]
    A = sp.coo_matrix((np.ones(len(edges)), (nodesOut, nodesIn)), 
                      shape=(len(nodes), len(nodes)), dtype="float32")
    I = sp.eye(len(nodes)) # identity matrix.
    # calcualte total adjency matrix.
    if direction == 'forward':
        M = A
    elif direction == 'backward':
        M = A.T
    elif direction == 'bidirect':
        M = A + A.T
    if contained:
        temp = I
        while (step):
            temp += M ** step
            step -= 1
        M = temp
    else:
        M = M ** step
    # calcualte the mask.
    print(M.toarray())
    _mask_ = np.array([1 if i else 0 for i in mask * M])

    return _mask_