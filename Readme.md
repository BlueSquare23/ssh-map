# SSH Mapper

This script is meant to help map (enumerate) ssh key networks.

The main script will go through and try to ssh to the hosts in the
`ssh-hosts.txt` file as each of the users in the `ssh-users.txt` file.

## Txt Files

The `ssh-hosts.txt` should be formatted host:port as per convention, one entry
per line.

For example:

```
example1.com:22
example2.com:2222
example3.com:12345
```

Likewise, the `ssh-users.txt` should be a new line separated list of usernames.

For example:

```
user1
user2
user3
```
