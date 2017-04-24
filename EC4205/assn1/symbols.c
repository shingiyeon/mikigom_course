#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/types.h>

void print_prompt(){
    char currentPath[256];
    getcwd(currentPath, 256);
    printf("%s> ", currentPath);
}

void exit_cmd(){
    exit(1);
}

void cd_cmd(Command* blocks, int block_num){
    if( blocks[0].commfile_len == 1)
        chdir( getenv("HOME") );
    else if( blocks[0].commfile_len == 2){
        if( chdir( blocks[0].commfile[1] ) )
             printf("No Directory\n");
    }
    else
        printf("error\n");
}

void execute_cmd(Command* blocks, int block_num, int num){
    int error;
    error = execvp( blocks[num].commfile[0], blocks[num].commfile );
    if( error == -1 ){
         printf("Error\n"); exit(0);
    }
}


void execute_redirect(Command* blocks,int block_num, int start_b, int final_b){
    int i = start_b;
    int fd;
    if(start_b == final_b)
        execvp( blocks[start_b].commfile[0], blocks[start_b].commfile );
    
    for( i = start_b; i <= final_b; i++){
        if( strcmp(blocks[i].optype, "<") == 0){
            //printf(" < %d %s\n",i,blocks[i].commfile[0]);
            if( (fd = open( blocks[i].commfile[0], O_RDONLY, 0644)) < 0){
                 perror("file open error");
                 exit(1);
            }     
            dup2(fd, 0);
            close(fd);
        }
        else if( strcmp(blocks[i].optype, ">") == 0){
            //printf(" > %d %s\n",i,blocks[i].commfile[0]);
            if( (fd = open( blocks[i].commfile[0], O_WRONLY | O_CREAT | O_TRUNC, 0644)) < 0){
                 perror("file open error");
                 exit(1);
            }
            dup2(fd, 1);
            close(fd);
        }
        else if( strcmp(blocks[i].optype, ">>") == 0){
            if( (fd = open( blocks[i].commfile[0], O_WRONLY | O_CREAT | O_APPEND, 0644)) < 0){
                 perror("file open error");
                 exit(1);
            }
            dup2(fd, 1);
            close(fd);
        }
    }
    //printf("%d %d\n",start_b,final_b);
    execute_cmd(blocks, block_num, start_b);
}

void execute_pipe(Command* blocks, int block_num){
    int pipen = 0;
    int temp = 1;
    int i, j;
    int fd[2];
    pid_t pid;
    for(i = 0; i < block_num; i++){
        if( strcmp( blocks[i].optype, "|") == 0 )
            pipen++;
    }
    int* pipegroup = malloc( (pipen+1)*sizeof(int) );
    //printf("pipeline allocation\n");
    pipegroup[0] = 0;
    for(i = 1; i < block_num; i++){
       // printf("%d\n",i);
        if( strcmp( blocks[i].optype, "|") == 0 ){
            pipegroup[temp] = i;
            temp++;
        }
    }
    i = 0;
    for(i = 0; i < pipen; i++)
    {
        pipe(fd);
        //printf("pipe %d\n", i);
        pid = fork();
        if( pid == -1 ){
            perror("Fork() error");
        }
        else if( pid == 0){
            close(fd[0]);
            dup2(fd[1], 1);
            execute_redirect(blocks,block_num, pipegroup[i], pipegroup[i+1]-1);
        }
        else{
            close(fd[1]);
            dup2(fd[0], 0);
        }
    }
    execute_redirect(blocks,block_num, pipegroup[pipen], block_num-1);
} 
           
void get_cmd(Command* blocks, int block_num){
    int status;
    if( !strcmp( blocks[0].commfile[0], "logout") || !strcmp( blocks[0].commfile[0], "exit")){
        exit_cmd();
    }
    else if( !strcmp(blocks[0].commfile[0], "cd") ){
        cd_cmd(blocks, block_num);
    }
    else{
        //execute_pipe(blocks, block_num);
        pid_t pid = fork();
        if( pid < 0 ) perror("fork() error");
        else if(!pid) execute_pipe(blocks, block_num);
        else { waitpid(pid,&status,0);  }
    }
}
