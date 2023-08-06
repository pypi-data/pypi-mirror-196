#include <cuda.h>
#include <cuda_runtime.h>
#include <torch/all.h>
#include <torch/python.h>

const int BLOCKWIDTH = 256;
const int BLOCKHEIGHT2 = 16;
const int BLOCKHEIGHT3 = 24;
const int BLOCKHEIGHT4 = 32;
const int BLOCKHEIGHT8 = 64;
const int BLOCKHEIGHT16 = 128;

#define VEC_MATRIX_MATMUL(BIT_NUM, FUN_NAM)                                    \
  void vecquant##BIT_NUM##matmul_cuda(torch::Tensor vec, torch::Tensor mat,    \
                                      torch::Tensor mul, torch::Tensor scales, \
                                      torch::Tensor zeros) {                   \
    int batch = vec.size(0);                                                   \
    int vec_height = vec.size(1);                                              \
    int height = mat.size(0);                                                  \
    int width = mat.size(1);                                                   \
    dim3 blocks((height + BLOCKHEIGHT##BIT_NUM - 1) / BLOCKHEIGHT##BIT_NUM,    \
                (width + BLOCKWIDTH - 1) / BLOCKWIDTH, batch);                 \
    dim3 threads(BLOCKWIDTH);                                                  \
    AT_DISPATCH_FLOATING_TYPES(                                                \
        vec.type(), FUN_NAM, ([&] {                                            \
          VecQuant##BIT_NUM##MatMulKernel<<<blocks, threads>>>(                \
              vec.data<scalar_t>(), mat.data<int>(), mul.data<scalar_t>(),     \
              scales.data<scalar_t>(), zeros.data<scalar_t>(), batch,          \
              vec_height, height, width);                                      \
        }));                                                                   \
  }

  #if !defined(__CUDA_ARCH__) || __CUDA_ARCH__ >= 600
  #else
  __device__ double atomicAdd(double* address, double val)
  {
      unsigned long long int* address_as_ull = (unsigned long long int*)address;
      unsigned long long int old = *address_as_ull, assumed;
      do {
          assumed = old;
          old = atomicCAS(address_as_ull, assumed,
                  __double_as_longlong(val + __longlong_as_double(assumed)));
      } while (assumed != old);
      return __longlong_as_double(old);
  }
  #endif

__device__ inline unsigned int as_unsigned(int i) {
  return *reinterpret_cast<unsigned int *>(&i);
}

template <typename T>
__global__ void
VecQuant2MatMulKernel(const T *__restrict__ vec, const int *__restrict__ mat,
                      T *__restrict__ mul, const T *__restrict__ scales,
                      const T *__restrict__ zeros, int batch, int vec_height,
                      int height, int width) {
  int b = blockIdx.z;
  int h = BLOCKHEIGHT2 * blockIdx.x;
  int w = BLOCKWIDTH * blockIdx.y + threadIdx.x;

  __shared__ T blockvec[BLOCKWIDTH];
  blockvec[threadIdx.x] =
      vec[b * vec_height + (h / BLOCKHEIGHT2) * BLOCKWIDTH + threadIdx.x];
  __syncthreads();

  const T scale = scales[w];
  const T zero = zeros[w];

  T res = 0;
  int i = width * h + w;
  int k = 0;

  unsigned int tmp;

  while (k < BLOCKWIDTH) {
    tmp = as_unsigned(mat[i]);
    res += (scale * T((tmp >> 0) & 0x3) - zero) * blockvec[k + 0];
    res += (scale * T((tmp >> 2) & 0x3) - zero) * blockvec[k + 1];
    res += (scale * T((tmp >> 4) & 0x3) - zero) * blockvec[k + 2];
    res += (scale * T((tmp >> 6) & 0x3) - zero) * blockvec[k + 3];
    res += (scale * T((tmp >> 8) & 0x3) - zero) * blockvec[k + 4];
    res += (scale * T((tmp >> 10) & 0x3) - zero) * blockvec[k + 5];
    res += (scale * T((tmp >> 12) & 0x3) - zero) * blockvec[k + 6];
    res += (scale * T((tmp >> 14) & 0x3) - zero) * blockvec[k + 7];
    res += (scale * T((tmp >> 16) & 0x3) - zero) * blockvec[k + 8];
    res += (scale * T((tmp >> 18) & 0x3) - zero) * blockvec[k + 9];
    res += (scale * T((tmp >> 20) & 0x3) - zero) * blockvec[k + 10];
    res += (scale * T((tmp >> 22) & 0x3) - zero) * blockvec[k + 11];
    res += (scale * T((tmp >> 24) & 0x3) - zero) * blockvec[k + 12];
    res += (scale * T((tmp >> 26) & 0x3) - zero) * blockvec[k + 13];
    res += (scale * T((tmp >> 28) & 0x3) - zero) * blockvec[k + 14];
    res += (scale * T((tmp >> 30) & 0x3) - zero) * blockvec[k + 15];
    i += width;
    k += 16;
  }
  atomicAdd(&mul[b * width + w], res);
}

template <typename T>
__global__ void
VecQuant3MatMulKernel(const T *__restrict__ vec, const int *__restrict__ mat,
                      T *__restrict__ mul, const T *__restrict__ scales,
                      const T *__restrict__ zeros, int batch, int vec_height,
                      int height, int width) {
  int b = blockIdx.z;
  int h = BLOCKHEIGHT3 * blockIdx.x;
  int w = BLOCKWIDTH * blockIdx.y + threadIdx.x;

  __shared__ T blockvec[BLOCKWIDTH];
  blockvec[threadIdx.x] =
      vec[b * vec_height + (h / BLOCKHEIGHT3) * BLOCKWIDTH + threadIdx.x];
  __syncthreads();

  T scale = scales[w];
  T zero = zeros[w];

  T res = 0;
  int i = width * h + w;
  int k = 0;

  unsigned int tmp1;
  unsigned int tmp2;
  unsigned int tmp;

  while (k < BLOCKWIDTH) {
    tmp1 = as_unsigned(mat[i]);
    res += (scale * T((tmp1 >> 0) & 0x7) - zero) * blockvec[k + 0];
    res += (scale * T((tmp1 >> 3) & 0x7) - zero) * blockvec[k + 1];
    res += (scale * T((tmp1 >> 6) & 0x7) - zero) * blockvec[k + 2];
    res += (scale * T((tmp1 >> 9) & 0x7) - zero) * blockvec[k + 3];
    res += (scale * T((tmp1 >> 12) & 0x7) - zero) * blockvec[k + 4];
    res += (scale * T((tmp1 >> 15) & 0x7) - zero) * blockvec[k + 5];
    res += (scale * T((tmp1 >> 18) & 0x7) - zero) * blockvec[k + 6];
    res += (scale * T((tmp1 >> 21) & 0x7) - zero) * blockvec[k + 7];
    res += (scale * T((tmp1 >> 24) & 0x7) - zero) * blockvec[k + 8];
    res += (scale * T((tmp1 >> 27) & 0x7) - zero) * blockvec[k + 9];
    i += width;
    tmp2 = as_unsigned(mat[i]);
    tmp = (tmp1 >> 30) | ((tmp2 << 2) & 0x4);
    tmp2 >>= 1;
    res += (scale * T(tmp) - zero) * blockvec[k + 10];
    k += 11;
    res += (scale * T((tmp2 >> 0) & 0x7) - zero) * blockvec[k + 0];
    res += (scale * T((tmp2 >> 3) & 0x7) - zero) * blockvec[k + 1];
    res += (scale * T((tmp2 >> 6) & 0x7) - zero) * blockvec[k + 2];
    res += (scale * T((tmp2 >> 9) & 0x7) - zero) * blockvec[k + 3];
    res += (scale * T((tmp2 >> 12) & 0x7) - zero) * blockvec[k + 4];
    res += (scale * T((tmp2 >> 15) & 0x7) - zero) * blockvec[k + 5];
    res += (scale * T((tmp2 >> 18) & 0x7) - zero) * blockvec[k + 6];
    res += (scale * T((tmp2 >> 21) & 0x7) - zero) * blockvec[k + 7];
    res += (scale * T((tmp2 >> 24) & 0x7) - zero) * blockvec[k + 8];
    res += (scale * T((tmp2 >> 27) & 0x7) - zero) * blockvec[k + 9];
    i += width;
    tmp1 = as_unsigned(mat[i]);
    tmp = (tmp2 >> 30) | ((tmp1 << 1) & 0x6);
    tmp1 >>= 2;
    res += (scale * T(tmp) - zero) * blockvec[k + 10];
    k += 11;
    res += (scale * T((tmp1 >> 0) & 0x7) - zero) * blockvec[k + 0];
    res += (scale * T((tmp1 >> 3) & 0x7) - zero) * blockvec[k + 1];
    res += (scale * T((tmp1 >> 6) & 0x7) - zero) * blockvec[k + 2];
    res += (scale * T((tmp1 >> 9) & 0x7) - zero) * blockvec[k + 3];
    res += (scale * T((tmp1 >> 12) & 0x7) - zero) * blockvec[k + 4];
    res += (scale * T((tmp1 >> 15) & 0x7) - zero) * blockvec[k + 5];
    res += (scale * T((tmp1 >> 18) & 0x7) - zero) * blockvec[k + 6];
    res += (scale * T((tmp1 >> 21) & 0x7) - zero) * blockvec[k + 7];
    res += (scale * T((tmp1 >> 24) & 0x7) - zero) * blockvec[k + 8];
    res += (scale * T((tmp1 >> 27) & 0x7) - zero) * blockvec[k + 9];
    i += width;
    k += 10;
  }

  atomicAdd(&mul[b * width + w], res);
}

template <typename T>
__global__ void
VecQuant4MatMulKernel(const T *__restrict__ vec, const int *__restrict__ mat,
                      T *__restrict__ mul, const T *__restrict__ scales,
                      const T *__restrict__ zeros, int batch, int vec_height,
                      int height, int width) {
  int b = blockIdx.z;
  int h = BLOCKHEIGHT4 * blockIdx.x;
  int w = BLOCKWIDTH * blockIdx.y + threadIdx.x;

  __shared__ T blockvec[BLOCKWIDTH];
  blockvec[threadIdx.x] =
      vec[b * vec_height + (h / BLOCKHEIGHT4) * BLOCKWIDTH + threadIdx.x];
  __syncthreads();

  T scale = scales[w];
  T zero = zeros[w];

  T res = 0;
  int i = width * h + w;
  int k = 0;

  unsigned int tmp;

  while (k < BLOCKWIDTH) {
    tmp = as_unsigned(mat[i]);
    res += (scale * T((tmp >> 0) & 0xF) - zero) * blockvec[k + 0];
    res += (scale * T((tmp >> 4) & 0xF) - zero) * blockvec[k + 1];
    res += (scale * T((tmp >> 8) & 0xF) - zero) * blockvec[k + 2];
    res += (scale * T((tmp >> 12) & 0xF) - zero) * blockvec[k + 3];
    res += (scale * T((tmp >> 16) & 0xF) - zero) * blockvec[k + 4];
    res += (scale * T((tmp >> 20) & 0xF) - zero) * blockvec[k + 5];
    res += (scale * T((tmp >> 24) & 0xF) - zero) * blockvec[k + 6];
    res += (scale * T((tmp >> 28) & 0xF) - zero) * blockvec[k + 7];
    i += width;
    k += 8;
  }

  atomicAdd(&mul[b * width + w], res);
}

template <typename T>
__global__ void
VecQuant8MatMulKernel(const T *__restrict__ vec, const int *__restrict__ mat,
                      T *__restrict__ mul, const T *__restrict__ scales,
                      const T *__restrict__ zeros, int batch, int vec_height,
                      int height, int width) {
  int b = blockIdx.z;
  int h = BLOCKHEIGHT8 * blockIdx.x;
  int w = BLOCKWIDTH * blockIdx.y + threadIdx.x;

  __shared__ T blockvec[BLOCKWIDTH];
  blockvec[threadIdx.x] =
      vec[b * vec_height + (h / BLOCKHEIGHT8) * BLOCKWIDTH + threadIdx.x];
  __syncthreads();

  T scale = scales[w];
  T zero = zeros[w];

  T res = 0;
  int i = width * h + w;
  int k = 0;

  unsigned int tmp;

  while (k < BLOCKWIDTH) {
    tmp = as_unsigned(mat[i]);
    res += (scale * T((tmp >> 0) & 0xFF) - zero) * blockvec[k + 0];
    res += (scale * T((tmp >> 8) & 0xFF) - zero) * blockvec[k + 1];
    res += (scale * T((tmp >> 16) & 0xFF) - zero) * blockvec[k + 2];
    res += (scale * T((tmp >> 24) & 0xFF) - zero) * blockvec[k + 3];
    i += width;
    k += 4;
  }

  atomicAdd(&mul[b * width + w], res);
}

template <typename T>
__global__ void
VecQuant16MatMulKernel(const T *__restrict__ vec, const int *__restrict__ mat,
                       T *__restrict__ mul, const T *__restrict__ scales,
                       const T *__restrict__ zeros, int batch, int vec_height,
                       int height, int width) {
  int b = blockIdx.z;
  int h = BLOCKHEIGHT16 * blockIdx.x;
  int w = BLOCKWIDTH * blockIdx.y + threadIdx.x;

  __shared__ T blockvec[BLOCKWIDTH];
  blockvec[threadIdx.x] =
      vec[b * vec_height + (h / BLOCKHEIGHT16) * BLOCKWIDTH + threadIdx.x];
  __syncthreads();

  T scale = scales[w];
  T zero = zeros[w];

  T res = 0;
  int i = width * h + w;
  int k = 0;

  unsigned int tmp;

  while (k < BLOCKWIDTH) {
    tmp = as_unsigned(mat[i]);
    res += (scale * T((tmp >> 0) & 0xFF) - zero) * blockvec[k + 0];
    res += (scale * T((tmp >> 16) & 0xFF) - zero) * blockvec[k + 1];
    i += width;
    k += 2;
  }

  atomicAdd(&mul[b * width + w], res);
}

VEC_MATRIX_MATMUL(2, "vecquant2matmul_cuda");
VEC_MATRIX_MATMUL(3, "vecquant3matmul_cuda");
VEC_MATRIX_MATMUL(4, "vecquant4matmul_cuda");
VEC_MATRIX_MATMUL(8, "vecquant8matmul_cuda");
VEC_MATRIX_MATMUL(16, "vecquant16matmul_cuda");
