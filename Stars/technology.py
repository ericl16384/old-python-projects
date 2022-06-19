class Tech:
    """Energy, Weapons, Propulsion, Construction, Electronics, Biotechnology"""
    
    def __init__(self, en=0, we=0, pr=0, co=0, el=0, bi=0):
        assert isinstance(en, int)
        assert isinstance(we, int)
        assert isinstance(pr, int)
        assert isinstance(co, int)
        assert isinstance(el, int)
        assert isinstance(bi, int)

        self.en = en
        self.we = we
        self.pr = pr
        self.co = co
        self.el = el
        self.bi = bi
    
    def __str__(self):
        return f"""Energy         {self.en}
Weapons        {self.we}
Propulsion     {self.pr}
Construction   {self.co}
Electronics    {self.el}
Biotechnology  {self.bi}"""
    
    def __add__(self, other):
        """Adding Tech objects will create a Tech object with the highest technology between the two."""

        assert isinstance(other, Tech)

        return Tech(
            max(self.en, other.en),
            max(self.we, other.we),
            max(self.pr, other.pr),
            max(self.co, other.co),
            max(self.el, other.el),
            max(self.bi, other.bi)
        )

    def energy(self):
        return self.en
    def weapons(self):
        return self.we
    def propulsion(self):
        return self.pr
    def construction(self):
        return self.co
    def electronics(self):
        return self.el
    def biotechnology(self):
        return self.bi