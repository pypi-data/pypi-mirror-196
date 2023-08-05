# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.visualization']

package_data = \
{'': ['*'], 'src.visualization': ['assets/*']}

install_requires = \
['dash-bio>=1.0.2,<2.0.0',
 'dash-bootstrap-components>=1.3.0,<2.0.0',
 'dash>=2.6.1,<3.0.0',
 'h5py>=3.7.0,<4.0.0',
 'kaleido==0.2.1',
 'llvmlite>=0.39.1,<0.40.0',
 'matplotlib>=3.5.3,<4.0.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.4.4,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'pyfaidx>=0.7.1,<0.8.0',
 'pyyaml>=6.0,<7.0',
 'seaborn>=0.12.0,<0.13.0',
 'umap-learn>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['rostspace = src.app:main']}

setup_kwargs = {
    'name': 'rostspace',
    'version': '0.1.1',
    'description': 'Protein Embedding Visualization Tool.',
    'long_description': '# RostSpace\n\nRostSpace visualizes embeddings in 3D and 2D space and colors them by groups, provided throug a CSV file. Dimensionality reduction can be performed with UMAP, PCA or t-SNE. Additional features for biologists are implemented, to display molecule structures by providing PDB files.\n\n## Installation\nRostSpace can be installed with `pip`:\n```shell\n# install it with pip\npip install rostspace\n```\n\n## Getting started\nAfter installation, RostSpace can be run using the `rostspace` command.\n\nThe required arguments are:\n\n    -o      Path to the output directory where generated files are stored\n    --hdf   Path to HDF5-file containing the per protein embeddings as key-value pair\n    --csv   Path to the .csv-file containing the metadata\n\nOptional arguments are:\n\n    --pdb   Path to the directory that holds the .pdb files\n    --fasta Path to the .fasta-file\n    -v      Verbose -- prints internal process to the terminal\n\n### Download example data\nExample data can be downloaded from [here](https://nextcloud.in.tum.de/index.php/s/BPWWA9tiXTawjjW).\n\n### Run RostSpace\nRostSpace can be run by providing arguments on the command line, by giving it a YAML file, or a combination of both.\n\n1. Giving arguments on the command line:\n    ```shell\n    rostspace -o data/KLK --hdf data/KLK/KLK_esm2.h5 --csv data/KLK/KLK.csv\n    ```\n\n2. Creating a YAML file:\n\n    Pla2g2.yaml\n    ```yaml\n    o: data/Pla2g2\n    hdf: data/Pla2g2/emb_esm2.h5\n    csv: data/Pla2g2/Pla2g2.csv\n    ```\n\n    ```bash\n    rostspace -conf conf/Pla2g2.yaml\n    ```\n\n3. Using a YAML file and giving extra arguments:\n    ```bash\n    rostspace -conf conf/Pla2g2.yaml --pdb data/Pla2g2/colabfold/pdb\n    ```\n\n\nFor more information to the arguments run\n```shell\nrostspace --help\n```\n',
    'author': 'Anton Spannagl',
    'author_email': 'None',
    'maintainer': 'Rostlab',
    'maintainer_email': 'admin@rostlab.org',
    'url': 'https://github.com/Rostlab/RostSpace',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
