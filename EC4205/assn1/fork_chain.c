#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "comm2block.c"
#include "print_block.c"
#include "symbols.c"

//int block_num = 0;
int counter = 0;
//Command* blocks;
/*
void child_func() {
    pid_t pid;
    if (counter < block_num) {
        counter++;
        pid = fork();
        if (pid < 0) {
            printf("fork failed counter = %d\n", counter);
        }
        else if (pid == 0) {
            printf("Hello world ! Greetings from pid %ld\n", (long)getpid());
            if (counter == block_num)
                exit(0);
            else 
                child_func();
        }
        else {
			blocks[counter-1].my_pid = getpid();
			blocks[counter-1].sibling_pid = pid;
			print_block(blocks[counter-1]);
            long var = pid;
            wait(&pid);
            printf("My pid is %ld and i am the parent of %ld child, i exit\n", (long)getpid(), var);
            exit(0);
        }
    }
}*/

int main(void) 
{
    while(1){
        Command* blocks;
        int block_num;
        print_prompt();
        blocks = comm2block(&block_num);
        if(feof(stdin)){
            printf("Ctrl+D exit\n");
            exit(0);
        }
        fflush(stdin);
        get_cmd(blocks, block_num);
        free(blocks);
    }
    return 0;
}
