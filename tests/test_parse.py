from src import parse
import random

class TestParse:
    test_folder = 'tests'

    def test_heap_sort(self):
        random.seed(124)
        arr = [[i, random.randint(0, 10)] for i in range(4)]
        parse.heap_sort(arr)
        target = [[2, 0],[3, 2],[0, 4],[1,8]]
        assert arr == target
    
    def test_find_files(self):
        target = ['cards_section_1.xml', 'cards_section_2.xml']
        pattern = "^cards_section_\\d+.xml$"
        files = parse.find_files(pattern, self.test_folder)
        assert set(files) == set(target)

    def test_get_files_specific(self):
        target = ['cards_section_1.xml', 'cards_section_2.xml']
        files_wanted = ['cards_section_1.xml', 'cards_section_2.xml']
        files_found = parse.get_files(files_wanted, self.test_folder)
        assert set(files_found) == set(target)
    
    def test_get_files_1(self):
        target = ['test_data_2.xml']
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.file = ['test_data_2.xml']
        files = parse.get_files(args.file, folder=self.test_folder)
        assert files == target

    def test_get_files_2(self):
        target = ['test_data_2.xml', 'test_data_1.xml']
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.file = ['test_data_2.xml', 'test_data_1.xml']
        files = parse.get_files(args.file, folder=self.test_folder)
        assert files == target

    def test_get_files_3(self):
        target = ['test_data_2.xml']
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.file = ['test_data_2.xml', 'test_data_5.xml']
        files = parse.get_files(args.file, folder=self.test_folder)
        assert files == target

    def test_get_files_4(self):
        target = ['cards_section_1.xml', 'cards_section_2.xml']
        files = parse.get_files(folder=self.test_folder)
        assert set(files) == set(target)

    # def test_ignored_list(self):
        # target = {'1999', '1'}
        # ignored_list = parse.get_ignored_list(self.test_folder)
        # assert target == ignored_list

    def test_score_by_fields(self):
        target = {1:{'adj_stats': 100, 'avg_skill': 50, 'score': 150}, 
        2:{'adj_stats': 90, 'avg_skill': 45, 'score': 135}, 
        3:{'adj_stats': 60, 'avg_skill': 95, 'score': 155}}
        data = {1:{'adj_stats': 100, 'avg_skill': 50}, 
        2:{'adj_stats': 90, 'avg_skill': 45}, 
        3:{'adj_stats': 60, 'avg_skill': 95}}
        parse.score_by_fields(data, 'adj_stats', 'avg_skill')
        assert data == target