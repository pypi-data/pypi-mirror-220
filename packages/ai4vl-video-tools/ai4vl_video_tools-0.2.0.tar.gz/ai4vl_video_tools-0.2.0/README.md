
# ai4vl video tools

Video handling tools for ai4vl.

## Install it from PyPI

```bash
pip install ai4vl-video-tools
```

## Usage

The tools expects a directory with video files as input and outputs a directory with the converted videos.
The source directory must have the following structure:

```bash
source_dir
└── some_study_name
    ├── 1-1  # these are patient number - case number
    │   ├── snipped01.mp4
    │   ├── snipped02.mp4
    │   └── snipped03.mp4
    └── 2-2
        └── snipped04.mp4
```

Run the help command to see the usage. A basic example is:

```bash
$ python -m video_tools -v aggregate -i tests/data/ -o tests/data/output -s 1
```
