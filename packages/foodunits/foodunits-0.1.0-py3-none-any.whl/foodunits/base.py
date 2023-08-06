from foodunits.utils.units import Convert_Dict
from foodunits.exceptions import ConversionFailure

class FoodUnitConvertor:
    """Class contains mainly food conversion functions."""
    # Assign the available dictionary
    metric_dict = Convert_Dict.metric_dict()
    imperial_vol_dict = Convert_Dict.imperial_vol_dict()
    imperial_mass_dict = Convert_Dict.imperial_mass_dict()
    physical_container_unit = {
        "cup": Convert_Dict.cup_by_country_dict(),
        "teaspoon": Convert_Dict.teaspoon_by_country_dict(),
        "tablespoon": Convert_Dict.tablespoon_by_country_dict()
    }

    def __init__(
        self,
        value,
        units_from: str,
        units_to: str,
        density: float = None,
        country: str = "US",
        decimal_places: int = None,
        **kwargs
    ):
        """Initialization"""
        self.value = value
        self.units_from = units_from
        self.units_to = units_to
        self.decimal_places = decimal_places
        self.density = density
        self.country = country
        self.metric_units_from = units_from[:-1] if len(units_from) > 1 else None
        self.metric_units_to = units_to[:-1] if len(units_to) > 1 else None
        self.__dict__.update(kwargs)

    def check_metric_imperial(self):
        """
        Conversion between metric and imperial units.
        """
        converted_value = None
        # Metric and Imperial volumes （metric volumetric units should be l and m³)
        if self.metric_units_from in self.metric_dict and self.units_to in self.imperial_vol_dict:
            metric_base = self.metric_dict.get(self.metric_units_from, None)
            imperial_base = self.imperial_vol_dict.get(self.units_to, None)
            converted_value = self.metric_to_imperial(self.value, metric_base, imperial_base, 33.814)
            # Mass to volume
            if "g" in self.units_from:
                converted_value = self.volume_mass_conversion(converted_value, self.density, vol_to_mass=False)

        elif self.units_from in self.imperial_vol_dict and self.metric_units_to in self.metric_dict:
            imperial_base = self.imperial_vol_dict.get(self.units_from, None)
            metric_base = self.metric_dict.get(self.metric_units_to, None)
            converted_value = self.imperial_to_metric(self.value, metric_base, imperial_base, 0.0295735)
            # Volume to mass
            if "g" in self.units_to:
                converted_value = self.volume_mass_conversion(converted_value, self.density, vol_to_mass=True)

        # Metric and Imperial masses （metric mass units should be g, but exception is l or m³)
        elif self.metric_units_from in self.metric_dict and self.units_to in self.imperial_mass_dict:
            metric_base = self.metric_dict.get(self.metric_units_from, None)
            imperial_base = self.imperial_mass_dict.get(self.units_to, None)
            # Volume to mass
            if "l" in self.units_from:
                converted_value = self.metric_to_imperial(
                    self.volume_mass_conversion(self.value, self.density, vol_to_mass=True),
                    metric_base, imperial_base, 0.00220462
                )
            else:
                converted_value = self.metric_to_imperial(self.value, metric_base, imperial_base, 0.00220462)

        elif self.units_from in self.imperial_mass_dict and self.metric_units_to in self.metric_dict:
            imperial_base = self.imperial_mass_dict.get(self.units_from, None)
            metric_base = self.metric_dict.get(self.metric_units_to, None)
            converted_value = self.imperial_to_metric(self.value, metric_base, imperial_base, 453.592)
            # Mass to volume
            if "l" in self.units_to:
                converted_value = self.volume_mass_conversion(converted_value, self.density, vol_to_mass=False)

        if converted_value:
            return {
                "converted value": round(converted_value, self.decimal_places),
                "unit": self.units_to
            }
        else:
            return False

    def check_physical_container_unit(self):
        """
        Conversion from or to physical container units, e.g. cup to ml, or vice versa.
        """
        if not self.units_from in self.physical_container_unit and not self.units_to in self.physical_container_unit:
            return False
        #TODO Add converstion from cup to teaspoon/tablespoon etc.
        if self.units_from in self.physical_container_unit and self.units_to in self.physical_container_unit:
            raise ConversionFailure(
                    f"""
                    Can not convert between cup, teaspoon and tablespoon yet. To be added...
                    """
                )

        converted_value = None
        if self.units_from in self.physical_container_unit.keys():
            country_base = self.physical_container_unit[self.units_from].get(self.country, None)

            # No country is found
            if not country_base:
                raise ConversionFailure(
                    f"""
                    The converted units involve physical containers, such as cup, teaspoon, or tablespoon, which depend on the country.
                    Provide the accepted value from the followings(or corresponding full name) for the "country" argument:
                        {self.physical_container_unit[self.units_from].keys()}
                    """
                )

            if self.units_to in self.imperial_vol_dict:
                imperial_base = self.imperial_vol_dict.get(self.units_to, None)
                # convert cup etc. to liter first, then other imperial units
                converted_ml = self.value * country_base
                converted_value =  self.metric_to_imperial(converted_ml, 1, imperial_base, 33.814)

            elif self.metric_units_to in self.metric_dict:
                metric_base = self.metric_dict.get(self.metric_units_to, None)
                converted_value = country_base * self.value / metric_base

                if "g" in self.units_to:
                    converted_value = self.volume_mass_conversion(converted_value, self.density, vol_to_mass=True)

        if self.units_to in self.physical_container_unit.keys():
            country_base = self.physical_container_unit[self.units_to].get(self.country, None)

            # No country is found
            if not country_base:
                raise ConversionFailure(
                    f"""
                    The converted units involve physical containers, such as cup, teaspoon or tablespoon which is country-matters.
                    Provide the accepted value for argument "country":
                        {self.physical_container_unit[self.units_to].keys()}
                    """
                )

            if self.units_from in self.imperial_vol_dict:
                # convert imperial units to liter first, then cup etc.
                imperial_base = self.imperial_vol_dict.get(self.units_from, None)
                converted_value = self.imperial_to_metric(self.value, 1, imperial_base, 0.0295735) / country_base

            elif self.metric_units_from in self.metric_dict:
                metric_base = self.metric_dict.get(self.metric_units_from, None)
                # convert to volume first
                if "g" in self.units_from:
                    converted_value = self.volume_mass_conversion(self.value, self.density, vol_to_mass=False) * metric_base / country_base
                else:
                    converted_value = self.value * metric_base / country_base



        if converted_value:
            return {
                "converted value": round(converted_value, self.decimal_places),
                "unit": self.units_to
            }
        else:
            return False

    @staticmethod
    def volume_mass_conversion(value, density, vol_to_mass: bool = True):
        """
        Convert between mass and volume using a certain density.
        """
        if vol_to_mass:
            result = 1000 * value * density
        else:
            result = value / (1000 * density)
        return result

    @staticmethod
    def metric_to_imperial(value, metric_base, imperial_base, imperial_multiplier):
        """
        Convert from metric to imperial units.
        """
        return value * metric_base * imperial_multiplier / imperial_base

    @staticmethod
    def imperial_to_metric(value, metric_base, imperial_base, metric_multiplier):
        """
        Convert from imperial to metric units.
        """
        return value * imperial_base * metric_multiplier / metric_base

    @staticmethod
    def metric_to_metric(value, metric_base, metric_multiplier):
        """
        Convert between metric units.
        """
        return value * metric_base * metric_multiplier
