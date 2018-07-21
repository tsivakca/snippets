#include <values.h>
#include <stdio.h>
int a[] = { -2,-1,2,-1,3,-2,1,1,-4,0,1,-1,0 }; //Sample array
#define MAX(a,b) (((a) > (b))?(a):(b))
int do_max_sub_seq(int * a, int len, int *sidx, int *eidx)
{
	int i,tmp;
	int	mss = MININT>>1; //to avoid -ve overflow
	int	csum = mss;
	for (i = 0; i < len; i++) {
		if (*(a+i) > csum + *(a+i)) {
			*sidx = i;
			csum = *(a+i);
		} else {
			csum += *(a+i);
		}
		mss = MAX(csum,mss);
		if (mss == csum)
			*eidx = i;
	}
	return mss;
}

int main() 
{
	int mss,sidx,eidx;
	mss = do_max_sub_seq(a,sizeof(a)/sizeof(int),&sidx,&eidx);
	printf("MSS:%d,sidx:%d,eidx:%d\n",mss,sidx,eidx);
	return 0;
}
