### Want to use `gentle` alone?
#### Gentle tutorial

##### Install the dependencies

Navigate to wherever you put your git repositories.

* Installing `gentle`

```
git clone https://github.com/lowerquality/gentle.git
cd gentle/
pip3 install -e . --user    # will install local python package
./install.sh                # will install dependences, e.g. sphinx
```

* Installing `praatio` is quite simple, as TJM put it on pypi.

```
pip3 install praatio --upgrade --user
```

##### Make your transcriptions

I can't tell you how to code your data. Only you know what you want to write. But, the beautiful thing about `gentle` is that it's robust to disfluencies and higher degrees of background noise. The quality of your transcription *will* affect how well the forced aligner does.

#### Run the forced aligner

You can run the forced aligner from within python. Here's a minimum working example:

```
import gentle
import multiprocessing

filename_to_transcribe = 'BayesForDays_tells_a_joke.wav'
transcript = """
Want to hear a joke about a piece of paper? Nevermind, it's terrible.
"""

resources = gentle.Resources()
nthreads = multiprocessing.cpu_count()

with gentle.resampled(filename_to_transcribe) as wavfile:
    aligner = gentle.ForcedAligner(resources, transcript, nthreads=nthreads)
    result = aligner.transcribe(wavfile)
```

And if you want to inspect `result`, you can get the contents in either json or csv format. If you choose csv formatting, the contents will look something like this (header not included):

```
raw_str     lower_str   start   end
Want        want        0.65	0.86
to          to	        0.86	0.9
hear        hear        0.9	1.11
a           a	        1.11	1.18
joke        joke        1.18	1.47
about       about       1.48	1.7
a           a	        1.7	1.75
piece       piece       1.75	1.97
of          of	        1.97	2.09
paper       paper	2.09	2.57
Nevermind   nevermind	3.04	3.72
it's        it's	3.88	4.13
terrible    terrible	4.13	4.76
```

