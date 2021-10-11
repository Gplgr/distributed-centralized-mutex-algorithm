# distributed-centralized-mutex-algorithm

A simple multiprocessed system made in Python consisting in a process with multiple threads that creates
and receives data from another processes through sockets to coordinate mutual exclusion access for writing
on a single text file.

The resulting file consists in lines created by each child process, each line containing the system ID of
the process who wrote it and the timestamp of when it wrote.

## Execution

* Make sure you have the latest Python 3 version installed on your system (tested with Python 3.9).

* Through a command line, execute coordenador.py, specifying:

  1. The number of processes (n).
  
  2. The time which each process should sleep while it holds the lock related to the critical region (k).
  
  3. The number of times each process should run (r).
 
Command line example, on the working directory with python on the system path:

```python coordenador.py 10 0.1 3```

* If you wish to check the integrity of the results, execute resultadoreader.py for "resultado.txt" and
logreader.py for "coordLog.txt", with the same specifications as the main program executed. Examples:

```python resultadoreader.py 10 0.1 3```

```python logreader.py 10 0.1 3```
