#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <wait.h>
#include <sys/types.h>
#include <signal.h>
#include "command_in.c"

//char str[512];
char** res = NULL;
char* _getln();
char** _strtok_by_space(char* str, int* len);
void exit_handler(void);
void print_prompt(void);
void get_cmd(char* str, int s, int e);
void exit_cmd();
void cd_cmd(char** tmpstr, int len);

int status;

void make_a_tree(char* str, int s, int e){
    int p;
    int temp;
    int fd[2]; // pipeline
    int pid; // process id
    char* pch;
    char tmpstr[512];
    int perrorc;
    strncpy(tmpstr, str+s, e-s+1);
    tmpstr[e-s+1] = '\0';
    //printf("Initial input: %s\n",tmpstr);

    if( (pch = strchr( tmpstr, '|' ))!= NULL ){
        //printf("find pipeline\n");
        p = pch - tmpstr;
        //printf("pipe %d\n", p);
        if( pipe(fd) == -1 ){
            printf("Fail to call pipe()\n");
            exit(1);
        }

        pid = fork();
        if(pid == -1){ // error
            perror("Fork() error");
        }
        else if(!pid){
                perrorc = close(1);
                if(perrorc == -1) perror("Close");
                dup(fd[1]);
                if(close(fd[0]) == -1 ||  close(fd[1]) == -1) perror("Close2");
                make_a_tree(tmpstr, s, p-1);
                perror("execlp");
        }
        else{
                perrorc = close(0);
                if(perrorc == -1) perror("Close3");
                dup(fd[0]);
                if( close(fd[0]) == -1 ||  close(fd[1]) == -1) perror("Close4");
                make_a_tree(tmpstr, p+1, e);
                perror("execlp");
                //exit(0);
        }
        if(close(fd[0]) == -1 || close(fd[1]) == -1) perror("Close5");
        while( wait(NULL) != -1);
    }
    else{
        int error;
        int len;
        char** res = _strtok_by_space(tmpstr, &len);
        error = execvp(res[0], res);
        free(res);
        if( error == -1){
            printf("Error\n"); exit(0);
        }
    }
}

int main(int argv, char* argc[]){
	/*
    if(atexit(exit_handler))
        printf("Failed to register exit_handler\n");
    char* str;
    while(1){
        print_prompt();
        int len, i;
        str  = _getln();
        if(feof(stdin)){
            printf("Ctrl+D exit\n");
            exit(0);
        }
        fflush(stdin);
        get_cmd(str, 0, strlen(str)-1);
    }
	*/

	pid_t pid = fork();

	if(pid == -1){
		perror("fork failed");
		exit(EXIT_FAILURE);
	}
	else if(pid == 0){
		printf("Hello from child!");
		_exit(EXIT_SUCCESS);
	}
	else{
		int status;
		(void)waitpid(pid, &status, 0);
	}
	
    return 0;
}

void print_prompt(){
        char currentPath[256];
        getcwd(currentPath, 256);
        printf("%s> ",currentPath);
}

void exit_handler(void){
    printf("Bye :)\n");
}

void exit_cmd(){
    exit(1);
    return;
}

void cd_cmd(char** tmpres, int len){
    if( len == 1)
        chdir( getenv("HOME") );
    else if( len == 2){
        if( chdir( tmpres[1] ) )
            printf("No Directory\n");
    }
    else
        printf("error\n");
}

void get_cmd(char* str, int s, int e){
    char strmem[512]; strcpy(strmem, str);
    int len; int pid;
    char** tmpres =  _strtok_by_space(str, &len);
    if( !strcmp(tmpres[0], "logout") || !strcmp(tmpres[0], "exit")){
        free(tmpres);
        exit_cmd();
    }
    else if( !strcmp(tmpres[0], "cd") ){
        cd_cmd(tmpres, len);
        free(tmpres);
    }
    else{
        free(str);
        pid = fork();
        if( pid < 0) perror("fork() error");
        else if (!pid) make_a_tree(strmem, s, e);
        else waitpid(pid, &status, 0);
    }
}
