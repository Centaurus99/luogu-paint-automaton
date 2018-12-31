#include<math.h>
#include<iomanip> 
#include<stdlib.h>
#include<windows.h>
#include<stdio.h>
#include<iostream>
#define sqr(x) ((x)*(x))
using namespace std;
typedef struct BGR{
	unsigned char b;
	unsigned char g;
	unsigned char r;
}BGR;
typedef struct RGB{
	unsigned char r;
	unsigned char g;
	unsigned char b;
}RGB;
const int NC=32;
RGB col[NC]={
{0, 0, 0},
{255, 255, 255},
{170, 170, 170},
{85, 85, 85},
{254, 211, 199},
{255, 196, 206},
{250, 172, 142},
{255, 139, 131},
{244, 67, 54},
{233, 30, 99},
{226, 102, 158},
{156, 39, 176},
{103, 58, 183},
{63, 81, 181},
{0, 70, 112},
{5, 113, 151},
{33, 150, 243},
{0, 188, 212},
{59, 229, 219},
{151, 253, 220},
{22, 115, 0},
{55, 169, 60},
{137, 230, 66},
{215, 255, 7},
{255, 246, 209},
{248, 203, 140},
{255, 235, 59},
{255, 193, 7},
{255, 152, 0},
{255, 87, 34},
{184, 63, 39},
{121, 85, 72}
};
const int INF=0x3f3f3f3f;
int deltax=0,deltay=0;
void BMPtoPPM(char *pFrameRGB){
	FILE* pBMP=fopen(pFrameRGB, "rb");
	BITMAPINFOHEADER infoHeader;
	BITMAPFILEHEADER fileHeader;
	FILE *pFile=fopen("todo.list", "wb");
	if (pFile == NULL){
		printf("file is null.\n");
		return;
	}
	fread(&fileHeader, sizeof(BITMAPFILEHEADER), 1, pBMP);
	fread(&infoHeader, sizeof(BITMAPINFOHEADER), 1, pBMP);
	if (infoHeader.biBitCount != 24){
		printf("it is not a 24-bit rgb image.\n");
		return;
	}
	long width = infoHeader.biWidth;
	long height = infoHeader.biHeight;
	int i, j;
	BGR *bmpBitsBGR = (BGR *)malloc(width*height * sizeof(BGR));
	
	//获取每一个像素点的BGR值
	fseek(pBMP, fileHeader.bfOffBits, 0);
	for (i = 0; i <height; i++){
		fread(&bmpBitsBGR[i*width], 3 * width, 1, pBMP);
		for (j = width - 1; j >= 0; j--){
			int tip=0,mn=INF;
			BGR tnow=bmpBitsBGR[i*width + j];
			RGB now=(RGB){tnow.r,tnow.g,tnow.b};
			for (int x=0;x<NC;++x){
				int val=sqr(abs((int)now.r-col[x].r))+sqr(abs((int)now.g-col[x].g))+sqr(abs((int)now.b-col[x].b));
				if (val<mn) mn=val,tip=x;
			}
			fprintf(pFile,"%d %d %d\n",j+deltax,(int)(height-i-1)+deltay,tip);
//		cerr<<(int)bmpBitsBGR[i*width + j].r<<' ';
//		cerr<<(int)bmpBitsBGR[i*width + j].g<<' ';
//		cerr<<(int)bmpBitsBGR[i*width + j].b<<' ';
//		cerr<<endl;
		}
	   fseek(pBMP, (4 - (width*3 % 4)) % 4, SEEK_CUR); //4字节对齐
	}
	
	// Close file
	fclose(pBMP);
	fclose(pFile);
	free(bmpBitsBGR);
	bmpBitsBGR = NULL;
	return;
}

int main(){
	printf("Please enter the starting coordinates:");
	scanf("%d%d",&deltax,&deltay);
    char readPath[]="a.bmp";
    BMPtoPPM(readPath); 
	return 0;
}
