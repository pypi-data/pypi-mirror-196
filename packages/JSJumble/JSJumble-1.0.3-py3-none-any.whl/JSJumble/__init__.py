import os

host = "127.0.0.1"
port = 80
static_dir = None
compress_dir = None
cache_dir = os.path.join(os.getcwd(),"cache.sql")
js_only = False
delete_unlisted = True
engine = {
    "compact": True,
    "controlFlowFlattening": False,
    "deadCodeInjection": False,
    "debugProtection": False,
    "debugProtectionInterval": 0,
    "disableConsoleOutput": True,
    "identifierNamesGenerator": "hexadecimal",
    "log": False,
    "numbersToExpressions": False,
    "renameGlobals": False,
    "selfDefending": True,
    "simplify": True,
    "splitStrings": False,
    "stringArray": True,
    "stringArrayCallsTransform": False,
    "stringArrayEncoding": [],
    "stringArrayIndexShift": True,
    "stringArrayRotate": True,
    "stringArrayShuffle": True,
    "stringArrayWrappersCount": 1,
    "stringArrayWrappersChainedCalls": True,
    "stringArrayWrappersParametersMaxCount": 2,
    "stringArrayWrappersType": "variable",
    "stringArrayThreshold": 0.75,
    "unicodeEscapeSequence": False
}

def start():
    if not static_dir: raise Exception('"static_dir" is required!')
    if not compress_dir: raise Exception('"compress_dir" is required!')
    from JSJumble import server
    server.start(
        host=host,
        port=port,
        static_dir=static_dir,
        compress_dir=compress_dir,
        cache_dir=cache_dir,
        js_only=js_only,
        delete_unlisted=delete_unlisted,
        engine=engine
    )
    