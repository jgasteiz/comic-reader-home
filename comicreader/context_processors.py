"""
All this has been taken from https://github.com/dobarkod/django-source-revision.
"""

from subprocess import CalledProcessError

from django.conf import settings

try:
    from subprocess import check_output
except ImportError:
    from subprocess import Popen, PIPE

    def check_output(cmd):
        return Popen(cmd, stdout=PIPE).communicate()[0]


__all__ = ["get_revision"]

_revision_loaded = False
_revision = None


def get_revision():
    global _revision, _revision_loaded

    if _revision_loaded:
        return _revision

    commands = getattr(
        settings, "SOURCE_REVISION_COMMANDS", ["git rev-parse --short HEAD", "hg id -i"]
    )

    def get_rev():
        for command in commands:
            try:
                rev = check_output(command.split(u" ")).decode("ascii").strip()
            except (CalledProcessError, OSError):
                continue
            if rev:
                return rev
        return None

    _revision = get_rev()
    _revision_loaded = True
    return _revision


def source_revision(request):
    return {u"SOURCE_REVISION": get_revision()}
