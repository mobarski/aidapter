import pickle
import os


class DummyKV(dict):
    "in-memory key-value store"

    def sync(self):
        pass

    def close(self):
        self.sync()

    def agg(self, mapping):
        if not mapping: return
        for k,v in mapping.items():
            if k not in self:
                self[k] = v
            else:
                self[k] += v


class KV(DummyKV):
    "persistent key-value store (disk-based)"

    def __init__(self, db_dir, label):
        self.db_dir = db_dir
        self.label = label
        self.path = os.path.join(db_dir, label+'.pkl')
        try:
            os.makedirs(db_dir)
        except:
            pass
        if os.path.exists(self.path):
            data = pickle.load(open(self.path,'rb'))
            self.update(data)
    
    def sync(self):
        pickle.dump(dict(self.items()), open(self.path,'wb'))


if __name__=="__main__":
    db = KV('usunmnie','test1')
    #db['a'] = 1
    #db['b'] = 2
    #db.sync()
    print(db)
