# AGENTS.md

## Product and compatibility

This released repository is a local Elasticsearch learning stack, not a PHP package or a production deployment. Docker Compose defines Elasticsearch (single node), Kibana, Nginx and networks; `Makefile` is the host-side convenience interface. `docker-configs/` owns images, templates, startup scripts and the synonym dictionary. Preserve documented configuration names, Make targets, existing bind-mounted Elasticsearch data, and opt-in integration expectations; changes to published access, network membership, version lines, data compatibility or dependencies require an owner decision before implementation. Do not add another service, framework, background job, production orchestration or speculative compatibility layer.

## Code and dependencies

- Use UTF-8, LF, two-space YAML indentation, four-space Bash/Python indentation, and real tabs in Make recipes. Preserve shell dialect and executable bits. Quote expansions, validate inputs at their trust boundary and propagate errors; do not pipe potentially long output into early-exit `grep -q` or `head` under `pipefail`. Keep comments meaningful; do not impose PHP-specific rules on this infrastructure project.
- Use official images and plugins; Elasticsearch and Kibana must have the same exact version for a reproducible run, and plugins must match Elasticsearch. Verify exact tags, supported upgrade paths, maintenance, license and security before proposing version changes. Never use a different base image or an unverified fallback to make a failing build pass. Use exact official tags and native image configuration and entrypoints.

## Security and runtime

- Elasticsearch security is disabled in the existing stack. The base Compose publishes only Nginx on loopback and uses the project backend bridge. Do not expose this configuration to untrusted clients or use real data. Only explicit WITH_EXTERNAL_NETWORK=1 adds Elasticsearch to a pre-existing trusted network. Its members receive unauthenticated access. Network/authentication/TLS defaults require explicit owner approval to change.
- Treat `.docker.env` as trusted local configuration (Make parses it); never read real credentials or run untrusted Make/configuration. Use synthetic data and trusted configurations only. Preserve both data-directory bind mounts and verify existing data compatibility before recreation.
- Before build/start/tests inspect effective users, ownership, resolved Compose project, network membership, ports and storage paths. Use a disposable checkout, unique project/container names, independent data and loopback port. Never touch the owner's running stack, shared network, existing indices or persistent directories. Do not perform broad chmod/chown, delete files or indices, run privileged fixes or production commands. Explicitly identify any targeted destructive test and its disposable resource. Use no real secrets in logs or CI.

## Checks and documentation

- Check Bash syntax, resolved Compose (including the explicit external extension), exact image/plugin versions and HTTP health via Nginx, both virtual hosts, the synthetic index/search and analyzers. Use bounded waits and assertions with full response consumption. CI must preserve failures rather than mask them. Distinguish PASS, FAIL, SKIPPED and NOT VERIFIED. Keep exercises and runtime examples accurate; never claim a screenshot or source inspection proves a successful live test.
- Root `README.md` and `.github/CONTRIBUTING.md` are Russian canon; thematic pages under `docs/langs/ru/`, localized README/CONTRIBUTING and matching guides/reference under `docs/langs/en|es|zh|fr|de/`. All six README files include ordered Source → stack → CI → license badges, language selector, overview, compact Mermaid, self-contained quick start, documentation navigation, GitHub Issues and Discussions feedback, and centered final GitHub-star CTA without emoji. No invented cover; preserve and label historic screenshots in `docs/assets/`. Use matching diagrams, valid links and copyable examples; keep technical values and semantics consistent. Do not change owner-controlled LICENSE/SECURITY/FUNDING without approval.

## Work and Git

Read before writing, define one coherent approved scope and exact allowlist, and triage security impact. Stop for new product, security, data, dependency or compatibility decisions. Preserve unrelated changes; inspect the full diff, run `git diff --check` (and `git diff --cached --check` when staged), and report actual checks and final Git state. Remote policy: `READ_ONLY_FOR_AI`; no commit, push, PR creation/merge, reset, restore, rebase, clean, stash, force, tag/branch deletion, release or production actions by agents without explicit permission. The owner creates a signed tag on the exact verified merge SHA only after green post-merge CI and required gates; verify the actual remote tag target and signature before Release.
