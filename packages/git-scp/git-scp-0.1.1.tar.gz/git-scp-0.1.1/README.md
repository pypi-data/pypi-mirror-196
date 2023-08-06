# Git-SCP

[PyPI](https://pypi.org/project/git-scp/)

As we are all aware, Git over SSH/TCP functions effectively and Git is a decentralized protocol.

However, in my experience, when uploading to an SCP path `/path/to/dir/`,
 we can only set the remote URL to the `.git` folder.
The remote URL should be `ssh://user@server:/path/to/dir/.git`.

To address this issue, I have developed the tool.
By simply typing `git-scp user@server:/path/to/dir`, it will upload the current Git repository to `/path/to/dir` on the remote server.

## Install

```
pip install git-scp
```

## Usage

```
usage: git-scp [-h] [remote]
```

```
git-scp user@server:/path/to/dir
upload to user@server:/path/to/dir

git-scp
upload to last path
```

## reference

- https://www.ruanyifeng.com/blog/2022/10/git-server.html