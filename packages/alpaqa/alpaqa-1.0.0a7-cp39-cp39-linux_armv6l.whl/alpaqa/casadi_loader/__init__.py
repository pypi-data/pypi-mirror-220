import casadi as cs
import os
from os.path import join, basename
import shelve
import uuid
import pickle
import base64
import glob
import subprocess
import platform
import sys
import warnings
from .. import alpaqa as pa
from ..casadi_generator import generate_casadi_problem, SECOND_ORDER_SPEC, write_casadi_problem_data
from ..cache import get_alpaqa_cache_dir

# TODO: factor out caching logic


def _load_casadi_problem(sofile):
    print("-- Loading:", sofile)
    prob = pa.load_casadi_problem(sofile)
    return prob


def generate_and_compile_casadi_problem(
    f: cs.Function,
    g: cs.Function,
    *,
    C = None,
    D = None,
    param = None,
    l1_reg = None,
    penalty_alm_split = None,
    second_order: SECOND_ORDER_SPEC = 'no',
    name: str = "alpaqa_problem",
    **kwargs,
) -> pa.CasADiProblem:
    """Compile the objective and constraint functions into a alpaqa Problem.

    :param f:            Objective function f(x).
    :param g:            Constraint function g(x).
    :param C:            Bound constraints on x.
    :param D:            Bound constraints on g(x).
    :param param:        Problem parameter values.
    :param l1_reg:       L1-regularization on x.
    :param penalty_alm_split: This many components at the beginning of g(x) are
                              handled using a quadratic penalty method rather
                              than an augmented Lagrangian method.
    :param second_order: Whether to generate functions for evaluating Hessians.
    :param name: Optional string description of the problem (used for filename).
    :param kwargs:       Parameters passed to 
                         :py:func:`..casadi_generator.generate_casadi_problem`.

    :return: Problem specification that can be passed to the solvers.
    """

    cachedir = get_alpaqa_cache_dir()
    cachefile = join(cachedir, 'problems')

    key = base64.b64encode(pickle.dumps(
        (f, g, second_order, name, kwargs))).decode('ascii')

    os.makedirs(cachedir, exist_ok=True)
    with shelve.open(cachefile) as cache:
        if key in cache:
            try:
                uid, soname = cache[key]
                probdir = join(cachedir, str(uid))
                sofile = join(probdir, soname)
                write_casadi_problem_data(sofile, C, D, param, l1_reg, penalty_alm_split)
                return _load_casadi_problem(sofile)
            except:
                del cache[key]
                # if os.path.exists(probdir) and os.path.isdir(probdir):
                #     shutil.rmtree(probdir)
                raise
        uid = uuid.uuid1()
        projdir = join(cachedir, "build")
        builddir = join(projdir, "build")
        os.makedirs(builddir, exist_ok=True)
        probdir = join(cachedir, str(uid))
        cgen = generate_casadi_problem(f, g, second_order, name, **kwargs)
        cfile = cgen.generate(join(projdir, ""))
        with open(join(projdir, 'CMakeLists.txt'), 'w') as f:
            f.write(f"""
                cmake_minimum_required(VERSION 3.17)
                project(CasADi-{name} LANGUAGES C)
                set(CMAKE_SHARED_LIBRARY_PREFIX "")
                add_library({name} SHARED {basename(cfile)})
                install(FILES $<TARGET_FILE:{name}>
                        DESTINATION lib)
                install(FILES {basename(cfile)}
                        DESTINATION src)
            """)
        build_type = 'Release'
        configure_cmd = ['cmake', '-B', builddir, '-S', projdir]
        if platform.system() == 'Windows':
            configure_cmd += ['-A', 'x64' if sys.maxsize > 2**32 else 'Win32']
        else:
            configure_cmd += ['-G', 'Ninja Multi-Config']
        build_cmd = ['cmake', '--build', builddir, '--config', build_type]
        install_cmd = [
            'cmake', '--install', builddir, '--config', build_type, '--prefix',
            probdir
        ]
        subprocess.run(configure_cmd, check=True)
        subprocess.run(build_cmd, check=True)
        subprocess.run(install_cmd, check=True)
        sofile = glob.glob(join(probdir, "lib", name + ".*"))
        if len(sofile) == 0:
            raise RuntimeError(
                f"Unable to find compiled CasADi problem '{name}'")
        elif len(sofile) > 1:
            warnings.warn(
                f"Multiple compiled CasADi problem files were found for '{name}'"
            )
        sofile = sofile[0]
        soname = os.path.relpath(sofile, probdir)
        cache[key] = uid, soname

        write_casadi_problem_data(sofile, C, D, param, l1_reg, penalty_alm_split)
        return _load_casadi_problem(sofile)


if pa.with_casadi_ocp:
    from .ocp import generate_and_compile_casadi_control_problem
