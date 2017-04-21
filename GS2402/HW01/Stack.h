template <class T>
class Stack{
	private:
		int Capacity;
		T *p;
		int length;
		int head;
	public:
		Stack(int cap);
		void push(T x);
		T pop();
		T peekHead();
		int size();
		bool isEmpty();
};

template <class T>
int Stack<T>::size(){return length;}
template <class T>
bool Stack<T>::isEmpty(){return (length==0);}
template <class T>
T Stack<T>::peekHead(){assert(length>0); return p[head];}
template <class T>
void Stack<T>::push(T x){
	if(length==0){p[head]=x; length++;}
	else if(length<Capacity){head++; p[head]=x; length++;}
	else{
		T *q = new T[2*Capacity];
		for (int i=0; i<Capacity; i++){q[i]=p[i];}
		head = Capacity;
		q[head] = x;
		length++;
		Capacity = 2*Capacity;
		delete [] p;
		p = q;
	}
}
template <class T>
T Stack<T>::pop(){
	assert(length>0);
	T x = p[head];
	head > 0 ? head-- : head = 0;
	length--;
	return x;
}


