#include <c10/cuda/CUDAGuard.h>
#include <torch/all.h>
#include <torch/python.h>

using TT = torch::Tensor;
using namespace at::cuda;

void vecquant2matmul_cuda(TT vec, TT mat, TT mul, TT scales, TT zeros);

void vecquant2matmul(TT vec, TT mat, TT mul, TT scales, TT zeros) {
  const OptionalCUDAGuard _g(device_of(vec));
  vecquant2matmul_cuda(vec, mat, mul, scales, zeros);
}

void vecquant3matmul_cuda(TT vec, TT mat, TT mul, TT scales, TT zeros);

void vecquant3matmul(TT vec, TT mat, TT mul, TT scales, TT zeros) {
  const OptionalCUDAGuard _g(device_of(vec));
  vecquant3matmul_cuda(vec, mat, mul, scales, zeros);
}

void vecquant4matmul_cuda(TT vec, TT mat, TT mul, TT scales, TT zeros);

void vecquant4matmul(TT vec, TT mat, TT mul, TT scales, TT zeros) {
  const OptionalCUDAGuard _g(device_of(vec));
  vecquant4matmul_cuda(vec, mat, mul, scales, zeros);
}

void vecquant8matmul_cuda(TT vec, TT mat, TT mul, TT scales, TT zeros);

void vecquant8matmul(TT vec, TT mat, TT mul, TT scales, TT zeros) {
  const OptionalCUDAGuard _g(device_of(vec));
  vecquant8matmul_cuda(vec, mat, mul, scales, zeros);
}

void vecquant16matmul_cuda(TT vec, TT mat, TT mul, TT scales, TT zeros);

void vecquant16matmul(TT vec, TT mat, TT mul, TT scales, TT zeros) {
  const OptionalCUDAGuard _g(device_of(vec));
  vecquant16matmul_cuda(vec, mat, mul, scales, zeros);
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("matvmul2", &vecquant2matmul,
        "2-bit Quantized Matrix Vector Multiplication (CUDA)");
  m.def("matvmul3", &vecquant3matmul,
        "3-bit Quantized Matrix Vector Multiplication (CUDA)");
  m.def("matvmul4", &vecquant4matmul,
        "4-bit Quantized Matrix Vector Multiplication (CUDA)");
  m.def("matvmul8", &vecquant8matmul,
        "8-bit Quantized Matrix Vector Multiplication (CUDA)");
  m.def("matvmul16", &vecquant8matmul,
        "16-bit Quantized Matrix Vector Multiplication (CUDA)");
}
