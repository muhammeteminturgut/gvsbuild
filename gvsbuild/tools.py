#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.

"""Default tools used to build the various projects."""

import os
import shutil
import subprocess
import sys

from .utils.base_expanders import extract_exec
from .utils.base_project import Project
from .utils.base_tool import Tool, tool_add
from .utils.simple_ui import log


@tool_add
class ToolCargo(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "cargo",
            archive_url="https://win.rustup.rs/x86_64",
            archive_file_name="rustup-init.exe",
            exe_name="cargo.exe",
        )

    def load_defaults(self):
        Tool.load_defaults(self)
        self.tool_path = os.path.join(self.build_dir, "bin")
        self.full_exe = os.path.join(self.tool_path, "cargo.exe")

        self.add_extra_env("RUSTUP_HOME", self.build_dir)
        self.add_extra_env("CARGO_HOME", self.build_dir)

    def unpack(self):
        env = os.environ.copy()
        env["RUSTUP_HOME"] = self.build_dir
        env["CARGO_HOME"] = self.build_dir

        rustup = os.path.join(self.build_dir, "bin", "rustup.exe")

        subprocess.check_call(
            f"{self.archive_file} --no-modify-path -y", shell=True, env=env
        )

        # add supported targets
        subprocess.check_call(
            f"{rustup} target add x86_64-pc-windows-msvc", shell=True, env=env
        )

        subprocess.check_call(
            f"{rustup} target add i686-pc-windows-msvc", shell=True, env=env
        )

        # switch to the right target
        subprocess.check_call(
            f'{rustup} default stable-{"i686" if self.opts.x86 else "x86_64"}-pc-windows-msvc',
            env=env,
        )

        self.mark_deps = True


@tool_add
class ToolCmake(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "cmake",
            archive_url="https://github.com/Kitware/CMake/releases/download/v3.23.1/cmake-3.23.1-windows-x86_64.zip",
            hash="9b509cc4eb7191dc128cfa3f2170036f9cbc7d9d5f93ff7fafc5b2d77b3b40dc",
            dir_part="cmake-3.23.1-windows-x86_64",
        )

    def load_defaults(self):
        Tool.load_defaults(self)
        self.tool_path = os.path.join(self.build_dir, "bin")
        self.full_exe = os.path.join(self.tool_path, "cmake.exe")

    def unpack(self):
        self.mark_deps = extract_exec(
            self.archive_file,
            self.opts.tools_root_dir,
            dir_part=self.dir_part,
            check_file=self.full_exe,
            check_mark=True,
        )


@tool_add
class ToolMeson(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "meson",
            archive_url="https://github.com/mesonbuild/meson/archive/refs/tags/0.62.1.tar.gz",
            archive_file_name="meson-0.62.1.tar.gz",
            hash="9fb52e66dbc613479a5f70e46cc2e8faf5aa65e09313f2c71fa63b8afd018107",
            dependencies=[
                "python",
            ],
            dir_part="meson-0.62.1",
            exe_name="meson.py",
        )

    def unpack(self):
        self.mark_deps = extract_exec(
            self.archive_file,
            self.builder.opts.tools_root_dir,
            dir_part=self.dir_part,
            check_file=self.full_exe,
            check_mark=True,
        )


@tool_add
class ToolMsys2(Tool):
    def __init__(self):
        Tool.__init__(self, "msys2")

    def load_defaults(self):
        Tool.load_defaults(self)
        self.tool_path = os.path.join(self.opts.msys_dir, "usr", "bin")

    def unpack(self):
        self.tool_mark()

    def get_path(self):
        # We always put msys at the end of path
        return None, self.tool_path


@tool_add
class ToolNasm(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "nasm",
            archive_url="https://github.com/wingtk/gvsbuild/releases/download/nasm-2.15.05/nasm-2.15.05-win64.zip",
            hash="f5c93c146f52b4f1664fa3ce6579f961a910e869ab0dae431bd871bdd2584ef2",
            dir_part="nasm-2.15.05",
            exe_name="nasm.exe",
        )

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        self.mark_deps = extract_exec(
            self.archive_file,
            self.builder.opts.tools_root_dir,
            dir_part=self.dir_part,
            check_file=self.full_exe,
            force_dest=self.full_exe,
            check_mark=True,
        )


@tool_add
class ToolNinja(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "ninja",
            archive_url="https://github.com/ninja-build/ninja/releases/download/v1.10.2/ninja-win.zip",
            archive_file_name="ninja-win-1.10.2.zip",
            hash="bbde850d247d2737c5764c927d1071cbb1f1957dcabda4a130fa8547c12c695f",
            dir_part="ninja-1.10.2",
            exe_name="ninja.exe",
        )

    def unpack(self):
        self.mark_deps = extract_exec(
            self.archive_file, self.build_dir, check_file=self.full_exe, check_mark=True
        )


@tool_add
class ToolNuget(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "nuget",
            archive_url="https://dist.nuget.org/win-x86-commandline/v6.1.0/nuget.exe",
            archive_file_name="nuget-6.1.0.exe",
            hash="432d322b16ffab3fed5d24ab7ea30ae10c555a00339a9bf53060aa4b2aee7925",
            dir_part="nuget-6.1.0",
            exe_name="nuget.exe",
        )

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        self.mark_deps = extract_exec(
            self.archive_file,
            self.build_dir,
            check_file=self.full_exe,
            force_dest=self.full_exe,
            check_mark=True,
        )


@tool_add
class ToolPerl(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "perl",
            archive_url="https://github.com/wingtk/gtk-win32/releases/download/Perl-5.20/perl-5.20.0-x64.tar.xz",
            hash="05e01cf30bb47d3938db6169299ed49271f91c1615aeee5649174f48ff418c55",
            dir_part="perl-5.20.0",
        )

    def load_defaults(self):
        Tool.load_defaults(self)
        # Set the builder object to point to the path to use, when we need to pass directly the executable to *make
        self.base_dir = os.path.join(self.build_dir, "x64")
        # full path, added to the environment when needed
        self.tool_path = os.path.join(self.base_dir, "bin")
        self.full_exe = os.path.join(self.tool_path, "perl.exe")

    def unpack(self):
        self.mark_deps = extract_exec(
            self.archive_file, self.build_dir, check_file=self.full_exe, check_mark=True
        )

    def get_base_dir(self):
        return self.base_dir


@tool_add
class ToolPython(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "python",
            dependencies=[
                "nuget",
            ],
        )

    def setup(self, install):
        """Using nuget install, locally, the specified version of python."""
        version = self.opts.python_ver
        # Get the last version we ask
        if version == "3.7":
            version = "3.7.13"
        elif version == "3.8":
            version = "3.8.13"
        elif version == "3.9":
            version = "3.9.12"
        elif version == "3.10":
            version = "3.10.4"

        name = "pythonx86" if self.opts.x86 else "python"
        t_id = f"{name}.{version}"
        dest_dir = os.path.join(self.opts.tools_root_dir, t_id)
        # directory to use for the .exe
        self.tool_path = os.path.join(dest_dir, "tools")
        self.full_exe = os.path.join(self.tool_path, "python.exe")

        if install:
            # see if it's already ok
            rd_file = ""
            try:
                with open(os.path.join(dest_dir, ".wingtk-extracted-file")) as fi:
                    rd_file = fi.readline().strip()
            except OSError:
                pass

            if rd_file == t_id:
                # Ok, exit
                log.log(f"Skipping python setup on '{dest_dir}'")
                # We don't rebuild the projects that depend on this
                return False

            # nuget
            nuget = Project.get_tool_executable("nuget")
            # Install python
            cmd = f"{nuget} install {name} -Version {version} -OutputDirectory {self.opts.tools_root_dir}"

            subprocess.check_call(cmd, shell=True)
            py = os.path.join(self.tool_path, "python.exe")

            # Update pip
            cmd = f"{py} -m pip install --upgrade pip setuptools wheel build --no-warn-script-location"
            subprocess.check_call(cmd, shell=True)

            python3 = os.path.join(self.tool_path, "python3.exe")
            if not os.path.exists(python3):
                # We create a python3.exe file so meson find our python and not some other
                # lying around (e.g. one from the Visual Studio installation ...)
                log.log(f"Create python3 copy on '{dest_dir}'")
                shutil.copy(self.full_exe, python3)

            # Mark that we have done all
            with open(os.path.join(dest_dir, ".wingtk-extracted-file"), "wt") as fo:
                fo.write(f"{t_id}\n")

        return True

    def load_defaults(self):
        Tool.load_defaults(self)
        self.setup(False)

    def unpack(self):
        if self.opts._load_python:
            # Get python version
            self.mark_deps = self.setup(True)
        else:
            self.tool_path = self.opts.python_dir or os.path.dirname(sys.executable)
            self.full_exe = os.path.join(self.tool_path, "python.exe")
            self.mark_deps = False


@tool_add
class ToolYasm(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "yasm",
            archive_url="http://www.tortall.net/projects/yasm/releases/yasm-1.3.0-win64.exe",
            hash="d160b1d97266f3f28a71b4420a0ad2cd088a7977c2dd3b25af155652d8d8d91f",
            dir_part="yasm-1.3.0",
            exe_name="yasm.exe",
        )

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        self.mark_deps = extract_exec(
            self.archive_file,
            self.build_dir,
            check_file=self.full_exe,
            force_dest=self.full_exe,
            check_mark=True,
        )


@tool_add
class ToolGo(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "go",
            archive_url="https://go.dev/dl/go1.18.1.windows-amd64.zip",
            hash="c30bc3f1f7314a953fe208bd9cd5e24bd9403392a6c556ced3677f9f70f71fe1",
            dir_part="go-1.18",
        )

    def load_defaults(self):
        Tool.load_defaults(self)
        self.tool_path = os.path.join(self.build_dir, "bin")
        self.full_exe = os.path.join(self.tool_path, "go.exe")

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        self.mark_deps = extract_exec(
            self.archive_file,
            self.build_dir,
            check_file=self.full_exe,
            check_mark=True,
            strip_one=True,
        )
