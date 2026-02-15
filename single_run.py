import subprocess
import time
from pathlib import Path

import numpy as np
import pandas as pd

DF_URL = "http://tmp-borza-public-cyx.s3.amazonaws.com/imdb-comp.csv.gz"

RUNS_DIR = Path("runs")
SOLUTIONS_DIR = Path("solutions")

TEST_DATA_PATH = Path("full-df.csv.gz")

coord_cols = ["x", "y"]
output_cols = [f"top{i}_{c}" for i in range(1, 4) for c in ["title", "id"]]


def load_test_df():
    if TEST_DATA_PATH.exists():
        return pd.read_csv(TEST_DATA_PATH)
    df = pd.read_csv(DF_URL)
    df.to_csv(TEST_DATA_PATH, index=False)
    return df


def main(solution: str, in_n: int = 1_000, q_n: int = 10, comparison="", seed=742):
    s_path = Path(SOLUTIONS_DIR, solution)
    assert s_path.exists()

    rng = np.random.RandomState(seed)
    in_p, q_p, out_p = map(s_path.joinpath, ["input.csv", "query.csv", "out.csv"])

    test_df = load_test_df()

    def call(comm):
        start_time = time.time()
        subprocess.call(["make", comm], cwd=s_path.as_posix())
        return time.time() - start_time

    def dump_input():
        test_df.sample(in_n, random_state=rng).to_csv(in_p, index=False)

    def dump_query():
        q_basis = test_df.loc[:, coord_cols].sample(q_n, random_state=rng)
        modified_q = q_basis + rng.normal(
            0, q_basis.std().mean() / 50, size=q_basis.shape
        )
        modified_q.to_csv(q_p, index=False)

    logs = [f"inputs: {in_n}", f"queries: {q_n}"]
    for comm, prep in [
        ("setup", lambda: None),
        ("preproc", dump_input),
        ("compute", dump_query),
    ]:
        prep()
        stime = call(comm)
        logs.append("{}: {:.6f}".format(comm, stime))
    in_p.unlink()
    q_p.unlink()
    call("cleanup")

    try:
        out_df = pd.read_csv(out_p)
    except:
        print(f"ERROR: could not read {out_p} to csv")
        return

    assert (
        out_df.columns.tolist() == output_cols
    ), f"output columns: {out_df.columns} are not {output_cols}"

    on = out_df.shape[0]
    assert on == q_n, f"output length ({on}) is not {in_n}"

    if comparison:
        main(comparison, in_n, q_n, seed)
        comp_df = pd.read_csv(SOLUTIONS_DIR / comparison / out_p.name)
        misses = (comp_df != out_df).any(axis=1)
        if misses.any():
            print("missed some values")
            print(f"{solution} output:")
            out_df.loc[misses, :]
            print(f"{comparison} output:")
            comp_df.loc[misses, :]

    logstr = "\n".join(logs)

    Path(f"{RUNS_DIR}/{time.time()}-{solution}").write_text(logstr)
    print("\n\nsuccess!", f"solution: {solution}")
    print(logstr)
    return logs
