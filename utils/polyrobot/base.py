class Deserializable:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def deserialize(cls, data: dict):
        return cls(**data)
