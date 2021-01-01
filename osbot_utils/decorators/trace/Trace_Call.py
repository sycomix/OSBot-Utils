# todo: refactor into separate project (since the idea is to minimize the dependencies on OSBot-Utils
# this method requires pycallgraph and dot installed
from pycallgraph.output import GraphvizOutput
from pycallgraph        import Color
from pycallgraph        import Config
from pycallgraph        import PyCallGraph
from pycallgraph        import GlobbingFilter

class Trace_Call:

    def __init__(self, include_filter=None, exclude_filter=None, include_osbot=True, img_file = None):
        self.img_file = img_file
        if self.img_file is None:  self.img_file  = '/tmp/trace_PyCallGraph.png'
        self.graphviz             = GraphvizOutput()
        self.graphviz.output_file = self.img_file
        if include_osbot:
            self.include_filter = ['osbot*', 'pbx*']
        else:
            self.include_filter = []
        self.exclude_filter       = ['pycallgraph*']
        self.add_include_filter(include_filter)
        self.add_exclude_filter(exclude_filter)


    def add_include_filter(self,  include_filter):
        if type(include_filter) is str : self.include_filter.append(include_filter)
        if type(include_filter) is list: self.include_filter.extend(include_filter)
        return self

    def add_exclude_filter(self,  exclude_filters):
        if type(exclude_filters) is str : self.exclude_filter.append(exclude_filters)
        if type(exclude_filters) is list: self.exclude_filter.extend(exclude_filters)
        return self

    def rainbow(node):
        return Color.hsv(node.time.fraction * 0.8, 0.4, 0.9)

    def greyscale(node):
        return Color.hsv(0, 0, node.time.fraction / 2 + 0.4)

    def orange_green(node):
        return Color(0.2 + node.time.fraction * 0.8,
                     0.2 + node.calls.fraction * 0.4,
                     0.2)


    def invoke_method(self, method, *args,**kwargs):
        self.graphviz.edge_color_func = lambda e: Color(0, 0, 0)
        # graphviz.node_color_func = rainbow #orange_green # greyscale

        config = Config(include_stdlib=True)  # max_depth=10)

        config.trace_filter = GlobbingFilter(include=self.include_filter, exclude=self.exclude_filter)

        with PyCallGraph(output=self.graphviz, config=config):
            try:
                return_value = method(*args,**kwargs)

                print(f'\n------------------------------------------' +
                      f'\nExecution trace saved to: {self.img_file}' +
                      f'\n------------------------------------------')

                return { 'status'  : 'ok'          ,
                         'data'    : return_value  ,
                         'img_file': self.img_file }

            except Exception as error:
                return {'status':'error', 'data': '{0}'.format(error)}
