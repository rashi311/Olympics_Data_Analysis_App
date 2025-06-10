import pandas as pd
import pyarrow


def preprocess(df, region_df):
    # Filter Summer Olympics
    df = df[df['Season'] == 'Summer'].copy()

    # Merge with region data
    df = df.merge(region_df, on='NOC', how='left')

    # Fill missing regions
    df['region'] = df['region'].fillna('Unknown')

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # One-hot encode Medal column
    medal_dummies = pd.get_dummies(df['Medal'])
    df = pd.concat([df, medal_dummies], axis=1)

    # Ensure all medal columns exist
    for medal in ['Gold', 'Silver', 'Bronze']:
        if medal not in df.columns:
            df[medal] = 0

    return df