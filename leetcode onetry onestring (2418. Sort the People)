class Solution:
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:
        return list(map(lambda y: y[0], sorted(zip(names, heights), key=lambda x: -x[1])))
