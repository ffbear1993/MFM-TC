## MFM-TC: Morphometric Feature Matrix & Tensor Completion

### Introduction

This repository is built for processing Morphometric Feature Matrix with outliers using Tensor Completion method.

### Installation

Creating a PYTHON virtual environment, PYTHON 3.6 has been tested to run all the code.

```
conda create -n ENV_NAME python=3.6
```

**NOTE**: The LRTC and STDC method (please check /package/TensorCode) are implemented and tested in MATLAB2018b. To make them available for PYTHON environment, I have generated python packages for them (please check /package/LRTC and /package/STDC). If you want to package them for yourself, you can check the link for more help (https://www.mathworks.com/help/compiler_sdk/gs/create-a-python-application-with-matlab-code.html)

Next, we need to install MATLAB engine for PYTHON to make the MATLAB code can be executed in python environment. The following instructions are suitable for MATLAB2018b, if your MATLAB version is higher, please check the MATLAB document for more help (https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)

```
conda activate ENV_NAME
cd /usr/local/MATLAB/R2018b/extern/engines/python
python setup.py install
```

If there is an error saying "MATLAB Engine for Python supports Python version 2.7, 3.5 but your version of Python...", you can modify the setup.py and add '3.6' in the `_supported_versions`

```
_supported_versions = ['2.7', '3.5', '3.6']
```

Then, We need to install the packaged LRTC and STDC method in PYTHON VIRTUAL ENV:

```
cd /package/LRTC/for_redistribution_files_only
python setup.py install

cd /package/STDC/for_redistribution_files_only
python setup.py install
```

Python packages yaml, loguru, numpy and scipy are necessary packages for executing the whole code:

```
pip install PyYaml loguru numpy scipy
```
Finally, you can run and test the whole repository:

```
python -m mfmtc.main
```

### Project Structure

#### Configuration

The project configuration is stored in `config.yml` file. We used yaml to manage all the variables.

If you want to change the location of data, you need to modify the `morpho` variable. The whole configuration is hierarchical, you can check the `/mfmtc/__init__.py and /mfmtc/main.py` file to see how to use the `config.yml` to configure the whole project.

#### Data and Dataset

'/mfmtc/data.py and /mfmtc/dataset.py' are two files to manage the data load and save. You can check the `/mfmtc/main.py line 13` to check how to use `MorphoDataset` class.

#### Outlier Check Phase

We use `Outlier` class (/mfmtc/outlier.py) to check the outliers in morphometric feature matrix. You need to call `checker` class function to process the data `X`:

```
Outlier.checker(X)
X: shape is [number_samples, number_regions, number_metrics]
tc_mask: 0 missing, 1 valued
```

It will return an `Outlier` instance with `tc_mask` property. The `tc_mask` is the outlier mask to identify which value is outlier in the input matrix. For the example, you can check `/mfmtc/main.py line 16-17` to see how to use it and save outlier mask.

#### Tensor Completion Phase

We provide two options for tensor completion: LRTC, STDC. You can check `/mfmtc/main.py, line 21 or line 26` to see how to use them and save the tensor completed result.

**NOTE**: In LRTC, `0` in `tc_mask` means true value, `1` in `tc_mask` means outlier, while in STDC, the situation is quite opposite, We have commented in `/mfmtc/outlier.py line 71 and line 117`, there is no need to change the original `tc_mask` for specific method.

#### Processed Results

`morphoTensor....aparc.mat` is the original morphometric feature matrix.

`origin_outlier_mask.mat` is the outlier mask after `Outlier.checker`.

`lrtc/stdc_tensor.mat` is the processed matrix after tensor completion.

### Contact

Free free to contact me with any questions, requests. It's always nice to know that we've helped someone or made their work easier. Contributing to the project is also acceptable and warmly welcomed.