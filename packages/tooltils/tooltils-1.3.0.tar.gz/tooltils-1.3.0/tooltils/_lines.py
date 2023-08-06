lines: int = 0

for i in ['sys/__init__.py', 'sys/info.py', '__init__.py', 
          'errors.py', 'files.py', 'info.py',
          'logging.py', 'requests.py', 'string.py', 'time.py',
          'wave.py', '_lines.py']:
    with open(i) as _f:
        lines += len(_f.readlines())

print(lines)
