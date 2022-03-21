class Deserializable:
    @classmethod
    def deserialize(cls, data: dict):
        return cls(**data)
