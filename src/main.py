import pandas as pd
import argparse
from gpt_communication import get_transformations_from_gpt
from transformations import apply_transformations

def load_data(file_path: str) -> pd.DataFrame:
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV file.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datafile", type=str, help="Path to the input data file (CSV or JSON).")
    parser.add_argument("--userprompt", type=str, help="User prompt describing the transformations.")
    args = parser.parse_args()
    
    if (args.datafile and not args.userprompt) or (args.userprompt and not args.datafile):
        print("Error: You must specify both --datafile and --userprompt, or use defaults.")
        return

    default_data = {
        "name": ["Sviatoslav", "Airat", "Alikhan", "Nikita"],
        "age": [22, 102, 22, 27],
        "salary": [50000, 60000, 70000, 100000]
    }
    default_prompt = """You have a dataframe with {columns} columns. 
                        Filter rows where either (age>23 AND salary>45000) OR salary==50000.
                        Select first column and column \"name\".
                     """

    if args.datafile and args.userprompt:
        try:
            df = load_data(args.datafile)
            user_query = f"You have a dataframe with {df.columns} columns. {args.userprompt}"
        except Exception as e:
            print(f"Error loading data file: {e}")
            return
    else:
        df = pd.DataFrame(default_data)
        columns = list(df.columns)
        user_query = default_prompt.format(columns=columns)

    print("User Query:")
    print(user_query)

    transformations = get_transformations_from_gpt(user_query)

    result_df = apply_transformations(df, transformations)

    print("Result:")
    print(result_df)

if __name__ == "__main__":
    main()
