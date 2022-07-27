#include<iostream>
#include <string.h>
#include <stdio.h>
#include <time.h>
#include"sm3.h"

#define u_char unsigned char



using namespace std;


int main()
{
	int batch;
	cout << "请输入测试规模：";
	cin >> batch;

	clock_t begin, end;
	string msg = "hello world";
	u_char* c_msg = (u_char*)msg.c_str();
	unsigned char res[32];
	
	begin = clock();
	for (int i = 0; i < batch; i++) {
		sm3(c_msg, msg.size(), res);
	}
	end = clock();

	cout << "Hash值:";
	for (int i = 0; i < 32; i++)
	{
		printf("%02x", res[i]);
		if (((i + 1) % 4) == 0) printf(" ");
	}
	
	cout << "\n测试次数：" << batch << endl;
	cout << "效率用时：" << double(end - begin) / CLOCKS_PER_SEC << "s" << endl;

	return 0;
}
