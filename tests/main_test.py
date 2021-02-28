from search_that_hash import api
from click.testing import CliRunner

from search_that_hash.__main__ import main


def test_it_works():

    hashes = ["5d41402abc4b2a76b9719d911017c592"]

    x = api.return_as_json(hashes)

    assert x is not None

def test_it_works_fast():

    hashes = ["5d41402abc4b2a76b9719d911017c592"]

    x = api.return_as_fast_json(hashes)

    assert x is not None


def test_password_in_md5():

    hashes = ["5f4dcc3b5aa765d61d8327deb882cf99"]

    x = set(
        list(
            api.return_as_json(hashes)[0]["5f4dcc3b5aa765d61d8327deb882cf99"][
                0
            ].values()
        )
    )

    assert "password" in x


def test_password_in_sha512():

    hashes = [
        "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86"
    ]

    x = set(
        list(
            api.return_as_json(hashes)[0][
                "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86"
            ][0].values()
        )
    )

    assert "password" in x


def test_cli():
    runner = CliRunner()
    result = runner.invoke(main, ["-t", "5f4dcc3b5aa765d61d8327deb882cf99"])
    assert result.exit_code == 0
    print(result.output)
    assert "password" in result.output


def test_cli_no_debug():
    runner = CliRunner()
    result = runner.invoke(main, ["-t", "5f4dcc3b5aa765d61d8327deb882cf99"])
    assert result.exit_code == 0
    assert "DEBUG" not in result.output


def test_cli_hash_type():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "-t",
            "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86",
        ],
    )
    assert result.exit_code == 0
    assert "password" in result.output
    assert "SHA-512" in result.output


def test_cli_greppable_no_text():
    runner = CliRunner()
    result = runner.invoke(main, ["-t", "5f4dcc3b5aa765d61d8327deb882cf99", "-g"])
    assert result.exit_code == 0
    assert "DEBUG" not in result.output
    assert "_____" not in result.output
    assert "https://twitter.com/bee_sec_san" not in result.output


def test_cli_verbose():
    runner = CliRunner()
    result = runner.invoke(main, ["-t", "5f4dcc3b5aa765d61d8327deb882cf99", "-vv"])
    assert result.exit_code == 0
    assert "INFO" in result.output


def test_cli_output():
    runner = CliRunner()
    result = runner.invoke(main, ["-t", "5f4dcc3b5aa765d61d8327deb882cf99"])
    assert result.exit_code == 0
    assert "password\nType" in result.output
    assert "MD5\n" in result.output


def test_cli_no_hashes():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Error." in result.output


def test_sth_api_key():
    hashes = ["5d41402abc4b2a76b9719d911017c592"]

    x = api.return_as_fast_json(hashes, "meow")

    assert x is not None
