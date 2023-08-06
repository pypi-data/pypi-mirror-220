import pytest
import os
from geovisio_cli import sequence, exception, model
from .conftest import FIXTURE_DIR, MOCK_API_URL
from pathlib import Path
from geopic_tag_reader import reader
import toml
import requests
from requests_mock import Adapter


def test_SplitParams_is_split_needed():
    sp = sequence.SplitParams()
    assert not sp.is_split_needed()
    sp = sequence.SplitParams(maxDistance=1)
    assert sp.is_split_needed()
    sp = sequence.SplitParams(maxTime=1)
    assert sp.is_split_needed()
    sp = sequence.SplitParams(maxDistance=1, maxTime=1)
    assert sp.is_split_needed()


def test_Picture_toml():
    p = sequence.Picture(
        path="/tmp/1.jpg",
        id="blerg",
        location="http://api.geovisio.fr/blerg",
        status="ready",
    )
    assert p == sequence.Picture.from_toml(p.toml())


def test_Sequence_toml():
    pics = [
        sequence.Picture(
            path="/tmp/bla/1.jpg",
            id="bla1",
            location="http://api.geovisio.fr/bla/1",
            status="ready",
        ),
        sequence.Picture(
            path="/tmp/bla/2.jpg",
            id="bla2",
            location="http://api.geovisio.fr/bla/2",
            status="ready",
        ),
    ]
    s = sequence.Sequence(
        title="Bla",
        path="/tmp/bla",
        id="blabla",
        location="http://api.geovisio.fr/bla",
        producer="BBC (Bla Bla Corporation)",
        pictures=pics,
        sort_method=sequence.SortMethod.time_desc,
    )
    assert s == sequence.Sequence.from_toml(s.toml())


def test_ManySequences_toml():
    pics1 = [
        sequence.Picture(
            path="/tmp/bla/1.jpg",
            id="bla1",
            location="http://api.geovisio.fr/bla/1",
            status="ready",
        ),
        sequence.Picture(
            path="/tmp/bla/2.jpg",
            id="bla2",
            location="http://api.geovisio.fr/bla/2",
            status="ready",
        ),
    ]
    seq1 = sequence.Sequence(
        title="Bla",
        path="/tmp/bla",
        id="blabla",
        location="http://api.geovisio.fr/bla",
        producer="BBC (Bla Bla Corporation)",
        pictures=pics1,
        sort_method=sequence.SortMethod.time_desc,
    )
    pics2 = [
        sequence.Picture(
            path="/tmp/bla2/1.jpg",
            id="bla2-1",
            location="http://api.geovisio.fr/bla2/1",
            status="ready",
        ),
        sequence.Picture(
            path="/tmp/bla2/2.jpg",
            id="bla2-2",
            location="http://api.geovisio.fr/bla2/2",
            status="ready",
        ),
    ]
    seq2 = sequence.Sequence(
        title="Bla2",
        path="/tmp/bla2",
        id="blabla2",
        location="http://api.geovisio.fr/bla2",
        producer="BBC (Bla Bla Corporation)",
        pictures=pics2,
        sort_method=sequence.SortMethod.time_asc,
    )
    ms = sequence.ManySequences(sequences=[seq1, seq2])
    assert ms == sequence.ManySequences.from_toml(ms.toml())


def test_ManySequences_has_same_sort_method():
    seq1 = sequence.Sequence(sort_method=sequence.SortMethod.time_asc)
    ms = sequence.ManySequences(sequences=[seq1])

    assert ms.has_same_sort_method(None)
    assert ms.has_same_sort_method(sequence.SortMethod.time_asc)
    assert not ms.has_same_sort_method(sequence.SortMethod.time_desc)

    ms = sequence.ManySequences(sequences=[])
    assert ms.has_same_sort_method(None)
    assert ms.has_same_sort_method(sequence.SortMethod.time_asc)


def test_ManySequences_is_empty():
    ms = sequence.ManySequences(sequences=[])
    assert ms.is_empty()

    seq1 = sequence.Sequence()
    ms = sequence.ManySequences(sequences=[seq1])
    assert ms.is_empty()

    pic1 = sequence.Picture(path="/tmp/bla/1.jpg")
    seq1 = sequence.Sequence(pictures=[pic1])
    ms = sequence.ManySequences(sequences=[seq1])
    assert not ms.is_empty()


def test_ManySequences_has_valid_pictures():
    ms = sequence.ManySequences(sequences=[])
    assert not ms.has_valid_pictures()

    pic1 = sequence.Picture(path="/tmp/bla/1.jpg", status="broken-metadata")
    seq1 = sequence.Sequence(pictures=[pic1])
    ms = sequence.ManySequences(sequences=[seq1])
    assert not ms.has_valid_pictures()

    pic1 = sequence.Picture(path="/tmp/bla/1.jpg")
    seq1 = sequence.Sequence(pictures=[pic1])
    ms = sequence.ManySequences(sequences=[seq1])
    assert ms.has_valid_pictures()


@pytest.mark.parametrize(
    ("data", "method", "expected"),
    (
        (["1.jpg", "2.jpg", "3.jpg"], "filename-asc", ["1.jpg", "2.jpg", "3.jpg"]),
        (["3.jpg", "1.jpg", "2.jpg"], "filename-asc", ["1.jpg", "2.jpg", "3.jpg"]),
        (["3.jpg", "1.jpg", "2.jpeg"], "filename-asc", ["1.jpg", "2.jpeg", "3.jpg"]),
        (["10.jpg", "5.jpg", "1.jpg"], "filename-asc", ["1.jpg", "5.jpg", "10.jpg"]),
        (["C.jpg", "A.jpg", "B.jpg"], "filename-asc", ["A.jpg", "B.jpg", "C.jpg"]),
        (
            ["CAM1_001.jpg", "CAM2_002.jpg", "CAM1_002.jpg"],
            "filename-asc",
            ["CAM1_001.jpg", "CAM1_002.jpg", "CAM2_002.jpg"],
        ),
        (["1.jpg", "2.jpg", "3.jpg"], "filename-desc", ["3.jpg", "2.jpg", "1.jpg"]),
        (["3.jpg", "1.jpg", "2.jpg"], "filename-desc", ["3.jpg", "2.jpg", "1.jpg"]),
        (["3.jpg", "1.jpg", "2.jpeg"], "filename-desc", ["3.jpg", "2.jpeg", "1.jpg"]),
        (["10.jpg", "5.jpg", "1.jpg"], "filename-desc", ["10.jpg", "5.jpg", "1.jpg"]),
        (["C.jpg", "A.jpg", "B.jpg"], "filename-desc", ["C.jpg", "B.jpg", "A.jpg"]),
        (
            ["CAM1_001.jpg", "CAM2_002.jpg", "CAM1_002.jpg"],
            "filename-desc",
            ["CAM2_002.jpg", "CAM1_002.jpg", "CAM1_001.jpg"],
        ),
    ),
)
def test_sort_files_names(data, method, expected):
    dataPictures = [sequence.Picture(path=p) for p in data]
    resPictures = sequence._sort_files(dataPictures, method)
    assert expected == [pic.path for pic in resPictures]


@pytest.mark.parametrize(
    ("data", "method", "expected"),
    (
        (
            [["1.jpg", 1], ["2.jpg", 2], ["3.jpg", 3]],
            "time-asc",
            ["1.jpg", "2.jpg", "3.jpg"],
        ),
        (
            [["1.jpg", 2], ["2.jpg", 3], ["3.jpg", 1]],
            "time-asc",
            ["3.jpg", "1.jpg", "2.jpg"],
        ),
        (
            [["1.jpg", 1.01], ["2.jpg", 1.02], ["3.jpg", 1.03]],
            "time-asc",
            ["1.jpg", "2.jpg", "3.jpg"],
        ),
        (
            [["1.jpg", 1], ["2.jpg", 2], ["3.jpg", 3]],
            "time-desc",
            ["3.jpg", "2.jpg", "1.jpg"],
        ),
        (
            [["1.jpg", 2], ["2.jpg", 3], ["3.jpg", 1]],
            "time-desc",
            ["2.jpg", "1.jpg", "3.jpg"],
        ),
        (
            [["1.jpg", 1.01], ["2.jpg", 1.02], ["3.jpg", 1.03]],
            "time-desc",
            ["3.jpg", "2.jpg", "1.jpg"],
        ),
    ),
)
def test_sort_files_time(data, method, expected):
    dataPictures = []
    for p in data:
        name, ts = p
        m = reader.GeoPicTags(
            lon=47.7,
            lat=-1.78,
            ts=ts,
            heading=0,
            type="flat",
            make="Panoramax",
            model="180++",
            focal_length=4,
            crop=None,
        )
        dataPictures.append(sequence.Picture(path=name, metadata=m))

    resPictures = sequence._sort_files(dataPictures, method)
    assert expected == [pic.path for pic in resPictures]


@pytest.mark.parametrize(
    ("pics", "maxTime", "maxDist"),
    (
        [  # Single sequence
            [
                {
                    "lat": 48.0000001,
                    "lon": -1.7800001,
                    "ts": 1,
                    "heading": 100,
                    "seq": 0,
                },
                {
                    "lat": 48.0000002,
                    "lon": -1.7800002,
                    "ts": 2,
                    "heading": 100,
                    "seq": 0,
                },
            ],
            None,
            None,
        ],
        [  # Time excedeed
            [
                {
                    "lat": 48.0000001,
                    "lon": -1.7800001,
                    "ts": 1,
                    "heading": 100,
                    "seq": 0,
                },
                {
                    "lat": 48.0000002,
                    "lon": -1.7800002,
                    "ts": 500,
                    "heading": 100,
                    "seq": 1,
                },
            ],
            10,
            None,
        ],
        [  # Time excedeed, reverse
            [
                {
                    "lat": 48.0000001,
                    "lon": -1.7800001,
                    "ts": 500,
                    "heading": 100,
                    "seq": 0,
                },
                {
                    "lat": 48.0000002,
                    "lon": -1.7800002,
                    "ts": 1,
                    "heading": 100,
                    "seq": 1,
                },
            ],
            10,
            None,
        ],
        [  # Distance excedeed
            [
                {
                    "lat": 48.0000001,
                    "lon": -1.7800001,
                    "ts": 1,
                    "heading": 100,
                    "seq": 0,
                },
                {
                    "lat": 48.1000000,
                    "lon": -1.7800002,
                    "ts": 2,
                    "heading": 100,
                    "seq": 1,
                },
            ],
            None,
            1,
        ],
        [  # Many sequences
            [
                {
                    "lat": 48.0000001,
                    "lon": -1.7800001,
                    "ts": 1,
                    "heading": 100,
                    "seq": 0,
                },
                {
                    "lat": 48.0000002,
                    "lon": -1.7800002,
                    "ts": 2,
                    "heading": 100,
                    "seq": 0,
                },
                {
                    "lat": 48.0000003,
                    "lon": -1.7800003,
                    "ts": 3,
                    "heading": 100,
                    "seq": 0,
                },
                # Distance excedeed
                {
                    "lat": 48.1000000,
                    "lon": -1.7800001,
                    "ts": 4,
                    "heading": 100,
                    "seq": 1,
                },
                {
                    "lat": 48.1000001,
                    "lon": -1.7800001,
                    "ts": 5,
                    "heading": 100,
                    "seq": 1,
                },
                {
                    "lat": 48.1000002,
                    "lon": -1.7800001,
                    "ts": 6,
                    "heading": 100,
                    "seq": 1,
                },
                # Time excedeed
                {
                    "lat": 48.1000003,
                    "lon": -1.7800001,
                    "ts": 100,
                    "heading": 100,
                    "seq": 2,
                },
                {
                    "lat": 48.1000004,
                    "lon": -1.7800001,
                    "ts": 101,
                    "heading": 100,
                    "seq": 2,
                },
                {
                    "lat": 48.1000005,
                    "lon": -1.7800001,
                    "ts": 102,
                    "heading": 100,
                    "seq": 2,
                },
            ],
            30,
            100,
        ],
    ),
)
def test_split_pictures_into_sequences(pics, maxTime, maxDist):
    sp = sequence.SplitParams(maxDistance=maxDist, maxTime=maxTime)
    inputPics = []
    expectedPics = [[]]

    for id, pic in enumerate(pics):
        inputPics.append(
            sequence.Picture(
                id=id,
                metadata=reader.GeoPicTags(
                    lat=pic["lat"],
                    lon=pic["lon"],
                    ts=pic["ts"],
                    heading=pic["heading"],
                    type="equirectangular",
                    make=None,
                    model=None,
                    focal_length=None,
                    crop=None,
                ),
            )
        )

        if len(expectedPics) - 1 < pic["seq"]:
            expectedPics.append([])
        expectedPics[pic["seq"]].append(id)

    res = sequence._split_pictures_into_sequences(inputPics, sp)
    print("Got     ", [[p.id for p in r.pictures] for r in res.sequences])
    print("Expected", expectedPics)
    assert len(res.sequences) == len(expectedPics)

    for i, resSubSeq in enumerate(res.sequences):
        print("Checking sequence", i)
        assert len(resSubSeq.pictures) == len(expectedPics[i])
        for j, resSubSeqPic in enumerate(resSubSeq.pictures):
            print(" -> Checking pic", j)
            assert resSubSeqPic.id == expectedPics[i][j]


def test_rw_sequences_toml(tmp_path):
    s = sequence.Sequence(
        title="SEQUENCE",
        id="blab-blabla-blablabla",
        path=str(tmp_path),
        pictures=[
            sequence.Picture(
                id="blou-bloublou-bloubloublou-1", path=str(tmp_path / "1.jpg")
            ),
            sequence.Picture(
                id="blou-bloublou-bloubloublou-2", path=str(tmp_path / "2.jpg")
            ),
            sequence.Picture(
                id="blou-bloublou-bloubloublou-3", path=str(tmp_path / "3.jpg")
            ),
        ],
        sort_method=sequence.SortMethod.time_desc,
    )
    ms = sequence.ManySequences(sequences=[s])
    tomlFile = tmp_path / "_geovisio.toml"
    res = sequence._write_sequences_toml(ms, tomlFile)
    assert res == tomlFile

    res2 = sequence._read_sequences_from_toml(tomlFile)
    assert ms == res2


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
)
def test_read_sequences(datafiles):
    # First read : position is based on picture names
    seqs = sequence._read_sequences(Path(datafiles))
    seqsTomlPath = os.path.join(datafiles, sequence.SEQUENCE_TOML_FILE)
    sequence._write_sequences_toml(seqs, seqsTomlPath)

    assert os.path.isfile(seqsTomlPath)

    # Edit TOML file : position is inverted
    with open(seqsTomlPath, "r+") as seqsToml:
        editedSeqsToml = seqsToml.read()
        editedSeqsToml = (
            editedSeqsToml.replace("position = 1", "position = A")
            .replace("position = 2", "position = 1")
            .replace("position = A", "position = 2")
        )
        seqsToml.seek(0)
        seqsToml.write(editedSeqsToml)
        seqsToml.close()

        # Read sequence 2 : position should match edited TOML
        seqs = sequence._read_sequences(Path(datafiles))
        seq = seqs.sequences[0]
        assert seq.pictures[0].path.endswith("e2.jpg")
        assert seq.pictures[1].path.endswith("e1.jpg")


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
    os.path.join(FIXTURE_DIR, "invalid_pic.jpg"),
)
def test_read_sequences_invalid_file(datafiles):
    # Read sequence from files
    seqs = sequence._read_sequences(Path(datafiles))
    seqsTomlPath = os.path.join(datafiles, sequence.SEQUENCE_TOML_FILE)
    sequence._write_sequences_toml(seqs, seqsTomlPath)

    # Check if invalid_pic is marked as broken
    with open(seqsTomlPath, "r") as seqToml:
        seq2toml = seqToml.read()
        seq2 = sequence.ManySequences.from_toml(toml.loads(seq2toml)).sequences[0]
        assert len(seq2.pictures) == 4
        assert seq2.pictures[0].status == "broken-metadata"
        assert seq2.pictures[1].status is None
        assert seq2.pictures[2].status is None
        assert seq2.pictures[3].status is None


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
)
def test_read_sequences_sort_method_changed_set2unset(datafiles):
    # Write toml with sort method defined
    seq = sequence._read_sequences(
        Path(datafiles), sortMethod=sequence.SortMethod.time_desc
    )
    seqTomlPath = os.path.join(datafiles, sequence.SEQUENCE_TOML_FILE)
    sequence._write_sequences_toml(seq, seqTomlPath)

    # Read sequence from toml without sort method = should reuse read one
    seq = sequence._read_sequences(Path(datafiles))
    assert seq.sequences[0].pictures[0].path.endswith("e2.jpg")
    assert seq.sequences[0].pictures[1].path.endswith("e1.jpg")


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
)
def test_read_sequences_sort_method_changed_different(datafiles):
    # Write toml with sort method defined
    seq = sequence._read_sequences(
        Path(datafiles), sortMethod=sequence.SortMethod.time_desc
    )
    seqTomlPath = os.path.join(datafiles, sequence.SEQUENCE_TOML_FILE)
    sequence._write_sequences_toml(seq, seqTomlPath)

    # Read sequence from toml without sort method = should reuse read one
    with pytest.raises(exception.CliException) as e:
        seq = sequence._read_sequences(
            Path(datafiles), sortMethod=sequence.SortMethod.filename_asc
        )

    assert e.match("Sort method passed as argument")


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "invalid_pic.jpg"),
)
def test_upload_with_no_valid_file(datafiles):
    with pytest.raises(exception.CliException) as e:
        seq = sequence._read_sequences(Path(datafiles))

    assert e.match("All read pictures have invalid metadata")


def mock_api_post_collection_fail(requests_mock):
    requests_mock.post(
        MOCK_API_URL + "/api/collections",
        exc=requests.exceptions.ConnectTimeout,
    )


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
)
def test_upload_collection_create_failure(requests_mock, datafiles):
    mock_api_post_collection_fail(requests_mock)

    with pytest.raises(exception.CliException) as e:
        sequence.upload(
            path=datafiles,
            geovisio=model.Geovisio(url=MOCK_API_URL),
            title="Test",
            alreadyBlurred=True,
        )

    assert str(e.value).startswith("Error while connecting to the API")


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
)
def test_upload_with_invalid_file(requests_mock, datafiles):
    # Put apart third picture
    os.rename(datafiles + "/e2.jpg", datafiles + "/e2.bak")
    os.rename(datafiles + "/e3.jpg", datafiles + "/e3.bak")

    # Mock collection creation
    gvsMock = model.Geovisio(url=MOCK_API_URL)
    seqId = "123456789"
    picId1 = "123"
    picId2 = "456"
    picId3 = "789"
    requests_mock.get(f"{MOCK_API_URL}/api", json={})
    requests_mock.get(f"{MOCK_API_URL}/api/configuration", json={})
    requests_mock.get(
        f"{MOCK_API_URL}/api/collections/{seqId}",
        json={"id": seqId, "title": "whatever"},
    )
    requests_mock.post(
        f"{MOCK_API_URL}/api/collections",
        json={"id": seqId},
        headers={"Location": f"{MOCK_API_URL}/api/collections/{seqId}"},
    )
    requests_mock.post(
        f"{MOCK_API_URL}/api/collections/{seqId}/items",
        json={"type": "Feature", "id": picId1},
        headers={"Location": f"{MOCK_API_URL}/api/collections/{seqId}/items/{picId1}"},
    )
    uploadReports = sequence.upload(path=Path(datafiles), geovisio=gvsMock, title=None)

    # Check previous pictures are OK
    assert len(uploadReports) == 1
    uploadReport = uploadReports[0]
    assert len(uploadReport.uploaded_pictures) == 1
    assert len(uploadReport.errors) == 0

    # Make other pictures available
    os.rename(datafiles + "/e2.bak", datafiles + "/e2.jpg")
    os.rename(datafiles + "/e3.bak", datafiles + "/e3.jpg")
    with open(datafiles + "/_geovisio.toml") as f:
        seq = toml.loads(f.read())
        seq["1"]["pictures"]["e2.jpg"] = {
            "path": str(datafiles) + "/e2.jpg",
            "position": 2,
        }
        seq["1"]["pictures"]["e3.jpg"] = {
            "path": str(datafiles) + "/e3.jpg",
            "position": 3,
        }
        f.close()

    with open(datafiles + "/_geovisio.toml", "w") as f2:
        f2.write(toml.dumps(seq))
        f2.close()

        # Mock item call to fail
        requests_mock.post(
            f"{MOCK_API_URL}/api/collections/{seqId}/items",
            [
                {
                    "json": {"type": "Feature", "id": picId2},
                    "status_code": 202,
                    "headers": {
                        "Location": f"{MOCK_API_URL}/api/collections/{seqId}/items/{picId2}"
                    },
                },
                {"status_code": 500},
            ],
        )
        uploadReports2 = sequence.upload(
            path=Path(datafiles), geovisio=gvsMock, title=None
        )

        assert len(uploadReports2) == 1
        uploadReport2 = uploadReports2[0]
        assert len(uploadReport2.uploaded_pictures) == 1
        assert len(uploadReport2.errors) == 1
