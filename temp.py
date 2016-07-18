PACKAGE = "timevortex"

options(
    sphinx=Bunch(
        builddir="build",
        sourcedir="source"
    ),

    bin=PACKAGE,

    test_package="tests",

    clone_file="reports/clone/index.html",

    stats_file="reports/stats/index.html",

    cover_folder="reports/cover",

    pylint_file=".pylintrc",

    files="*.py %s/*.py bin/%s features/steps/*.py" % (PACKAGE, PACKAGE),
)


def create_new_release(new_version):
    """Create new release adding a message on changelog, updating version
    in setup.py and conf.py.
    """
    regex = '16s/^.*$/VERSION = "%s"/g' % new_version
    # Update setup.py version
    sh("sed -i '%s' setup.py" % regex)
    # Update conf.py version
    sh("sed -i '%s' docs/source/conf.py" % regex)
    # Add new release message in changelog
    message_starting = "Starting release %s" % new_version
    command = "dch --newversion %s %s" % (new_version, message_starting)
    sh(command)


def get_version(release_type):
    """This method return actual version of package and the next according
    to release_type
    """
    version = release_type
    temp_file = "version.package.txt"
    sh("python setup.py -V > %s" % temp_file)
    with open(temp_file) as filename:
        actual_version = filename.readline().replace("\n", "")
        actual_version = actual_version.replace("\r", "")
        filename.close()
    sh("rm %s" % temp_file)
    array_actual_version = actual_version.split(".")

    if len(array_actual_version) != 3:
        array_actual_version = ["0", "0", "0"]

    if version == "micro":
        new_version = "%s.%s.%d" % (
            array_actual_version[0],
            array_actual_version[1],
            int(array_actual_version[2]) + 1)
    elif version == "minor":
        new_version = "%s.%d.%d" % (
            array_actual_version[0],
            int(array_actual_version[1]) + 1,
            0)
    elif version == "major":
        new_version = "%d.%d.%d" % (int(array_actual_version[0]) + 1, 0, 0)
    else:
        sh("exit(-1)")

    return actual_version, new_version


@task
@consume_args
def release_stable(args):
    """Publish stable release:
        * push package on pip,
        * push code on master git branch with according tag
        * push code on master bazaar branch with according tag
        * test master pip package
        * indicate build status and pip package in README
        * return on develop branch
        * generate debian package
        * test debian package
        * switch to next release
    """
    if len(args) != 1:
        print("Missing next release type argument. Please provide a type.")
        return(0)
    release_type = args[0]
    actual_version, next_version = get_version(release_type)
    message_ending = "Finish release %s" % actual_version
    # Upload package on Pypi
    upload()
    # Create release branch and close it
    sh("git flow release start %s" % actual_version)
    sh("git flow release finish -m '%s' %s" % (
        message_ending, actual_version))
    # Push master branch to github and return on develop
    sh("git push origin master")
    sh("git co develop")
    # Commit code on bazaar and push it
    sh("bzr push '%s'" % (BZR_REPO))
    # Switch to next release
    create_new_release(next_version)

TimeVortex (2.0.0) stable; urgency=low

* Migrate TimeVortex application to Django
* Create timevortex app for utils and timeserieslogger
* Create energy app for currentcost command
* Create weather app for METEAR command
* Migrate pavement utils to timevortex command

Pierre Leray <pierreleray64@gmail.com>  2016-07-17 23:18:43




@task
@consume_args
def release(args):
    """Prepare next release taking into account message in parameter

    """
    # Variables
    version = args[0]
    commit = args[1]
    day = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Create new version number from previous tag
    filename = "tmp.txt"
    cmd = "git describe --tags `git rev-list --tags --max-count=1` > %s"
    sh(cmd % filename)
    fil = open(filename)
    tag_version = fil.readlines()
    fil.close()
    sh("rm %s" % filename)
    tag_version = tag_version[0].replace("\n", "")
    old_version = tag_version.replace("v", "").split(".")

    if len(old_version) != 3:
        old_version = ["0", "0", "0"]

    if version == "micro":
        new_version = "v%s.%s.%d" % (
            old_version[0],
            old_version[1],
            int(old_version[2]) + 1)
    elif version == "minor":
        new_version = "v%s.%d.%d" % (
            old_version[0],
            int(old_version[1]) + 1,
            0)
    elif version == "major":
        new_version = "v%d.%d.%d" % (int(old_version[0]) + 1, 0, 0)
    else:
        sh("exit(-1)")
    # Update changelog
    changelog = "timevortex.%s (%s) stable; urgency=low\n\n" % (
        PACKAGE, new_version)
    changelog += "* %s\n\n" % commit
    changelog += "Pierre Leray <pierreleray64@gmail.com>  %s\n" % day
    cmd = "echo '%s' | cat - CHANGELOG.rst > /tmp/out"
    cmd += " && mv /tmp/out CHANGELOG.rst"
    sh(cmd % changelog)
    # Update setup.py version
    regex = "9s/^.*$/VERSION = '%s'/g" % new_version[1:]
    sh("sed -i '%s' setup.py" % regex)
    # Update conf.py version
    regex = "67s/^.*$/version = '%s'/g" % ".".join(
        new_version[1:].split(".")[:2])
    sh("sed -i '%s' docs/source/conf.py" % regex)
    regex = "69s/^.*$/release = '%s'/g" % new_version[1:]
    sh("sed -i '%s' docs/source/conf.py" % regex)
    # Deploy new release on PYPi
    upload()
    # Commit change
    sh("git add . && git ci -a -m '%s' && git push origin develop" % commit)
    # Create release branch and close it
    sh("git flow release start %s" % new_version)
    sh("git flow release finish -m '%s' %s" % (commit, new_version))
    # Push master branch to github and return on develop
    sh("git push origin master")
    sh("git co develop")
