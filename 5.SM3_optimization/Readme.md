# ✅ Optimize SM3 implementation

### 1. 代码说明

​	此处，主要在参考代码的基础上，在实现方面做了循环展开，以及单指令多数据SIMD方法来优化SM3的算法效率

### 2.运行方式

windows中，在Visual Studio中导入sm3.cpp以及sm3.h文件，运行sm3.cpp文件即可。

### 3.实现效果

#### 测试

测试msg为：**"hello world"**

用户自定义输入规模，在这里展示了500000和5000000数据量规模的效率。

基本上**1.3s**可以进行**50w**组数据的运算。效率还是比较可观的。

#### 50w规模

![](https://github.com/lunan0320/Crypto_projects/blob/main/5.SM3_optimization/50w.png)

#### 500w规模

![](https://github.com/lunan0320/Crypto_projects/blob/main/5.SM3_optimization/500w.png)



#### 优化部分

```c++
	uint32_t SS1, SS2, TT1, TT2, T[64];
	for (j = 0; j < 16; j += 4) {
		X = _mm_loadu_si128((__m128i*)(block + j * 4)); 
		X = _mm_shuffle_epi8(X, V);
		_mm_storeu_si128((__m128i*)(W + j), X);
	}
```

```c++
//X = (W[j - 3], W[j - 2], W[j - 1], 0) 
	for (j = 16; j < 68; j += 4) {
		X = _mm_loadu_si128((__m128i*)(W + j - 3));   
		X = _mm_andnot_si128(M, X);

		X = _mm_rotl_epi32(X, 15);
		Y = _mm_loadu_si128((__m128i*)(W + j - 9));
		X = _mm_xor_si128(X, Y);
		Y = _mm_loadu_si128((__m128i*)(W + j - 16));
		X = _mm_xor_si128(X, Y);

		//计算P1(x) (x^ROL32(x,15)^ROL32(x,23))
		Y = _mm_rotl_epi32(X, (23 - 15));  
		Y = _mm_xor_si128(Y, X);
		Y = _mm_rotl_epi32(Y, 15);
		X = _mm_xor_si128(X, Y);

		Y = _mm_loadu_si128((__m128i*)(W + j - 13));
		Y = _mm_rotl_epi32(Y, 7);
		X = _mm_xor_si128(X, Y);
		Y = _mm_loadu_si128((__m128i*)(W + j - 6));
		X = _mm_xor_si128(X, Y);

		// W[j + 3] ^= P1(rol32(W[j + 1], 15)) 
		R = _mm_shuffle_epi32(X, 0); 
		R = _mm_and_si128(R, M);
		Y = _mm_rotl_epi32(R, 15);
		Y = _mm_xor_si128(Y, R);
		Y = _mm_rotl_epi32(Y, 9);
		R = _mm_xor_si128(R, Y);
		R = _mm_rotl_epi32(R, 6);
		X = _mm_xor_si128(X, R);

		_mm_storeu_si128((__m128i*)(W + j), X);
	}
```

### 4.参考代码

[GmSSL--> src--> sm3.c](https://github.com/guanzhi/GmSSL/blob/develop/src/sm3.c)

> 主要是对于代码中的SSE3的部分展开调用，使得在SIMD的基础上，达到更好的FULL UNROLL的效果。
