.. _admin.ram:

=========================
Analyzing RAM usage
=========================

These are just my personal notes. No warranty whatsoever.

.. contents::
    :local:
    :depth: 1


Show available memory::

  $ free -h

To show the top memory using processes, run :command:`top` and then hit :kbd:`M`
to sort them by memory usage.

Show active processes sorted by memory usage in percent::

  $ ps -o pid,user,%mem,command ax | sort -b -k3 -r

Or::

  $ ps aux --sort '%mem'

Or a command that uses awk to sum up the total memory used by processes of the
same name::

  $ ps -e -orss=,args= |awk '{print $1 " " $2 }'| awk '{tot[$2]+=$1;count[$2]++} END {for (i in tot) {print tot[i],i,count[i]}}' | sort -n



Thanks to

- https://linuxhint.com/check_memory_usage_process_linux/
- https://stackoverflow.com/questions/4802481/how-to-see-top-processes-sorted-by-actual-memory-usage
