#include <iostream>
#include "applebox.h"
using namespace std;

int main(void){
	AppleBox AppBox1, AppBox2, AppBox3;
	int box1size, box2size, box3size;
	int add_substract_selection;
	int box_selection=0;

	cout<<"Size of the 1st box : ";
	cin>>box1size;
	cout<<"Size of the 2nd box : ";
	cin>>box2size;
	cout<<"Size of the 3rd box : ";
	cin>>box3size;
	AppBox1.set_box_size(box1size);
	AppBox2.set_box_size(box2size);
	AppBox3.set_box_size(box3size);
	
	for(;;){
		cout<<"If you want to put an apple, enter 1. take out, enter 2, quit the program, enter the other number : ";
		cin>>add_substract_selection;

		if(add_substract_selection!=1 && add_substract_selection!=2){break;}

		for(;;){
		cout<<"which Box? (1, 2, 3): ";
		cin>>box_selection;
		if(box_selection==1||box_selection==2||box_selection==3){break;}
		}

		if(add_substract_selection==1){
			if(box_selection==1){
				if(AppBox1.is_full()==true){cout<<"The box is full!"<<endl;}
				else{AppBox1.add_one_apple();}
				}
			else if(box_selection==2){
				if(AppBox2.is_full()==true){cout<<"The box is full!"<<endl;}
				else{AppBox2.add_one_apple();}
				}
			else if(box_selection==3){
				if(AppBox3.is_full()==true){cout<<"The box is full!"<<endl;}
				else{AppBox3.add_one_apple();}
				}
			}
		else if(add_substract_selection==2){
			if(box_selection==1){
				if(AppBox1.is_empty()==true){cout<<"The box is empty!"<<endl;}
				else{AppBox1.remove_one_apple();}
				}
			else if(box_selection==2){
				if(AppBox2.is_empty()==true){cout<<"The box is empty!"<<endl;}
				else{AppBox2.remove_one_apple();}
				}
			else if(box_selection==3){
				if(AppBox3.is_empty()==true){cout<<"The box is empty!"<<endl;}
				else{AppBox3.remove_one_apple();}
				}
		}
	}

	cout<<"box 1 => size : "<<AppBox1.get_box_size()<<" apple : "<<AppBox1.get_num_apple()<<endl;
	cout<<"box 2 => size : "<<AppBox2.get_box_size()<<" apple : "<<AppBox2.get_num_apple()<<endl;
	cout<<"box 3 => size : "<<AppBox3.get_box_size()<<" apple : "<<AppBox3.get_num_apple()<<endl;

	return 0;
}
