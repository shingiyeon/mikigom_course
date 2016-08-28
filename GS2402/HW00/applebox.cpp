#include "applebox.h"

AppleBox::AppleBox()
{
	num_apple=0;
}

void AppleBox::set_box_size(int size)
{
	size_of_box=size;
}

void AppleBox::set_num_apple(int n)
{
	num_apple=n;
}

void AppleBox::add_one_apple(void)
{
	num_apple++;
}

void AppleBox::remove_one_apple(void)
{
	num_apple--;
}

int AppleBox::get_num_apple(void)
{
	return num_apple;
}

int AppleBox::get_box_size(void)
{
	return size_of_box;
}

bool AppleBox::is_empty(void)
{
	if(num_apple==0){return true;}
	else{return false;}
}

bool AppleBox::is_full(void)
{
	if(num_apple==size_of_box){return true;}
	else{return false;}
}
