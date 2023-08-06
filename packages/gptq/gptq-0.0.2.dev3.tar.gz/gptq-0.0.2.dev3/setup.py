from setuptools import setup
from torch.utils import cpp_extension
import os, sys
try:
    import torch
except:
    print("💀: gptq requires pytorch and GPU. Please install pytorch with the instruction in the README.md file.")
    sys.exit(0)

here = os.path.dirname(os.path.abspath(__file__))


def _get_version():
    with open(os.path.join(here, "gptq", "version.py")) as f:
        try:
            version_line = next(line for line in f if line.startswith("__version__"))
        except StopIteration:
            raise ValueError("__version__ not defined in itree/version.py")
        else:
            ns = {}
            exec(version_line, ns)  # pylint: disable=exec-used
            return ns["__version__"]

def _parse_requirements(path):
    with open(os.path.join(here, path)) as f:
        return [
            line.rstrip() for line in f if not (line.isspace() or line.startswith("#"))
        ]

VERSION = _get_version()
DESCRIPTION = "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers"

def package_files(ds):
    paths = []
    for d in ds:
        for (path, directories, filenames) in os.walk(d):
            for filename in filenames:
                if '__pycache__' not in str(filename):
                    paths.append(str(os.path.join(path, filename)))
    return paths


extra_files = package_files(['gptq/'])


setup(
    name='gptq',
    version=VERSION,
    author="Juncong Moo",
    author_email="<juncongmoo@gmail.com>",
    description=DESCRIPTION,
    long_description=open(os.path.join(here, "README.md")).read(),
    long_description_content_type="text/markdown",
    packages=['gptq','gptq.models'],
    include_package_data=True,
    install_requires=_parse_requirements("requirements.txt"),
    ext_modules=[cpp_extension.CUDAExtension(
        name='quant_cuda',
        sources=['gptq/quant_cuda.cpp', 'gptq/quant_cuda_kernel.cu'],
    )] if torch.cuda.is_available() else [],
    package_data={"gptq": extra_files, "": ['requirements.txt', 'README.md']},
    zip_safe=False,
    cmdclass={'build_ext': cpp_extension.BuildExtension} if torch.cuda.is_available() else {},
    keywords=["gptq"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries",
    ],
    license="Apache 2.0",
)
