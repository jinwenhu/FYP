from gensim.models import word2vec
import networkx
import logging

class graph():
    def __init__(self):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        self.model = word2vec.Word2Vec.load("data/text8.model")
        self.read("data/test.graphml")
        # self.G = networkx.Graph()

    def fill_in_convex(self, keyword, level):
        if level == 0:
            return
        y2 = self.model.most_similar(keyword, topn=10)
        temp_list = []
        for item in y2:
            temp_list.append((keyword, item[0], item[1]))
        self.add_edges(temp_list)
        level -= 1
        for item in y2:
            self.fill_in_convex(item[0], level)

    def fill_in_single(self, keyword):
        y2 = self.model.most_similar(keyword, topn=10)
        temp_list = []
        for item in y2:
            temp_list.append((keyword, item[0], item[1]))
        self.add_edges(temp_list)

    def add_edges(self,list):
        self.G.add_weighted_edges_from(list)

    def print_result(self, a, b):
        if self.G.has_node(a) and self.G.has_node(b):
            if networkx.has_path(self.G, a, b):
                print networkx.shortest_path(self.G, a, b)
            else:
                print "path not exist"
        else:
            print "nodes not in graph"

    def query(self, a, b):
        if self.G.has_node(a) and self.G.has_node(b):
            if networkx.has_path(self.G, a, b):
                return networkx.shortest_path(self.G, a, b)

    def train(self, path):
        with open(path) as input:
            words_list = input.read().splitlines()
        input.close()
        success_word = 0
        fail_word = 0
        for line in words_list:
            line = line.split("\t")
            word = line[1]
            try:
                self.fill_in_single(word)
                success_word += 1
            except:
                fail_word += 1
                continue
        print "success: %d" % success_word
        print "fail: %d" % fail_word

    def save(self, path):
        networkx.write_graphml(self.G, path)

    def read(self, path):
        self.G = networkx.read_graphml(path)

if __name__ == "__main__":
    temp = graph()
    temp.read("data/test.graphml")
    # temp.train("data/tags.dat")
    a = "science"
    b = "ghost"
    temp.print_result(a,b)
    # temp.save("test.graphml")