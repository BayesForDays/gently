# gently
Gentle and praatio for easy production data transcription

To install gently, simply clone from this repository. You can do so with pip from within the `gently` directory:

```
cd wherever_you_put_your_github_repos
git clone https://github.com/BayesForDays/gently.git
cd gently
pip3 install -e .
```

To use `gently` from within Python (currently only tested on 3.7) you will need a csv describing your data containing two things:

1. A csv containing transcriptions (first column) and filenames (second column). Filenames can be absolute or relative paths.
2. .wav files corresponding to those filenames / paths.

As-is, the alignment functions will save textgrids to the same folder as your wav files. It is always a good idea to do backups. If you have existing TextGrids, consider moving them to another folder OR making a copy of your wav files and running your script over the copies. Here is a skeleton of an example:

```
from gently.align import align_csv
import pandas as pd

example_df = pd.read_csv("example_df.txt", sep="\t")

```