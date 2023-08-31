import pogoapi


class Type:

    def __init__(self, type):
        self.type = type.capitalize()

    def __str__(self):
        return self.type

    def __repr__(self):
        return f'Type("{self.type}")'

    def __eq__(self, other):
        return self.type == str(other).capitalize()

    def __hash__(self):
        return self.type.__hash__()

    def _get_types_by_effectiveness(self, effectiveness):
        db = pogoapi.get_type_effectiveness()
        return [Type(key)
                for key, value in db[self.type].items()
                if value == effectiveness]

    def super_effective(self):
        return self._get_types_by_effectiveness(1.6)

    def normal(self):
        return self._get_types_by_effectiveness(1.0)

    def not_very_effective(self):
        return self._get_types_by_effectiveness(0.625)

    def ineffective(self):
        return self._get_types_by_effectiveness(0.390625)
