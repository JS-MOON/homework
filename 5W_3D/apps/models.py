class Tweet:
    title = None
    contents = None
    num = None
    count_plus = None
    count_minus = None

    def __init__(self, title, contents, num, count_plus, count_minus):
        self.title = title
        self.contents = contents
        self.num = num
        self.count_plus = count_plus
        self.count_minus = count_minus