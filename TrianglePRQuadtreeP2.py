import sys

class Vertex(object):
    def __init__(self,x=None,y=None,z=None):
        self.x = x
        self.y = y
        self.z = z
    def __getitem__(self,i):
        if i == 0 : return self.x
        if i == 1 : return self.y
        if i == 2 : return self.z
    def __str__(self):
        return "(X:%s,Y:%s,Z:%s)"%(self.x,self.y,self.z)
    

class Triangle(object): 
    def __init__(self,v1,v2,v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    def __getitem__(self,i):
        if i == 0 : return self.v1
        if i == 1 : return self.v2
        if i == 2 : return self.v3
    def __iter__(self):
        return self
    def __str__(self):
        return "(v1:%s,v2:%s,v3:%s)"%(self.v1,self.v2,self.v3)
        
    
class Domain(object):
    def __init__(self, cx=0, cy=0, length=None):
        self.cx = cx
        self.cy = cy
        self.length = length
        

class Node(object):
    def __init__(self,nodetype=None,square=None):
        self.nodetype = nodetype
        self.square = square
        self.ne = None
        self.nw = None
        self.sw = None
        self.se = None
        self.vertices = []
        self.triangles = []
    
    def is_leaf(self):
        return self.ne == None and self.nw == None and self.sw == None and self.se == None
        
    def contains_point(self,pt):
        px = pt.x
        py = pt.y
        x0 = self.square.cx - (self.square.length/2)
        x1 = self.square.cx + (self.square.length/2)
        y0 = self.square.cy - (self.square.length/2)
        y1 = self.square.cy + (self.square.length/2)
        if x1 == 512:
            if px < x0 or px > x1:
                return False
        elif px < x0 or px >= x1:
            return False
        if y1 == 512:
            if py < y0 or py > y1:
                return False
        elif py < y0 or py >= y1:
            return False
        return True
    
    def contains_triangle(self,tri,vert): 
        if self.contains_point(vert[tri.v1]):
            return True
        elif self.contains_point(vert[tri.v2]):
            return True
        elif self.contains_point(vert[tri.v3]):
            return True
        else:
            return False
        

class Tree(object):
    def __init__(self,root,cap):
        self.root = root
        self.cap = cap
    
    def point_query(self,node,node_label,search_point,points):
        #points is the list of point coords read from file every time point is searched
        #search point use Point class
        if node == None:
            return
        else:
            if node.contains_point(search_point):
                print(node_label, end =" ")
                if node.is_leaf():
                    for i in node.points:
                        if search_point.x == points[i].x and search_point.y == points[i].y:
                            print("\nFOUND, Equal to Point Index",i)
                            return
                    print("\nPOINT NOT FOUND")
                    return
                elif node.nodetype == "INTERNAL":
                    child_label = 4*node_label + 1
                    self.point_query(node.ne,child_label,search_point,points)
                    child_label = 4*node_label + 2
                    self.point_query(node.nw,child_label,search_point,points)
                    child_label = 4*node_label + 3
                    self.point_query(node.sw,child_label,search_point,points)
                    child_label = 4*node_label + 4
                    self.point_query(node.se,child_label,search_point,points)
    
        
    def insert_point(self,node,node_label,p_index,points):
        #points is the list of point coords read from file every time point is inserted
        if node.contains_point(points[p_index]):
            if node.nodetype == "EMPTY":
                node.vertices.append(p_index)
                node.nodetype = "FULL"
                print("\tINSERTED",str(p_index),"INTO NODE:",str(node_label),str(node.square.cx),str(node.square.cy),str(node.square.length))
            
            elif node.nodetype == "FULL":
                node.vertices.append(p_index)
                if len(node.vertices) > self.cap:
                    node.nodetype = "INTERNAL"
                    
                    childLen = node.square.length / 2
                    nechildcx = node.square.cx + childLen / 2
                    nechildcy = node.square.cy + childLen / 2
                    node.ne = Node("EMPTY",Domain(nechildcx,nechildcy,childLen))
                    
                    nwchildcx = node.square.cx - childLen / 2
                    nwchildcy = node.square.cy + childLen / 2
                    node.nw = Node("EMPTY",Domain(nwchildcx,nwchildcy,childLen))
                    
                    swchildcx = node.square.cx - childLen / 2
                    swchildcy = node.square.cy - childLen / 2
                    node.sw = Node("EMPTY",Domain(swchildcx,swchildcy,childLen))
                    
                    sechildcx = node.square.cx + childLen / 2
                    sechildcy = node.square.cy - childLen / 2
                    node.se = Node("EMPTY",Domain(sechildcx,sechildcy,childLen))
                    
                    for i in node.vertices:
                        self.insert_point(node.ne,4*node_label + 1,i,points)
                        self.insert_point(node.nw,4*node_label + 2,i,points)
                        self.insert_point(node.sw,4*node_label + 3,i,points)
                        self.insert_point(node.se,4*node_label + 4,i,points)
                    node.vertices = []
                    
            elif node.nodetype == "INTERNAL":
               self.insert_point(node.ne,4*node_label + 1,p_index,points)
               self.insert_point(node.nw,4*node_label + 2,p_index,points)
               self.insert_point(node.sw,4*node_label + 3,p_index,points)
               self.insert_point(node.se,4*node_label + 4,p_index,points)
        
        
    def insert_triangle(self,node,node_label,triindex,tris,verts):
        if node.contains_triangle(tris,verts): 
            if node.nodetype == "FULL":
                node.triangles.append(triindex)
                print("\tINSERTED",str(triindex),"INTO NODE:",str(node_label))
            elif node.nodetype == "INTERNAL":
                self.insert_triangle(node.ne,4*node_label + 1,triindex,tris,verts)
                self.insert_triangle(node.nw,4*node_label + 2,triindex,tris,verts)
                self.insert_triangle(node.sw,4*node_label + 3,triindex,tris,verts)
                self.insert_triangle(node.se,4*node_label + 4,triindex,tris,verts)
            return
    
        
    def min_max_query(self,node,tris,verts,minarray,maxarray):
        #check if node is full or internal
        #need min max arrays outside this function
        if node.nodetype == "FULL":
            VV = []
            for j in node.vertices:
                VV.append(set())
            for i in node.triangles:
                tri = tris[i]
                if node.contains_point(verts[tri.v1]):
                    pos = node.vertices.index(tri.v1)
                    VV[pos].add(tri.v1)
                    VV[pos].add(tri.v2)
                    VV[pos].add(tri.v3)
                elif node.contains_point(verts[tri.v2]):
                    pos2 = node.vertices.index(tri.v2)
                    VV[pos2].add(tri.v1)
                    VV[pos2].add(tri.v2)
                    VV[pos2].add(tri.v3)
                elif node.contains_point(verts[tri.v3]):
                    pos3 = node.vertices.index(tri.v3)
                    VV[pos3].add(tri.v1)
                    VV[pos3].add(tri.v2)
                    VV[pos3].add(tri.v3)
            
            for k in VV:
                arr = []
                arr2 = []
                for j in k:
                    arr.append(verts[j].z)
                    arr2.append(j)
                minpos = arr.index(min(arr))
                maxpos = arr.index(max(arr))
                minarray.add(arr2[minpos])
                maxarray.add(arr2[maxpos])
                    
        elif node.nodetype == "INTERNAL":
            self.min_max_query(node.ne,tris,verts,minarray,maxarray)
            self.min_max_query(node.nw,tris,verts,minarray,maxarray)
            self.min_max_query(node.sw,tris,verts,minarray,maxarray)
            self.min_max_query(node.se,tris,verts,minarray,maxarray)
            return 
        
            
    def preorder(self,node,node_label):
        if node == None:
            return
        else:
            if node.nodetype == "EMPTY":
                print("Node:",node_label,"EMPTY LEAF")
                
            elif node.nodetype == "FULL":
                print("Node:",node_label,"FULL LEAF\n","\tV",str(len(node.vertices)),str([i for i in node.vertices]),
                      "\n","\tT",str(len(node.triangles)),str([j for j in node.triangles]))
                
            elif node.nodetype == "INTERNAL":
                print("Node:",node_label,"INTERNAL")
                self.preorder(node.ne,4*node_label + 1)
                self.preorder(node.nw,4*node_label + 2)
                self.preorder(node.sw,4*node_label + 3)
                self.preorder(node.se,4*node_label + 4)
                
                
            
def read_mesh_file(url_in):
    points=[]
    triangles=[]

    with open(url_in) as infile:
        vertices_num= infile.readline().strip()
        vertices_num=int(vertices_num)
        for l in range(vertices_num):
            line = (infile.readline()).split()
            point=Vertex(int(line[0]),int(line[1]),int(line[2]))
            points.append(point)
        triangles_num = infile.readline().strip()
        triangles_num = int(triangles_num)
        for l in range(triangles_num):
            line = (infile.readline()).split()
            triangle=Triangle(int(line[0]),int(line[1]),int(line[2]))
            triangles.append(triangle)
        infile.close()
        return (vertices_num,points,triangles_num,triangles)
    

if __name__ == "__main__":
    meshdata = sys.argv[1]
    
    Mesh = read_mesh_file(meshdata)
    Vertices = Mesh[1]
    Triangles = Mesh[3]
    cap = int(sys.argv[2])
        
    rootDom = Domain(256,256,512)
    rootNode = Node("EMPTY",rootDom)
    QT = Tree(rootNode,cap)
    
    print("START POINT TRIANGLE INPUT\n")
    for i in range(len(Vertices)):
        print("INSERT POINT:",i,str(Vertices[i]))
        QT.insert_point(rootNode,0,i,Vertices)
        
    print("\n")
    
    for j in range(len(Triangles)):
        print("INSERT TRIANGLE",j,str(Triangles[j]))
        QT.insert_triangle(rootNode,0,j,Triangles[j],Vertices)
        
    print("\nEND POINT TRIANGLE INPUT")
    print("\n")
    print("START TRIANGLE PR")
    QT.preorder(rootNode,0)
    print("END TRIANGLE PR\n")
    
    print("BEGIN MIN-MAX QUERY")
    minarr = set()
    maxarr = set()
    
    QT.min_max_query(rootNode,Triangles,Vertices,minarr,maxarr)
    print("Minima:",minarr)
    print("Maxima:",maxarr)
    
    
    print("END MIN-MAX QUERY")






























