/* function declarations defined by the standard library */
extern int open(char *filename, int flags);
extern int read(int fd, char *buffer, unsigned int count);
extern int close(int fd);
extern int printf(const char *format, ...);
extern void *malloc(int size);
extern void *realloc(void *ptr, int size);
extern void free(void *ptr);
extern void abort();

/* type declarations */
enum TOKEN_KIND {
    ID_OR_KEYWORD, 
    OPERATOR_OR_SEPARATOR, 
    INT_CONSTANT, 
    CHAR_CONSTANT, 
    STRING_LITERAL, 
    FLOATING_CONSTANT, 
    WHITE_SPACE, 
    COMMENT, 
    EOF 
};

struct token { 
    enum TOKEN_KIND kind;
    int begin;
    int end;
};

/* function declarations */
char *read_text_file(char *filename);
char *token_kind_to_str(enum TOKEN_KIND kind);
void print_token(char *prog, struct token t);
struct token new_token(enum TOKEN_KIND kind, int begin, int end);
struct token get_token(char prog[], int begin);
void error(char *message, char prog[], int index);

/* The "main" entry point */
void main(int argc, char *argv[]) {    
    int cur, i;
    char *prog;

    if (argc <= 1) {
        prog = read_text_file("clex.c");
    } else {
        prog = read_text_file(argv[1]);
    }
    cur = 0;
    while (1) {
        struct token t;
        t = get_token(prog, cur);
        print_token(prog, t);
        if (t.kind == EOF) {
            break;
        }
        cur = t.end + 1;
    }
    free(prog);
}

void error(char *message, char prog[], int index) {
    int cur = index, maxlen =50;

    printf("error: %s\n", message);
    printf("error begins from:\n");

    while (prog[cur] != '\0' && maxlen > 0) {
        printf("%c", prog[cur]);
        cur = cur + 1;
        maxlen = maxlen - 1;
    }
    printf("\n");
}

/* Open "filename" and load the content into the memory. The return
 value is the memory address. */
char *read_text_file(char *filename) {
    int fd, nread, buf_size, src_len=0;
    char *buf;

    fd = open(filename, 0);
    buf_size=4096;
    buf = malloc(buf_size);
    do {
        int avail = buf_size - (src_len + 1);
        if (avail <= 0) {
            /* increase buffer size */
            buf_size = buf_size * 2;
            buf = realloc(buf, buf_size);
            avail = buf_size - (src_len + 1);
        }
        nread = read(fd, buf + src_len, avail);
        src_len += nread;
    } while (nread > 0 );
    buf[src_len] = '\0';
    close(fd);
    return buf;
}

/* Return abbreviated string for a kind of the token. */
char *token_kind_to_str(enum TOKEN_KIND kind) {
    switch(kind) {
    case ID_OR_KEYWORD: return "IDKW";
    case OPERATOR_OR_SEPARATOR: return "OS";
    case INT_CONSTANT: return "IC";
    case CHAR_CONSTANT: return "CC";
    case STRING_LITERAL: return "SL";
    case FLOATING_CONSTANT: return "FC";
    case WHITE_SPACE: return "WS";
    case COMMENT: return "CM";
    case EOF: return "EOF";
    default:
        printf("unreachable\n");
        abort();
        break;
    }
}

/* Print the token. */
void print_token(char *prog, struct token t) {
    char c;
    int i;

    if (t.kind == EOF) {
        printf("%5s\n", token_kind_to_str(t.kind));
        return;
    }

    printf("%5s %5d     \"", 
           token_kind_to_str(t.kind), 
           t.end - t.begin + 1);
    for(i = t.begin; i <= t.end;i++) {
        c = prog[i];
        /* see http://www.asciitable.com/ */
        if ((c >= ' ') && (c <= '~')) {
            printf("%c", c);
        } else {
            switch(c) {
            case '\n':
                printf("\\n");
                break;
            case '\t':
                printf("\\t");
                break;
            case '"':
                printf("\\\"");
                break;
            case '\\':
                printf("\\\\");
                break;
            case '\r':
                printf("\\r");
                break;
            default:
                printf("not printable character: 0x%2x\n", c);
                abort();
                break;
            }
        }
    }
    printf("\"\n");
}

/* Create a token object */
struct token new_token(enum TOKEN_KIND kind, int begin, int end) {
    struct token t;
    t.kind = kind;
    t.begin = begin;
    t.end = end;
    return t;
}

/* Begin Your Implmentation Here */
struct token get_token(char prog[], int begin) {
    int cur = begin;

    error("not implemented", prog, cur);
    return new_token(EOF, begin, begin);
}
