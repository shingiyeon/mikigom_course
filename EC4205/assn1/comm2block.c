#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <wait.h>
#include <sys/types.h>
#include <signal.h>
#include "command_in.c"
#include "comm.h"

Command* comm2block(int* bn){
	char* str;
	int token_num, i;
	str = _getln();

	char** tokens = _strtok_by_space(str, &token_num);
	/*
	for(i = 0; i < token_num; ++i){
		printf("%s\n", tokens[i]);
	}
	*/

	int pipe_count = 0;
	for(i = 0; i < token_num; ++i){
		if(strcmp(tokens[i], ">") == 0 ||
		   strcmp(tokens[i], "<") == 0 ||
		   strcmp(tokens[i], ">>") == 0 ||
		   strcmp(tokens[i], "|") == 0 ||
		   strcmp(tokens[i], "&&") == 0 ||
		   strcmp(tokens[i], "||") == 0 ||
		   strcmp(tokens[i], ";") == 0 ){
			pipe_count += 1;
		}
	}

	int args_count = 0;
	int args_number_by_block[pipe_count+1];
	pipe_count = 0;
	for(i = 0; i < token_num; ++i){
		if(strcmp(tokens[i], ">") == 0 ||
		   strcmp(tokens[i], "<") == 0 ||
		   strcmp(tokens[i], ">>") == 0 ||
		   strcmp(tokens[i], "|") == 0 ||
		   strcmp(tokens[i], "&&") == 0 ||
		   strcmp(tokens[i], "||") == 0 ||
		   strcmp(tokens[i], ";") == 0 ){
			args_number_by_block[pipe_count] = args_count;
			pipe_count += 1;
			args_count = 0;
		}
		else
			args_count += 1;
	}
	args_number_by_block[pipe_count] = args_count;

	int** args_length_by_block_and_order = malloc((pipe_count+1)*sizeof(int*));
	for(i = 0; i < pipe_count+1; ++i)
		args_length_by_block_and_order[i] = malloc(args_number_by_block[i]*sizeof(int));
	args_count = 0;
	pipe_count = 0;
	for(i = 0; i < token_num; ++i){
		if(strcmp(tokens[i], ">") == 0 ||
		   strcmp(tokens[i], "<") == 0 ||
		   strcmp(tokens[i], ">>") == 0 ||
		   strcmp(tokens[i], "|") == 0 ||
		   strcmp(tokens[i], "&&") == 0 ||
		   strcmp(tokens[i], "||") == 0 ||
		   strcmp(tokens[i], ";") == 0 ){
			pipe_count += 1;
			args_count = 0;
		}
		else{
			args_length_by_block_and_order[pipe_count][args_count] = strlen(tokens[i]);
			args_count += 1;
		}
	}

	char* command_ops[pipe_count + 1];
	command_ops[0] = "\0";
	int k = 0;
	char *** command_block_string = malloc((pipe_count + 1)*sizeof(char**));
	for(i = 0; i < pipe_count + 1; ++i){
		command_block_string[i] = malloc(args_number_by_block[i]*sizeof(char*));
		for(k = 0; k < args_number_by_block[i]; ++k)
			command_block_string[i][k] = malloc(args_length_by_block_and_order[i][k]*sizeof(char));
	}

	char** commands = malloc((args_number_by_block[0])*sizeof(char*));
	for(i = 0; i < args_number_by_block[0]; ++i){
		commands[i] = malloc(args_length_by_block_and_order[0][i]*sizeof(char));
	}

	pipe_count = 0;
	args_count = 0;

	for(i = 0; i < token_num; ++i){
		if(strcmp(tokens[i], ">") == 0 ||
		   strcmp(tokens[i], "<") == 0 ||
		   strcmp(tokens[i], ">>") == 0 ||
		   strcmp(tokens[i], "|") == 0 ||
		   strcmp(tokens[i], "&&") == 0 ||
		   strcmp(tokens[i], "||") == 0 ||
		   strcmp(tokens[i], ";") == 0 ){
			for(k = 0; k < args_number_by_block[pipe_count]; ++k)
				command_block_string[pipe_count][k] = commands[k];
			pipe_count += 1;
		    commands = malloc((args_number_by_block[pipe_count])*sizeof(char*));
		    for(k = 0; k < args_number_by_block[pipe_count]; ++k){
			   commands[k] = malloc(args_length_by_block_and_order[pipe_count][k]*sizeof(char));
			}
			args_count = 0;
			command_ops[pipe_count] = tokens[i];
		}
		else{
			commands[args_count] = tokens[i];
			args_count += 1;
		}
	}
	for(k = 0; k < args_number_by_block[pipe_count]; ++k)
		command_block_string[pipe_count][k] = commands[k];

	/*
	int j = 0;
	for(i = 0; i < pipe_count + 1; ++i){
		printf("block %d, Args number by block : %d\n", i, args_number_by_block[i]);
		printf("%s\n", command_ops[i]);
		for(j = 0; j < args_number_by_block[i]; ++j){
			printf("%d %d %s\n", i, j, command_block_string[i][j]);
		}
	}
	*/

	Command* com_block;
	com_block = malloc((pipe_count + 1)*sizeof(Command));

	for(i = 0; i < pipe_count + 1; ++i){
		com_block[i].commfile = command_block_string[i];
		com_block[i].optype = command_ops[i];
		com_block[i].commfile_len = args_number_by_block[i];
	}

	*bn = pipe_count + 1;

	return com_block;
}
