# gently
Get textgrids from your transcriptions of American English speech in Python 3 without pulling teeth! Leverage the dual power of `gentle` and `praatio` for VERY easy transcription forced alignment -- no more downsampling, figuring out sphinx, worrying about things like small pauses or disfluencies, etc.

#### Installation

To install gently, simply clone from this repository:
 
You can do so with pip from within the `gently` directory:

```
cd wherever_you_put_your_github_repos
git clone https://github.com/BayesForDays/gently.git
cd gently
pip3 install -e .
```

#### Use within Python 3

To use `gently` from within Python (currently only tested on 3.7) you will need a csv describing your data containing two things: transcriptions (first column) and filenames (second column). Specifically,

1. Filenames can be absolute or relative paths.
2. .wav files corresponding to those filenames / paths.

As-is, the big alignment functions (`align_csv`) will save textgrids to the same folder as your wav files but use the `TextGrid` extension.

Caveat emptor: It is always a good idea to do backups. If you have existing TextGrids, consider moving them to another folder OR making a copy of your wav files and running the script below over the copies. The `gently.aligner.align_csv` effectively does the below:

```
from gently.aligner import align_file, alignment_to_textgrid, save_textgrid
import pandas as pd

example_df = pd.read_csv("example_df.txt", sep="\t")

for ix, t in example_df.iterrows():
    transcription = t['transcription']
    path = t['path_to_file']
    textgrid_path = path.split(".")[0] + '.TextGrid'
    alignment = align_file(transcription, path)
    textgrid = alignment_to_textgrid(alignment, path)
    save_textgrid(textgrid, textgrid_path)
```

More concisely, however, you might just want to use `gently.aligner.align_csv` which does the same things:

```
from gently.aligner import align_csv
import pandas as pd

align_csv(filename="example_df.txt", delim="\t")
```

Note: This project is still very much in beta! Please provide feedback if there are missing features and I will be happy to make changes to accommodate other use cases.

### Gently from the command line

You may be coming to gently from `p2fa` or even `gentle`, who include an `align.py` script. p2fa is a bit of a [process](https://phon.wordpress.ncsu.edu/lab-manual/forced-alignment/) and requires figuring out how to install HTK. Even gentle's alignment script only transcribes one file at a time. Unlike the existing frameworks, the `align.py` script provided as part of `gently` loops through a CSV that you specify. So, if you want, you can just align one file or multiples at the same time.

To use gently from the command line, you can simply use the `align.py` script in the top-level directory of `gently.` You can copy-paste this file anywhere you want. If you want to use the regular `align.py`, simply tell it where your CSV is with your filenames / addresses and what delimiter (tabs, commas, etc.) separates the two columns.

For example, the top of my `example_df` is a tab-delimited file with transcriptions (left) and filenames (right):

```
transcription           path_to_file
The rose flashes	./test_wavs/audio/rope_rose_flashes_20_1_sayCohortFirst.wav
The scale flashes	./test_wavs/audio/rooster_scale_flashes_20_1_noCohortPresent.wav
The hook flashes	./test_wavs/audio/kangaroo_hook_flashes_20_1_noCohortSaid.wav
The plate flashes	./test_wavs/audio/plane_plate_flashes_20_1_hearCohortFirst.wav
The saddle flashes	./test_wavs/audio/tie_saddle_flashes_20_1_noCohortSaid.wav
```

To run from the command line, simply make sure the script is in the right place. Because my filenames use _relative_ paths, I want to have `align.py` in the directory above `test_wavs`. If I used an absolute path (e.g. `~/Documents/path/to/test_wavs/`), then where `align.py` does not matter. To learn more about absolute and relative paths, there are a number of resources, but you might like this video tutorial: https://www.youtube.com/watch?v=ephId3mYu9o
