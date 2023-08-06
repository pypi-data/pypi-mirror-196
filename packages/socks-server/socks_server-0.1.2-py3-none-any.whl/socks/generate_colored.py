base = "\033[{}m{}\033[0m"


def red(msg):
    return base.format("31", msg)


def green(msg):
    return base.format("92", msg)


def cyan(msg):
    return base.format("26", msg)


def gray(msg):
    return base.format("90", msg)
