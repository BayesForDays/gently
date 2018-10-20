"""
This script will take a CSV of transcription, file path pairs and make textgrids for you
These are saved in a new folder (textgrids)
"""

import pandas as pd
import gentle
from contextlib import contextmanager
import signal, json, wave, contextlib
from praatio import tgio

resources = gentle.Resources()
nthreads = 1

def align_csv(filename, delim): # so basically, from gently.align import align_csv
    """
    Read in a file of transcription, sound filename pairs.
    :param filename: May be relative or absolute.
    :param delim: If your csv is a csv, make sure your transcriptions are properly formatted
    :return: Nothing -- writes to local textgrid/ directory.
    """
    t_sfid_df = pd.read_csv(
        filename, delimiter=delim
    ).rename(columns={0: "transcription", 1: "path_to_file"})
    align_files(t_sfid_df)


def align_files(t_sfid_df):
    for ix, t in t_sfid_df.iterrows():
        transcription = t['transcription']
        path = t['path_to_file']
        textgrid_path = path.split(".")[0] + '.TextGrid'
        alignment = align_file(transcription, path)
        textgrid = _to_textgrid(alignment, path)
        _save_textgrid(textgrid, textgrid_path)


def align_file(transcription, snd_filename):
    # TODO: Add a file of "sound files that did not finish"
    class TimeoutException(Exception):
        pass
    @contextmanager
    def time_limit(seconds):
        def signal_handler(signum, frame):
            raise TimeoutException("Timed out!")

        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)

    with gentle.resampled(snd_filename) as wavfile:
        aligner = gentle.ForcedAligner(resources, transcription, nthreads=nthreads)
        try:
            with time_limit(10):
                result = {snd_filename: aligner.transcribe(wavfile)}
        except TimeoutException as e:
            print("Transcription of {} timed out! Please check that your transcription is accurate.".format(fid))
            result = {snd_filename: None}
    return result


def _to_textgrid(alignment, path):
    """
    Take a filename and its associated transcription and fill in all the gaps
    """
    with contextlib.closing(wave.open(path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    rearranged_words = []
    file_ons = 0
    try:
        content = json.loads(alignment.to_json())
        all_ons = content['words'][0]['start']
        for ix, word in enumerate(content['words']):
            word_ons = word['start']
            word_off = word['end']
            target = word['alignedWord']
            if (ix >= 1) and (ix < (len(content['words']))):
                prev_word = content['words'][ix - 1]
                prev_ons = prev_word['start']
                prev_off = prev_word['end']
                if word['start'] > prev_off:
                    rearranged_words.append((prev_off, word_ons, ''))
            elif ix == 0:
                rearranged_words.append((file_ons, all_ons, ''))  # make empty first tier
            rearranged_words.append((word_ons, word_off, target))
        if word_off < duration:
            rearranged_words.append((word_off, duration, ''))
    except:
        rearranged_words = [(0, duration, '')]
    tg = tgio.Textgrid()
    tg.addTier(tgio.IntervalTier('word', rearranged_words))
    return tg


def _save_textgrid(textgrid, path):
    if path is not None:
        textgrid.save(path)


