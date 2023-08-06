

class Settings:
    def __init__(self) -> None:
        self.order = None
        self.rows_display = 16
        self.decimals_display = 2
        self.oneshot_display = False
        self.keep_zeros = False
        self.sort_coords = False
        self.feather_with = "pandas" # "pandas", "polars"
        self.fill_missing = False
        self.df_with = "pandas"  # "pandas", "polars"

settings = Settings()