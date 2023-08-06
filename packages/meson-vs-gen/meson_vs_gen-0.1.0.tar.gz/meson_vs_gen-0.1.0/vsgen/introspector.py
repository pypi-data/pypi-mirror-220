from functools import lru_cache
import json
from pathlib import Path
import re
from typing import Any, Optional


def lmfind(d: list[dict[str, Any]], v: Any, key: str = 'name', default: Any = None) -> Any:
    for item in d:
        if item.get(key, ...) == v:
            return item
    return default


def lmget(d: list[dict[str, Any]], v: Any, key: str = 'name', value: str = 'value', default: Any = None) -> Any:
    item = lmfind(d, v, key, ...)
    if item is ...:
        return default
    return item[value]


class MesonVersionError(RuntimeError):
    pass


class UnconfiguredProject(RuntimeError):
    pass


class UnsuportedLanguageError(RuntimeError):
    pass


class Introspector:

    INFO_DIR = 'meson-info'
    INFO_FILE = 'meson-info.json'
    LANGUAGES = {'cpp', 'c'}

    def __init__(self, build_dir: Path):
        self.build_dir = build_dir
        self.intro_data = {}

        info_file = self.build_dir / self.INFO_DIR / self.INFO_FILE
        if not info_file.exists():
            raise UnconfiguredProject(f"{self.build_dir} does not contain a configured meson project")

        with info_file.open('r', encoding='utf8') as f:
            info_data = json.load(f)

        meson_version = info_data['meson_version']['full']
        meson_version = tuple(map(int, meson_version.split('.')))
        if meson_version < (1, 1, 99):
            raise MesonVersionError("vsgen requires at lest meson 1.2.0")

        for name, data in info_data['introspection']['information'].items():
            with (self.build_dir / self.INFO_DIR / data['file']).open('r', encoding='utf8') as f:
                self.intro_data[name] = json.load(f)

    def cpu_family(self) -> str:
        return self.intro_data["machines"]["host"]["cpu_family"]

    def is_debug(self) -> bool:
        return lmget(self.intro_data['buildoptions'], 'debug')

    def toolset(self) -> str:

        for lang in self.LANGUAGES:
            compiler = self.intro_data['compilers']['host'].get(lang)
            if compiler:
                compiler_version = compiler['version']
                version = compiler_version.split('.')
                if version[0] == '19':
                    return f'v14{version[1][0]}'
                else:
                    return f'v{int(version[0])-6}0'

        raise UnsuportedLanguageError(
            "vsgen is only compatible with projects using {} language".format(" and ".join(self.LANGUAGES))
        )

    def get_target_filename(self, target: str) -> Optional[str]:
        data = self._target_data(target)
        if not data:
            return None

        return data['filename'][0]

    def get_target_params(self, target: str) -> tuple[list[Path], list[str], list[str]]:
        data = self._target_data(target)
        if not data:
            return [], [], []

        includes = []
        macros = []
        options = []

        for sources in data["target_sources"]:
            lang = sources.get("language")
            if lang in self.LANGUAGES:
                for param in sources['parameters']:
                    if param.startswith(('-I', '/I')):
                        includes.append(Path(param[2:]))
                    elif param.startswith(('-D', '/D')):
                        macros.append(param[2:])
                    else:
                        options.append(param)

        return includes, macros, options

    def get_target_sources(self, target: str) -> list[Path]:
        data = self._target_data(target)
        if not data:
            return []

        sources = []
        for source_item in data["target_sources"]:
            if source_item.get("linker"):
                continue
            sources.extend(map(Path, source_item['sources']))
            sources.extend(map(Path, source_item.get('unity_sources', [])))
            for s in source_item['generated_sources']:
                if not re.search(r'-unity\d+\.c', s):
                    sources.append(Path(s))

        return sources

    def get_target_headers(self, target: str) -> list[Path]:
        data = self._target_data(target)
        if not data:
            return []

        headers = []
        for s in data['extra_files']:
            if s.endswith(('.h', '.hh', '.hpp', 'h++', '.H')):
                headers.append(Path(s))

        return headers

    def get_target_extra_files(self, target: str, sources_root: Path) -> list[Path]:
        data = self._target_data(target)
        if not data:
            return []

        extras = set()
        for s in data['extra_files']:
            if s.endswith(('.h', '.hh', '.hpp', 'h++', '.H')):
                extras.add(Path(s))

        # meson.build files
        source_dir = Path(data['defined_in']).parent
        for m in self.intro_data['buildsystem_files']:
            if (e := Path(m)).is_relative_to(source_dir):
                extras.add(e)

        if def_file := data.get('vs_module_defs'):
            def_file = (sources_root / def_file).resolve()
            extras.add(def_file)

        return list(sorted(extras))

    def get_target_extra_paths(self, target: str) -> list[Path]:
        data = self._target_data(target)
        if not data:
            return []

        target_id = data["id"]

        test_data = lmfind(self.intro_data["tests"], [target_id], key="depends")
        if not test_data:
            return []

        return list(map(Path, test_data.get("extra_paths", [])))

    def get_build_files(self) -> list[Path]:
        return list(map(Path, self.intro_data['buildsystem_files']))

    @lru_cache(maxsize=None)
    def _target_data(self, target: str) -> Optional[dict]:
        target_data = lmfind(self.intro_data["targets"], target)

        if target_data and target_data['type'] == "alias":

            depends = target_data.get("depends")
            if depends and len(depends) > 0:
                target_data = lmfind(self.intro_data["targets"], depends[0], key="id")

            else:
                # Fallback waiting for #11758
                name = target_data['id'].removesuffix('@run')
                for data in self.intro_data["targets"]:
                    if data['id'].startswith(name) and data['id'] != target_data['id']:
                        return data
                return None

        return target_data

    def all_targets(self) -> list[str]:
        targets = {}

        for target_data in self.intro_data['targets']:
            if target_data['type'] == 'alias':
                prefix = target_data['id'].removesuffix('@run')
                for tname, tid in reversed(targets.items()):
                    if tid.startswith(prefix):
                        del targets[tname]
                        break

            targets[target_data['name']] = target_data['id']

        return list(targets)
