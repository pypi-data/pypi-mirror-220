import os
import pathlib
import platform
import re
import subprocess
from subprocess import CompletedProcess

import pytest
from helper import check_skip_xpdf_exe_dir, check_skip_xpdf_exe_dir_msg
from importlib_resources import as_file, files

from leaf_focus import utils
from leaf_focus.pdf.model import XpdfTextArgs
from leaf_focus.pdf.xpdf import XpdfProgram


@pytest.mark.skipif(check_skip_xpdf_exe_dir(), reason=check_skip_xpdf_exe_dir_msg)
def test_xpdf_text_with_exe(capsys, caplog, resource_example1, tmp_path):
    package = resource_example1.package
    package_path = files(package)

    pdf = resource_example1.pdf_name
    with as_file(package_path.joinpath(pdf)) as p:
        pdf_path = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    exe_dir = pathlib.Path(os.getenv("TEST_XPDF_EXE_DIR"))

    prog = XpdfProgram(exe_dir)
    args = XpdfTextArgs(
        line_end_type="dos",
        use_verbose=True,
        use_simple2_layout=True,
    )
    result = prog.text(pdf_path, output_path, args)
    content = result.output_path.read_text(encoding="windows-1252")
    assert content.startswith("Release 450 Driver for Windows, Version")

    content_pages = [i.strip() for i in content.split("\f") if i]
    assert len(content_pages) == 42

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""

    assert caplog.record_tuples == []


@pytest.mark.skipif(check_skip_xpdf_exe_dir(), reason=check_skip_xpdf_exe_dir_msg)
def test_xpdf_text_valid_pgs_with_exe(capsys, caplog, resource_example1, tmp_path):
    package = resource_example1.package
    package_path = files(package)
    first_page = 3
    last_page = 25
    count_pages = 23
    pdf = resource_example1.pdf_name
    with as_file(package_path.joinpath(pdf)) as p:
        pdf_path = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    exe_dir = pathlib.Path(os.getenv("TEST_XPDF_EXE_DIR"))

    prog = XpdfProgram(exe_dir)
    args = XpdfTextArgs(
        line_end_type="dos",
        use_verbose=True,
        use_simple2_layout=True,
        first_page=first_page,
        last_page=last_page,
    )
    result = prog.text(pdf_path, output_path, args)

    content = result.output_path.read_text(encoding="windows-1252")
    content_pages = [i.strip() for i in content.split("\f") if i]
    assert len(content_pages) == count_pages

    output_contents = set()
    for content_page in content_pages:
        assert content_page not in output_contents
        output_contents.add(content_page)

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""

    assert caplog.record_tuples == []


def test_xpdf_text_without_exe(
    capsys,
    caplog,
    resource_example1,
    tmp_path,
    monkeypatch,
):
    package = resource_example1.package
    package_path = files(package)
    pg = 22
    pdf = resource_example1.pdf_name
    with as_file(package_path.joinpath(pdf)) as p:
        pdf_path = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    exe_dir = tmp_path / "exe-dir"
    exe_dir.mkdir(exist_ok=True, parents=True)
    exe_xpdf_text_file = exe_dir / (
        "pdftotext.exe" if platform.system() == "Windows" else "pdftotext"
    )
    exe_xpdf_text_file.touch()
    output_file = (
        f"{resource_example1.prefix_norm}-output-f-22-l-22-verbose-simple2-eol-dos.txt"
    )

    def mock_subprocess_run(cmd, capture_output, check, timeout, text):
        cmd_args = [
            str(exe_xpdf_text_file),
            "-f",
            str(pg),
            "-l",
            str(pg),
            "-verbose",
            "-simple2",
            "-eol",
            "dos",
            str(pdf_path),
            str(output_path / output_file),
        ]
        if cmd == cmd_args:
            return CompletedProcess(
                args=cmd_args,
                returncode=0,
                stdout="[processing page 22]\n",
                stderr="",
            )
        msg = f"Unknown cmd '{cmd}'"
        raise ValueError(msg)

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)

    prog = XpdfProgram(exe_dir)
    args = XpdfTextArgs(
        line_end_type="dos",
        use_verbose=True,
        use_simple2_layout=True,
        first_page=22,
        last_page=22,
    )
    result = prog.text(pdf_path, output_path, args)

    assert result.output_path.name == output_file

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""

    assert caplog.record_tuples == []


@pytest.mark.skipif(check_skip_xpdf_exe_dir(), reason=check_skip_xpdf_exe_dir_msg)
def test_xpdf_text_invalid_pgs_with_exe(capsys, caplog, resource_example1, tmp_path):
    package = resource_example1.package
    package_path = files(package)
    first_page = 6
    last_page = 5
    pdf = resource_example1.pdf_name
    with as_file(package_path.joinpath(pdf)) as p:
        pdf_path = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    exe_dir = pathlib.Path(os.getenv("TEST_XPDF_EXE_DIR"))

    prog = XpdfProgram(exe_dir)
    args = XpdfTextArgs(
        line_end_type="dos",
        use_verbose=True,
        use_simple2_layout=True,
        first_page=first_page,
        last_page=last_page,
    )
    with pytest.raises(
        utils.LeafFocusError,
        match=re.escape("First page (6) must be less than or equal to last page (5)."),
    ):
        prog.text(pdf_path, output_path, args)

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""

    assert caplog.record_tuples == []
