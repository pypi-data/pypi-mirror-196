


class Element:
    @property
    def total(self):
        return len(self)

    def nan_count(self):
        return self.isnull().sum()

    def dup_count(self):
        return self.duplicated().sum() 