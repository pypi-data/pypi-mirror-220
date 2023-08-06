import os, shutil, sys, glob

package_name = "imutum_python_tool"
abbreviation_name = "mtmtool"
description = " A Personal Python Tool Library."
version = "1.2.11"


def check_requires(requires: list):
    pip_file = "pip.exe" if "win" in sys.platform else "pip"
    pip_paths = [
        os.path.join(os.path.dirname(sys.executable), "Scripts", pip_file),
        os.path.join(os.path.dirname(sys.executable), pip_file),
    ]
    for _path in pip_paths:
        if os.path.exists(_path):
            pip_exe = _path
            break
    for require in requires:
        try:
            __import__(require)
        except:
            os.system(f"{pip_exe} install {require}")


# Setiptools Support
check_requires(["setuptools"])
import setuptools

# Path Support
os.chdir(os.path.dirname(__file__))
if os.path.isdir('build'):
    print('INFO del dir ', 'build')
    shutil.rmtree('build')

# README Doc
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Setup
setuptools.setup(
    name=abbreviation_name,  #应用名
    author="imutum",
    author_email="",
    version=version,  #版本号
    description=(f"{package_name}" if not len(description) else description),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/imutum/{package_name}",
    packages=setuptools.find_packages("src"),  #包括在安装包内的Python包
    package_dir={"": "src"},
    zip_safe=False,
    include_package_data=True,  #启用清单文件MANIFEST.in,包含数据文件
    install_requires=["requests", "pyyaml", "dill"],
    # ext_modules=ext_modules,
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
)
