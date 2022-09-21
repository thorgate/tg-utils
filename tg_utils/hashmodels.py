from django.conf import settings

from hashids import Hashids


class ModelHashIdMixin:
    """Easy hashids for Django models.

    To use in your model, inherit it from this class, in addition to models.Model
    Then user obj.hashid property or cls.pk_from_hashid() function

    """

    @classmethod
    def get_hashids_object(cls):
        salt = cls.__name__ + settings.SECRET_KEY[:20]
        return Hashids(salt=salt, min_length=12)

    @classmethod
    def pk_from_hashid(cls, hashid):
        return cls.get_hashids_object().decode(hashid)[0]

    @property
    def hashid(self):
        return self.get_hashids_object().encode(self.id)
