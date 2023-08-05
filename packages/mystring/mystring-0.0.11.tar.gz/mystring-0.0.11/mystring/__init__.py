class string(str):
    def rep(self,substring):
        self = string(self.replace(substring,''))
        return self

    def repsies(self,*args):
        for arg in args:
            self = self.rep(arg)
        return self

    def ad(self, value):
        self = string(self + getattr(self, 'delim', "")  + value)
        return self

    def delim(self, value):
        self.delim = value

    def pre(self, value):
        self = string(value + getattr(self, 'delim', "")  + self)
        return self

    def pres(self, *args):
        for arg in args:
            self = self.pre(arg)
        return self

    @property
    def empty(self):
        return self is None or self.strip() == '' or self.strip().lower() == 'nan'

    @property
    def notempty(self):
        return not self.empty

    def format(self, numstyle='06'):
        return format(int(self),numstyle)

    def splitsies(self,*args,joiner=":"):
        output_list = []
        for splitter_itr, splitter in enumerate(args):
            if splitter_itr == 0:
                output_list = self.split(splitter)
            else:
                temp_list = string(joiner.join(output_list)).splitsies(splitter,joiner=joiner)
                output_list = []
                for temp_item in temp_list:
                    for temp_split_item in temp_item.split(joiner):
                        output_list.append(temp_split_item)

        return output_list

    def tohash(self, hash_type='sha512', encoding='utf-8'):
        import hashlib
        return getattr(hashlib, hash_type)(self.encode(encoding)).hexdigest()

    def tobase64(self, encoding='utf-8'):
        import base64
        return base64.b64encode(self.encode(encoding)).decode(encoding)

    @staticmethod
    def frombase64(string, encoding='utf-8'):
        import base64
        return base64.b64decode(string.encode(encoding)).decode(encoding)