import pandas as pd

TRUE_FALSE = ['DSL', 'Fiber optic', 'Bank transfer (automatic)', 'Credit card (automatic)',
              'Electronic check', 'automatic_pay', 'HasInternet']

YES_NO = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling', 'Churn']

INTERNET_VARS = ['StreamingMovies', 'StreamingTV', 'TechSupport', 'DeviceProtection', 'OnlineSecurity', 'OnlineBackup']

TRUE_FALSE_MAPPING = {True : 1, False : 0}

YES_NO_MAPPING = {'Yes' : 1, 'No' : 0}

INTERNET_VARS_MAPPING = {'No internet service' : 0, 'No' : 0, 'Yes' : 1}

DUMMIES_VARS = ['InternetService','PaymentMethod']

TO_DROP = ['No','Mailed check']

TO_SCALE = ['tenure','MonthlyCharges','TotalCharges']

def mapping(df: pd.DataFrame,
            columns: list[str],
            mapping_dict: dict) -> pd.DataFrame:
    """
    Apply value mapping to specific columns in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame to be transformed.
    columns : list[str]
        List of column names to apply the mapping to.
    mapping_dict : dict
        Dictionary defining the mapping (e.g., {'Yes': 1, 'No': 0}).

    Returns
    -------
    pd.DataFrame
        Transformed DataFrame with specified columns mapped.
    """
    for col in columns:
        df[col] = df[col].map(mapping_dict)
    
    return df


def dummies(df: pd.DataFrame,
            columns: list[str],
            to_drop: list[str],
            prefix: str = '',
            prefix_sep: str = '') -> pd.DataFrame:
    """
    Create one-hot encoded dummy variables for categorical columns and drop unwanted features.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame to be transformed.
    columns : list[str]
        List of categorical columns to convert into dummy variables.
    to_drop : list[str]
        List of column names (after encoding) to drop from the DataFrame.
    prefix : str, optional
        String to append as a prefix to new dummy variable names (default is '').
    prefix_sep : str, optional
        Separator between prefix and dummy variable names (default is '').

    Returns
    -------
    pd.DataFrame
        Transformed DataFrame with dummy variables created and specified columns dropped.
    """
    df = pd.get_dummies(df,
                        columns=columns,
                        prefix=prefix,
                        prefix_sep=prefix_sep)

    df.drop(to_drop, axis=1, inplace=True, errors='ignore')
    
    return df