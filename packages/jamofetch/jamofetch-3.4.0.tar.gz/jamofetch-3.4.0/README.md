# jamofetch
thin wrapper on JAMO to allow sequence retrieval on Dori and at NERSC

## Installation
Jamofetch requires python 3.8 or higher.

### Adding via requirements.txt
Include the following two lines in the requirements.txt of your project:
```python
jamofetch==3.4.0
--extra-index-url https://code.jgi.doe.gov/api/v4/projects/479/packages/pypi/simple
```
### Manual installation
First option:
```bash
$ pip install jamofetch --index-url https://code.jgi.doe.gov/api/v4/projects/479/packages/pypi/simple
```
Second option:
```bash
$ pip install git+https://code.jgi.doe.gov/DNScott/jamofetch
```
## Usage
See script **docs/demo_script.py** in the project for a sample script.

Create a JamoFetcher:
```pthon
from jamofetch.jamofetch import JamoFetcher, JamoLibSeq

WAIT_INTERVAL = 10  # check if JAMO has provisioned sequence every 10 seconds
WAIT_MAX = 7200     # max wait for sequence is 7200 seconds or 2 hours

# directory where JAMO will link sequence, will be created if it doesn't exist
link_dir = '/tmp/sequence-links'

# create a fetcher
fetcher: JamoFetcher = JamoFetcher(link_dir=link_dir, wait_interval_secs=WAIT_INTERVAL, wait_max_secs=WAIT_MAX)
```

Note the following default configuration parameters for JamoLibSeq.
Setting wait_max_secs to -1 causes the JamoFetcher instance to wait indefenitely for
JAMO sequence.
```python
class JamoFetcher():
    def __init__(self, link_dir='.', wait_interval_secs=10, wait_max_secs=-1):
```

Fetch sequence for a library, print path of symlink to sequence file and the real path
to the file.
```python
LIBRARY = 'NPUNN'
# Call JAMO to link sequence in the background.  Symlinks to the sequence
# files are created by JAMO in the directory specified by the
# link_dir parameter supplied to the JamoFetcher constructor.
lib_seq: JamoLibSeq = fetcher.fetch_lib_seq(LIBRARY)

printf(f"library name: {lib_seq.get_lib_name()}")
print(f"sequence symlink: {lib_seq.get_seq_path()}")
print(f"sequence real path: {lib_seq.get_real_path()}")
```

Check if sequence has been provided by JAMO, i.e. the symlink is not broken.  Wait
for sequence if it isn't ready.
```python
if lib_seq.seq_exists():
    print("sequence ready")
else:
    # wait for JAMO
    real_path = lib_seq.get_real_path_wait()
    print(f"sequence ready at {real_path}")
```
## Command Line Tool
Installing jamofetch with pip exposes a command line interface.
```
(venv) [dnscott@ln004 jamofetch]$ jamofetch  -h
usage: jamofetch [-h] [-l LIBRARY] [-d DIRECTORY] [-i INTERVAL] [-m MAX] [-w] [-v] [--logging LOGGING]

options:
  -h, --help            show this help message and exit
  -l LIBRARY, --library LIBRARY
                        library name(s) for which to retrieve sequence
  -d DIRECTORY, --directory DIRECTORY
                        directory where to link sequence, defaults to current directory. Directory will be created if it doesn't exit.
  -i INTERVAL, --interval INTERVAL
                        wait interval in seconds to check if sequence has been fetched, ignored if wait flag not set
  -m MAX, --max MAX     maximum time to wait for sequence in seconds, ignored if wait flag not set. Specify -1 to wait indefinetely.
  -w, --wait            wait for jamo to link sequence, output real path of linked sequence
  -v, --version         print jamofetch version
  --logging LOGGING     logging level (specify DEBUG for verbose logging)
(venv) [dnscott@ln004 jamofetch]$ jamofetch -d data -l NPUNN -l NOOHG -l HOGH -w --max -1
fetching sequence:
NPUNN /global/dna/dm_archive/sdm/pacbio/00/27/47/pbio-2747.27352.bc1001_BAK8A_OA--bc1001_BAK8A_OA.ccs.fastq.gz BACKUP_COMPLETE 6391936239a7711d789a9380
NOOHG /global/dna/dm_archive/sdm/pacbio/00/26/91/pbio-2691.26653.bc1001_BAK8A_OA--bc1001_BAK8A_OA.ccs.fastq.gz RESTORED 6347dbb35bc59487d7e768d6
HOGH /global/dna/dm_archive/sdm/illumina/00/63/97/6397.2.44053.GGCTAC.fastq.gz RESTORE_IN_PROGRESS 51d52a82067c014cd6ef4f6f

sequence links:
HOGH symlink: /clusterfs/jgi/groups/dsi/homes/dnscott/git/jamofetch/data/HOGH.6397.2.44053.GGCTAC.fastq.gz
HOGH realpath: /clusterfs/jgi/scratch/dsi/aa/dm_archive/sdm/illumina/00/63/97/6397.2.44053.GGCTAC.fastq.gz
NOOHG symlink: /clusterfs/jgi/groups/dsi/homes/dnscott/git/jamofetch/data/NOOHG.pbio-2691.26653.bc1001_BAK8A_OA--bc1001_BAK8A_OA.ccs.fastq.gz
NOOHG realpath: /clusterfs/jgi/scratch/dsi/aa/dm_archive/sdm/pacbio/00/26/91/pbio-2691.26653.bc1001_BAK8A_OA--bc1001_BAK8A_OA.ccs.fastq.gz
NPUNN symlink: /clusterfs/jgi/groups/dsi/homes/dnscott/git/jamofetch/data/NPUNN.pbio-2747.27352.bc1001_BAK8A_OA--bc1001_BAK8A_OA.ccs.fastq.gz
NPUNN realpath: /clusterfs/jgi/scratch/dsi/aa/dm_archive/sdm/pacbio/00/27/47/pbio-2747.27352.bc1001_BAK8A_OA--bc1001_BAK8A_OA.ccs.fastq.gz

waiting for JAMO to provision sequence . . . .
NOOHG sequence ready
NPUNN sequence ready
```
## Credits

`jamofetch` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

