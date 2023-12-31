from app import db
from app.models.category import Category
from app.models.comment import Comment
from app.models.poem import Poem
from app.models.theme import Theme
from app.models.user import User


class DBStorage(object):
    """Database Storage class containing methods
    for interacting with the database.
    """

    __session = db.session

    classes = {
        "Category": Category,
        "Comment": Comment,
        "Poem": Poem,
        "Theme": Theme,
        "User": User,
    }

    # def __init__(self, db):
    #     self.__session = db.session

    def all(self, cls=None):
        """Return all objects on current database session of class cls.
        If cls is None return all objects.

        Args:
            cls (class): Class of the objects to return. Defaults to None.
        """
        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for value in self.classes.values():
                objs.extend(self.__session.query(value).all())

        return {f"{obj.__class__.__name__}.{obj.id}": obj for obj in objs}

    def new(self, obj):
        """Add obj to the current database session

        Args:
            obj (object): Object to add to the session
        """

        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session if not none.

        Args:
            obj (object): Object to delete. Defaults to None.
        """

        if obj:
            self.__session.delete(obj)

    def get(self, cls, id):
        """Retrieve one object.

        Args:
            cls (class): Class of the object.
            id (str) : Object ID.

        Returns:
            obj : Object based on cls and id,
                or None if not found.
        """
        retrieved_obj = None
        new_dict = self.all(cls)
        for obj in new_dict.values():
            if obj.id == id:
                retrieved_obj = obj

        return retrieved_obj

    def count(self, cls=None):
        """count the number of object in storage

        Args:
            cls (class, optional): Class. Defaults to None.

        Returns:
            int : number of objects in storage matching the given class.
                If no class is passed, returns the count of all objects in
                storage.
        """
        if cls:
            count = len(self.all(cls).values())
        else:
            count = len(self.all().values())

        return count
