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

    def test_ignored_list(self):
        target = {'1999', '1'}
        ignored_list = parse.get_ignored_list(self.test_folder)
        assert target == ignored_list

    def test_score_by_fields(self):
        target = {1:{'adj_stats': 100, 'avg_skill': 50, 'score': 150}, 
        2:{'adj_stats': 90, 'avg_skill': 45, 'score': 135}, 
        3:{'adj_stats': 60, 'avg_skill': 95, 'score': 155}}
        data = {1:{'adj_stats': 100, 'avg_skill': 50}, 
        2:{'adj_stats': 90, 'avg_skill': 45}, 
        3:{'adj_stats': 60, 'avg_skill': 95}}
        parse.score_by_fields(data, 'adj_stats', 'avg_skill')
        assert data == target
    
    def test_parse_cards(self):
        target = {'1': {'id': '1', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 1, 'health': 6, 'level': '1', 'type': 1, 'adj_stats': 7.0, 'avg_skill': 0, 'skills': [], 'upgrade_id': '2'}, '2': {'id': '2', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 2, 'health': 9, 'level': '2', 'type': 1, 'adj_stats': 11.0, 'avg_skill': 0, 'skills': [], 'upgrade_id': '3'}, '3': {'id': '3', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 3, 'health': 12, 'level': '3', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 0, 'skills': [], 'upgrade_id': None}, 
                  '4': {'id': '4', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 9, 'level': '1', 'type': 1, 'adj_stats': 6.0, 'avg_skill': 5.0, 'skills': ['pierce 5'], 'upgrade_id': '350'}, '350': {'id': '350', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 5, 'health': 14, 'level': '2', 'type': 1, 'adj_stats': 9.5, 'avg_skill': 7.0, 'skills': ['pierce 7'], 'upgrade_id': '351'}, '351': {'id': '351', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 6, 'health': 18, 'level': '3', 'type': 1, 'adj_stats': 12.0, 'avg_skill': 10.0, 'skills': ['pierce 10'], 'upgrade_id': None}}
        files = parse.find_files('^test_data_2.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        print(cards)
        assert cards == target
    
    def test_parse_cards_set_1(self):
        target = {'380': {'id': '380', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 45, 'level': '1', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15'], 'upgrade_id': '381'}, '381': {'id': '381', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 45, 'level': '2', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15'], 'upgrade_id': '382'}, '382': {'id': '382', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 45, 'level': '3', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15'], 'upgrade_id': '383'}, '383': {'id': '383', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 55, 'level': '4', 'type': 1, 'adj_stats': 17.5, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15'], 'upgrade_id': '384'}, '384': {'id': '384', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 55, 'level': '5', 'type': 1, 'adj_stats': 17.5, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15'], 'upgrade_id': '385'}, '385': {'id': '385', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 55, 'level': '6', 'type': 1, 'adj_stats': 17.5, 'avg_skill': 23.333333333333332, 'skills': ['armored 30', 'heal all 20', 'besiege 20'], 'upgrade_id': None}}
        files = parse.find_files('^test_data_1.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.set = [9000]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        print(cards)
        assert cards == target

    def test_parse_cards_set_2(self):
        target = {}
        files = parse.find_files('^test_data_2.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.set = [2000]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        assert cards == target