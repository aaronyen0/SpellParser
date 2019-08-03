import pickle

class ObjPickleSaveLoad:
    """
    object save or load by pickle
    """

    def __init__(self, file_name: str, obj_type = None):
        """
        Args:
            file_name(str): the filename we want to save or load
            obj_type: I will check obj_type if it is not None
        """

        self.file_name = file_name
        self.obj_type = obj_type


    def obj_save(self, my_obj):
        """
        svae the my_obj into a file
        
        Args:
            my_obj: the object we want to save

        Returns:
            True / False: return True if we successfully save the object, otherwise return Flase
        """

        if self.obj_type and type(my_obj) != self.obj_type:
            return False

        try:
            fp = open(self.file_name, 'wb')
            pickle.dump(my_obj, fp)
            fp.close()
            return True
        except:
            return False


    def obj_load(self):
        """
        load an object from a file
        
        Returns:
            my_obj / None: return my_obj if we successfully load an object from a file, 
                           otherwise return None
        """

        try:
            fp = open(self.file_name, 'rb')
            my_obj = pickle.load(fp)
            fp.close()
            if self.obj_type and type(my_obj) != self.obj_type:
                return None
            return my_obj
        except:
            return None

