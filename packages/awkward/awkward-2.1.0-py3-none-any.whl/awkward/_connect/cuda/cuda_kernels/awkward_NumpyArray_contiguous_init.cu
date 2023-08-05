// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

template <typename T>
__global__ void
awkward_NumpyArray_contiguous_init(T* toptr,
                                   int64_t skip,
                                   int64_t stride,
                                   uint64_t invocation_index,
                                   uint64_t* err_code) {
  if (err_code[0] == NO_ERROR) {
    int64_t thread_id = blockIdx.x * blockDim.x + threadIdx.x;
    if (thread_id < skip) {
      toptr[thread_id] = (thread_id * stride);
    }
  }
}
