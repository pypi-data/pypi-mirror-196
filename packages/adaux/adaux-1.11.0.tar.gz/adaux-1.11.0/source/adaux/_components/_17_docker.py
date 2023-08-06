# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
import collections
import contextlib
import copy
import typing as tp

from .._parser import Jinja2Parser
from .._parser import YamlParser
from .._proto_namespace import _ProtoNamespace
from ._04_project import ProjectMixin
from ._05_dependency import DependencyMixin


class DockerMixin(DependencyMixin, ProjectMixin):
    def set_defaults(self) -> None:
        super().set_defaults()
        self.auxcon.setdefault("docker", _ProtoNamespace())
        for key in self.__keys():
            self.auxcon.docker.setdefault(key, [])

    def cleanup(self, **kwgs: tp.Any) -> None:
        super().cleanup(docker=self.__keys(), **kwgs)

    @classmethod
    def __keys(cls) -> tp.Tuple[str, ...]:
        return ("services",)

    def clear_to_template(self, **kwgs: str) -> None:
        super().clear_to_template(**kwgs)
        data = self.auxcon.docker
        vslug = self.python_version_slug
        data.services = [f"python-deps-{vslug}"]
        if self.is_enabled("pre-commit"):
            data.services.append(f"pre-commit-{vslug}")
            data.services.append(f"pre-commit-all-{vslug}")
        if self.is_enabled("pytest"):
            data.services.append(f"pytest-{vslug}")
        if self.is_enabled("coverage"):
            data.services.append(f"pycov-{vslug};coverage=95")
        if self.is_enabled("docs"):
            data.services.append(f"docs-{vslug};extra_req=docs")
        if self.is_enabled("gitlab"):
            data.services += [
                "gitlab-release",
                "pkg-gitlab",
            ]

    def clear_to_demo(self, **kwgs: str) -> None:
        super().clear_to_demo(**kwgs)
        data = self.auxcon.docker
        data.platform = "amd64"
        data.compositions = _ProtoNamespace(
            dev=_ProtoNamespace(
                pre_build=["python-deps"],
                pre_script=["ls"],
                services=["pytest"],
                overwrite=["x.yml"],
            )
        )

    def update_to_template(self, tpl: _ProtoNamespace, full: _ProtoNamespace) -> None:
        super().update_to_template(tpl, full)

        data = self.auxcon.docker
        old = list(map(self._job_name, data.services))
        new = list(map(self._job_name, tpl.docker.services))

        last_idx = 0
        for job in full.docker.services:
            name = self._job_name(job)
            if name in new and name not in old:
                data.services.insert(last_idx + 1, job)
                old.insert(last_idx + 1, name)
                self._print(f"docker.services: added {name}", fg="green")
            elif name in old and name not in new:
                del data.services[old.index(name)]
                old.remove(name)
                self._print(f"docker.services: removed {name}", fg="red")
            if name in old and name in new:
                last_idx = old.index(name)

    @contextlib.contextmanager
    def extra(self, stage1: bool = False) -> tp.Iterator[_ProtoNamespace]:
        with super().extra(stage1) as auxcone:
            data = auxcone.docker
            if stage1:
                data.services = self.list2nsl(data.services)
                yield auxcone
                return
            data.services = self.list2ns(data.services)
            data.setdefault("base_match", {})
            data.base_match = collections.OrderedDict(
                (key, _ProtoNamespace(val)) for key, val in data.base_match.items()
            )
            for key, opts in data.services.items():
                if "extra_req" in opts:
                    opts["extra_req"] = opts["extra_req"].split(",")
                res = []
                if "assets" in opts:
                    opts["assets"] = opts["assets"].split(",")
                    for x in opts["assets"]:
                        shortname = x.rsplit("/", 1)[1]
                        url = (
                            "$CI_API_V4_URL/projects/$CI_PROJECT_ID/packages/generic/"
                            + x
                        )
                        res.append(
                            r"{\"name\":\""
                            + shortname
                            + r"\",\"url\":\""
                            + url
                            + r"\"}"
                        )
                opts["assets"] = res
                opts.setdefault("pip_req", [])
                opts.setdefault("script", [])
                opts.setdefault("base", None)
                self._adjust_base_on_match_entry(opts, auxcone)

                opts.setdefault("apt_req", [])
                if "-" in key:
                    opts.pure_name, opts.version_slug = key.rsplit("-", 1)
                else:
                    opts.pure_name = key
                    opts.version_slug = "  "

                if opts.version_slug[0] in "3" and opts.version_slug[1:] in [
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13",
                ]:
                    opts.version = f"{opts.version_slug[0]}.{opts.version_slug[1:]}"
                else:
                    opts.pure_name = key
                    del opts.version_slug

                opts.full_name = f"{auxcone.project.slug}-{key}"
                # we dont duplicate the slug
                if opts.pure_name == auxcone.project.slug:
                    opts.full_name = key

                if "mode" in opts:
                    supported = ["django", "django+nginx"]
                    if opts.mode not in supported:
                        raise RuntimeError(
                            f"mode {opts.mode} is not supported {supported}"
                        )

            data.setdefault("platform", None)
            data.project_dir = "../.."
            data.source_dir = f"../../{auxcone.project.source_dir}"
            yield auxcone

    def _adjust_base_on_match_entry(
        self,
        opts: _ProtoNamespace,
        auxcone: _ProtoNamespace,
    ) -> None:
        base_match = auxcone.docker.base_match
        if opts.base is None:
            return
        image, tag = opts.base.rsplit(":", 1)
        if image not in base_match:
            return
        fallback = base_match[image].fallback
        var = (
            f'{image.upper().replace("/", "_").replace(".", "_").replace("-", "_")}_TAG'
        )
        skip = [auxcone.gitlab.release_branch]

        # changing this order affects the jinja2 files!
        opts.base_match = [(image, var, skip, fallback, tag)]

        opts.base = f"{image}:${var}"

    def bake(self) -> None:
        super().bake()
        data = self.auxcon.docker

        extra_req_default = {
            "python-deps": ["default"],
            "pytest": ["test"],
            "pre-commit": ["test", "dev"],
            "pytest-standalone": ["default", "test"],
            "docs": ["docs"],
            "ansible-deploy": ["deploy"],
        }
        deps = self.auxcon.dependencies
        for opts in data.services.values():
            fallback = extra_req_default.get(opts.pure_name, [])
            needed = opts.get("extra_req", fallback)
            opts.pip_req = self._unique_sum(
                opts.pip_req, *[deps.get(x, []) for x in needed]
            )
            opts.apt_req = self._unique_sum(
                opts.apt_req, *[deps.get(x + "_apt", []) for x in needed]
            )
            opts.script = self._sum(
                opts.script, *[deps.get(x + "_script", []) for x in needed]
            )
            assert all('"' not in x for x in opts.pip_req)

            if self.is_enabled("pip"):
                self.branch_match_and_cred_passing(opts)

        config = _ProtoNamespace([("version", "3.6"), ("services", {})])

        must_be_custom = []
        for opts in data.services.values():
            src_dir = self.root / f"docker/services/{opts.pure_name}"
            # Dockerfile
            src = src_dir / "Dockerfile.jinja2"
            if src.exists():
                self.bake_file(
                    f"docker/services/{opts.pure_name}/Dockerfile",
                    f"docker/{opts.full_name}.dockerfile",
                    opts=opts,
                )

            elif (src_dir / "Dockerfile").exists():
                raise NotImplementedError("plain Dockerfiles")
            # docker-compose.yml
            srcj = src_dir / "docker-compose.yml.jinja2"
            if srcj.exists():
                with Jinja2Parser.render_to_tmp(
                    srcj, aux=self.auxcon, opts=opts
                ) as src:
                    part = YamlParser.read(src).services

                config["services"].update(part)
            else:
                must_be_custom.append(opts.full_name)

        # modifies config!
        self._add_custom_services(must_be_custom, config)

        dest = self.target / "docker/compose.yml"
        written = YamlParser.write(config, dest)
        if written:
            self._print(f"baked {dest}", fg="green")

        self._add_compositions(config)

    def _add_custom_services(
        self, must_be_custom: tp.List[str], config: _ProtoNamespace
    ) -> None:
        data = self.auxcon.docker
        custom_config = self.target_custom / "docker" / "compose.yml"
        if not custom_config.exists():
            return
        custom_config = YamlParser.read(custom_config)
        if list(custom_config.keys()) != ["services"]:
            raise RuntimeError(
                "only services can be defined in custom docker-compose.yml."
            )
        custom_services = custom_config.services
        set1 = set(must_be_custom)
        set2 = set(custom_services.keys())
        if set1 != set2:
            raise RuntimeError(
                f"the service declaration {set2} in custom is not equal to the needed services by aux: {set1}"
            )
        config["services"].update(custom_config.services)
        for service_name in custom_services:
            prefix = f"{self.auxcon.project.slug}-"
            if not service_name.startswith(prefix):
                raise RuntimeError(
                    f"custom service '{service_name}' must start with '{prefix}'"
                )
            candidates = [
                x for x in data.services.values() if x.full_name == service_name
            ]
            assert len(candidates) == 1
            opts = candidates[0]
            name = f"docker/{service_name}.dockerfile"
            self.bake_file(name, custom=True, ignore_absent=True, opts=opts)

    def _add_compositions(self, compose_all_config: _ProtoNamespace) -> None:
        data = self.auxcon.docker
        for comp_name, comp in data.get("compositions", {}).items():
            # check validity and set defaults
            valid_keys = {"pre_build", "pre_script", "services", "overwrite"}
            invalid_keys = set(comp.keys()) - valid_keys
            if invalid_keys:
                raise RuntimeError(
                    f"invalid keys {invalid_keys} in composition '{comp_name}'. "
                    f"Valid key are {valid_keys}."
                )
            for key in valid_keys:
                comp.setdefault(key, [])
            comp.name = comp_name
            prefix = self.auxcon.project.slug
            comp.services = [f"{prefix}-{key}" for key in comp.services]
            comp.pre_build = [f"{prefix}-{key}" for key in comp.pre_build]
            og_overwrite = comp.overwrite
            comp.overwrite = [f"../custom/docker/{key}" for key in comp.overwrite]
            for overwrite, file in zip(og_overwrite, comp.overwrite):
                search = (self.target / "docker" / file).resolve()
                if not search.exists():
                    raise RuntimeError(
                        f"overwrite file '{overwrite}' does not exist at '{search.relative_to(self.target.resolve().parent)}'"
                    )

            # docker-compose file
            config = copy.deepcopy(compose_all_config)
            config.services = {
                key: val
                for key, val in compose_all_config.services.items()
                if key in comp.services
            }
            config.setdefault("networks", {})
            config["networks"][f"{comp.name}-network"] = {}

            for val in config.services.values():
                val.setdefault("networks", [])
                val["networks"].append(f"{comp.name}-network")
            comp.compose_filename = f"{comp.name}-compose.yml"
            dest = self.target / f"docker/{comp.compose_filename}"
            written = YamlParser.write(config, dest)
            if written:
                self._print(f"baked {dest}", fg="green")

            # helper bash file
            self.bake_file(
                "docker/comp-helper.sh", f"docker/{comp.name}-compose.sh", comp=comp
            )

    @staticmethod
    def _unique_sum(*args: tp.List[str]) -> tp.List[str]:
        res = []
        for part in args:
            for x in part:
                if x not in res:
                    res.append(x)
        return res

    @staticmethod
    def _sum(*args: tp.List[str]) -> tp.List[str]:
        res = []
        for part in args:
            for x in part:
                res.append(x)
        return res

    @staticmethod
    def _job_name(job: str) -> str:
        if ";" in job:
            return job.split(";", 1)[0].strip()
        if isinstance(job, _ProtoNamespace):
            return job.id
        return job
