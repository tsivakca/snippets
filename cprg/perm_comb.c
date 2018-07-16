#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXLEN 40
void print_array(char *a, int len)
{
	int i;
	for (i=0; i < len; i++) 
		printf("%c",*(a+i));
	printf("\n");
}

void swap(char *a , int i, int j)
{
	char t = *(a+i);
	*(a+i) = *(a+j);
	*(a+j) = t;
}

void perm(char *a, int n, int r, int pos,int lvl)
{
	int i;
	if (lvl == r)
		print_array(a,r);
	else {
		for(i = pos;i < n;i++) {
			swap(a,i,lvl);
			perm(a,n,r,pos+1,lvl+1);
			swap(a,i,lvl);
		}	
	}
}

void cmb(char *a, int n, int r, int pos,int lvl)
{
	int i;
	if (lvl == r) { 
		print_array(a,r);
		return;
	} else {
		for(i = pos;i < n;i++) {
			swap(a,i,lvl);
			cmb(a,n,r,pos+1,lvl+1);
 // all combinations done for pos now move to next to make it unique
			pos++;
			swap(a,i,lvl);
		}	
	}
}

int main(int argc, char *argv[])
{
	int r;
	char str[MAXLEN+1];

	if (argc != 3) {
		printf("%s <string> <num>\n",argv[0]);
		return -1;
	}

	memset(str,0,MAXLEN+1);
	strncpy(str,argv[1],MAXLEN);
	
	r = atoi(argv[2]);
	printf("----Permutation----\n");
	perm(str,strlen(str),r,0,0);
	memset(str,0,MAXLEN+1);
	strncpy(str,argv[1],MAXLEN);
	printf("----Combination----\n");
	cmb(str,strlen(str),r,0,0);
	return 0;
}
