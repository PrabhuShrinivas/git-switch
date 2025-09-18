# git-switch

Effortlessly manage multiple Git identities and SSH keys. Generate keys, save per-profile Git name/email, and switch profiles in one command. Auto-updates ~/.ssh include and your global Git config for GitHub/GitLab.

## Usage

After installing the project in a virtual environment, run:

```bash
git-switch
```

You should see:

```text
Hello from git-switch 👋

## SSH profiles utility

Manage multiple Git SSH accounts and switch keys quickly.

### Setup

```bash
git-switch ssh init
```

### Version

Print the installed version:

```bash
git-switch --version
```

This creates a managed include at `~/.ssh/git-switch-managed.conf` and ensures your `~/.ssh/config` includes it.

### Add a profile

Generate a new ed25519 key managed by this tool:

```bash
git-switch ssh add --name personal --email you@example.com --generate
```

If a key already exists at the generated path, either remove it or force overwrite:

```bash
git-switch ssh add --name personal --email you@example.com --generate --force
```

Or use an existing private key:

```bash
git-switch ssh add --name work --key-path ~/.ssh/id_ed25519_work --hosts github.com,gitlab.com
```

View the public key path printed, and add it to GitHub/GitLab.

### List profiles

```bash
git-switch ssh list
```

### Activate a profile

```bash
git-switch ssh use --name work                  # applies Git identity globally
```

This updates `~/.ssh/git-switch-managed.conf` with the selected key for configured hosts.

### Remove a profile

```bash
git-switch ssh remove --name personal
# To also delete generated keys (only if under the managed directory):
git-switch ssh remove --name personal --delete-keys --force
```

Profiles are stored at `~/.config/git-switch/profiles.json`. Generated keys live under `~/.ssh/git-switch/<profile>/`.

### Store Git identity on profile

You can save Git identity per profile during add:

```bash
git-switch ssh add --name work --key-path ~/.ssh/id_ed25519_work --git-name "Your Work Name" --git-email your.name@company.com
```

When you run `ssh use`, the saved Git identity is applied automatically to your global Git config.

### Update a profile's Git identity

```bash
git-switch ssh update --name personal --git-name "New Name" --git-email new@example.com
```
Then apply it:
```bash
git-switch ssh use --name personal
```

### Copy a profile's public key

Copy a profile's public key to your clipboard for adding to GitHub/GitLab:

```bash
git-switch copy-key personal   # copy 'personal' profile's public key
git-switch copy-key            # copy the active profile's public key
```

This uses your OS clipboard tool (pbcopy on macOS, wl-copy/xclip on Linux, clip on Windows). If unavailable, the key is printed to stdout.

## HTTPS (PAT) profiles utility

Manage Git over HTTPS using Personal Access Tokens stored via Git's credential helper.

### Add a PAT profile

Provide your token via stdin (recommended):

```bash
printf "%s" "$GITHUB_TOKEN" | git-switch pat add \
  --name work-https \
  --username your-username \
  --hosts github.com \
  --token-stdin \
  --git-name "Your Work Name" \
  --git-email your.name@company.com
```

Or pass it directly:

```bash
git-switch pat add --name personal-https --username your-username --hosts github.com \
  --token "$GITHUB_TOKEN"
```

This stores the token in your configured Git credential helper (e.g., osxkeychain/libsecret/manager-core).

### List and activate PAT profiles

```bash
git-switch pat list
git-switch pat use --name work-https
```

Note: PAT auth works with HTTPS remotes. Convert SSH remotes as needed:

```bash
git remote set-url origin https://github.com/<owner>/<repo>.git
```

### Remove a PAT profile

```bash
git-switch pat remove --name work-https
```

This also erases saved credentials for its hosts via the credential helper.

## Development

### Makefile commands

- **Install**: creates/uses a virtual environment and installs the package in editable mode

```bash
make install
# If no venv was active, this will drop you into an interactive shell
# with the venv activated. Exit with Ctrl-D when done.
# To skip opening a shell (CI usage):
# NO_SHELL=1 make install
```

- **Shell in venv**: launches a subshell with the venv activated

```bash
make shell
# Exit with Ctrl-D when done
```

- **Build**: builds sdist and wheel into `dist/`

```bash
make build
```

- **Test with coverage**: runs the full test suite and generates terminal + HTML coverage (`htmlcov/index.html`)

```bash
make test
```

- **Test an individual file or test**: pass FILE to run a specific test file or node id

```bash
make test-file FILE=tests/test_cli.py
make test-file FILE=tests/test_cli.py::test_handle_copy_key_fallback_prints_key
```
