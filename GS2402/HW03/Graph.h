#include <cassert>

using namespace std;

class Queue{
	public:
	Queue(int cap = 20);
	void enqueue(double x);
	double dequeue();
	double peekHead();
	double peekTail();
	int size();
	bool isEmpty();
	private:
	int capacity;
	double* p;
	int length;
	int head;
	int tail;
};

Queue::Queue(int cap){
	this->capacity = cap;
	p = new double[capacity];
	length=0; head=0; tail=0;
};

int Queue::size() {return length;}

bool Queue::isEmpty() {return (length==0);}

double Queue::peekHead(){assert(length>0); return p[head];}

double Queue::peekTail(){assert(length>0); return p[tail];}

void Queue::enqueue(double x){
	if(length==0){p[tail] =x; length++;}
	else if (length<capacity){length++; tail = (tail+1)%capacity; p[tail] = x;}
	else{
		double* q = new double[2*capacity];
		int j = head;
		for(int i=0;i<capacity;i++){q[i] = p[j]; j = (j+1)%capacity;}
		head =0;
		tail = capacity;
		q[tail] = x;
		length++;
		capacity = 2*capacity;
		delete []p;
		p=q;
	}
};

double Queue::dequeue(){
	assert(length>0);
	double x = p[head];
	head = (head+1)%capacity;
	length--;
	return x;
};
class Graph {
	public :
 	Graph(int n = 0); // creates a graph of n nodes and no edges
	bool isEdge(int i, int j);
	void setEdge(int i, int j, bool x); // set edge to true or false
	int getNumberOfNodes() { return numberOfNodes; }
	void setDistance(int i, int j, double dist);
	double getDistance(int i, int j);
	private :
	double** l;
	bool** p; // a 2-D array, i.e., an adjacency matrix
	int numberOfNodes;
};

Graph::Graph(int n) {
	assert(n >= 0);
	numberOfNodes = n;
	if (n == 0) p = NULL;
	else {
		p = new bool*[n];
		l = new double*[n];
		for (int i=0; i<n; i++) {
			p[i] = new bool[n];
			l[i] = new double[n];
			for (int j=0; j<n; j++){
				p[i][j] = false;
				l[i][j] = 0;
			}
		}
	}
}

bool Graph::isEdge(int i, int j){
	assert(i>=0 && j>=0);
	return p[i][j];
};

void Graph::setEdge(int i, int j, bool x){
	assert(i>=0 && j>=0);
	p[i][j] = x;
};

void Graph::setDistance(int i, int j, double dist){
	assert(i>= 0 && j>=0);
	setEdge(i, j, true);
	setEdge(j, i, true);
	l[i][j] = dist;
	l[j][i] = dist;
	setEdge(i, i, true);
	setEdge(i, i, true);
	l[i][i] = 0;
	l[j][j] = 0;
}

double Graph::getDistance(int i, int j){
	assert(i>= 0 && j>=0);
	return l[i][j];
}

int getNextUnvisitedNeighbor(int t, Graph *G, bool visited[], int n) {
	for (int j=0; j<n; j++)
		if (G->isEdge(t, j) && !visited[j]) return j;
		// if no unvisited neighbors left:
	return n;
}

int getNextUnvisited(bool visited[], int n, int lastVisited) {
	int j = lastVisited + 1;
		while (visited[j] && j<n) j++;
	return j;
}

void visit(int x){
	cout << x <<" ";
}

int* dfs(Graph *G) { // returns a parent array
	int n = G->getNumberOfNodes(); // representing the DFS tree
	int *parent = new int[n];
	Queue S; bool visited[n];
	for (int i=0; i<n; i++) visited[i] = false;
	int x = 0; // begin DFS from node 0
	int numOfConnectedComponents = 0;
	while (x < n) { // begin a new DFS from x
		visit(x);
		numOfConnectedComponents++;
		visited[x] = true; 
		S.enqueue(x); 
		parent[x] = -1; // x is root
		while(!S.isEmpty()){ // traverse the current piece{
			double t = S.peekHead( );
			int y = getNextUnvisitedNeighbor(t, G, visited, n);
			if (y < n) {
				visit(y);
				visited[y] = true; S.enqueue(y); parent[y] = t;
			}
			else S.dequeue( );
		}
		// insert here the yellow box from the next slide
		x = getNextUnvisited(visited, n, x);
	}
	cout << "\nGraph has " << numOfConnectedComponents << " connected components\n";
	return parent;
}
