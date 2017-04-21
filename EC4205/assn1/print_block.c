#include <stdio.h>

void print_block(Command command_block){
	int i, j;

	printf("==========================\n");
	printf("OPTYPE : %s\n", command_block.optype);
	printf("COMMAND : ");
	for(j = 0; j < command_block.commfile_len; ++j){
		printf("%s ", command_block.commfile[j]);
	}
	printf("\n");
	printf("MY_PID : %d\n", command_block.my_pid);
	printf("SIBLING_PID : %d\n", command_block.sibling_pid);
	printf("==========================\n");
}
void print_blocks(Command* command_block, int command_num){
	int i, j;

	for(i = 0; i < command_num; ++i){
		printf("==========================\n");
		printf("OPTYPE : %s\n", command_block[i].optype);
		printf("COMMAND : ");
		for(j = 0; j < command_block[i].commfile_len; ++j){
			printf("%s ", command_block[i].commfile[j]);
		}
		printf("\n");
		printf("MY_PID : %d\n", command_block[i].my_pid);
		printf("SIBLING_PID : %d\n", command_block[i].sibling_pid);
	}
	printf("==========================\n");
}
