import sys

if str(sys.version[0]) == "3":
    import pandas
    print('/'.join(pandas.__file__.replace('\\', '/').split('/')[:-2]))