import os
import pathlib
import platform
import re
import subprocess
from subprocess import CompletedProcess

import pytest
from helper import (
    check_skip_slow,
    check_skip_slow_msg,
    check_skip_xpdf_exe_dir,
    check_skip_xpdf_exe_dir_msg,
)
from importlib_resources import as_file, files

from leaf_focus import utils
from leaf_focus.pdf.model import XpdfImageArgs
from leaf_focus.pdf.xpdf import XpdfProgram


@pytest.mark.skipif(check_skip_xpdf_exe_dir(), reason=check_skip_xpdf_exe_dir_msg)
@pytest.mark.skipif(check_skip_slow(), reason=check_skip_slow_msg)
def test_xpdf_image_with_exe(capsys, caplog, resource_example1, tmp_path):
    package = resource_example1.package
    package_path = files(package)
    pg = 22
    pdf = resource_example1.pdf_name
    with as_file(package_path.joinpath(pdf)) as p:
        pdf_path = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    exe_dir = pathlib.Path(os.getenv("TEST_XPDF_EXE_DIR"))

    prog = XpdfProgram(exe_dir)
    args = XpdfImageArgs(first_page=pg, last_page=pg)
    result = prog.image(pdf_path, output_path, args)

    assert result.output_dir
    assert len(result.output_files) == 1
    assert result.output_files[0].name.endswith(f"-{pg:06}.png")

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""

    assert caplog.record_tuples == []


@pytest.mark.skipif(check_skip_xpdf_exe_dir(), reason=check_skip_xpdf_exe_dir_msg)
@pytest.mark.skipif(check_skip_slow(), reason=check_skip_slow_msg)
def test_xpdf_image_valid_pgs_with_exe(capsys, caplog, resource_example1, tmp_path):
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
    args = XpdfImageArgs(first_page=first_page, last_page=last_page)
    result = prog.image(pdf_path, output_path, args)

    assert result.output_dir
    assert len(result.output_files) == count_pages

    output_contents = set()
    for index, output_file in enumerate(result.output_files):
        assert output_file.name.endswith(f"-{index + first_page:06}.png")

        output_content = output_file.read_bytes()
        assert output_content not in output_contents
        output_contents.add(output_content)

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""

    assert caplog.record_tuples == []


def test_xpdf_image_without_exe(
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
    exe_xpdf_png_file = exe_dir / (
        "pdftopng.exe" if platform.system() == "Windows" else "pdftopng"
    )
    exe_xpdf_png_file.touch()
    output_file = resource_example1.image_stem

    def mock_subprocess_run(cmd, capture_output, check, timeout, text):
        cmd_args = [
            str(exe_xpdf_png_file),
            "-f",
            str(pg),
            "-l",
            str(pg),
            "-gray",
            str(pdf_path),
            str(output_path / output_file),
        ]
        if cmd == cmd_args:
            return CompletedProcess(
                args=cmd_args,
                returncode=0,
                stdout="",
                stderr="Config Error: No display font for 'Symbol'\nConfig Error: No display font for 'ZapfDingbats'\n",
            )
        msg = f"Unknown cmd '{cmd}'"
        raise ValueError(msg)

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)

    prog = XpdfProgram(exe_dir)
    args = XpdfImageArgs(first_page=pg, last_page=pg, use_grayscale=True)
    result = prog.image(pdf_path, output_path, args)

    assert result.output_dir == output_path / output_file

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""

    assert caplog.record_tuples == [
        ("leaf_focus.pdf.xpdf", 30, "No page images found."),
    ]


@pytest.mark.skipif(check_skip_xpdf_exe_dir(), reason=check_skip_xpdf_exe_dir_msg)
@pytest.mark.skipif(check_skip_slow(), reason=check_skip_slow_msg)
def test_xpdf_image_invalid_pgs_with_exe(capsys, caplog, resource_example1, tmp_path):
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
    args = XpdfImageArgs(first_page=first_page, last_page=last_page)
    with pytest.raises(
        utils.LeafFocusError,
        match=re.escape("First page (6) must be less than or equal to last page (5)."),
    ):
        prog.image(pdf_path, output_path, args)

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""

    assert caplog.record_tuples == []
