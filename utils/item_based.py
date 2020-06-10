import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def getDataframe(query, database, recent_id):
    df = pd.read_sql(query, database)
    df_rearranged = df.pivot_table('history_count', index='interest_id', columns='user_id').fillna(0)
    item_based_collabor = cosine_similarity(df_rearranged)

    item_based = pd.DataFrame(data=item_based_collabor, index=df_rearranged.index, columns=df_rearranged.index)
    # print(item_based[interest_name].index)
    new_df = item_based[recent_id].reset_index()

    new2_df = new_df.sort_values(by=recent_id, ascending=False)
    # print(new2_df)
    # print(type(new2_df))
    # print(new2_df.iloc[1,0])

    return new2_df.iloc[1, 0]