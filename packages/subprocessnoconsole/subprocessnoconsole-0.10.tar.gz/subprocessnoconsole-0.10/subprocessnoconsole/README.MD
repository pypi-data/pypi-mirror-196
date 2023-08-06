# Runs a process using subprocess without console output 

## pip install subprocessnoconsole


```python
from subprocessnoconsole import popen_start,popen_start_devnull,popen_start_stdout_read
popen_start(['cmd.exe'])
Out[3]: <Popen: returncode: None args: ['cmd.exe']>
popen_start_devnull(['cmd.exe'])
Out[4]: <Popen: returncode: None args: ['cmd.exe']>
popen_start_stdout_read(['cmd.exe'])

```

