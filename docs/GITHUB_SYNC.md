# GitHub Sync Notes

This project is intended to be mirrored to both:

- Personal remote: `https://github.com/madnaelo/ejari-workflows-automation.git`
- Company remote: `https://github.com/Datacell-Solutions/Dubai-Now.git`

Current local branch should be `main`.

Suggested remotes:

```powershell
git remote -v
git remote add datacell https://github.com/Datacell-Solutions/Dubai-Now.git
```

Push both remotes:

```powershell
git push madnaelo main
git push datacell main
```

If GitHub returns `Repository not found`, confirm:

- the repository URL is correct,
- the GitHub account on this machine has access,
- the account is `aqeel-datacell`,
- SSO is authorized if the organization requires it.
