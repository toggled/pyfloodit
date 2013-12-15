'''
unionfind.py

A class that implements the Union Find data structure and algorithm.  This
data structure allows one to find out which set an object belongs to, as well
as join two sets.

The algorithm's performance, given m union/find operations of any ordering, on
n elements has been shown to take log* time per operation, where log* is
pronounced log-star, and is the INVERSE of what is known as the Ackerman
function, which is given below:
A(0) = 1
A(n) = 2**A(n-1)

I include the functions to be complete.  Note that we can be 'inefficient'
when performing the inverse ackerman function, as it will only take a maximum
of 6 iterations to perform; A(5) is 65536 binary digits long (a 1 with 65535
zeroes following).  A(6) is 2**65536 binary digits long, and cannot be
represented by the memory of the entire universe.


The Union Find data structure is not a universal set implementation, but can
tell you if two objects are in the same set, in different sets, or you can
combine two sets.
ufset.find(obja) == ufset.find(objb)
ufset.find(obja) != ufset.find(objb)
ufset.union(obja, objb)


This algorithm and data structure are primarily used for Kruskal's Minimum
Spanning Tree algorithm for graphs, but other uses have been found.

August 12, 2003 Josiah Carlson
'''

class node:
        def __init__(self,val):
                self.val=val
                self.parent=None
                self.rank=0
                self.child=[]
        def __str__(self):
                return str(self.val)
        def getchild(self):
                return [x.val for x in self.child]

class UnionFind:
        def __init__(self):
                #To hold the clusters
                self.clusters = []

        #create a new set(cluster) with a node
   	def makeSet(self,node):
                #set the nodes parent to the node itself
                node.parent = node
                #set initial rank of node to 0
                #node.rank = 0
                #add the node to cluster list
                self.clusters.append(node)

        #union the nodeA and nodeB clusters
        def union(self, nodeA, nodeB):
                self.link(self.findSet(nodeA), self.findSet(nodeB))

        #link the nodeA to nodeB or vice versa based upon the rank(number of nodes in the cluster) of the cluster
        def link(self, nodeA, nodeB):
               # print "inside link: ",nodeA,nodeB
                #if nodeA.rank > nodeB.rank:
                 #       nodeB.parent = nodeA
                        #remove the nodeB from the cluster list, since it is merged with nodeA
                        #self.clusters.remove(nodeB)
                #else:
                        #print "here is: ",nodeA
                nodeA.parent = nodeB
                nodeB.child.append(nodeA)
                        #remove the nodeA from the cluster list, since it is merged with nodeB
                        #self.clusters.remove(nodeA)
                        #increade the rank of the cluster after merging the cluster
                #if nodeA.rank == nodeB.rank:
                nodeB.rank = nodeB.rank + 1

        #find set will path compress(makes the nodes in cluster points to single leader/parent) and returns the leader/parent of the cluster
        def findSet(self, node):
                if node.parent==None:
                        node.parent=node
                if node != node.parent:
                        node.parent = self.findSet(node.parent)
                return node.parent


        def print_set(self,obj):
                for ob in obj:
                        print ob,"->",self.findSet(ob),"child: ",[x.val for x in ob.child]

if __name__ == '__main__':
    print "Testing..."
    uf = UnionFind()

    node0=node(0)
    node1=node(1)
    node2=node(2)
    uf.makeSet(node0)
    uf.makeSet(node1)
    uf.makeSet(node2)
    #print uf
    uf.union(node0,node1)
    print uf.findSet(node0)
    print uf.findSet(node1)
    print uf.findSet(node2)
    print "another test"
    uf.union(node1,node2)
    print uf.findSet(node0)
    print uf.findSet(node1)
    print uf.findSet(node2)

    node3=node(3)
    uf.union(node3,node0)
    node4=node(4)
    uf.union(node4,node1)
    uf.union(node4,node3)
    print uf.findSet(node0)
    print uf.findSet(node1)
    print uf.findSet(node2)
    print uf.findSet(node3)
    print uf.findSet(node4)
    #print uf.findSet(node)

    print "Testing complete."
    #print uf.find('a')
    #uf.union(uf.findSet('a'),uf.findSet('b'))
    #print uf