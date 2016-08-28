#include <iostream>
#include <cassert>
#include <algorithm>
#include <stdlib.h>
#include "Stack.h"
#include <stdio.h>

using namespace std;

template <class T>
Stack<T>::Stack(int cap)
{
	Capacity = cap;
	p = new T[this->Capacity];
	length=0;
	head=0;
}

char* toPostfix (char* expr){
	int i=0;
	int k=0;
	int len;
	char* PostStr = new char[len*2];
	Stack<char> stack(100);
	char head;

	while(1){
		if(expr[i]=='\0')
		{
			len=i;
			break;
		}
		i++;
	}

	for(i=0;i<len;i++)
	{
		char token = expr[i];
		if(token=='(')
		{
			stack.push('(');
		}
		else if(token==')')
		{
			while(stack.peekHead()!='(')
			{
				PostStr[k] = stack.pop();
				k++;
			}
			if(stack.peekHead()=='(')
				stack.pop();
		}
		else if(token=='+' or token=='-')
		{	
			while(1)
			{
				if(stack.size()==0)
					break;
				head = stack.peekHead();
				if((head == '+' or head == '-' or head == '*' or head == '/'))
				{
					PostStr[k]=stack.pop();
					k++;
				}
				else
					break;
			}
			stack.push(token);
		}
		else if(token=='*' or token=='/')
		{	
			while(1)
			{
				if(stack.size()==0)
					break;
				head = stack.peekHead();
				if((head == '*' or head == '/'))
				{
					PostStr[k]=stack.pop();
					k++;
				}
				else
					break;
			}
			stack.push(token);
		}
		else{
			PostStr[k]=token;
			k++;
		}
	}

	while(stack.size()>0)
	{
		if(stack.peekHead()=='(')
			stack.pop();
		PostStr[k]=stack.pop();
		k++;
	}
	PostStr[len] = '\0';
	return PostStr;
}

double eval(char* expr){
	int charon=0;
	int i=0;
	int len;
	Stack<double> stack(100);

	while(1){
		if(expr[i]=='\0')
		{
			len=i;
			break;
		}
		i++;
	}

	for(i=0;i<len;i++)
	{
		char token = expr[i];

		if(int(token)>=48 and int(token)<=57)
			stack.push(double(static_cast<int>(token)-48));

		else if(token == '*')
		{
			double oper1 = stack.pop();
			double oper2 = stack.pop();
			stack.push(oper2*oper1);
		}
		else if(token == '/')
		{
			double oper1 = stack.pop();
			double oper2 = stack.pop();
			stack.push(oper2/oper1);
		}
		else if(token == '+')
		{
			double oper1 = stack.pop();
			double oper2 = stack.pop();
			stack.push(oper2+oper1);
		}
		else if(token == '-')
		{
			double oper1 = stack.pop();
			double oper2 = stack.pop();
			stack.push(oper2-oper1);
		}
		else
		{
			if(charon==0)
				cout<<endl<<"There are some character operands like 'a', 'b', 'c', 'd', and 'e'."<<endl<< "Those will be considered 4, 2, 2, 3, and 3, repectively."<<endl<<"i.e.) a=4, b=c=2, and d=e=3"<<endl<<endl;
			if(token=='a')
				stack.push(4);
			else if(token=='b' or token=='c')
				stack.push(2);
			else if(token=='d' or token=='e')
				stack.push(3);
			charon++;
		}
	}

	return stack.pop();
}


int main(void){
	char input[50];
	cout<<endl<<"Enter an infix expression : ";
	cin>>input;
	cout<<"Postfix expression : "<<toPostfix(input)<<endl;
	cout<<"Evaluation value is... "<<eval(toPostfix(input))<<endl<<endl;

	return 0;
}
