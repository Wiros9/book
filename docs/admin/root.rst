=======================
Providing a Lino server
=======================

As a :term:`server provider` you are responsible for installing and maintaining
a :term:`Lino server`, i.e. a virtual or physical machine used to run one or
several :term:`Lino sites <Lino site>`. A Lino server runs a Linux operating
system and must be connected to a network.

The :term:`server provider` holds root access to the server and creates user
accounts with sudo rights for each :term:`site maintainer`.  He configures
secure remote shell access (SSH) to that machine for each site maintainer.  He
provides support to the site maintainers. See `Creating a user account`_.

The :term:`server provider` is *not* responsible for installing and maintaining
specific system packages, Lino source code and configuration,  or for giving
:term:`end-user support` to the  users of any :term:`Lino site` hosted on this
site.

The :term:`server provider` *may optionally* be responsible for providing backup
service for the server as a whole.


Where to get a virtual server
=============================

If you don't have your own in-house hardware or dedicated server, you can get a
Virtual Private Server from many providers. Here is a list of VPS providers we
have tested:

- https://www.ovh.ie/order/vps   3€/month
- https://www.hetzner.com/cloud  2.89€/month
- https://mochahost.com/vps.php  6.94€/month (Up to 50% OFF)


System requirements for a Lino site
===================================

We recommend a `stable Debian <https://www.debian.org/releases/stable/>`__ as
operating system.  Currently this means Debian 10 "Buster".

**One CPU** should be enough for a site with a few dozens of users.

You need **at least 10 GB of disk space**. You can see how much disk space you have
by saying::

  $ df -h

We recommend **at least 2GB of RAM** (because we didn't yet test production
sites with less).  How to see how much memory you have::

  $ free -h

Preparing a new server
======================

Before creating system users, the root user should check the following.

In your :file:`/etc/ssh/sshd_config` make sure that ``PasswordAuthentication``
is set to ``no``.  We require site maintainers to have a
:xfile:`~/.ssh/authorized_keys` file. They will need their password only for
running `sudo` commands.

All maintainers must have a umask `002` or `007` (not `022` or `077` as is the
default value).

Edit the file :file:`/etc/bash.bashrc` (site-wide for all users)::

    # nano /etc/bash.bashrc

And add the following line at the end::

    umask 002

The :cmd:`umask` command is used to mask (disable) certain file permissions from
any new file created by a given user. See :doc:`umask` for more detailed
information.

The system should have installed the `sudo` package::

  # apt-get install sudo

Also run::

  # apt-get update && apt-get upgrade


Creating a user account
=======================

As a root user you will create a user account for every :term:`site maintainer`.

In the following examples we assume that the user account to create is ``joe``.

Agree upon a temporary password with Joe (who can later change their password
using :cmd:`passwd`), and then type::

  # adduser joe

Site maintainers must be members of the `sudo` and `www-data` groups::

  # adduser joe sudo
  # adduser joe www-data

Creating the user's :xfile:`~/.ssh/authorized_keys` file with the maintainer's
public ssh key::

  # su - joe
  $ mkdir .ssh && chmod 700 .ssh
  $ touch .ssh/authorized_keys && chmod 600 .ssh/authorized_keys
  $ cat >> .ssh/authorized_keys

Paste the maintainer's public key to the terminal.  Press :kbd:`ENTER` to add at
least one newline.  Press :kbd:`Ctrl+D` to say you're finished with pasting
content.

Footnotes:

- `useradd` is a native binary compiled with the system, while `adduser`
  is a perl script that uses `useradd` in back-end.

- ssh requires that the :xfile:`.ssh` directory and its content should have
  permissions set so that only the owner can read, write, or open them.


How to generate a SSH key pair
==============================

As a :term:`site maintainer` you must have generated public and private ssh keys
using the command `ssh-keygen -t rsa`.



How to change the hostname
==========================

Every server has a "hostname", a relatively short "nickname" to designate it.
The hostname is not the same as the FQDN.

How to change the hostname of a Lino server::

  $ sudo hostnamectl set-hostname newname

If you use `mailutils
<http://mailutils.org/manual/html_node/configuration.html>`__, you must also check
your :file:`/etc/mail/local-host-names` file.

If that file doesn't exist, try::

  $ mail --show-config-options | grep SYSCONFDIR
  SYSCONFDIR=/etc 	- System configuration directory

Which means that actually the config files are in :file:`/etc/mail`. And one of
them, :file:`/etc/mail/local-host-names` contains my default ``From`` header.
