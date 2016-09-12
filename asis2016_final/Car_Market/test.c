#include <stdio.h>
#include <stdlib.h>

int main(){
	void *heap1 = malloc(0x8);
	void *heap2 = malloc(0x20);
	memset(heap1,'A',12);
	memset(heap2,'B',0x20);
	free(heap2);
	heap1 = realloc(heap1,0x28);
	void *heap3 = malloc(0x20);
	printf("%s",heap1);
}
