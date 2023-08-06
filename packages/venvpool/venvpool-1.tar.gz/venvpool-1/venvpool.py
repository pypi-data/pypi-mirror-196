#!/usr/bin/env python

# Copyright 2013, 2014, 2015, 2016, 2017, 2020, 2022, 2023 Andrzej Cichocki

# This file is part of venvpool.
#
# venvpool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# venvpool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with venvpool.  If not, see <http://www.gnu.org/licenses/>.

from collections import OrderedDict
from contextlib import contextmanager
from random import shuffle # XXX: Expensive?
from stat import S_IXUSR, S_IXGRP, S_IXOTH
from tempfile import mkdtemp, mkstemp # TODO: Over a hundredth.
import errno, logging, operator, os, re, shutil, sys # XXX: Still expensive?

class subprocess:

    def __getattr__(self, name):
        import subprocess # Up to a hundredth.
        return getattr(subprocess, name)

log = logging.getLogger(__name__)
cachedir = os.path.join(os.path.expanduser('~'), '.cache', 'pyven') # TODO: Honour XDG_CACHE_HOME.
dotpy = '.py'
executablebits = S_IXUSR | S_IXGRP | S_IXOTH
initbinname = 'initbin.py'
oserrors = {code: type(name, (OSError,), {}) for code, name in errno.errorcode.items()}
pooldir = os.path.join(cachedir, 'pool')
scriptregex, = (r"^if\s+(?:__name__\s*==\s*{main}|{main}\s*==\s*__name__)\s*:\s*$".format(**locals()) for main in ['''(?:'__main__'|"__main__")'''])
try:
    set_inheritable = os.set_inheritable
except AttributeError:
    from fcntl import fcntl, FD_CLOEXEC, F_GETFD, F_SETFD
    def set_inheritable(h, inherit):
        assert inherit
        fcntl(h, F_SETFD, fcntl(h, F_GETFD) & ~FD_CLOEXEC)
subprocess = subprocess()
userbin = os.path.join(os.path.expanduser('~'), '.local', 'bin')

def safe_name(name, unsafeseq = re.compile('[^A-Za-z0-9.]+')):
    return unsafeseq.sub('-', name)

def to_filename(name):
    return name.replace('-', '_')

def _osop(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except OSError as e:
        raise oserrors[e.errno](*e.args)

def initlogging():
    logging.basicConfig(format = "%(asctime)s %(levelname)s %(message)s", level = logging.DEBUG)

@contextmanager
def TemporaryDirectory():
    tempdir = mkdtemp()
    try:
        yield tempdir
    finally:
        shutil.rmtree(tempdir)

@contextmanager
def _onerror(f):
    try:
        yield
    except:
        f()
        raise

class Pip:

    envpatch = dict(PYTHON_KEYRING_BACKEND = 'keyring.backends.null.Keyring')

    def __init__(self, pippath):
        self.pippath = pippath

    def pipinstall(self, command):
        subprocess.check_call([self.pippath, 'install'] + command, env = dict(os.environ, **self.envpatch), stdout = sys.stderr)

def listorempty(d, xform = lambda p: p):
    try:
        names = _osop(os.listdir, d)
    except oserrors[errno.ENOENT]:
        return []
    return [xform(os.path.join(d, n)) for n in sorted(names)]

class LockStateException(Exception): pass

class ReadLock:

    def __init__(self, handle):
        self.handle = handle

    def unlock(self):
        try:
            _osop(os.close, self.handle)
        except oserrors[errno.EBADF]:
            raise LockStateException

def _idempotentunlink(path):
    try:
        _osop(os.remove, path)
        return True
    except oserrors[errno.ENOENT]:
        pass

def _chunkify(n, v):
    i = iter(v)
    while True:
        chunk = []
        for _ in range(n):
            try:
                x = next(i)
            except StopIteration:
                if chunk:
                    yield chunk
                return
            chunk.append(x)
        yield chunk

if '/' == os.sep:
    def _swept(readlocks):
        for chunk in _chunkify(1000, readlocks):
            # Check stderr instead of returncode for errors:
            stdout, stderr = subprocess.Popen(['lsof', '-t'] + chunk, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
            if not stderr and not stdout:
                for readlock in chunk:
                    if _idempotentunlink(readlock):
                        yield readlock
else:
    def _swept(readlocks): # TODO: Untested!
        for readlock in readlocks:
            try:
                if _idempotentunlink(readlock):
                    yield readlock
            except oserrors[errno.EACCES]:
                pass

class SharedDir(object):

    def __init__(self, dirpath):
        self.readlocks = os.path.join(dirpath, 'readlocks')

    def _sweep(self):
        paths = list(_compress(list(_swept(listorempty(self.readlocks)))))
        n = len(paths)
        if 2 == n:
            log.debug("Swept: %s%s", *paths)
        elif 2 < n:
            log.debug("Swept: %s{%s}", paths[0], ','.join(paths[1:]))

    def trywritelock(self):
        self._sweep()
        try:
            _osop(os.rmdir, self.readlocks)
            return True
        except (oserrors[errno.ENOENT], oserrors[errno.ENOTEMPTY]):
            pass

    def createortrywritelock(self):
        try:
            _osop(os.mkdir, os.path.dirname(self.readlocks))
            return True
        except oserrors[errno.EEXIST]:
            return self.trywritelock()

    def writeunlock(self):
        try:
            _osop(os.mkdir, self.readlocks)
        except oserrors[errno.EEXIST]:
            raise LockStateException

    def tryreadlock(self):
        try:
            h = _osop(mkstemp, dir = self.readlocks, prefix = 'lock')[0]
            set_inheritable(h, True)
            return ReadLock(h)
        except oserrors[errno.ENOENT]:
            pass

def _safewhich(name):
    poolprefix = pooldir + os.sep
    for bindir in os.environ['PATH'].split(os.pathsep):
        if bindir.startswith(poolprefix) or not os.path.isabs(bindir):
            log.debug("Ignore bin directory: %s", bindir)
        else:
            path = os.path.join(bindir, name)
            if os.path.exists(path):
                return path

class Venv(SharedDir):

    @property
    def site_packages(self):
        libpath = os.path.join(self.venvpath, 'lib')
        pyname, = (n for n in os.listdir(libpath) if n.startswith('python'))
        return os.path.join(libpath, pyname, 'site-packages')

    def __init__(self, venvpath):
        super(Venv, self).__init__(venvpath)
        self.venvpath = venvpath

    def create(self, pyversion):
        def isolated(*command):
            subprocess.check_call(command, cwd = tempdir, stdout = sys.stderr)
        executable = _safewhich("python%s" % pyversion)
        absvenvpath = os.path.abspath(self.venvpath) # XXX: Safe when venvpath has symlinks?
        with TemporaryDirectory() as tempdir:
            if pyversion < 3:
                isolated('virtualenv', '-p', executable, absvenvpath)
            else:
                isolated(executable, '-m', 'venv', absvenvpath)
                isolated(os.path.join(absvenvpath, 'bin', 'pip'), 'install', '--upgrade', 'pip', 'setuptools', 'wheel')

    def delete(self, label = 'transient'):
        log.debug("Delete %s venv: %s", label, self.venvpath)
        shutil.rmtree(self.venvpath)

    def programpath(self, name):
        return os.path.join(self.venvpath, 'bin', name)

    def install(self, args, pip = None):
        log.debug("Install: %s", ' '.join(args))
        if args:
            if pip is None:
                Pip(self.programpath('pip')).pipinstall(args)
            else:
                Pip(pip).pipinstall(args + ['--prefix', self.venvpath])

    def compatible(self, installdeps):
        for i in installdeps.volatileprojects:
            if not self._hasvolatileproject(i):
                return
        for r in installdeps.pypireqs:
            version = self._reqversionornone(r.namepart)
            if version is None or version not in r.parsed:
                return
        log.debug("Found compatible venv: %s", self.venvpath)
        return True

    def _hasvolatileproject(self, info):
        return os.path.exists(os.path.join(self.site_packages, "%s-%s.dist-info" % (to_filename(safe_name(info.config.name)), info.devversion())))

    def _reqversionornone(self, name):
        patterns = [re.compile(format % nameregex) for nameregex in [re.escape(to_filename(safe_name(name)).lower())] for format in [
            "^%s-(.+)[.]dist-info$",
            "^%s-([^-]+).*[.]egg-info$"]]
        for lowername in (n.lower() for n in os.listdir(self.site_packages)):
            for p in patterns:
                m = p.search(lowername)
                if m is not None:
                    return m.group(1)

    def run(self, mode, localreqs, module, scriptargs, **kwargs):
        argv = [os.path.join(self.venvpath, 'bin', 'python'), __file__, '-x', os.pathsep.join(_compress(localreqs)), module] + scriptargs
        if 'call' == mode:
            return subprocess.call(argv, **kwargs)
        if 'check_call' == mode:
            return subprocess.check_call(argv, **kwargs)
        if 'exec' == mode:
            os.execv(argv[0], argv, **kwargs)
        raise ValueError(mode)

def _compress(paths, splitchar = os.sep):
    if not paths:
        yield '-' # Avoid empty word in command line.
        return
    firstdiff = -1
    for firstdiff, chars in enumerate(zip(*paths)):
        if 1 != len(set(chars)):
            break
    else:
        firstdiff += 1
    while firstdiff and paths[0][firstdiff - 1] != splitchar:
        firstdiff -= 1
    yield paths[0][:firstdiff]
    for p in paths:
        yield p[firstdiff:]

def _decompress(paths):
    i = iter(paths)
    prefix = next(i)
    try:
        while True:
            yield prefix + next(i)
    except StopIteration:
        pass

class Execute:

    letter = 'x'

    @staticmethod
    def main():
        import runpy # A few thousandths.
        assert '-x' == sys.argv.pop(1)
        sys.path[0] = bindir = os.path.dirname(sys.executable)
        try:
            envpath = os.environ['PATH']
        except KeyError:
            envpath = bindir
        else:
            envpath = bindir + os.pathsep + envpath
        os.environ['PATH'] = envpath
        sys.path[slice(*[_insertionpoint(sys.path)] * 2)] = _decompress(sys.argv.pop(1).split(os.pathsep))
        runpy.run_module(sys.argv.pop(1), run_name = '__main__', alter_sys = True)

def _insertionpoint(v, suffix = os.sep + 'site-packages'):
    i = n = len(v)
    while not v[i - 1].endswith(suffix):
        i -= 1
        if not i:
            return n
    while i and v[i - 1].endswith(suffix):
        i -= 1
    return i

class Pool:

    @property
    def versiondir(self):
        return os.path.join(pooldir, str(self.pyversion))

    def __init__(self, pyversion):
        self.readonlyortransient = {
            False: self.readonly,
            True: self._transient,
        }
        self.readonlyorreadwrite = {
            False: self.readonly,
            True: self.readwrite,
        }
        self.pyversion = pyversion

    def _newvenv(self, installdeps):
        try:
            _osop(os.makedirs, self.versiondir)
        except oserrors[errno.EEXIST]:
            pass
        venv = Venv(mkdtemp(dir = self.versiondir, prefix = 'venv'))
        with _onerror(venv.delete):
            venv.create(self.pyversion)
            installdeps.invoke(venv)
            assert venv.compatible(installdeps) # Bug if not.
            return venv

    def _lockcompatiblevenv(self, trylock, installdeps):
        venvs = listorempty(self.versiondir, Venv)
        shuffle(venvs)
        for venv in venvs:
            lock = trylock(venv)
            if lock is not None:
                with _onerror(lock.unlock):
                    if venv.compatible(installdeps): # TODO: Upgrade venv if it has a subset.
                        return venv, lock
                lock.unlock()

    @contextmanager
    def _transient(self, installdeps):
        venv = self._newvenv(installdeps)
        try:
            yield venv
        finally:
            venv.delete()

    @contextmanager
    def readonly(self, installdeps):
        while True:
            t = self._lockcompatiblevenv(Venv.tryreadlock, installdeps)
            if t is not None:
                venv, readlock = t
                break
            venv = self._newvenv(installdeps)
            # XXX: Would it be possible to atomically convert write lock to read lock?
            venv.writeunlock()
            readlock = venv.tryreadlock()
            if readlock is not None:
                break
        try:
            yield venv
        finally:
            readlock.unlock()

    @contextmanager
    def readwrite(self, installdeps):
        def trywritelock(venv):
            if venv.trywritelock():
                class WriteLock:
                    def unlock(self):
                        venv.writeunlock()
                return WriteLock()
        t = self._lockcompatiblevenv(trywritelock, installdeps)
        if t is None:
            venv = self._newvenv(installdeps)
        else:
            venv = t[0]
            with _onerror(venv.writeunlock):
                for dirpath, dirnames, filenames in os.walk(venv.venvpath):
                    for name in filenames:
                        p = os.path.join(dirpath, name)
                        if 1 != os.stat(p).st_nlink:
                            h, q = mkstemp(dir = dirpath)
                            os.close(h)
                            shutil.copy2(p, q)
                            os.remove(p) # Cross-platform.
                            os.rename(q, p)
        try:
            yield venv
        finally:
            venv.writeunlock()

class BaseReq:

    @classmethod
    def parselines(cls, lines):
        from pkg_resources import parse_requirements # Expensive module!
        return [cls(parsed) for parsed in parse_requirements(lines)]

    @property
    def namepart(self):
        return self.parsed.name

    @property
    def reqstr(self):
        return str(self.parsed)

    def __init__(self, parsed):
        self.parsed = parsed

class FastReq:

    class Version:

        def __init__(self, operator, splitversion):
            self.operator = operator
            self.splitversion = splitversion

        def accept(self, splitversion):
            def pad(v):
                return v + [0] * (n - len(v))
            versions = [splitversion, self.splitversion]
            n = max(map(len, versions))
            return self.operator(*map(pad, versions))

    @staticmethod
    def _splitversion(versionstr):
        return [int(k) for k in versionstr.split('.')]

    s = r'\s*'
    name = '([A-Za-z0-9._-]+)' # Slightly more lenient than PEP 508.
    version = "(<|<=|!=|==|>=|>){s}([0-9.]+)".format(**locals()) # Subset of features.
    versionmatch = re.compile("^{s}{version}{s}$".format(**locals())).search
    getmatch = re.compile("^{s}{name}{s}({version}{s}(?:,{s}{version}{s})*)?$".format(**locals())).search
    skipmatch = re.compile("^{s}(?:#|$)".format(**locals())).search
    del s, name, version
    operators = {
        '<': operator.lt,
        '<=': operator.le,
        '!=': operator.ne,
        '==': operator.eq,
        '>=': operator.ge,
        '>': operator.gt,
    }

    @classmethod
    def parselines(cls, lines):
        def g():
            for line in lines:
                if cls.skipmatch(line) is not None:
                    continue
                namepart, versionspec = cls.getmatch(line).groups()[:2]
                versions = []
                reqstrversions = []
                if versionspec is not None:
                    for onestr in versionspec.split(','):
                        operatorstr, versionstr = cls.versionmatch(onestr).groups()
                        versions.append(cls.Version(cls.operators[operatorstr], cls._splitversion(versionstr)))
                        reqstrversions.append(operatorstr + versionstr)
                yield cls(namepart, versions, namepart + ','.join(sorted(reqstrversions)))
        return list(g())

    @property
    def parsed(self):
        return self

    def __init__(self, namepart, versions, reqstr):
        self.namepart = namepart
        self.versions = versions
        self.reqstr = reqstr

    def __contains__(self, versionstr):
        splitversion = self._splitversion(versionstr)
        return all(v.accept(splitversion) for v in self.versions)

class SimpleInstallDeps:

    volatileprojects = ()

    def __init__(self, requires, pip = None, reqcls = BaseReq):
        self.pypireqs = reqcls.parselines(requires)
        self.pip = pip
        self.reqcls = reqcls

    def invoke(self, venv):
        venv.install([r.reqstr for r in self.pypireqs], self.pip)

    def poplocalreqs(self, workspace, makerequirementslines):
        local = OrderedDict()
        reqs = list(self.pypireqs)
        del self.pypireqs[:]
        while reqs:
            nextreqs = []
            for req in reqs:
                projectdir = os.path.join(workspace, req.namepart)
                if projectdir in local:
                    continue
                if os.path.exists(projectdir):
                    local[projectdir] = None
                    nextreqs.extend(self.reqcls.parselines(makerequirementslines(projectdir))) # FIXME: Can pass None into parselines.
                else:
                    self.pypireqs.append(req)
            reqs = nextreqs
        return list(local)

def _getrequirementslinesornone(projectdir):
    def linesornone(acceptnull, *names):
        path = os.path.join(projectdir, *names)
        if os.path.exists(path):
            log.debug("Found requirements: %s", path)
            with open(path) as f:
                return f.read().splitlines()
        if acceptnull:
            log.debug("Null requirements: %s", path)
            return []
    v = linesornone(False, 'requirements.txt')
    if v is not None:
        return v
    names = [name for name in os.listdir(projectdir) if name.endswith('.egg-info')]
    if names:
        name, = names # XXX: Could there legitimately be multiple?
        return linesornone(True, name, 'requires.txt')

class Command:

    @classmethod
    def main(cls):
        from argparse import ArgumentParser # Two or three hundredths.
        initlogging()
        parser = cls.createparser(ArgumentParser)
        if cls.letter is not None:
            parser.add_argument('-' + cls.letter, action = 'store_true')
        parser.add_argument('-v', action = 'store_true')
        args = parser.parse_args()
        if cls.letter is not None:
            assert getattr(args, cls.letter)
        if not args.v:
            logging.getLogger().setLevel(logging.INFO)
        cls.mainimpl(args)

class Launch(Command):

    letter = 'l'

    @staticmethod
    def createparser(parsercls):
        parser = parsercls(add_help = False)
        parser.add_argument('--pip')
        parser.add_argument('scriptpath', type = os.path.abspath) # XXX: Safe when scriptpath has symlinks?
        parser.add_argument('scriptargs', nargs = '*')
        return parser

    @classmethod
    def mainimpl(cls, args):
        scriptpath = args.scriptpath
        assert scriptpath.endswith(dotpy)
        projectdir, requirementslines = _findrequirements(os.path.dirname(scriptpath))
        installdeps = SimpleInstallDeps(requirementslines, args.pip, FastReq)
        localreqs = installdeps.poplocalreqs(os.path.normpath(os.path.join(projectdir, '..')), _getrequirementslinesornone)
        localreqs.insert(0, projectdir)
        module = os.path.relpath(scriptpath[:-len(dotpy)], projectdir).replace(os.sep, '.')
        with Pool(sys.version_info.major).readonly(installdeps) as venv: # TODO: Likely to be major 2 when launching manually.
            venv.run('exec', localreqs, module, args.scriptargs)

class NoRequirementsFoundException(Exception): pass

def _findrequirements(projectdir):
    while True:
        requirementslines = _getrequirementslinesornone(projectdir)
        if requirementslines is not None:
            return projectdir, requirementslines
        parent = os.path.dirname(projectdir)
        if parent == projectdir:
            raise NoRequirementsFoundException
        projectdir = parent

class Activate(Command):

    letter = None

    @staticmethod
    def createparser(parsercls):
        parser = parsercls()
        parser.add_argument('-f', action = 'store_true')
        parser.add_argument('projectdir', nargs = '*', default = ['.'])
        return parser

    @classmethod
    def mainimpl(cls, args):
        for projectdir in args.projectdir:
            try:
                cls._scan(_findrequirements(os.path.realpath(projectdir))[0], 3, args.f) # XXX: Always 3?
            except NoRequirementsFoundException:
                log.exception("Skip: %s", projectdir)

    @staticmethod
    def _srcpaths(rootdir):
        for dirpath, dirnames, filenames in os.walk(rootdir):
            for name in filenames:
                if name.endswith(dotpy):
                    path = os.path.join(dirpath, name)
                    with open(path) as f:
                        if re.search(scriptregex, f.read(), re.MULTILINE) is not None:
                            yield path

    @classmethod
    def _scan(cls, projectdir, pyversion, force):
        venvpoolpath = os.path.realpath(__file__)
        for srcpath in cls._srcpaths(projectdir):
            if not checkpath(projectdir, srcpath):
                log.debug("Not a project source file: %s", srcpath)
                continue
            command = commandornone(srcpath)
            if command is None:
                log.debug("Bad source name: %s", srcpath)
                continue
            text = """#!/usr/bin/env python{pyversion}
import sys
sys.argv[1:1] = '-l', '--', {srcpath!r}
__file__ = {venvpoolpath!r}
with open(__file__) as f: venvpoolsrc = f.read()
del sys, f
exec(venvpoolsrc)
""".format(**locals())
            scriptpath = os.path.join(userbin, command) # TODO: Warn if shadowed.
            if os.path.exists(scriptpath):
                mode = os.stat(scriptpath).st_mode
                if mode | executablebits == mode:
                    with open(scriptpath) as f:
                        if f.read() == text:
                            log.debug("Identical: %s", scriptpath)
                            continue
                if not force:
                    log.info("Exists: %s", scriptpath)
                    continue
                log.info("Overwrite: %s", scriptpath)
            else:
                log.info("Create: %s", scriptpath)
            with open(scriptpath, 'w') as f:
                f.write(text)
            os.chmod(scriptpath, os.stat(scriptpath).st_mode | executablebits)

def checkpath(projectdir, path):
    while True:
        path = os.path.dirname(path)
        if path == projectdir:
            return True
        if not os.path.exists(os.path.join(path, '__init__.py')): # XXX: What about namespace packages?
            break

def commandornone(srcpath):
    name = os.path.basename(srcpath)
    name = os.path.basename(os.path.dirname(srcpath)) if '__init__.py' == name else name[:-len(dotpy)]
    if '-' not in name:
        return name.replace('_', '-')

class Compact(Command):

    letter = 'c'

    @staticmethod
    def createparser(parsercls):
        return parsercls()

    @classmethod
    def mainimpl(cls, args): # XXX: Combine venvs with orthogonal dependencies?
        venvtofreeze = {}
        try:
            for versiondir in listorempty(pooldir):
                for venv in listorempty(versiondir, Venv):
                    if venv.trywritelock():
                        venvtofreeze[venv] = set(subprocess.check_output([venv.programpath('pip'), 'freeze'], universal_newlines = True).splitlines())
                    else:
                        log.debug("Busy: %s", venv.venvpath)
            log.info('Find redundant venvs.')
            while True:
                venv = cls._redundantvenv(venvtofreeze)
                if venv is None:
                    break
                venv.delete('redundant')
                venvtofreeze.pop(venv)
            cls._compactvenvs([l.venvpath for l in venvtofreeze])
        finally:
            for l in venvtofreeze:
                l.writeunlock()

    @staticmethod
    def _redundantvenv(venvtofreeze):
        for venv, freeze in venvtofreeze.items():
            for othervenv, otherfreeze in venvtofreeze.items():
                if venv != othervenv and os.path.dirname(venv.venvpath) == os.path.dirname(othervenv.venvpath) and freeze <= otherfreeze:
                    return venv

    @staticmethod
    def _compactvenvs(venvpaths):
        log.info("Compact %s venvs.", len(venvpaths))
        if venvpaths:
            subprocess.check_call(['jdupes', '-Lrq'] + venvpaths)
        log.info('Compaction complete.')

def main():
    try:
        firstarg = sys.argv[1]
    except IndexError:
        pass
    else:
        if firstarg.startswith('-'):
            letter = firstarg[1]
            for cls in Execute, Launch, Compact:
                if letter == cls.letter:
                    return cls.main()
    Activate.main()

if ('__main__' == __name__): # Hide from scriptregex.
    main()
