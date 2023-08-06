from pathlib import Path, PurePath
from dataclasses import dataclass, field
from typing import List, Optional, Union
import requests
from rich import print
from rich.table import Table
from rich.markup import escape
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    BarColumn,
    MofNCompleteColumn,
    track,
)
from rich.panel import Panel
from rich.console import Group
from rich.live import Live
from geovisio_cli.exception import CliException, raise_for_status
from geovisio_cli.auth import login
from geovisio_cli.model import Geovisio
from geovisio_cli import utils
from geopic_tag_reader import reader
from PIL import Image
from time import sleep
from datetime import timedelta
import os
import toml
from . import exception
from enum import Enum
import logging
from haversine import haversine, Unit  # type: ignore

SEQUENCE_TOML_FILE = "_geovisio.toml"


class SortMethod(str, Enum):
    filename_asc = "filename-asc"
    filename_desc = "filename-desc"
    time_asc = "time-asc"
    time_desc = "time-desc"


@dataclass
class SplitParams:
    maxDistance: Optional[int] = None
    maxTime: Optional[int] = None

    def is_split_needed(self):
        return self.maxDistance is not None or self.maxTime is not None


@dataclass
class InteriorOrientation:
    make: str
    model: str
    field_of_view: Optional[int]


@dataclass
class Picture:
    path: Optional[str] = None
    id: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    metadata: Optional[reader.GeoPicTags] = None

    def toml(self):
        return {
            "path": self.path,
            "id": self.id,
            "location": self.location,
            "status": self.status,
        }

    @staticmethod
    def from_toml(data):
        return Picture(
            path=data.get("path"),
            id=data.get("id"),
            location=data.get("location"),
            status=data.get("status"),
        )


@dataclass
class Sequence:
    title: str = ""
    path: str = ""
    id: Optional[str] = None
    location: Optional[str] = None
    producer: Optional[str] = None
    interior_orientation: List[InteriorOrientation] = field(default_factory=lambda: [])
    pictures: List[Picture] = field(default_factory=lambda: [])
    sort_method: Optional[SortMethod] = None

    def toml(self):
        res = {
            "sequence": {
                "title": self.title,
                "path": self.path,
                "id": self.id,
                "location": self.location,
                "producer": self.producer,
                "sort_method": self.sort_method.value
                if self.sort_method is not None
                else None,
            },
            "pictures": {},
        }

        for pos, pic in enumerate(self.pictures, start=1):
            pict = pic.toml()
            pict["position"] = pos
            res["pictures"][os.path.basename(pic.path)] = pict

        return res

    @staticmethod
    def from_toml(data):
        s = Sequence()
        s.update_from_toml(data)
        return s

    def update_from_toml(self, data):
        if data.get("sequence"):
            self.title = data["sequence"].get("title", "")
            self.path = data["sequence"].get("path", "")
            self.id = data["sequence"].get("id")
            self.location = data["sequence"].get("location")
            self.producer = data["sequence"].get("producer")
            self.sort_method = (
                SortMethod(data["sequence"]["sort_method"])
                if "sort_method" in data["sequence"]
                else None
            )

        if data.get("pictures"):
            self.pictures = [
                Picture.from_toml(picData)
                for picId, picData in sorted(
                    data["pictures"].items(), key=lambda item: int(item[1]["position"])
                )
            ]

    def all_done(self):
        return self.nb_waiting() + self.nb_preparing() == 0

    def nb_ready(self):
        return sum((1 for p in self.pictures if p.status == "ready"))

    def nb_waiting(self):
        return sum((1 for p in self.pictures if p.status == "waiting-for-process"))

    def nb_preparing(self):
        return sum(
            (
                1
                for p in self.pictures
                if (p.status and p.status.startswith("preparing"))
            )
        )

    def nb_broken(self):
        return sum((1 for p in self.pictures if p.status == "broken"))


@dataclass
class Split:
    prevPic: Picture
    nextPic: Picture
    reason: str


@dataclass
class ManySequences:
    """ManySequences is a single handler for multiple sequences found in a single folder."""

    sequences: List[Sequence] = field(default_factory=lambda: [])
    splits: List[Split] = field(default_factory=lambda: [])

    def toml(self):
        res = {}
        for i, s in enumerate(self.sequences, start=1):
            res[str(i)] = s.toml()
        return res

    def has_same_sort_method(self, sortMethod):
        if sortMethod is None:
            return True
        else:
            for s in self.sequences:
                if s.sort_method != sortMethod:
                    return False
            return True

    def is_empty(self):
        if len(self.sequences) == 0:
            return True
        return not any((len(s.pictures) != 0 for s in self.sequences))

    def has_valid_pictures(self):
        for s in self.sequences:
            for p in s.pictures:
                if p.status != "broken-metadata":
                    return True
        return False

    @staticmethod
    def from_toml(data):
        ms = ManySequences()
        ms.sequences = [Sequence.from_toml(seqData) for seqId, seqData in data.items()]
        return ms


@dataclass
class UploadError:
    position: int
    picture_path: str
    error: Union[str, dict]
    status_code: int


@dataclass
class UploadReport:
    location: str
    uploaded_pictures: List[Picture] = field(default_factory=lambda: [])
    errors: List[UploadError] = field(default_factory=lambda: [])


def process(
    path: Path,
    title: Optional[str],
    sortMethod: Optional[SortMethod] = None,
    splitParams: Optional[SplitParams] = None,
) -> ManySequences:
    ms = _read_sequences(path, title, sortMethod, splitParams)
    _write_sequences_toml(ms, Path(os.path.join(path, SEQUENCE_TOML_FILE)))

    if (
        splitParams is not None
        and splitParams.is_split_needed()
        and len(ms.sequences) > 1
    ):
        print(f"\n🗂️  Pictures are split into {len(ms.sequences)} sequences")
        for i in range(len(ms.splits)):
            if i == 0:
                print(f"  Sequence 1 ({len(ms.sequences[0].pictures)} pictures)")
            print(f"    ✂️ {ms.splits[i].reason}")
            print(f"  Sequence {i+2} ({len(ms.sequences[i+1].pictures)} pictures)")
    else:
        print(f"\n🗂️  All pictures belong to a single sequence")

    return ms


def upload(
    path: Path,
    geovisio: Geovisio,
    title: Optional[str],
    wait: bool = False,
    alreadyBlurred: bool = False,
    sortMethod: Optional[SortMethod] = None,
    splitParams: Optional[SplitParams] = None,
) -> List[UploadReport]:
    # early test that the given url is correct
    utils.test_geovisio_url(geovisio.url)
    with requests.session() as s:
        # early test login
        if not _login_if_needed(s, geovisio):
            raise CliException(
                "🔁 Computer not authenticated yet, impossible to upload pictures, but you can try again the same upload command after finalizing the login"
            )

        ms = process(path, title, sortMethod, splitParams)
        res = []
        for i in range(len(ms.sequences)):
            print("")  # Do not remove, gives a bit of spacing in output
            res.append(_publish(path, s, ms, i, geovisio, wait, alreadyBlurred))

        return res


def _publish(
    path: Path,
    session: requests.Session,
    sequences: ManySequences,
    sequenceId: int,
    geovisio: Geovisio,
    wait: bool,
    alreadyBlurred: bool,
) -> UploadReport:
    sequence = sequences.sequences[sequenceId]
    tomlFile = os.path.join(path, SEQUENCE_TOML_FILE)

    # Read sequence data
    if sequence.id:
        sequence = info(sequence)
        print(
            f'📡 Resuming upload of sequence "{sequence.title}" (part {sequenceId+1}/{len(sequences.sequences)})'
        )
        print(f"  - Folder: {sequence.path}")
        print(f"  - API ID: {sequence.id}")
    else:
        print(
            f'📡 Uploading sequence "{sequence.title}" (part {sequenceId+1}/{len(sequences.sequences)})'
        )
        print(f"  - Folder: {sequence.path}")

    data = {}
    if sequence.title:
        data["title"] = sequence.title

    # List pictures to upload
    picturesToUpload = {}
    for i, p in enumerate(sequence.pictures, start=1):
        if p.id is None or p.status == "broken":
            picturesToUpload[i] = p

    # Create sequence on initial publishing
    if not sequence.id:
        seq = session.post(
            f"{geovisio.url}/api/collections", data=data, timeout=utils.REQUESTS_TIMEOUT
        )
        raise_for_status(seq, "Impossible to query GeoVisio")

        sequence.id = seq.json()["id"]
        sequence.location = seq.headers["Location"]
        _write_sequences_toml(sequences, Path(tomlFile))

        print(f"\n  ✅ Created collection {sequence.location}")

    else:
        if len(picturesToUpload) == 0:
            print(
                f"\n  ✅ Everything ({len(sequence.pictures)} picture{'s' if len(sequence.pictures) != 1 else ''}) have already been uploaded, nothing to do"
            )
            assert sequence.location
            return UploadReport(location=sequence.location)
        print(
            f"\n  ⏭️ Skipping {len(sequence.pictures) - len(picturesToUpload)} already published pictures"
        )

    if not sequence.location:
        raise CliException("Sequence has no API location defined")

    report = UploadReport(location=sequence.location)

    uploading_progress = Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        TextColumn("[{task.completed}/{task.total}]"),
    )
    current_pic_progress = Progress(
        TextColumn("  📷 Processing [bold purple]{task.fields[file]}"),
        SpinnerColumn("simpleDots"),
    )
    error_progress = Progress(TextColumn("{task.description}"))

    last_error = Progress(
        TextColumn("🔎 Last error 🔎\n{task.description}"),
    )
    error_panel = Panel(Group(error_progress, last_error), title="Errors")
    uploading_task = uploading_progress.add_task(
        f"  [green]🚀 Uploading pictures...",
        total=len(picturesToUpload),
    )
    current_pic_task = current_pic_progress.add_task("", file="")
    progress_group = Group(
        uploading_progress,
        current_pic_progress,
        error_panel,
    )
    error_task = error_progress.add_task("[green]No errors")
    last_error_task = last_error.add_task("", visible=False)
    with Live(progress_group):
        for i, p in picturesToUpload.items():
            if not p.path:
                raise CliException(f"Missing path for picture {i}")

            uploading_progress.advance(uploading_task)
            current_pic_progress.update(current_pic_task, file=p.path.split("/")[-1])
            try:
                picture_response = session.post(
                    f"{sequence.location}/items",
                    files={"picture": open(p.path, "rb")},
                    data={
                        "position": i,
                        "isBlurred": "true" if alreadyBlurred else "false",
                    },
                    timeout=utils.REQUESTS_TIMEOUT,
                )
            except (requests.Timeout,) as timeout_error:
                raise CliException(
                    f"""Timeout while trying to post picture. Maybe the instance is overloaded? Please contact your instance administrator.

            [bold]Error:[/bold]
            {timeout_error}"""
                )
            except (
                requests.ConnectionError,
                requests.ConnectTimeout,
                requests.TooManyRedirects,
            ) as cnx_error:
                raise CliException(
                    f"""Impossible to reach GeoVisio while trying to post a picture, connection was lost. Please contact your instance administrator.

            [bold]Error:[/bold]
            {cnx_error}"""
                )

            # Picture at given position exists -> mark it as OK
            if picture_response.status_code == 409:
                sequence = status(sequence)
                _write_sequences_toml(sequences, Path(tomlFile))
                report.uploaded_pictures.append(p)

            elif picture_response.status_code >= 400:
                body = (
                    picture_response.json()
                    if picture_response.headers.get("Content-Type")
                    == "application/json"
                    else picture_response.text
                )
                report.errors.append(
                    UploadError(
                        position=i,
                        picture_path=p.path,
                        status_code=picture_response.status_code,
                        error=body,
                    )
                )

                error_progress.update(
                    error_task,
                    description=f"[bold red]{len(report.errors)} errors",
                )
                last_error.update(last_error_task, description=body, visible=True)
                p.status = "broken"
                _write_sequences_toml(sequences, Path(tomlFile))

            else:
                p.location = picture_response.headers["Location"]
                p.id = picture_response.json()["id"]
                p.status = None
                report.uploaded_pictures.append(p)
                _write_sequences_toml(sequences, Path(tomlFile))

    if not report.uploaded_pictures:
        print(
            f"  [red]💥 All pictures upload of sequence {sequence.title} failed! 💥[/red]"
        )
    else:
        print(
            f"  🎉 [bold green]{len(report.uploaded_pictures)}[/bold green] pictures uploaded"
        )
    if report.errors:
        print(f"  [bold red]{len(report.errors)}[/bold red] pictures not uploaded:")
        for e in report.errors:
            msg: Union[str, dict] = e.error
            if isinstance(e.error, str):
                msg = escape(e.error.replace("\n", "\\n"))
            print(f" - {e.picture_path} (status [bold]{e.status_code}[/]): {msg}")

    if wait:
        wait_for_sequence(sequence)
    else:
        print(f"  Note: You can follow the picture processing with the command:")
        from rich.syntax import Syntax

        print(
            f"    [bold]geovisio collection-status --wait --location {sequence.location}"
        )
    return report


def _sort_files(
    pictures: List[Picture], method: Optional[SortMethod] = SortMethod.time_asc
) -> List[Picture]:
    """Sorts pictures according to their file name

    Parameters
    ----------
    pictures : Picture[]
        List of pictures to sort
    method : SortMethod
        Sort logic to adopt (time-asc, time-desc, filename-asc, filename-desc)

    Returns
    -------
    Picture[]
        List of pictures, sorted
    """

    if method is None:
        method = SortMethod.time_asc

    if method not in [item.value for item in SortMethod]:
        raise exception.CliException("Invalid sort strategy: " + str(method))

    # Get the sort logic
    strat, order = method.split("-")

    # Sort based on filename
    if strat == "filename":

        def sort_fct(p):
            try:  # Try to sort based on numeric notation
                return int(PurePath(p.path or "").stem)
            except:  # Otherwise, sort as strings
                return PurePath(p.path or "").stem

        pictures.sort(key=sort_fct)

    # Sort based on picture ts
    elif strat == "time":
        pictures.sort(key=lambda p: p.metadata.ts if p.metadata is not None else 0)

    if order == "desc":
        pictures.reverse()

    return pictures


def _split_pictures_into_sequences(
    pictures: List[Picture],
    splitParams: Optional[SplitParams] = SplitParams(),
    title: Optional[str] = None,
    path: Optional[str] = None,
    sort_method: Optional[SortMethod] = None,
) -> ManySequences:
    """Split a list of pictures into multiple lists of pictures (to create sequences)
    based on maximum distance, time and rotation between two pictures.

    Note that this function expect pictures to be sorted and have their metadata set.

    Parameters
    ----------
    pictures : Picture[]
        List of pictures to check, sorted and with metadata defined
    splitParams : SplitParams
        The parameters to define deltas between two pictures
    title : str
        Title to set on resulting sequences
    path : str
        Folder to set on resulting sequences
    sort_method : SortMethod
        Sort method to set on resulting sequences

    Returns
    -------
    ManySequences
        List of pictures splitted into smaller sequences
    """

    ms = ManySequences()

    # No split parameters given -> just return given pictures
    if splitParams is None or not splitParams.is_split_needed():
        ms.sequences = [
            Sequence(
                title=title or "",
                path=path or "",
                pictures=pictures,
                sort_method=sort_method,
            )
        ]
        return ms

    currentPicList: List[Picture] = []

    for pic in pictures:
        if len(currentPicList) == 0:  # No checks for 1st pic
            currentPicList.append(pic)
        else:
            lastPic = currentPicList[-1]

            # Missing metadata -> skip
            if lastPic.metadata is None or pic.metadata is None:
                currentPicList.append(pic)
                continue

            # Time delta
            timeOutOfDelta = (
                False
                if splitParams.maxTime is None
                else abs(lastPic.metadata.ts - pic.metadata.ts) > splitParams.maxTime
            )

            # Distance delta
            distance = haversine(
                (lastPic.metadata.lat, lastPic.metadata.lon),
                (pic.metadata.lat, pic.metadata.lon),
                unit=Unit.METERS,
            )
            distanceOutOfDelta = (
                False
                if splitParams.maxDistance is None
                else distance > splitParams.maxDistance
            )

            # One of deltas maxed -> create new sequence
            if timeOutOfDelta or distanceOutOfDelta:
                # Mark the reason for split
                picRangeTxt = f"between {PurePath(lastPic.path or '').stem} and {PurePath(pic.path or '').stem}"
                if timeOutOfDelta:
                    reason = f"Too much time {picRangeTxt} ({round(abs(lastPic.metadata.ts - pic.metadata.ts))} seconds)"
                elif distanceOutOfDelta:
                    reason = (
                        f"Too much distance {picRangeTxt} ({round(distance)} meters)"
                    )

                ms.splits.append(Split(lastPic, pic, reason))
                ms.sequences.append(
                    Sequence(
                        title=title or "",
                        path=path or "",
                        pictures=currentPicList,
                        sort_method=sort_method,
                    )
                )
                currentPicList = [pic]

            # Otherwise, still in same sequence
            else:
                currentPicList.append(pic)

    ms.sequences.append(
        Sequence(
            title=title or "",
            path=path or "",
            pictures=currentPicList,
            sort_method=sort_method,
        )
    )

    return ms


def _read_sequences(
    path: Path,
    title: Optional[str] = None,
    sortMethod: Optional[SortMethod] = None,
    splitParams: Optional[SplitParams] = None,
) -> ManySequences:
    if not path.is_dir():
        raise CliException(f"{path} is not a directory, cannot read pictures")

    if title is None:
        title = path.name

    sequences = None
    stoml = os.path.join(path, SEQUENCE_TOML_FILE)

    # Check if a TOML file exists, then use it instead of generating one
    if os.path.isfile(stoml):
        try:
            sequences = _read_sequences_from_toml(Path(stoml))
            print(f"📄 Using metadata from existing config file: {stoml}")

            # Check sort method
            if sortMethod is not None and not sequences.has_same_sort_method(
                sortMethod
            ):
                raise CliException(
                    f'Sort method passed as argument ({sortMethod.value}) is different from the one defined in your metadata file.\nYou may either change --sort-method argument from command-line, or change "sort_method" in your metadata file.'
                )
        except EOFError:
            pass

    # Create sequence from pictures files
    if sequences is None:
        files = []
        pictures = []

        # Identify pictures files
        for f in path.iterdir():
            if not f.is_file():
                continue
            if f.suffix.lower() not in [".jpg", ".jpeg"]:
                continue
            files.append(f)

        # Read pictures metadata (with loader)
        for f in track(files, description="🔍 Listing pictures..."):
            try:
                meta = reader.readPictureMetadata(Image.open(str(f)))
                pictures.append(Picture(path=str(f), metadata=meta))
            except Exception as e:
                logging.warning(f"Picture {str(f)} has invalid metadata: {str(e)}")
                pictures.append(Picture(path=str(f), status="broken-metadata"))

        # Sort, split and create sequences
        pictures = _sort_files(pictures, sortMethod)
        sequences = _split_pictures_into_sequences(
            pictures, splitParams, title=title, path=str(path), sort_method=sortMethod
        )

    if sequences.is_empty():
        raise CliException(
            "❌ No picture was found in given folder.\nMake sure your folder contains at least one valid JPEG file."
        )

    # Check if at least one picture is valid
    if not sequences.has_valid_pictures():
        raise CliException(
            "❌ All read pictures have invalid metadata.\nPlease check if your pictures are geolocated and have a date defined.\nFor more information: https://gitlab.com/geovisio/api/-/blob/develop/docs/15_Pictures_requirements.md"
        )

    return sequences


def _write_sequences_toml(sequences: ManySequences, tomlFile: Path):
    """Writes TOML sequence metadata file"""

    with open(tomlFile, "w") as f:
        f.write(toml.dumps(sequences.toml()))
        f.close()

    return tomlFile


def _read_sequences_from_toml(tomlFile: Path) -> ManySequences:
    """Read multiple sequences from a single TOML config file"""

    with open(tomlFile, "r") as f:
        tomlFileContent = f.read()
        if len(tomlFileContent) == 0:
            raise EOFError("Config file is empty")
        tomlContent = toml.loads(tomlFileContent)
        f.close()

        # Retro-compatibility with old file formats (single-sequence in file)
        if tomlContent.get("sequence") is not None:
            ms = ManySequences(sequences=[Sequence.from_toml(tomlContent)])
        else:
            ms = ManySequences.from_toml(tomlContent)

        return ms


def _login_if_needed(session: requests.Session, geovisio: Geovisio) -> bool:
    # Check if API needs login
    apiConf = session.get(f"{geovisio.url}/api/configuration")
    if apiConf.json().get("auth", {}).get("enabled", False):
        logged_in = login(session, geovisio)
        if not logged_in:
            return False
    return True


def status(sequence: Sequence) -> Sequence:
    s = requests.get(
        f"{sequence.location}/geovisio_status", timeout=utils.REQUESTS_TIMEOUT
    )
    if s.status_code == 404:
        raise CliException(f"Sequence {sequence.location} not found")
    if s.status_code >= 400:
        raise CliException(
            f"Impossible to get sequence {sequence.location} status: {s.text}"
        )
    r = s.json()

    if len(sequence.pictures) == 0:
        sequence.pictures = [
            Picture(id=p["id"], status=p["status"]) for p in r["items"]
        ]
    else:
        for i, p in enumerate(r["items"]):
            sequence.pictures[i].id = p["id"]
            sequence.pictures[i].status = p["status"]

    return sequence


def info(sequence: Sequence) -> Sequence:
    if not sequence.location:
        raise CliException(f"Sequence has no location set")

    s = requests.get(sequence.location, timeout=utils.REQUESTS_TIMEOUT)
    if s.status_code == 404:
        raise CliException(f"Sequence {sequence.location} not found")
    if s.status_code >= 400:
        raise CliException(
            f"Impossible to get sequence {sequence.location} status: {s.text}"
        )
    r = s.json()
    producer = next(
        (p["name"] for p in r.get("providers", []) if "producer" in p["roles"]), None
    )
    summary = r.get("summaries", {}).get("pers:interior_orientation", [])

    sequence.id = r["id"]
    sequence.title = r["title"]
    sequence.producer = producer
    sequence.interior_orientation = [
        InteriorOrientation(
            make=s.get("make"),
            model=s.get("model"),
            field_of_view=s.get("field_of_view"),
        )
        for s in summary
    ]

    return sequence


def display_sequence_status(sequence: Sequence):
    seq_status = status(sequence)
    seq_info = info(sequence)

    s = f"Sequence [bold]{seq_info.title}[/bold]"
    if seq_info.producer is not None:
        s += f" produced by [bold]{seq_info.producer}[/bold]"
    s += " taken with"
    for i in seq_info.interior_orientation:
        s += f" [bold]{i.make} {i.model}[/bold]"
        if i.field_of_view:
            s += f" ({i.field_of_view}°)"

    print(s)
    table = Table()

    table.add_column("Total")
    table.add_column("Ready", style="green")
    table.add_column("Waiting", style="magenta")
    table.add_column("Preparing", style="magenta")
    table.add_column("Broken", style="red")

    table.add_row(
        f"{len(seq_status.pictures)}",
        f"{seq_status.nb_ready()}",
        f"{seq_status.nb_waiting()}",
        f"{seq_status.nb_preparing()}",
        f"{seq_status.nb_broken()}",
    )
    print(table)


def _print_final_sequence_status(sequence: Sequence):
    nb_broken = sequence.nb_broken()
    nb_ready = sequence.nb_ready()
    if nb_ready == 0:
        print(f"[red]💥 No picture processed")
        return
    s = f"✅ {nb_ready} pictures processed"
    if nb_broken:
        s += f"([red]{nb_broken}[/red] cannot be processed)"
    print(s)


def wait_for_sequence(sequence: Sequence, timeout: Optional[timedelta] = None):
    seq_status = status(sequence)
    if seq_status.all_done():
        _print_final_sequence_status(seq_status)
        return

    print("🔭 Waiting for pictures to be processed by geovisio")
    status_progress = Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        MofNCompleteColumn(),
        "•",
        TextColumn("{task.fields[processing]}"),
    )
    processing_task = status_progress.add_task(
        f"[green]⏳ Processing ...",
        total=1,
        processing="",
    )
    progress_group = Group(
        status_progress,
    )
    waiting_time = timedelta(seconds=2)
    elapsed = timedelta(0)

    with Live(progress_group):
        while True:
            # TODO: display some stats about those errors

            nb_preparing = seq_status.nb_preparing()
            nb_waiting = seq_status.nb_waiting()
            processing = f"{nb_preparing} picture{('s' if nb_preparing != 0 else '')} currently processed"
            status_progress.update(
                processing_task,
                total=len(seq_status.pictures),
                completed=seq_status.nb_ready(),
                processing=processing,
            )

            if nb_waiting + nb_preparing == 0:
                break

            elapsed += waiting_time
            if timeout is not None and elapsed > timeout:
                raise CliException(f"❌ Sequence not ready after {elapsed}, stoping")

            sleep(waiting_time.total_seconds())
            seq_status = status(sequence)

    _print_final_sequence_status(seq_status)
