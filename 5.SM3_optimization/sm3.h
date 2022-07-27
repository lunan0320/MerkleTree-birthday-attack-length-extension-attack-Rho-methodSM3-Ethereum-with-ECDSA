#pragma once
#include<iostream>
#include <immintrin.h>
using namespace std;

#define SM3_DIGEST_SIZE		32
#define SM3_BLOCK_SIZE		64
#define SM3_STATE_WORDS		8


#define ROL32(x,j) ((x<<j)|(x>>(32-j)))

#define P0(x) (x^ROL32(x,9)^ROL32(x,17))
#define P1(x) (x^ROL32(x,15)^ROL32(x,23))

#define FF0(x,y,z) x^y^z
#define FF1(x,y,z)(x&y) | x&z | (y&z)

#define GG0(x,y,z) x^y^z
#define GG1(x,y,z)(x&y) | ((~x)&z)


# define _mm_rotl_epi32(X,i) \
	_mm_xor_si128(_mm_slli_epi32((X),(i)), _mm_srli_epi32((X),32-(i)))


#define UNROLL(A, B, C, D, E, F, G, H, xx)					\
	SS1 = ROL32((ROL32(A, 12) + E + ROL32(T[j],j)), 7);		\
	SS2 = SS1 ^ ROL32(A, 12);								\
	TT1 = FF##xx(A, B, C) + D + SS2 + (W[j] ^ W[j + 4]);	\
	TT2 = GG##xx(E, F, G) + H + SS1 + W[j];					\
	B = ROL32(B, 9);										\
	H = TT1;												\
	F = ROL32(F, 19);										\
	D = P0(TT2);											\
	j++

#define UNROLL8(A, B, C, D, E, F, G, H, xx)			\
	UNROLL(A, B, C, D, E, F, G, H, xx);				\
	UNROLL(H, A, B, C, D, E, F, G, xx);				\
	UNROLL(G, H, A, B, C, D, E, F, xx);				\
	UNROLL(F, G, H, A, B, C, D, E, xx);				\
	UNROLL(E, F, G, H, A, B, C, D, xx);				\
	UNROLL(D, E, F, G, H, A, B, C, xx);				\
	UNROLL(C, D, E, F, G, H, A, B, xx);				\
	UNROLL(B, C, D, E, F, G, H, A, xx)

//定义结构体
typedef struct sm3_ctx_t {
	uint32_t digest[SM3_STATE_WORDS];
	int nblocks;  
	uint8_t block[SM3_BLOCK_SIZE];
	int num;
}sm3_ctx;

//主要函数部分的声明
void sm3_init(sm3_ctx* ctx);
void sm3_update(sm3_ctx* ctx, const uint8_t* data, size_t data_len);
void sm3_final(sm3_ctx* ctx, uint8_t* digest);
void sm3(const uint8_t* message, size_t mlen, uint8_t res[SM3_BLOCK_SIZE]);
static void sm3_compress(uint32_t digest[SM3_BLOCK_SIZE / sizeof(uint32_t)], const uint8_t block[SM3_BLOCK_SIZE]);

//字节转换
uint64_t byte_swap64(uint64_t i)
{
	uint64_t j;
	j = (i << 56);
	j += (i << 40) & UINT64_C(0x00FF000000000000);
	j += (i << 24) & UINT64_C(0x0000FF0000000000);
	j += (i << 8) & UINT64_C(0x000000FF00000000);
	j += (i >> 8) & UINT64_C(0x00000000FF000000);
	j += (i >> 24) & UINT64_C(0x0000000000FF0000);
	j += (i >> 40) & UINT64_C(0x000000000000FF00);
	j += (i >> 56);
	return j;
}
uint32_t byte_swap32(uint32_t i)
{
	uint32_t j;
	j = (i << 24);
	j += (i << 8) & 0x00FF0000;
	j += (i >> 8) & 0x0000FF00;
	j += (i >> 24);
	return j;
}

//初始化函数
void sm3_init(sm3_ctx* ctx) {
	ctx->digest[0] = 0x7380166F;
	ctx->digest[1] = 0x4914B2B9;
	ctx->digest[2] = 0x172442D7;
	ctx->digest[3] = 0xDA8A0600;
	ctx->digest[4] = 0xA96F30BC;
	ctx->digest[5] = 0x163138AA;
	ctx->digest[6] = 0xE38DEE4D;
	ctx->digest[7] = 0xB0FB0E4E;

	ctx->nblocks = 0;
	ctx->num = 0;
}

void sm3_update(sm3_ctx* ctx, const uint8_t* data, size_t dlen) {
	if (ctx->num) {
		unsigned int left = SM3_BLOCK_SIZE - ctx->num;
		if (dlen < left) {
			memcpy(ctx->block + ctx->num, data, dlen);
			ctx->num += dlen;
			return;
		}
		else {
			memcpy(ctx->block + ctx->num, data, left);
			sm3_compress(ctx->digest, ctx->block);
			ctx->nblocks++;
			data += left;
			dlen -= left;
		}
	}
	while (dlen >= SM3_BLOCK_SIZE) {
		sm3_compress(ctx->digest, data);
		ctx->nblocks++;
		data += SM3_BLOCK_SIZE;
		dlen -= SM3_BLOCK_SIZE;
	}
	ctx->num = dlen;
	if (dlen) {
		memcpy(ctx->block, data, dlen);
	}
}

void sm3_final(sm3_ctx* ctx, uint8_t* digest) {
	size_t i;
	uint32_t* pdigest = (uint32_t*)(digest);
	uint64_t* count = (uint64_t*)(ctx->block + SM3_BLOCK_SIZE - 8);

	ctx->block[ctx->num] = 0x80;

	if (ctx->num + 9 <= SM3_BLOCK_SIZE) {
		memset(ctx->block + ctx->num + 1, 0, SM3_BLOCK_SIZE - ctx->num - 9);
	}
	else {
		memset(ctx->block + ctx->num + 1, 0, SM3_BLOCK_SIZE - ctx->num - 1);
		sm3_compress(ctx->digest, ctx->block);
		memset(ctx->block, 0, SM3_BLOCK_SIZE - 8);
	}

	count[0] = (uint64_t)(ctx->nblocks) * 512 + (ctx->num << 3);
	count[0] = byte_swap64(count[0]);

	sm3_compress(ctx->digest, ctx->block);
	for (i = 0; i < sizeof(ctx->digest) / sizeof(ctx->digest[0]); i++) {
		pdigest[i] = byte_swap32(ctx->digest[i]);
	}
}

//sm3的压缩部分
static void sm3_compress(uint32_t digest[SM3_BLOCK_SIZE / sizeof(uint32_t)], const uint8_t block[SM3_BLOCK_SIZE]) {
	int j;
	uint32_t W[68], W1[64];
	__m128i X, Y, R, Q, Z;
	__m128i M = _mm_setr_epi32(0, 0, 0, 0xffffffff);
	__m128i V = _mm_setr_epi8(3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12);


	uint32_t A = digest[0], B = digest[1], C = digest[2], D = digest[3];
	uint32_t E = digest[4], F = digest[5], G = digest[6], H = digest[7];

	//此处利用了SIMD的单指令多数据模式优化
	uint32_t SS1, SS2, TT1, TT2, T[64];
	for (j = 0; j < 16; j += 4) {
		X = _mm_loadu_si128((__m128i*)(block + j * 4)); 
		X = _mm_shuffle_epi8(X, V);
		_mm_storeu_si128((__m128i*)(W + j), X);
	}
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
	//for (j = 0; j < 64; j+=4) W1[j] = W[j] ^ W[j + 4];
	for (j = 0; j < 64; j += 4)
	{
		Q = _mm_loadu_si128((__m128i*)(W + j)); 
		Z = _mm_loadu_si128((__m128i*)(W + j + 4));
		Z = _mm_xor_si128(Q, Z);
		_mm_storeu_si128((__m128i*)(W1 + j), Z);

	}
	for (j = 0; j < 16; j++)
	{
		T[j] = 0x79CC4519;
		SS1 = ROL32((ROL32(A, 12) + E + ROL32(T[j], j)), 7);
		SS2 = SS1 ^ ROL32(A, 12);
		TT1 = FF0(A, B, C) + D + SS2 + W1[j];
		TT2 = GG0(E, F, G) + H + SS1 + W[j];
		D = C;
		C = ROL32(B, 9);
		B = A;
		A = TT1;
		H = G;
		G = ROL32(F, 19);
		F = E;
		E = P0(TT2);
	}
	for (j = 16; j < 64; j++)
	{
		T[j] = 0x7AB79D8A;
		SS1 = ROL32(ROL32(A, 12) + E + ROL32(T[j], j), 7);
		SS2 = SS1 ^ ROL32(A, 12);
		TT1 = FF1(A, B, C) + D + SS2 + W1[j];
		TT2 = GG1(E, F, G) + H + SS1 + W[j];
		D = C;
		C = ROL32(B, 9);
		B = A;
		A = TT1;
		H = G;
		G = ROL32(F, 19);
		F = E;
		E = P0(TT2);
	}

	j = 0;
	UNROLL8(A, B, C, D, E, F, G, H, 0);
	UNROLL8(A, B, C, D, E, F, G, H, 0);
	UNROLL8(A, B, C, D, E, F, G, H, 1);
	UNROLL8(A, B, C, D, E, F, G, H, 1);
	UNROLL8(A, B, C, D, E, F, G, H, 1);
	UNROLL8(A, B, C, D, E, F, G, H, 1);
	UNROLL8(A, B, C, D, E, F, G, H, 1);
	UNROLL8(A, B, C, D, E, F, G, H, 1);
	
	digest[0] ^= A;
	digest[1] ^= B;
	digest[2] ^= C;
	digest[3] ^= D;
	digest[4] ^= E;
	digest[5] ^= F;
	digest[6] ^= G;
	digest[7] ^= H;
}

void sm3(const uint8_t* message, size_t mlen, uint8_t res[SM3_BLOCK_SIZE])
{
	sm3_ctx ctx;
	sm3_init(&ctx);
	sm3_update(&ctx, message, mlen);
	sm3_final(&ctx, res);
}
