.. _hosting.borg:
.. highlight:: console

============================================
Ho we set up a Borg backup client and server
============================================

For example we have a backup server named ``backup-server.net``  and a client
server named ``myserver``. The client's name ``myserver`` is not a domain name,
just an account name on the server.

On the client::

  $ sudo apt install borgbackup
  $ sudo ssh-keygen -t rsa

When asked for a passphrase, leave it empty because this key will be used by a
cron job. The key will be saved to :file:`/root/.ssh/id_rsa`.


On the server, install borgbackup, create user `myserver`::

  $ sudo apt install borgbackup
  $ sudo adduser --disabled-password myserver
  $ sudo su - myserver
  $ mkdir backups
  $ mkdir .ssh && chmod 700 .ssh
  $ touch .ssh/authorized_keys && chmod 600 .ssh/authorized_keys
  $ cat >> .ssh/authorized_keys

Paste the clients's public key to the terminal.  Press :kbd:`ENTER` to add at
least one newline.  Press :kbd:`Ctrl+D` to say you're finished with pasting
content.

Back on the client::

  $ sudo borg init --encryption=repokey-blake2 myserver@backup-server.net:/home/myserver/backups

Create a file :file:`/etc/cron.d/backup2borg` with this content::

  # Not finished. Inspired from https://borgbackup.readthedocs.io/en/stable/quickstart.html

  #!/bin/sh

  # Setting this, so the repo does not need to be given on the commandline:
  export BORG_REPO=ssh://myserver@backup-server.com/~/backups

  # See the section "Passphrase notes" for more infos.
  export BORG_PASSPHRASE='XYZl0ngandsecurepa_55_phrasea&&123'

  # some helpers and error handling:
  info() { printf "\n%s %s\n\n" "$( date )" "$*" >&2; }
  trap 'echo $( date ) Backup interrupted >&2; exit 2' INT TERM

  info "Starting backup"

  # Backup the most important directories into an archive named after
  # the machine this script is currently running on:

  borg create                         \
      --verbose                       \
      --filter AME                    \
      --list                          \
      --stats                         \
      --show-rc                       \
      --compression lz4               \
      --exclude-caches                \
      --exclude '/home/*/.cache/*'    \
      --exclude '/var/cache/*'        \
      --exclude '/var/tmp/*'          \
                                      \
      ::'{hostname}-{now}'            \
      /etc                            \
      /home                           \
      /root                           \
      /var                            \

  backup_exit=$?

  info "Pruning repository"

  # Use the `prune` subcommand to maintain 7 daily, 4 weekly and 6 monthly
  # archives of THIS machine. The '{hostname}-' prefix is very important to
  # limit prune's operation to this machine's archives and not apply to
  # other machines' archives also:

  borg prune                          \
      --list                          \
      --prefix '{hostname}-'          \
      --show-rc                       \
      --keep-daily    7               \
      --keep-weekly   4               \
      --keep-monthly  6               \

  prune_exit=$?

  # use highest exit code as global exit code
  global_exit=$(( backup_exit > prune_exit ? backup_exit : prune_exit ))

  if [ ${global_exit} -eq 0 ]; then
      info "Backup and Prune finished successfully"
  elif [ ${global_exit} -eq 1 ]; then
      info "Backup and/or Prune finished with warnings"
  else
      info "Backup and/or Prune finished with errors"
  fi

  exit ${global_exit}


Notes
=====

You can also log in manually::

  $ sudo ssh myserver@backup-server.net

The first time ssh will ask you to confirm that IP address and server name are
correct::

  The authenticity of host 'backup-server.net (backup-server.net)' can't be established.
  ECDSA key fingerprint is SHA256:/xxxxx.
  Are you sure you want to continue connecting (yes/no)? yes
  Warning: Permanently added 'backup-server.net' (ECDSA) to the list of known hosts.
