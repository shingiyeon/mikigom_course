#define CHUNK 1

// _getln() : Read string input with memory-efficient dynamic allocation
// IN : 
// OUT : 
// RETURN : dynamic allocated string input
char* _getln(){
    char *line = NULL, *tmp = NULL;
    size_t size = 0, index = 0;
    int ch = EOF;

    while (ch) {
        ch = getc(stdin);

        /* Check if we need to stop. */
        if (ch == EOF || ch == '\n')
            ch = 0;

        /* Check if we need to expand. */
        if (size <= index) {
            size += CHUNK;
            tmp = realloc(line, size);
            if (!tmp) {
                free(line);
                line = NULL;
                break;
            }
            line = tmp;
        }

        /* Actually store the thing. */
        line[index++] = ch;
    }

    return line;
}

// You must free the result if result is non-NULL.
char* str_replace(char *orig, char *rep, char *with) {
    char *result; // the return string
    char *ins;    // the next insert point
    char *tmp;    // varies
    int len_rep;  // length of rep (the string to remove)
    int len_with; // length of with (the string to replace rep with)
    int len_front; // distance between rep and end of last rep
    int count;    // number of replacements

    // sanity checks and initialization
    if (!orig || !rep)
        return NULL;
    len_rep = strlen(rep);
    if (len_rep == 0)
        return NULL; // empty rep causes infinite loop during count
    if (!with)
        with = "";
    len_with = strlen(with);

    // count the number of replacements needed
    ins = orig;
    for (count = 0; tmp = strstr(ins, rep); ++count) {
        ins = tmp + len_rep;
    }

    tmp = result = malloc(strlen(orig) + (len_with - len_rep) * count + 1);

    if (!result)
        return NULL;

    // first time through the loop, all the variable are set correctly
    // from here on,
    //    tmp points to the end of the result string
    //    ins points to the next occurrence of rep in orig
    //    orig points to the remainder of orig after "end of rep"
    while (count--) {
        ins = strstr(orig, rep);
        len_front = ins - orig;
        tmp = strncpy(tmp, orig, len_front) + len_front;
        tmp = strcpy(tmp, with) + len_with;
        orig += len_front + len_rep; // move to next "end of rep"
    }
    strcpy(tmp, orig);
    return result;
}

// _strtok_by_space : Return arr of string splited by space with dynamic allocation
// IN : str(char*)
// OUT : len(int*) - length of arr of string
// RETURN : dynamic allocated arr of string
char** _strtok_by_space(char* str, int* len){
    char*  p    = strtok(str, " ");
    int n_spaces = 0;
    char** res = NULL;

    /* split string and append tokens to 'res' */
    while (p) {
        res = realloc(res, sizeof (char*) * ++n_spaces);

        if (res == NULL)
            exit(-1); /* memory allocation failed */

        res[n_spaces-1] = p;

        p = strtok(NULL, " ");
    }

    /* realloc one extra element for the last NULL */
    res = realloc(res, sizeof (char*) * (n_spaces+1));
    res[n_spaces] = 0;

    *len = n_spaces;
    return res;
}
