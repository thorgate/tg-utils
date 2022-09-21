from compressor.filters import CompilerFilter


class UglifyFilter(CompilerFilter):
    """Compress JavaScript with UglifyJS 2

    Requires uglifyjs to be available in the $PATH: https://github.com/mishoo/UglifyJS2
    """

    command = "uglifyjs - --compress --mangle"


class CleanCssFilter(CompilerFilter):
    """Compress CSS with clean-css

    Requires cleancss to be available in the $PATH: https://github.com/jakubpawlowicz/clean-css
    """

    command = "cleancss"
