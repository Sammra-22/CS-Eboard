class UpdateModelMixin:
    allowed_attributes = {}

    def update(self, **kwargs):
        for key, value in kwargs.items():
            assert key in self.allowed_attributes
            setattr(self, key, value)
        self.save()
