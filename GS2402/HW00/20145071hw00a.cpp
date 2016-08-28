#include <iostream>
#include "applebox.h"
using namespace std;

int main(void){
	AppleBox AppBox1;
	int number_apple;
	int add_num_selection;

	cout<<"How many apples in the box? : ";
	cin>>number_apple;

	AppBox1.set_num_apple(number_apple);
	
	for(;;){
		cout<<"If you want to put an apple, enter 1. If you want to quit, enter other number : ";
		cin>>add_num_selection;
		if(add_num_selection==1){AppBox1.add_one_apple();}
		else{break;}
	}

	cout<<"apple : "<<AppBox1.get_num_apple()<<endl;

	return 0;
}
