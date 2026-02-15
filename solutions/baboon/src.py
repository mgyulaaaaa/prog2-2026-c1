import pandas as pd

if __name__ == "__main__":

    df = pd.read_csv("input.csv")
    query_df = pd.read_csv("query.csv")

    out = []
    for idx, row in query_df.iterrows():

        diffs = df[["x", "y"]] - row
        squares = diffs**2
        dists = squares.sum(axis=1) ** 0.5

        out_dic = {}
        for i in range(3):
            ith_closest_idx = dists.sort_values().index[i]
            out_dic[f"top{i+1}_title"] = df.loc[ith_closest_idx, "title"]
            out_dic[f"top{i+1}_id"] = df.loc[ith_closest_idx, "imdb_id"]

        out.append(out_dic)

    pd.DataFrame(out).to_csv("out.csv", index=False)
