import pandas as pd
import pygal

from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS


class ReviewProcess:

    def __init__(self):
        self.file = 'data.tsv'
        self.data = None
        self.vec_positive = dict()
        self.vec_negative = dict()

    def parse_tsv(self):
        self.data = pd.DataFrame.from_csv(self.file, sep='\t', index_col=None)

        for index, row in self.data.iterrows():
            for word in row[2].split(' '):
                self.vec_negative[word] = 0
                self.vec_positive[word] = 0

        for index, row in self.data.iterrows():
            if row[1] == 0:
                for word in row[2].split(' '):
                    self.vec_negative[word] += 1
                    self.vec_positive[word] += 0

            if row[1] == 1:
                for word in row[2].split(' '):
                    self.vec_positive[word] += 1
                    self.vec_negative[word] += 0

    def statistical_test(self):
        df = pd.from_dict(self.vec_negative)
        print(df.head())

    def make_histogram(self):
        vec_positive = dict(sorted(self.vec_positive.items(), key=lambda x: x[1], reverse=True)[:50])
        vec_negative = dict(sorted(self.vec_negative.items(), key=lambda x: x[1], reverse=True)[:50])

        # Make visualization.
        my_style = LS('#333366', base_style=LCS)

        my_config = pygal.Config()
        my_config.x_label_rotation = 45
        my_config.show_legend = False
        my_config.title_font_size = 24
        my_config.label_font_size = 14
        my_config.major_label_font_size = 18
        my_config.truncate_label = 15
        my_config.show_y_guides = False
        my_config.width = 1000

        chart = pygal.Bar(my_config, style=my_style)
        chart.title = '50 Most Frequent Used Words'
        chart.x_labels = [vec_positive.keys(), vec_negative.keys()]

        chart.add('positive', vec_positive.values())
        chart.add('negative', vec_negative.values())
        chart.render_to_file('{}.svg'.format('histogram'))


if __name__ == "__main__":
    x = ReviewProcess()
    x.parse_tsv()
    # x.make_histogram()
    x.statistical_test()
