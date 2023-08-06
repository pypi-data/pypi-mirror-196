import argparse
import subprocess

__version__ = "0.1.0"


def cmd_call(cmd, print_stdout=True):
    print(">>> " + cmd)
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
    out = ""
    for stdout_line in iter(p.stdout.readline, ""):
        if print_stdout:
            print("    " + stdout_line.strip())
        out += stdout_line.strip() + "\n"
    return_code = p.wait()
    p.stdout.close()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd, out)
    return out


def compare_local_and_remote(remote_server, remote_dir):
    local_show = cmd_call(f"git rev-parse HEAD").strip()
    remote_show = (cmd_call(f"ssh {remote_server} 'cd {remote_dir} && git rev-parse HEAD'")).strip()

    # fixture for my env
    if remote_show.find("Connection to") > -1 and remote_show.find("[tcp/ssh] succeeded!"):
        remote_show = "\n".join(remote_show.splitlines()[1:])

    if local_show == remote_show:
        return True
    else:
        print("local is:", local_show)
        print("remote is:", remote_show)
        return False


def upload(remote=None):
    branch = "master"
    remote_name = "__git_upload__"

    # Find old remote URL
    try:
        existed_remote = cmd_call(f"git remote get-url {remote_name}")
        existed_remote = existed_remote.strip()
        existed_remote = existed_remote.lstrip("ssh://")
        existed_remote = existed_remote.rstrip("/.git")
    except:
        existed_remote = None

    assert existed_remote or remote, "Please specify remote scp path first. (e.g.: user@server:/some/folder)"

    if existed_remote:
        print(f"[Remote Ref Existed]  {existed_remote=}")

    if not remote:
        remote = existed_remote

    try:
        server = remote.split(":")[0]
        server_path = remote.split(":")[1]
    except IndexError:
        print("Incorrect scp path: " + remote)
        return

    assert remote or existed_remote
    print(f"{remote=}, {existed_remote=}")

    if remote != existed_remote:
        print("[Remote Ref Set]")
        # update or set new remote
        # need check before write
        cmd_call(
            f"ssh {server} 'mkdir -p {server_path} && cd {server_path} && git init && git config receive.denyCurrentBranch ignore'"
        )

        if existed_remote:
            cmd_call(f"git remote set-url {remote_name} ssh://{server}:{server_path}/.git")
        else:
            cmd_call(f"git remote add {remote_name} ssh://{server}:{server_path}/.git")

    cmd_call(f"git push -u -f {remote_name} {branch}")
    cmd_call(f"ssh {server} 'cd {server_path} && git reset --hard HEAD'")
    assert compare_local_and_remote(server, server_path)


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('remote', type=str, nargs="?", default=None)

    args = parser.parse_args()
    upload(args.remote)


if __name__ == '__main__':
    main()
