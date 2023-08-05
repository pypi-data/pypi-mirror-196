from dataclasses import dataclass, field

from devgoldyutils import DictDataclass

@dataclass
class Test(DictDataclass):

    bruh:str = field(init=False)

    def __post_init__(self):
        self.bruh = self.get("owo")

test = Test()

print(test.bruh)