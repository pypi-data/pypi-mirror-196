# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imdm', 'imdm.data_models', 'imdm.data_models.testing']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0',
 'pillow>=9.4.0,<10.0.0',
 'pydicom>=2.3.1,<3.0.0',
 'pytest>=7.2.2,<8.0.0',
 'ruff>=0.0.254,<0.0.255',
 'simpleitk>=2.2.1,<3.0.0',
 'termcolor>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'imdm',
    'version': '0.1.0',
    'description': 'Data models for MRI and image applications',
    'long_description': '# `imdm` - Python data models for images (and other stuff!)\n\n## What\'s the point\n\nThis module contains a few helpful and flexible data models which can be easily extended for other applications. Here, I focused on making some (very) specific validators focusing on MRI data. These can be used to test DICOM files, SITK-readable images or numpy-loadable arrays.\n\n## Installation\n\nThe project should be readily instalable with `poetry` (recommended) by running `poetry install`. \n\n## Usage\n\nTwo fundamental classes are used here: `DataValidator`, which focuses on validating a specific type of data, and `DataModel` which focuses on validating a sample (composed by multiple types of data).\n\n### `DataValidators`\n\nDefining `DataValidators` is relatively easy:\n\n```python\nfrom mridm import DataValidator\n\ndata_validator = DataValidator(type=str,length=11,shape=None,range=None)\n```\n\nand running data validations is just as easy:\n\n```python\noutput = data_validator.validate("test_string")\n\nprint(output)\n\n>>> {"type":True,"length":True,"shape":None,"range":None}\n```\n\nThe `DataValidator` method automatically checks for `type`, `length`, `shape` and `range` (if specified). If necessary, users can also add their own methods. For example, if you would to check whether a given path exists:\n\n```python\nimport os\n\ndata_validator.add_test(key="path",test_fn=os.path.exists,data_stage="raw")\n\noutput = data_validator.validate("test_string")\n\nprint(output)\n\n>>> {"type":True,"length":True,"shape":None,"range":None,"path":False}\n```\n\nEasy! All arguments are relatively clear, but `data_stage` is somewhat more ellusive; for this reason I introduce here the concept of three data stages:\n\n* `raw` - the input exactly as it is. This is useful to test whether a file exists.\n* `preprocessed_data` - if a `preprocess_fn` is specified in the `DataValidator` constructor, tests can be applied to these functions. For instance, the `type` check is automatically ran on the `preprocessed_data` stage. \n* `value_data` - some files (SITK-readable files, for instance) require some non-obvious wrangling before one can actually use their values as `numpy` arrays, which is the assumed format for checking the `range`. This function (`value_fn`) is applied to the output of `preprocess_fn`. \n\nIf no `preprocess_fn` or `value_fn` are supplied, then `preprocessed_data` and `value_fn` will be identical to the input data.\n\n### `DataModel`\n\nA `DataModel` is simply a structure of `DataValidators`, i.e.\n\n```python\nfrom mridm import DataValidator,DataModel\n\ndata_model = DataModel(structures={\n    "a":DataValidator(type=str,length=11,shape=None,range=None),\n    "b":DataValidator(type=int,length=None,shape=None,range=[-10,10])\n    })\n```\n\nThis `data_model` can then be applied to any given data input that follows a structure similar to `data_model.structures`.\n\n### MRI- and image-specific data validators\n\nAn easy-to-use data validators have been implemented specifically for image data (`ImageFile`). I work with images, so these were especially useful for me. \n\nAdditionally, since I work with a lot of MRI data, specific methods for MRI data were also implemented (`DicomFile` and `SitkFile`). A more generic method for `numpy` files has also been (`NumpyFile`).\n\n### `pprint`\n\n`pprint` is a simple function that allows you to more easily inspect the output of `DataValidator` and `DataModel`. It comes with colours!\n\n## Testing\n\nTests for the data validators and models are available in `mridm/data_models/testing`. Test images were collected from:\n\n* https://www.rubomedical.com/dicom_files/ (.dcm)\n* https://github.com/neurolabusc/niivue-images (.nii.gz)',
    'author': 'josegcpa',
    'author_email': 'jose.almeida@research.fchampalimaud.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
