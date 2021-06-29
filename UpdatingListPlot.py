'''
holds a set of data [[y00, y01, y02 ...], [y10, y11, y12 ...], ...]
as well as the associated plot image (.gif)
'''
from wolframclient.language import wl

class UpdatingListPlot():
    
    def __init__(self, data_set, wolfram_session, plot_name):
        self.session = wolfram_session
        self.data = data_set
        self.plot = self.plot_data()
        self.name = plot_name
        
    def update(self, data):
        self.data = data
    
    def plot_data(self):
        return self.session.evaluate(wl.Export(wl.LocalObject(self.name), wl.Listplot(self.data), "GIF"))
        
if __name__ == "__main__":
    pass