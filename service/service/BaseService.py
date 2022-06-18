from abc import ABC,abstractclassmethod, abstractmethod

class BaseService(ABC):
    
    def __init__(self):
        self.pageSize=5
        print("0")

    
    def get(self,rid):
        try:
            r=self.get_model().objects.get( id=rid)
            return r
        except self.get_model().DoesNotExist:
            return None
    
    
    def search(self):
        try:
            r=self.get_model().objects.all()
            return r
        except self.get_model().DoesNotExist:
            return None
    
    
    def preload(self,rid):
        try:
            r=self.get_model().objects.all()
            return r
        except self.get_model().DoesNotExist:
            return None

    
    def save(self,mobj):
        print("----baseService mobj",mobj)
        if(mobj.id == 0):
            mobj.id = None
        mobj.save()
        
    
    def delete(self,rid):
        r= self.get(rid)
        r.delete()
    
    
    def find_by_unique_key(self,rid):
        try:
            r=self.get_model().objects.get(id=rid)
            return r
        except self.get_model().DoesNotExist:
            return None
    
    
    @abstractmethod
    def get_model(self):
        pass