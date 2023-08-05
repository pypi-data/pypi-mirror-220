# -*- coding: utf-8 -*-
# Copyright (C) 2023 Mandiant, Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: [package root]/LICENSE.txt
# Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
import io
import zlib
from pathlib import Path

from fixtures import get_data_path_by_name

import capa.features.extractors.elf


def test_elf_sh_notes():
    # guess: osabi: None
    # guess: ph notes: None
    # guess: sh notes: OS.LINUX
    # guess: linker: None
    # guess: ABI versions needed: None
    # guess: symtab: None
    # guess: needed dependencies: None
    path = get_data_path_by_name("2f7f5f")
    with Path(path).open("rb") as f:
        assert capa.features.extractors.elf.detect_elf_os(f) == "linux"


def test_elf_pt_notes():
    # guess: osabi: None
    # guess: ph notes: None
    # guess: sh notes: OS.LINUX
    # guess: linker: OS.LINUX
    # guess: ABI versions needed: OS.LINUX
    # guess: symtab: None
    # guess: needed dependencies: None
    path = get_data_path_by_name("7351f.elf")
    with Path(path).open("rb") as f:
        assert capa.features.extractors.elf.detect_elf_os(f) == "linux"


def test_elf_so_needed():
    # guess: osabi: None
    # guess: ph notes: None
    # guess: sh notes: OS.HURD
    # guess: linker: None
    # guess: ABI versions needed: OS.HURD
    # guess: symtab: None
    # guess: needed dependencies: OS.HURD
    path = get_data_path_by_name("b5f052")
    with Path(path).open("rb") as f:
        assert capa.features.extractors.elf.detect_elf_os(f) == "hurd"


def test_elf_abi_version_hurd():
    # guess: osabi: None
    # guess: ph notes: None
    # guess: sh notes: OS.HURD
    # guess: linker: None
    # guess: ABI versions needed: OS.HURD
    # guess: symtab: None
    # guess: needed dependencies: None
    path = get_data_path_by_name("bf7a9c")
    with Path(path).open("rb") as f:
        assert capa.features.extractors.elf.detect_elf_os(f) == "hurd"


def test_elf_symbol_table():
    # guess: osabi: None
    # guess: ph notes: None
    # guess: sh notes: None
    # guess: linker: None
    # guess: ABI versions needed: None
    # guess: symtab: OS.LINUX
    # guess: needed dependencies: None
    path = get_data_path_by_name("2bf18d")
    with Path(path).open("rb") as f:
        assert capa.features.extractors.elf.detect_elf_os(f) == "linux"


def test_elf_parse_capa_pyinstaller_header():
    # error after misidentified large pydata section with address 0; fixed in #1454
    # compressed ELF header of capa-v5.1.0-linux
    #  SHA256 e16974994914466647e24cdcfb6a6f8710297a4def21525e53f73c72c4b52fcf
    elf_header = zlib.decompress(
        b"".join(
            [
                b"\x78\x9C\x8D\x56\x4F\x88\x1C\xD5\x13\xAE\x1D\x35\x0A\x7A\x58\x65",
                b"\xD1\xA0\x9B\xB0\x82\x11\x14\x67\x63\xD6\xCD\x26\xF1\xF0\x63\x49",
                b"\xDC\xC4\xC8\x26\x98\x7F\x07\x89\xA4\xED\xE9\x7E\x6F\xA6\x99\xD7",
                b"\xAF\xDB\xEE\x37\xBB\x13\x3D\xB8\x78\x8A\x28\x28\x1E\xBC\x09\x7B",
                b"\xF0\xCF\x82\xA0\x41\x10\x23\xA8\x07\x89\x17\x41\x85\x88\x07\x2F",
                b"\xE2\x25\xB0\x17\x51\x7E\x07\xD9\x5B\x52\xF5\xFE\xCC\x36\x71\x0A",
                b"\x6C\x98\xA9\xF7\xBE\xF9\xEA\xAB\xAF\xEA\x35\x3D\xFD\xDA\xD2\xF2",
                b"\xD1\xD6\xC4\x04\x84\xAB\x05\xFF\x03\xDA\x2D\xED\x59\xB4\x7B\xF7",
                b"\x8D\xF1\xEF\x57\x5B\x81\xB3\x08\x07\xE1\x6E\xFC\x9E\x86\x87\x60",
                b"\x07\xEE\x6F\x6F\xF2\xFC\x2A\xC4\x9E\xCF\x0A\xF1\x2E\xCF\xBB\xCD",
                b"\xE7\x6D\x78\x7C\xA3\xE5\xF8\x21\x4E\x7B\x5E\x88\xC1\x21\x45\xCA",
                b"\xDB\xBE\xB6\x2B\xD3\x75\xE9\x01\xB7\x0B\x11\x26\xB7\xF3\xEE\xA0",
                b"\xC5\x8C\xC7\x67\x7C\x9E\x8F\xF9\x8B\x6E\x1B\x62\x33\xCF\xD6\x5B",
                b"\xF3\xF8\x9A\xCF\xF3\xF1\xCA\x7E\xB7\x0D\xB1\x99\x47\xB3\xD9\xFC",
                b"\xC6\xED\x37\x7F\x74\xFC\x10\xAF\xF8\x26\x36\x86\xBE\x33\x9F\x47",
                b"\xE3\xA0\xBC\x2D\x9F\xB7\xE5\xF9\x21\x5A\x42\x23\x86\x79\x92\x1C",
                b"\x7D\xAE\x7A\xFC\xAA\x9F\x63\x88\xCF\x78\x5E\x88\x61\x86\xCF\x5F",
                b"\x37\x29\xAD\x37\xD7\xBD\xCF\x75\xEF\xD3\xC7\x27\xE8\xA0\x1A\x31",
                b"\xE4\x9D\xC2\x3C\xF2\xF9\x5F\x2F\xDF\x1E\x9C\x0E\xF5\x98\xB9\xEC",
                b"\xF4\xFE\x43\x0C\xE7\xBE\x57\x65\x9D\x85\xF9\xBD\x2A\x6D\xAB\x4C",
                b"\x0F\x86\xED\xE1\xC1\x85\xF6\xC2\xFC\x6C\x5D\xCC\xCE\x59\x4F\x53",
                b"\xFE\x9E\x3A\x76\xF2\x1C\x9C\xFD\xE5\xD9\x33\xE2\xCC\x4B\x17\x76",
                b"\x7F\xFD\xD1\xD4\xE6\xE5\xA9\xE5\xF3\x4F\xFF\x7C\x82\x38\xE4\x81",
                b"\xF4\x88\xD3\x9C\x35\xDD\x12\x94\x7B\xAA\x71\x6E\x30\x31\x03\x6B",
                b"\x13\x93\x2D\xC2\x4E\x7B\x0F\x8F\xED\x7A\x6B\x5A\x9E\x8B\x27\x0F",
                b"\xFD\xFF\xCD\x70\x5B\xFE\xEB\xD2\x28\x7A\xDF\x18\xFC\x1A\x0A\x8F",
                b"\xC3\xFF\x60\xF0\x0B\xF8\x19\x87\x7F\xC7\xE8\x3F\xC7\xE0\x27\x18",
                b"\x9D\x1B\x0C\x7E\x9D\xC1\xE9\xB8\xC6\xE1\x6F\x33\xF8\x97\x4C\x5F",
                b"\x6D\x86\xBF\x83\xE1\x7F\xC0\xF4\xF5\x08\x83\xFF\xC9\xE8\xFF\xC5",
                b"\xE8\x4B\x06\x7F\x90\xC1\xDF\x60\xF0\x1F\x18\xFC\x13\xC6\xE7\x49",
                b"\x86\x7F\x88\xC1\xFF\x61\xFA\xA2\xA7\xF2\x38\xFC\x08\x83\x7F\xC5",
                b"\xE0\x47\x99\xBA\x37\x18\xFC\x4E\x46\xE7\x57\xC6\xE7\xF7\x0C\xFE",
                b"\x2E\xA3\x73\x96\xA9\xFB\x05\xA3\x33\xC7\xF0\x5F\x67\xF4\x7F\x67",
                b"\x74\x1E\x67\xF8\x6D\x46\x9F\x9E\x17\xE1\x2F\xA5\x79\x9D\x67\xF8",
                b"\x9F\x72\x3E\x19\x7C\x91\xC1\x0F\x33\xFE\x1F\x66\xF8\x2F\x33\xFC",
                b"\xFB\x99\x7E\x25\x83\xBF\xCF\xE8\xEC\x66\xF0\x75\xC6\xCF\x25\x86",
                b"\xFF\x2D\xC3\x7F\x87\xC1\xE9\x99\x3E\x0E\xBF\x87\xE1\xBF\xC0\xF4",
                b"\x45\x7F\xEF\xE3\xF0\x0F\x19\xFC\x3D\x06\xA7\xD7\x80\x71\xF8\x01",
                b"\xA6\x6E\xC6\xF0\x3F\x67\xF8\x9F\x31\xFC\x9F\x18\xFC\x51\x66\x0E",
                b"\x29\x83\x6F\x31\xF8\xC7\x0C\xBE\x8B\xF1\x99\x73\xCF\x4F\x86\xBF",
                b"\x93\xF1\x9F\x32\xF8\x1E\xEE\x79\x88\x75\xEF\x45\xB5\xF5\x6B\xEE",
                b"\x7D\x22\xBC\x1F\x4D\x79\x7C\xE3\x16\xFC\x37\x8F\x5F\xBE\x05\x87",
                b"\x28\xEA\xE6\x85\x8E\x6A\x13\x57\x26\x8A\x20\x55\x89\x2A\x6A\x81",
                b"\xB1\xBE\x98\xE3\x77\x51\x0A\x8D\x41\x54\x55\x51\x41\xA6\xA5\x8A",
                b"\x8D\x08\xF1\xB8\xCE\x4C\x14\x36\x4B\x3A\x45\x2D\xE4\xE9\x22\x52",
                b"\x45\x12\x9B\xAC\xD0\x50\xC5\x19\x6A\xC9\xA2\xEA\xC3\x6A\x9C\x99",
                b"\x32\x23\xCE\xB0\xEC\x46\x9D\xB8\x16\x3A\xCE\x05\xE4\xFD\xD4\x88",
                b"\xBC\x04\x29\xD5\xA0\xEE\x41\x6D\xAA\xA4\xBC\x08\x32\xE9\xE5\x45",
                b"\x0A\x95\x88\xD3\x34\xAB\xA0\x16\x86\x24\x15\x49\x91\x9F\xD5\xA4",
                b"\xD6\x44\x43\xB6\x4E\x30\x39\x42\xFB\x55\x3A\x28\xA1\x74\x3E\x6D",
                b"\x0B\x36\x31\xEB\xEA\x58\x39\x1E\xF2\xF3\x4E\x6D\x0A\x4C\xC6\x04",
                b"\x35\xC4\x8E\x0D\x0C\x34\xBE\x66\xF5\xC9\x05\xB2\xB1\x9C\xC2\x3A",
                b"\x48\x4F\x33\x0D\x5D\x61\xFD\xF6\x33\x65\x05\x4C\xD1\x07\x29\x0A",
                b"\x09\xE8\xC3\x91\x2A\x85\x56\xCA\x2A\x31\x0A\x30\xDB\x76\x53\xE5",
                b"\xA4\x93\x8B\x9C\x5C\x25\x4A\xC4\x15\x1A\xC2\x22\xD8\x80\xD0\x2B",
                b"\x58\x56\x96\x55\xA6\x8D\x8C\x92\x5E\x9F\xCA\x14\x03\x63\xD9\xB6",
                b"\x65\x3B\xF7\x28\x5A\xA9\x75\x83\x94\x8F\xAA\xE1\x48\xAD\xC3\x32",
                b"\x36\x3D\x90\x46\x20\x0E\x5A\x45\x2A\xD6\x5D\x3C\x82\x02\x68\x32",
                b"\x54\x1D\x7D\x53\x2D\x54\xA7\xDA\x38\x9A\xA6\x1C\x4D\xD4\x76\x2C",
                b"\x86\x22\x59\x29\xDD\x64\x50\x38\x8A\x82\xB4\xA5\xC9\x0C\x7B\x2B",
                b"\x40\xAE\x56\x19\x1E\xB7\xA4\x2C\xA4\x38\xA7\x96\x80\x9D\x10\xE8",
                b"\xFB\xA8\x92\x1E\x55\x5A\x69\x76\x67\xCF\x64\x9B\xEE\xC6\xED\xC0",
                b"\xD8\xB8\x3C\x61\x3A\x03\x69\xD3\x71\x5A\x18\xDC\xE1\xE1\xD9\x64",
                b"\x9D\xC4\xDF\x90\x79\x8C\x27\x21\xDD\x0F\xB5\x29\xED\xA0\x6A\x21",
                b"\xFA\x05\x84\xB6\xC8\x9D\x00\x4C\x49\x95\x7B\x4B\xC6\xE5\x2B\xB4",
                b"\xDA\x47\xAB\xD2\xF4\xC8\x27\xED\x9F\xA4\x7D\x42\xAB\x05\x38\xB6",
                b"\x7C\xFC\xF0\x91\x68\x6E\x76\x6E\x76\xFF\x68\x7D\x60\xB4\xDA\x37",
                b"\x3F\x5A\x3E\x35\x5A\x35\x30\x5C\xC3\x4D\x95\x6E\xA4\x60",
            ]
        )
    )
    assert capa.features.extractors.elf.detect_elf_os(io.BytesIO(elf_header)) == "linux"
