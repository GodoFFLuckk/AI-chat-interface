import pandas as pd

def filter_df(df: pd.DataFrame, column: str, operator: str, value) -> pd.DataFrame:
    if operator == "==":
        return df[df[column] == value]
    elif operator == "!=":
        return df[df[column] != value]
    elif operator == ">":
        return df[df[column] > value]
    elif operator == "<":
        return df[df[column] < value]
    elif operator == ">=":
        return df[df[column] >= value]
    elif operator == "<=":
        return df[df[column] <= value]
    else:
        raise ValueError(f"Unsupported operator: {operator}")

def apply_filter_subarray(df: pd.DataFrame, transformations: list[dict]) -> pd.DataFrame:
    new_df = df
    for step in transformations:
        op = step["operation"]
        if op == "filter":
            new_df = filter_df(new_df, step["column"], step["operator"], step["value"])
        else:
            raise ValueError(f"Unexpected operation {op} in filter-only subarray")
    return new_df

def apply_select_subarray(df: pd.DataFrame, transformation: dict) -> pd.DataFrame:
    if transformation[0]["operation"] == "select":
        return df[transformation[0]["columns"]]
    else:
        return df


def apply_transformations(df: pd.DataFrame, transformations_list: list[list[dict]]) -> pd.DataFrame:
    if not transformations_list:
        return df

    filter_subarrays = transformations_list[:-1]
    select_subarray = transformations_list[-1]

    partial_results = []
    for subarray in filter_subarrays:
        filtered_df = apply_filter_subarray(df, subarray)
        partial_results.append(filtered_df)

    if partial_results:
        concatenated = pd.concat(partial_results, ignore_index=True)
    else:
        concatenated = df.copy()
    concatenated = concatenated.drop_duplicates()
    final_df = apply_select_subarray(concatenated, select_subarray)

    return final_df