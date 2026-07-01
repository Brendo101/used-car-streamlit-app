import pandas as pd

def load_and_clean_data(path: str):
    df = pd.read_csv(path)


    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("\u00A0", "", regex=False)
            )

   
    url_parts = df["url"].astype(str).str.split("/", expand=True)

    # Expected structure:
    # /car-for-sale/{make}/{model}/{variant}/{id}

    df["make"] = url_parts[4]
    df["model"] = url_parts[5]

    # Clean formatting
    df["make"] = (
        df["make"]
        .str.replace("-", " ", regex=False)
        .str.title()
    )

    df["model"] = (
        df["model"]
        .str.replace("-", " ", regex=False)
        .str.title()
    )

  
    df["year"] = pd.to_numeric(
        df["title"].str.extract(r"^(\d{4})")[0],
        errors="coerce"
    )

  
    df["variant"] = (
        df["variant"]
        .astype(str)
        .str.replace("nan", "", regex=False)
        .str.strip()
    )

   
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("\u00A0", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace("R", "", regex=False)
        .str.replace("POA", "", regex=False)
    )

    df["price"] = pd.to_numeric(df["price"], errors="coerce")


    df["mileage"] = (
        df["mileage"]
        .astype(str)
        .str.replace("\u00A0", "", regex=False)
        .str.replace("km", "", regex=False)
        .str.replace(" km", "", regex=False)
        .str.replace("N/A", "", regex=False)
        .str.strip()
    )

    df["mileage"] = pd.to_numeric(df["mileage"], errors="coerce")

  
    df["scraped_at"] = pd.to_datetime(
        df["scraped_at"],
        errors="coerce"
    )

  
    location_split = df["location"].astype(str).str.split(",", n=1, expand=True)

    df["city"] = location_split[0].str.strip()
    df["region"] = location_split[1].str.strip()

  
    df = df.drop_duplicates(subset=["url"])

    return df