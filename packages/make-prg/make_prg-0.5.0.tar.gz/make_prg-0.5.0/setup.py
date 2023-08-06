# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['make_prg',
 'make_prg.from_msa',
 'make_prg.subcommands',
 'make_prg.update',
 'make_prg.utils']

package_data = \
{'': ['*'],
 'make_prg.utils': ['mafft-linux64/*',
                    'mafft-linux64/mafftdir/bin/*',
                    'mafft-linux64/mafftdir/libexec/*']}

install_requires = \
['biopython==1.79',
 'intervaltree>=3.1.0,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'numpy>=1.24.4,<2.0.0',
 'scikit-learn>=1.3.0,<2.0.0',
 'setuptools>=65,<66']

extras_require = \
{'debug-graphs': ['pygraphviz==1.7',
                  'networkx>=2.6.3,<3.0.0',
                  'matplotlib>=3.5.0,<4.0.0'],
 'precompiled-binary': ['pygraphviz==1.7',
                        'networkx>=2.6.3,<3.0.0',
                        'matplotlib>=3.5.0,<4.0.0',
                        'pyinstaller>=5.6,<6.0']}

entry_points = \
{'console_scripts': ['make_prg = make_prg.__main__:main']}

setup_kwargs = {
    'name': 'make-prg',
    'version': '0.5.0',
    'description': 'Code to create a PRG from a Multiple Sequence Alignment file',
    'long_description': '# make_prg\n\nA tool to create and update PRGs for input to [Pandora][pandora] and [Gramtools][gramtools] from a set of \nMultiple Sequence Alignments.\n\n![master branch badge](https://github.com/iqbal-lab-org/make_prg/actions/workflows/ci.yaml/badge.svg) \n[![codecov](https://codecov.io/github/iqbal-lab-org/make_prg/branch/master/graph/badge.svg?token=6IQSY13MSH)](https://codecov.io/github/iqbal-lab-org/make_prg)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n# Support\n\nWe fully support `make_prg` on `linux` with `python` versions `3.8`-`3.11`. For other operating systems, `make_prg`\ncan be run through containers.\n\n[TOC]: #\n\n## Table of Contents\n- [Install](#install)\n  - [No installation needed - precompiled portable binary](#no-installation-needed---precompiled-portable-binary)\n  - [pip](#pip)\n  - [conda](#conda)\n  - [Container](#container)\n- [Running on a sample example](#running-on-a-sample-example)\n- [Usage](#usage)\n\n## Install\n\n### No installation needed - precompiled portable binary\n\nYou can use `make_prg` with no installation at all by simply downloading the precompiled binary, and running it.\nIn this binary, all libraries are linked statically. Compilation is done using [PyInstaller](https://github.com/pyinstaller/pyinstaller).\n\n#### Requirements\n`GLIBC >= 2.29` (present on `Ubuntu >= 19.04`, `Debian >= 11`, `CentOS >= 9`, etc);\n\n#### Download\n```\nwget https://github.com/iqbal-lab-org/make_prg/releases/download/0.5.0/make_prg_0.5.0\n```\n\n#### Run\n```\nchmod +x make_prg_0.5.0\n./make_prg_0.5.0 -h\n```\n\n### pip\n\n**Requirements**: `python>=3.8,<=3.11`\n\n```sh\npip install make_prg\n```\n\n### conda\n\n```sh\nconda install -c bioconda make_prg\n```\n\n### Container\n\nDocker images are hosted at [quay.io].\n\n#### `singularity`\n\nPrerequisite: [`singularity`][singularity]\n\n```sh\nURI="docker://quay.io/iqballab/make_prg"\nsingularity exec "$URI" make_prg --help\n```\n\nThe above will use the latest version. If you want to specify a version then use a\n[tag][quay.io] (or commit) like so.\n\n```sh\nVERSION="0.5.0"\nURI="docker://quay.io/iqballab/make_prg:${VERSION}"\n```\n\n#### `docker`\n\n[![Docker Repository on Quay](https://quay.io/repository/iqballab/make_prg/status "Docker Repository on Quay")](https://quay.io/repository/iqballab/make_prg)\n\nPrerequisite: [`docker`][docker]\n\n```sh\ndocker pull quay.io/iqballab/make_prg\ndocker run quay.io/iqballab/make_prg --help\n```\n\nYou can find all the available tags on the [quay.io repository][quay.io].\n\n## Running on a sample example\n\nTo see how to input files to both `make_prg from_msa` and `make_prg update`, and the outputs\nthey create on a sample example, see [sample example](sample_example).\n\n## Usage\n\n```\n$ make_prg --help\nusage: make_prg <subcommand> <options>\n\nSubcommand entrypoint\n\noptions:\n  -h, --help     show this help message and exit\n  -V, --version  show program\'s version number and exit\n\nAvailable subcommands:\n  \n    from_msa     Make PRG from multiple sequence alignment\n    update       Update PRGs given new sequences.\n```\n\n#### `from_msa`\n\n```\n$ make_prg from_msa --help\nusage: make_prg from_msa\n\noptions:\n  -h, --help            show this help message and exit\n  -i INPUT, --input INPUT\n                        Multiple sequence alignment file or a directory containing such files\n  -s SUFFIX, --suffix SUFFIX\n                        If the input parameter (-i, --input) is a directory, then filter for files with this suffix. If this parameter is not given, all files in the input directory is considered.\n  -o OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX\n                        Prefix for the output files\n  -f ALIGNMENT_FORMAT, --alignment-format ALIGNMENT_FORMAT\n                        Alignment format of MSA, must be a biopython AlignIO input alignment_format. See http://biopython.org/wiki/AlignIO. Default: fasta\n  -N MAX_NESTING, --max-nesting MAX_NESTING\n                        Maximum number of levels to use for nesting. Default: 5\n  -L MIN_MATCH_LENGTH, --min-match-length MIN_MATCH_LENGTH\n                        Minimum number of consecutive characters which must be identical for a match. Default: 7\n  -O OUTPUT_TYPE, --output-type OUTPUT_TYPE\n                        p: PRG, b: Binary, g: GFA, a: All. Combinations are allowed i.e., gb: GFA and Binary. Default: a\n  -F, --force           Force overwrite previous output\n  -t THREADS, --threads THREADS\n                        Number of threads. 0 will use all available. Default: 1\n  -v, --verbose         Increase output verbosity (-v for debug, -vv for trace - trace is for developers only)\n  --log LOG             Path to write log to. Default is stderr\n```\n\n#### `update`\n\n```\n$ make_prg update --help\nusage: make_prg update\n\noptions:\n  -h, --help            show this help message and exit\n  -u UPDATE_DS, --update-DS UPDATE_DS\n                        Filepath to the update data structures (a *.update_DS.zip file created from make_prg from_msa or update)\n  -o OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX\n                        Prefix for the output files\n  -d DENOVO_PATHS, --denovo-paths DENOVO_PATHS\n                        Filepath containing denovo sequences. Should point to a denovo_paths.txt file\n  -D LONG_DELETION_THRESHOLD, --deletion-threshold LONG_DELETION_THRESHOLD\n                        Ignores long deletions of the given size or longer. If long deletions should not be ignored, put a large value. Default: 10\n  -O OUTPUT_TYPE, --output-type OUTPUT_TYPE\n                        p: PRG, b: Binary, g: GFA, a: All. Combinations are allowed i.e., gb: GFA and Binary. Default: a\n  -F, --force           Force overwrite previous output\n  -t THREADS, --threads THREADS\n                        Number of threads. 0 will use all available. Default: 1\n  -v, --verbose         Increase output verbosity (-v for debug, -vv for trace - trace is for developers only)\n  --log LOG             Path to write log to. Default is stderr\n```\n\n[pandora]: https://github.com/rmcolq/pandora\n[gramtools]: https://github.com/iqbal-lab-org/gramtools/\n[docker]: https://docs.docker.com/v17.12/install/\n[quay.io]: https://quay.io/repository/iqballab/make_prg\n[singularity]: https://sylabs.io/guides/3.4/user-guide/quick_start.html#quick-installation-steps\n',
    'author': 'Michael Hall',
    'author_email': 'michael@mbh.sh',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/iqbal-lab-org/make_prg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)
