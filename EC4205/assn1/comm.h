typedef struct CommandX{
	char* optype;
	char** commfile; // COMMand or FILE
	int commfile_len;

	int my_pid, sibling_pid;
} Command;
