from pprint import pprint


class HelperLocation:

    location: dict = {}

    settlement_type: str = None  # тип поселения (город, село)
    settlement_name: str = None  # название поселения
    full_name_settlement: str = None
    region_name: str = None  # название региона
    region_type: str = None  # тип региона
    district: str = None  # район
    district_full_name: str = None
    district_type: str = None
    full_name_region: str = None  # полное название

    def __init__(self, location: str):
        self.set_location(location)
        self.location["full_adress"] = location
        self.get_location()

    def set_location(self, text: str):
        list_location = text.split(", ")
        for item in list_location:
            if "край" in item or "обл." in item:
                if "автономная" in item:
                    self.region_name = item.split("автономная обл.")[0]  #
                    self.region_type = "Автономная область"
                    self.full_name_region = item
                else:
                    self.region_name = item.split(" ")[0]  #
                    self.region_type = item.split(" ")[1]
                    self.full_name_region = item
            if "Республика " in item:
                self.region_name = item.split(" ")[1]  #
                self.region_type = item.split(" ")[0]
                self.full_name_region = item
            if " Республика" in item:
                self.region_name = item.split(" ")[0]  #
                self.region_type = item.split(" ")[1]
                self.full_name_region = item

            if " р-н" in item:
                self.district = item.split(" ")[0]
                self.district_type = "район"
                self.district_full_name = f"{self.district} {self.district_type}"
            if "станица " in item:
                self.settlement_type = item.split(" ")[0]  #
                self.settlement_name = item.split(" ")[1]
                self.full_name_settlement = item
            if "с. " in item:
                self.settlement_type = "село"  #
                self.settlement_name = item.split(" ")[1]
                self.full_name_settlement = (
                    f"{self.settlement_type} {self.settlement_name}"
                )
            if "д. " in item:
                self.settlement_type = "деревня"  #
                self.settlement_name = item.split(" ")[1]
                self.full_name_settlement = (
                    f"{self.settlement_type} {self.settlement_name}"
                )
            if "хутор" in item:
                self.settlement_type = item.split(" ")[0]  #
                self.settlement_name = item.split(" ")[1]
                self.full_name_settlement = item
            if "пгт. " in item:
                self.settlement_type = "посёлок городского типа"
                self.settlement_name = item.split(" ")[1]
                self.full_name_settlement = (
                    f"{self.settlement_type} {self.settlement_name}"
                )

    def get_location(self):
        self.location["region"] = {
            "region_type": self.region_type,
            "region_name": self.region_name,
            "full_name_region": self.full_name_region,
        }
        self.location["settlement"] = {
            "settlement_type": self.settlement_type,
            "settlement_name": self.settlement_name,
            "full_name_settlement": self.full_name_settlement,
        }
        self.location["district"] = {
            "district": self.district,
            "district_full_name": self.district_full_name,
            "district_type": self.district_type,
        }


# obj = HelperLocation(
#     "Краснодарский край, муниципальное образование Анапа, станица Анапская"
# )
# pprint(obj.location)

# obj1 = HelperLocation(
#     "Республика Крым, Бахчисарайский р-н, Железнодорожненское сельское поселение, с. Речное"
# )
