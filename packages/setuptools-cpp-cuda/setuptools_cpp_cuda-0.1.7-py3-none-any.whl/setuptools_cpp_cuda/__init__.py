"""
The setuptools-cpp-cuda is a module that extends setuptools functionality for building hybrid C++ and CUDA extensions
for Python wrapper modules.
"""
from .build_ext import BuildExtension, fix_dll
from .extension import CppExtension, CUDAExtension, CUDA_HOME, CUDNN_HOME
from .find_cuda import find_cuda_home, find_cuda_home_path

__version__ = '0.1.7'
raise ModuleNotFoundError(
    '***Warning:***'
    ' This project has been renamed to "pypi/setuptools-cuda-cpp" (https://pypi.org/project/setuptools-cuda-cpp) for'
    ' visibility reasons in Pypi and migrated to GitHub for enhance community Issues feedback. Please uninstall this'
    ' module ("pip uninstall setuptools-cpp-cuda") and install the new package ("pip install setuptools-cuda-cpp").'
    ' Sorry for the inconveniences.'
)
# __all__ = [
#     'BuildExtension', 'CppExtension', 'CUDAExtension',
#     'find_cuda_home', 'find_cuda_home_path',
#     'fix_dll', 'nvml'
# ]
