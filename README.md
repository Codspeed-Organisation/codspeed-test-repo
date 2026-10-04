# CodSpeed Playground

A small Python repository for trying CodSpeed with **synthetic data only**.
It contains order-processing code, 10 correctness tests, six benchmark cases,
and a GitHub Actions workflow. No database, real payments or external dataset
is required.

## Upload from a Mac, without installing developer tools

1. Unzip `codspeed-playground.zip`, then open the extracted folder in Finder.
2. Sign in to GitHub in your browser. Create a **private** repository named
   `codspeed-playground`, leaving the README, .gitignore and license options off.
3. On the empty repository page, choose **uploading an existing file**.
4. In the extracted folder in Finder, press **Command + Shift + .** to show
   hidden items. Select the contents inside the folder, including `.github`
   and `.gitignore`, and drag them into GitHub's upload area. Upload the
   contents, not the ZIP or the outer `codspeed-playground` folder.
5. Check that `.github/workflows/codspeed.yml` is in the upload list, and
   `playground.py` is at the repository root. Commit the files to `main`.
6. Continue with the CodSpeed setup below. The first workflow may fail until
   you import/authorize the repository in CodSpeed; rerun it after setup.

## Connect it to CodSpeed

1. Sign in to https://app.codspeed.io/ using the GitHub account that owns or can
   access this repository.
2. Import this repository. If it is missing, grant the CodSpeed GitHub App access
   to it, then return to CodSpeed and import it.
3. Open this repository's **Actions → CodSpeed Benchmarks**. If the initial
   push run failed before import, open that run and choose **Re-run all jobs**.
   A successful push run on `main` establishes the baseline for PR comparisons.
   **Run workflow → main** is also available for additional manual smoke runs.
4. Wait for the workflow to finish, then open the repository in CodSpeed.
   You should see six benchmarks and profiling data from a simulation run.
5. Connect the CodSpeed plugin using the same account and ask it to list
   repositories and inspect the latest completed run.

The workflow uses GitHub OIDC (`id-token: write`), so it does not need a
`CODSPEED_TOKEN` secret. Importing/authorizing the repository is still required.
The first run can fail if the workflow starts before that setup is complete;
rerun it after importing. GitHub Actions usage follows your GitHub plan.

## Try these prompts

- List this repository's latest CodSpeed runs and explain its benchmarks.
- Inspect the large customer-totals benchmark flamegraph. Where is the hotspot?
- Optimize `totals_by_customer` without changing its output. Run correctness
  tests, create a branch/PR, then compare its completed benchmark run to `main`.
- Explain the performance impact of that PR using completed base/head runs.

`totals_by_customer` deliberately scans orders repeatedly, giving an agent a
real optimisation exercise. The other functions provide comparison workloads.
Results and gains are not pre-generated. Comparing releases/PRs requires at
least two completed, comparable runs.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
python -m pytest benchmarks --codspeed -q
```

The last command smoke-tests the benchmark harness. It does not by itself
produce an uploaded simulation report outside an instrumented CodSpeed runtime.
Use the GitHub workflow for the actual profiles and reporting.

## Files

- `playground.py`: synthetic data and three functions to inspect/optimise.
- `tests/`: correctness checks that should remain green after optimisation.
- `benchmarks/`: small/large workloads, with input setup outside measurements.
- `.github/workflows/codspeed.yml`: correctness checks and CodSpeed simulation
  on `main` pushes, pull requests and manual runs.

## Team access

For shared team membership, CodSpeed follows your GitHub/GitLab organisation.
A personal repository is suitable for an initial solo test; do not assume it
creates an organisation or adds other users automatically.

## Official setup references

- https://codspeed.io/docs/benchmarks/python
- https://codspeed.io/docs/integrations/ci/github-actions
- https://codspeed.io/docs/features/roles-and-permissions
