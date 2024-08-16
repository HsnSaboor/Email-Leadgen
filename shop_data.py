from shop import Shop
from dataclasses import field, asdict
import pandas as pd
import os

class ShopData:
    """Holds list of establishments and saves to CSV."""
    business_list: list[Shop] = []
    save_at = 'output'

    def dataframe(self):
        return pd.json_normalize(
            (asdict(shop) for shop in self.business_list), sep="_"
        )

    def save_to_csv(self, filename):
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"{self.save_at}/{filename}.csv", index=False)
