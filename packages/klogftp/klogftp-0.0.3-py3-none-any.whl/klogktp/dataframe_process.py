import unicodedata

# 轉換utf-8
def convert_to_utf8(df):
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.encode('utf-8', errors='ingore').str.decode('utf-8')
    return df

# 刪除特殊字元
def exclude_special_characters(df):
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(lambda x: remove_spacial_character(x))
    return df

def remove_spacial_character(text):
    normalized_text = unicodedata.normalize('NFKD', text)
    stripped_text = ''.join(c for c in normalized_text if not unicodedata.combining(c))
    return stripped_text