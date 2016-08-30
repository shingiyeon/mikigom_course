#include <iostream>
#include <cstdlib>
using namespace std;

class TreeNode{	
	public:
		TreeNode *left, *right, *parent;		
		bool isLeaf;					
		char DATA;					
		int freq;						
		void Insert(TreeNode *one, TreeNode *two);	
		TreeNode();
};
TreeNode::TreeNode() {
	left=NULL;
	right=NULL;
	parent=NULL;
	isLeaf=true;
	DATA=0;
	freq=0;
}

void TreeNode::Insert(TreeNode *one, TreeNode *two){
	if (one&&two) {
		if (one->freq<two->freq){
			left=one;
			right=two;
		}
		else{
			left=two;
			right=one;
		}
		left->parent=this;
		right->parent=this;
		freq = left->freq + right->freq;
		isLeaf= false;
	}
	else if (one){
		left = one;
		left -> parent = this;
		freq = left -> freq;
		isLeaf= false;
	}
	else if (two){
		left=two;
		left->parent=this;
		freq=left->freq;
		isLeaf= false;
	}
	else
		return;
}

#define		IsBig(a, b)		((a)&&(b)&&(a)->freq>(b)->freq)

template <class T>
class Tree{	
	public:
		void setRoot(TreeNode *ptr){rootPtr = ptr;}
		TreeNode* getRoot(){return rootPtr;}
		int length;							
		void Insert(TreeNode *toInsert);				
		TreeNode* getMin();							
		Tree(){for (int n=0; n<1024; n++){array[n]=NULL;} length=0;}

	private:
		TreeNode *rootPtr;
		TreeNode *array[1024];					
		void RebuildUp(int index);					
		void RebuildDown(int index);					
		void Swap(int index1, int index2);
};

template <class T>
void Tree<T>::RebuildUp(int index)
{
	while ((index>0)&&IsBig(array[index/2], array[index]))
	{
		Swap(index, index/2);
		index/=2;
	}
}

template <class T>
void Tree<T>::RebuildDown(int index)
{
	while ((index*2<=length)&&(IsBig(array[index], array[index*2])||IsBig(array[index], array[index*2+1])))
	{	
		if (IsBig(array[index*2], array[index*2+1]))
		{	
			Swap(index, index*2+1);
			index=index*2+1;
		}
		else
		{
			Swap(index, index*2);
			index=index*2;
		}
	}
}

template <class T>
void Tree<T>::Swap(int index1, int index2)
{
	TreeNode *temp=array[index1];
	array[index1]=array[index2];
	array[index2]=temp;
}

template <class T>
void Tree<T>::Insert(TreeNode *toInsert)
{
	length++;
	array[length]=toInsert;
	RebuildUp(length);
}

template <class T>
TreeNode* Tree<T>::getMin()
{
	TreeNode *min=array[1];
	array[1]=array[length];
	array[length]=NULL;
	length--;
	RebuildDown(1);
	return min;
}
