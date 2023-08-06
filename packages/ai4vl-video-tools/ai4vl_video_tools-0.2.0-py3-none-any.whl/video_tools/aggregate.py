import itertools
import logging
import re
import shutil
from fractions import Fraction
from pathlib import Path
from typing import List

import ffmpeg
from natsort import natsorted
from slugify import slugify
from tqdm import tqdm

DEFAULT_OUTPUT_FILENAME_TEMPLATE = "{study_slug}_{case_number}{output_extension}"
DEFAULT_INPUT_PATH_PATTERN = r"(?P<study_name>[-\w ]+)\/(?P<case_number>[-\d]+)\/(?P<stem>[-\w ]+)(?P<input_extension>\.\w+)$"

logger = logging.getLogger(__name__)


class Aggregator:
    def __init__(
        self,
        input_folder: Path,
        output_folder: Path,
        input_path_pattern: str = DEFAULT_INPUT_PATH_PATTERN,
        input_extension: str = ".mp4",
        output_extension: str = ".mp4",
        output_filename_template: str = DEFAULT_OUTPUT_FILENAME_TEMPLATE,
        seperator_frames=30,
        dry_run=False,
        overwrite=False,
    ):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.input_path_pattern = input_path_pattern
        self.input_extension = input_extension
        self.output_extension = output_extension
        self.output_filename_template = output_filename_template
        self.seperator_frames = seperator_frames
        self.dry_run = dry_run
        self.temp_path = self.output_folder / "_temp"
        self.overwrite = overwrite

    def _get_input_path_re(self):
        return re.compile(self.input_path_pattern)

    def search_for_input_matches(self):
        expression = self._get_input_path_re()
        for path in self.input_folder.glob("**/*"):
            relative_path = path.relative_to(self.input_folder)
            if relative_path.suffix.lower() != self.input_extension.lower():
                continue
            if match := expression.match(relative_path.as_posix()):
                yield {"path": path, **match.groupdict()}

    def get_aggregations(self, input_matches):
        case_key = lambda match: match["case_number"]
        stem_key = lambda match: match["stem"]
        grouper = itertools.groupby(sorted(input_matches, key=case_key), case_key)
        for case_number, group in grouper:
            group = list(group)
            paths = [match["path"] for match in natsorted(group, key=stem_key)]
            yield {
                "case_number": case_number,
                "study_name": group[0]["study_name"],
                "study_slug": slugify(group[0]["study_name"]),
                "snippet_count": len(paths),
                "paths": paths,
            }

    def _run_stream(self, stream):
        if self.dry_run:
            logger.info("[dry run] %s", " ".join(stream.compile()))
        else:
            out, err = stream.run(quiet=True)
            logger.debug(out)
            logger.debug(err)

    def _get_seperator_file_path(self, vary_on):
        return (
            self.temp_path
            / "seperator"
            / f"{'_'.join(str(on) for on in vary_on)}{self.input_extension}"
        )

    def _clear_seperator_files(self):
        if self.temp_path.exists():
            logger.info("Clearing seperator files")
            if self.dry_run:
                return
            shutil.rmtree(self.temp_path)

    def _get_playlist_file(self, input_paths: List[Path], case_number):
        playlist_file = self.temp_path / "playlists" / f"{case_number}.txt"
        if not self.dry_run:
            playlist_file.parent.mkdir(parents=True, exist_ok=True)
            with open(playlist_file, "w") as f:
                for paths in input_paths:
                    f.write(f"file '{paths.absolute().as_posix()}'\n")
        return playlist_file

    def generate_output_file(self, job):
        output_file_path = self.output_folder / self.output_filename_template.format(
            study_slug=job["study_slug"],
            case_number=job["case_number"],
            snippet_count=job["snippet_count"],
            output_extension=self.output_extension,
        )
        if not self.overwrite and output_file_path.exists():
            logger.info("Skipping case %s, output file already exists", job["case_number"])
            return

        seperator_file_path = None
        if len(job["paths"]) > 1 and self.seperator_frames:
            probe_info = ffmpeg.probe(job["paths"][0])
            v_stream = probe_info["streams"][0]
            assert v_stream["codec_type"] == "video"
            fps = Fraction(v_stream["r_frame_rate"])
            duration = float(round(self.seperator_frames / fps, 2))
            seperator_file_path = self._get_seperator_file_path(
                vary_on=[
                    "black",
                    f"{v_stream['width']}x{v_stream['height']}",
                    f"{self.seperator_frames}_at_{float(fps):.2f}_fps",
                ]
            )
            if not seperator_file_path.exists():
                if not self.dry_run:
                    seperator_file_path.parent.mkdir(parents=True, exist_ok=True)
                stream = (
                    ffmpeg.input(
                        f"color=black:s={v_stream['width']}x{v_stream['height']}:r={v_stream['r_frame_rate']}",
                        format="lavfi",
                    )
                    .trim(end=f"00:00:{duration}")
                    .output(seperator_file_path.as_posix())
                    .overwrite_output()
                )
                logger.info("Preparing seperator file for case %s", job["case_number"])
                self._run_stream(stream)

        logger.info("Generating case %s", job["case_number"])

        input_paths = []
        for idx, path in enumerate(job["paths"]):
            input_paths.append(path)
            if self.seperator_frames and idx < len(job["paths"]) - 1:
                input_paths.append(seperator_file_path)

        playlist_file_path = self._get_playlist_file(input_paths, job["case_number"])
        stream = ffmpeg.input(playlist_file_path.as_posix(), format="concat", safe=0).output(
            output_file_path.as_posix(), c="copy"
        )
        if self.overwrite:
            stream = stream.overwrite_output()
        self._run_stream(stream)

    def run(self):
        input_matches = self.search_for_input_matches()
        aggregations = self.get_aggregations(input_matches)
        if not self.dry_run:
            self.output_folder.mkdir(parents=True, exist_ok=True)
        aggregations = natsorted(list(aggregations), key=lambda job: job["case_number"])
        for job in tqdm(aggregations, desc="Generating videos"):
            self.generate_output_file(job)
        self._clear_seperator_files()
