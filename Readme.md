# SSH Mapper

This script is meant to help map (enumerate) ssh key networks.

The main `ssh-mapper.py` script will go through and try to ssh to the hosts in
the `ssh-hosts.txt` file as each of the users in the `ssh-users.txt` file.

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

## Intended Usage

There are a few simple parts to this package. First, there's the main
`ssh-mapper.py` script. After you've created the text files for your use case
run `ssh-mapper.py` to generate a `ssh-map.json` file.

```
> ./ssh-mapper.py
Trying SSH Connections...................
Results written to: ssh-map.json
```

From there you can use the `injest-data.py` script to slurp the json into
an SQLite db.

Tip: You can use a tool like the [sqlite3 cli](https://sqlite.org/cli.html) to
quickly query the DB on the fly.

```
> sqlite3 ssh-map.db ".mode box"  "select * from ssh_map;"
┌─────────┬────────────────┬──────────────┬────────────────────┐
│  lhost  │  lhost_pub_ip  │    rhost     │       users        │
├─────────┼────────────────┼──────────────┼────────────────────┤
│  host1  │ 111.111.111.11 │ example1.com │ ['user1']          │
│  host1  │ 111.111.111.11 │ example2.com │ ['user1']          │
│  host1  │ 111.111.111.11 │ example3.com │ ['user1', 'user2'] │
└─────────┴────────────────┴──────────────┴────────────────────┘
```

## Goals

The plan is to then use that data to actually map out connections b/w nodes on
an ssh network. This might be a proper visual map (I figure there gotta be node
graphing packages for python, matplotlib maybe?). But also it might just end up
being a loose ascii representation of a 'map' idk. Haven't gotten that far yet.
