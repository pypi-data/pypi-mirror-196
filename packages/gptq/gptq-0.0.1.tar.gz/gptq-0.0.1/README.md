# GPTQ - Accurate Post-training Compression for Generative Pretrained Transformers

> This repo is a refactoring and polished version of the original repo for the paper [GPTQ: Accurate Post-training Compression for Generative Pretrained Transformers](https://arxiv.org/abs/2210.17323).


The current release includes the following features:

* An efficient implementation of the GPTQ algorithm
* A 3-bit quantized matrix full-precision vector product CUDA kernel


![](https://images.deepai.org/converted-papers/2210.17323/x3.png)


## Installation

```bash
pip install gptq
```

### 📝 Install PyTorch

`gptq` requires PyTorch and GPU, and installing PyTorch with CUDA is tricky. To install PyTorch correctly, the following steps are recommended:

- run `nvcc --version` to get the version. For example, the following result means we have cuda compiler version 116

```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Tue_Mar__8_18:18:20_PST_2022
Cuda compilation tools, release 11.6, V11.6.124
Build cuda_11.6.r11.6/compiler.31057947_0
```
- run `pip install light-the-torch` to install ltt
- run `ltt install --pytorch-computation-backend=cu116 torch torchvision torchaudio` to install the torch suite. Please replace the `116` according to your environment!

## Cite

If you found this work useful, please consider citing:

```
@article{frantar-gptq,
  title={{GPTQ}: Accurate Post-training Compression for Generative Pretrained Transformers}, 
  author={Elias Frantar and Saleh Ashkboos and Torsten Hoefler and Dan Alistarh},
  year={2022},
  journal={arXiv preprint arXiv:2210.17323}
}
```

All credits go to [IST Austria Distributed Algorithms and Systems Lab](https://ist.ac.at/en/research/alistarh-group)

