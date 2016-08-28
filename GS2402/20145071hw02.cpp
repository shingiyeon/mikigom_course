#include <iostream>
#include <cstring>
#include <stdio.h>
#include "Tree.h"

using namespace std;

TreeNode ascii[128];
TreeNode node[200];

template <class T>
Tree<T>* CreateHuffmanTree(char* text){
	Tree<T> heap; int nodeNumber=0;

	for(int i=0; i<128;i++){
		ascii[i].left=NULL;
		ascii[i].DATA=i;
		ascii[i].right=NULL;
		}

	for(int i = 0; i < strlen(text); i++)
		ascii[text[i]].freq++;

	for(int n=0; n<128; n++)
		heap.Insert(&ascii[n]);

	while(heap.length>1){
		node[nodeNumber].Insert(heap.getMin(), heap.getMin());
		heap.Insert(&node[nodeNumber]);
		nodeNumber++;
	}
	
	Tree<T> *Huffman = new Tree<T>;
	Huffman->setRoot(heap.getMin());

	return Huffman;
}

template <class T>
char* compress(Tree<T>* HuffmanTree, char* text){
	int j;
	int compressed=0;
	int codeLength[128]={0,};	
	int temp_codeLength[128];
	int code[128][20];
		
	for (int i=0; i < 128; ++i)
		for (int j=0; j<20; ++j)
			code[i][j]=0;

	for (int n=0; n<128; n++){
		int index;
		TreeNode *nowNode=&ascii[n];	
		int tempCode[2000]={0,};
		for (index=0; nowNode->parent!=NULL; index++)
		{
			if (nowNode==nowNode->parent->left)
				tempCode[index]=0;
			else								
				tempCode[index]=1;
			nowNode=nowNode->parent;
		}
		codeLength[n]=index;

		for (int i=0, j=codeLength[n]-1; i<codeLength[n]; i++, j--)
			code[n][i]=tempCode[j];

		if (ascii[n].freq!=0){
			printf("%c : ",n);
			for(int i=0; i<codeLength[n];i++)
				cout<<code[n][i];
			cout<<"  "<<codeLength[n]<<"bits"<<endl;
			temp_codeLength[n]=codeLength[n];
			}
	}
	
	char compressed_arr[20000];
	int k=0;
	
	for(int i=0;i<strlen(text);i++){
		int token = static_cast<int>(text[i]);
		for(int j=0;j<temp_codeLength[token];j++){
			if(code[token][j]==1)
				compressed_arr[k]='1';
			else
				compressed_arr[k]='0';
			k++;
		}
	}
	compressed_arr[k]='\0';
	
	return compressed_arr;
}

template <class T>
char* decompress(Tree<T>* HuffmanTree, char* bitarray){
	int arr_len = strlen(bitarray);
	TreeNode *nodePtr = HuffmanTree->getRoot();
	char decompressed_arr[20000];
	int k=0;

	for(int i=0; i<arr_len; i++){
		char token = bitarray[i];
		if(token == '0')
			nodePtr = nodePtr->left;
		else if(token == '1')
			nodePtr = nodePtr->right;

		if(nodePtr->left == NULL && nodePtr->right == NULL && nodePtr->freq != 0){
			decompressed_arr[k]=static_cast<char>(nodePtr->DATA);
			nodePtr = HuffmanTree->getRoot();
			k++;
		}
	}

	decompressed_arr[k] = '\0';
	return decompressed_arr;	
}
	
int main(void){
	char selec;
	cout << "Start of the program"<<endl;
	cout << "==================================================================="<<endl;
	cout << "This program is for implementation of Huffman coding/decoding." <<endl<<endl;
	cout << "This program is going to test the case 1 'free input', and the case 2 'Steve Jobs'."<<endl;

	char text[2000]={0,};
	int i;
	char *compressed_text, *decompressed_text;

	cout << "Enter the text whatever you want to encode :"<<endl;
	cin.getline(text,2000);
	cout<<endl<<endl;

	Tree<int>* HuffmanTree = CreateHuffmanTree<int>(text);

	compressed_text = compress(HuffmanTree, text);
	cout<<endl<<"The compressed text is the following : "<<endl<<compressed_text<<endl;

	decompressed_text = decompress(HuffmanTree, compressed_text);
	cout<<endl<<"The decompressed text of the former is the following : "<<endl<<decompressed_text<<endl<<endl;
	
	cout<<"The size of the original text is "<<strlen(text)*8<<"bits."<<endl;
	cout<<"The encoded size of it is "<<strlen(compressed_text)<<"bits."<<endl;
	cout<<"The modulus of compression is "<<100*static_cast<double>(strlen(compressed_text))/static_cast<double>((strlen(text)*8))<<'%'<<'.'<<endl<<endl;

	cout<<"The end of free input text case."<<endl;
	cout<<"-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -"<<endl;
	cout<<"After this line, the 'Steve Jobs' text is encoded/decoded."<<endl<<endl;

	char steve[] = "On a warm June day in 2005, Steve Jobs went to his first college graduation - as the commencement speaker. The billionaire founder and leader of Apple Computer wasn't just another stuffed-shirt businessman. Though only fifty years old, the college dropout was a technology rock star, a living legend to millions of people around the world. In his early twenties, Jobs almost single-handedly introduced the world to the first computer that could sit on your desk and actually do something all by itself. He revolutionized music and the ears of a generation with a spiffy little music player called the iPod and a wide selection of songs at the at the iTunes store. He funded and nurtured a company called Pixar that made the most amazing computer-animated movies - Toy Story, Cars, and Finding Nemo - bringing to life imaginary characters like never before. Though he was neither an engineer nor a computer geek, he helped create one gotta-have-it product after another by always designing it with you and me, the actul users, in mind. Unknown to those listening to him that day, more insanely awesome technology was in the works, including the iPhone, which would put much of the power of a computer neatly into the palm of your hand. The father of four would be repeatedly compared with the inventor Thomas Edison and auto magnate Henry Ford, who both introduced affordable, life-changing conveniences that transformed the way Americans lived.";

	char steve_arr[2000];
	for(i=0;steve[i]!='\0';i++)
		steve_arr[i]=steve[i];
	steve_arr[i]='\0';

	cout<<endl<<"The original text is the following : "<<endl<<steve<<endl<<endl;

	Tree<int> *SteveHuffmanTree = CreateHuffmanTree<int>(steve_arr);

	compressed_text = compress(SteveHuffmanTree, steve_arr);
	cout<<endl<<"The compressed text is the following : "<<endl<<compressed_text<<endl;

	decompressed_text = decompress(SteveHuffmanTree, compressed_text);
	cout<<endl<<"The decompressed text of the former is the following : "<<endl<<decompressed_text<<endl<<endl;
	
	cout<<"The size of the original text is "<<strlen(steve)*8<<"bits."<<endl;
	cout<<"The encoded size of it is "<<strlen(compressed_text)<<"bits."<<endl;
	cout<<"The modulus of compression is "<<100*(static_cast<double>(strlen(compressed_text))/static_cast<double>((strlen(steve)*8)))<<'%'<<'.'<<endl<<endl;
	cout<<"End of the 'Steve Jobs' test case."<<endl;
	cout<<"- - - - - - - - - - - - - - - - - - "<<endl;

	cout<<"End of Program"<<endl<<"==================================================="<<endl;
	return 0;
}
