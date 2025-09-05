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
        target = {'1': {'id': '1', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 1, 'health': 6, 'level': '1', 'type': 1, 'adj_stats': 7.0, 'avg_skill': 0, 'skills': []}, '2': {'id': '2', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 2, 'health': 9, 'level': '2', 'type': 1, 'adj_stats': 11.0, 'avg_skill': 0, 'skills': []}, '3': {'id': '3', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 3, 'health': 12, 'level': '3', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 0, 'skills': []}, '4': {'id': '4', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 9, 'level': '1', 'type': 1, 'adj_stats': 6.0, 'avg_skill': 5.0, 'skills': ['pierce 5']}, '350': {'id': '350', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 5, 'health': 14, 'level': '2', 'type': 1, 'adj_stats': 9.5, 'avg_skill': 7.0, 'skills': ['pierce 7']}, '351': {'id': '351', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 6, 'health': 18, 'level': '3', 'type': 1, 'adj_stats': 12.0, 'avg_skill': 10.0, 'skills': ['pierce 10']}}
        files = parse.find_files('^test_data_2.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        print(cards)
        assert cards == target
    
    def test_parse_cards_set_1(self):
        target = {'380': {'id': '380', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 45, 'level': '1', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15']}, '381': {'id': '381', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 45, 'level': '2', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15']}, '382': {'id': '382', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 45, 'level': '3', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15']}, '383': {'id': '383', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 55, 'level': '4', 'type': 1, 'adj_stats': 17.5, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15']}, '384': {'id': '384', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 55, 'level': '5', 'type': 1, 'adj_stats': 17.5, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15']}, '385': {'id': '385', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 55, 'level': '6', 'type': 1, 'adj_stats': 17.5, 'avg_skill': 23.333333333333332, 'skills': ['armored 30', 'heal all 20', 'besiege 20']}}
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

    def test_parse_cards_rarity_1(self):
        target = {'26': {'id': '26', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 30, 'level': '1', 'type': 1, 'adj_stats': 11.333333333333334, 'avg_skill': 5.0, 'skills': ['heal 6', 'weaken 4']}, '27': {'id': '27', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 30, 'level': '2', 'type': 1, 'adj_stats': 12.0, 'avg_skill': 6.0, 'skills': ['heal Imperial 8', 'weaken all 4']}, '28': {'id': '28', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 34, 'level': '3', 'type': 1, 'adj_stats': 13.333333333333334, 'avg_skill': 6.5, 'skills': ['heal all Imperial 8', 'weaken all 5']}, '29': {'id': '29', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 8, 'health': 34, 'level': '4', 'type': 1, 'adj_stats': 14.0, 'avg_skill': 7.333333333333333, 'skills': ['heal all Imperial 10', 'protect Imperial 6', 'weaken all 6']}, '30': {'id': '30', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 8, 'health': 37, 'level': '5', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 8.666666666666666, 'skills': ['heal all Imperial 12', 'protect all Imperial 6', 'weaken all 8']}, '31': {'id': '31', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 10, 'health': 40, 'level': '6', 'type': 1, 'adj_stats': 16.666666666666668, 'avg_skill': 11.0, 'skills': ['heal all Imperial 15', 'protect all Imperial 8', 'weaken all 10']}, '59': {'id': '59', 'name': 'Omega', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 43, 'level': '1', 'type': 2, 'adj_stats': 21.5, 'avg_skill': 19.0, 'skills': ['strike all 19', 'weaken all 19', 'besiege all 19']}, '60': {'id': '60', 'name': 'Omega', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 48, 'level': '2', 'type': 2, 'adj_stats': 24.0, 'avg_skill': 21.0, 'skills': ['strike all 21', 'weaken all 21', 'besiege all 21']}, '61': {'id': '61', 'name': 'Omega', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 52, 'level': '3', 'type': 2, 'adj_stats': 26.0, 'avg_skill': 24.0, 'skills': ['strike all 24', 'weaken all 24', 'besiege all 24']}, '62': {'id': '62', 'name': 'Omega', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 57, 'level': '4', 'type': 2, 'adj_stats': 28.5, 'avg_skill': 26.0, 'skills': ['strike all 26', 'weaken all 26', 'besiege all 26']}, '63': {'id': '63', 'name': 'Omega', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 61, 'level': '5', 'type': 2, 'adj_stats': 30.5, 'avg_skill': 28.0, 'skills': ['strike all 28', 'weaken all 28', 'besiege all 28']}, '64': {'id': '64', 'name': 'Omega', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 66, 'level': '6', 'type': 2, 'adj_stats': 33.0, 'avg_skill': 30.0, 'skills': ['strike all 30', 'weaken all 30', 'besiege all 30']}, '92': {'id': '92', 'name': 'Malgoth', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 6, 'health': 40, 'level': '1', 'type': 3, 'adj_stats': 11.5, 'avg_skill': 7.0, 'skills': ['heal Xeno 8', 'rally all Xeno 6']}, '93': {'id': '93', 'name': 'Malgoth', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 9, 'health': 45, 'level': '2', 'type': 3, 'adj_stats': 13.5, 'avg_skill': 8.0, 'skills': ['heal all Xeno 8', 'rally all Xeno 8']}, '94': {'id': '94', 'name': 'Malgoth', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 9, 'health': 50, 'level': '3', 'type': 3, 'adj_stats': 14.75, 'avg_skill': 10.0, 'skills': ['heal all Xeno 10', 'rally all Xeno 10']}, '95': {'id': '95', 'name': 'Malgoth', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 12, 'health': 50, 'level': '4', 'type': 3, 'adj_stats': 15.5, 'avg_skill': 12.0, 'skills': ['heal all Xeno 12', 'rally all Xeno 12']}, '96': {'id': '96', 'name': 'Malgoth', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 12, 'health': 55, 'level': '5', 'type': 3, 'adj_stats': 16.75, 'avg_skill': 12.0, 'skills': ['heal all Xeno 13', 'rally all Xeno 13', 'berserk 10']}, '97': {'id': '97', 'name': 'Malgoth', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 60, 'level': '6', 'type': 3, 'adj_stats': 18.75, 'avg_skill': 15.0, 'skills': ['heal all Xeno 15', 'rally all Xeno 15', 'berserk 15']}, '125': {'id': '125', 'name': 'Apex', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 10, 'health': 80, 'level': '1', 'type': 4, 'adj_stats': 22.5, 'avg_skill': 25.666666666666668, 'skills': ['poison 35', 'strike 12', 'refresh 30']}, '126': {'id': '126', 'name': 'Apex', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 80, 'level': '2', 'type': 4, 'adj_stats': 23.75, 'avg_skill': 30.0, 'skills': ['poison 40', 'strike 15', 'refresh 35']}, '127': {'id': '127', 'name': 'Apex', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 90, 'level': '3', 'type': 4, 'adj_stats': 26.25, 'avg_skill': 34.0, 'skills': ['poison 45', 'strike 17', 'refresh 40']}, '128': {'id': '128', 'name': 'Apex', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 100, 'level': '4', 'type': 4, 'adj_stats': 28.75, 'avg_skill': 34.0, 'skills': ['poison 45', 'strike 17', 'refresh 40']}, '129': {'id': '129', 'name': 'Apex', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 20, 'health': 100, 'level': '5', 'type': 4, 'adj_stats': 30.0, 'avg_skill': 37.333333333333336, 'skills': ['poison 50', 'strike all 17', 'refresh 45']}, '130': {'id': '130', 'name': 'Apex', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 25, 'health': 110, 'level': '6', 'type': 4, 'adj_stats': 33.75, 'avg_skill': 41.0, 'skills': ['poison 55', 'strike all 18', 'refresh 50']}, '158': {'id': '158', 'name': 'Benediction', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 4, 'attack': 5, 'health': 40, 'level': '1', 'type': 5, 'adj_stats': 9.0, 'avg_skill': 9.0, 'skills': ['rally Righteous 9']}, '159': {'id': '159', 'name': 'Benediction', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 4, 'attack': 7, 'health': 43, 'level': '2', 'type': 5, 'adj_stats': 10.0, 'avg_skill': 9.0, 'skills': ['rally Righteous 11', 'besiege 7']}, '160': {'id': '160', 'name': 'Benediction', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 4, 'attack': 9, 'health': 48, 'level': '3', 'type': 5, 'adj_stats': 11.4, 'avg_skill': 10.0, 'skills': ['evade 1', 'rally Righteous 13', 'besiege all 7']}, '161': {'id': '161', 'name': 'Benediction', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 4, 'attack': 11, 'health': 52, 'level': '4', 'type': 5, 'adj_stats': 12.6, 'avg_skill': 11.333333333333334, 'skills': ['evade 1', 'rally Righteous 15', 'besiege all 9']}, '162': {'id': '162', 'name': 'Benediction', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 4, 'attack': 13, 'health': 56, 'level': '5', 'type': 5, 'adj_stats': 13.8, 'avg_skill': 15.666666666666666, 'skills': ['evade 2', 'rally all Righteous 15', 'besiege all 12']}, '163': {'id': '163', 'name': 'Benediction', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 4, 'attack': 15, 'health': 60, 'level': '6', 'type': 5, 'adj_stats': 15.0, 'avg_skill': 21.0, 'skills': ['evade 3', 'rally all Righteous 18', 'besiege all 15']}}
        files = parse.find_files('^test_data_1.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.rarity = [4]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        print(cards)
        assert cards == target

    def test_parse_cards_rarity_2(self):
        target = {}
        files = parse.find_files('^test_data_2.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.rarity = [2]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        assert cards == target

    def test_parse_cards_rarity_3(self):
        target = {'1': {'id': '1', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 1, 'health': 6, 'level': '1', 'type': 1, 'adj_stats': 7.0, 'avg_skill': 0, 'skills': []}, 
                  '2': {'id': '2', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 2, 'health': 9, 'level': '2', 'type': 1, 'adj_stats': 11.0, 'avg_skill': 0, 'skills': []}, 
                  '3': {'id': '3', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 3, 'health': 12, 'level': '3', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 0, 'skills': []}, 
                  '4': {'id': '4', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 9, 'level': '1', 'type': 1, 'adj_stats': 6.0, 'avg_skill': 5.0, 'skills': ['pierce 5']}, 
                  '350': {'id': '350', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 5, 'health': 14, 'level': '2', 'type': 1, 'adj_stats': 9.5, 'avg_skill': 7.0, 'skills': ['pierce 7']}, 
                  '351': {'id': '351', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 6, 'health': 18, 'level': '3', 'type': 1, 'adj_stats': 12.0, 'avg_skill': 10.0, 'skills': ['pierce 10']}, 
                  '5': {'id': '5', 'name': 'Medic', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 2, 'health': 10, 'level': '1', 'type': 1, 'adj_stats': 6.0, 'avg_skill': 2.0, 'skills': ['fortify 2']}, 
                  '352': {'id': '352', 'name': 'Medic', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 15, 'level': '2', 'type': 1, 'adj_stats': 9.0, 'avg_skill': 4.0, 'skills': ['fortify 4']}, 
                  '353': {'id': '353', 'name': 'Medic', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 19, 'level': '3', 'type': 1, 'adj_stats': 11.0, 'avg_skill': 6.0, 'skills': ['fortify 6']}, 
                  '6': {'id': '6', 'name': 'Dreadnaught', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 3, 'health': 13, 'level': '1', 'type': 1, 'adj_stats': 5.333333333333333, 'avg_skill': 4.0, 'skills': ['armored 4']}, 
                  '7': {'id': '7', 'name': 'Dreadnaught', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 18, 'level': '2', 'type': 1, 'adj_stats': 7.666666666666667, 'avg_skill': 6.5, 'skills': ['armored 7', 'besiege 6']}, 
                  '8': {'id': '8', 'name': 'Dreadnaught', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 22, 'level': '3', 'type': 1, 'adj_stats': 9.333333333333334, 'avg_skill': 10.0, 'skills': ['armored 10', 'besiege 10']}, 
                  '9': {'id': '9', 'name': 'Rally Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 3, 'health': 12, 'level': '1', 'type': 1, 'adj_stats': 5.0, 'avg_skill': 6.0, 'skills': ['rally 6']}, 
                  '10': {'id': '10', 'name': 'Rally Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 4, 'health': 14, 'level': '2', 'type': 1, 'adj_stats': 9.0, 'avg_skill': 7.0, 'skills': ['rally 7']}, 
                  '11': {'id': '11', 'name': 'Rally Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 5, 'health': 16, 'level': '3', 'type': 1, 'adj_stats': 10.5, 'avg_skill': 9.0, 'skills': ['rally 9']}, 
                  '12': {'id': '12', 'name': 'Trap Setter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 5, 'health': 22, 'level': '1', 'type': 1, 'adj_stats': 5.4, 'avg_skill': 5.5, 'skills': ['counter 6', 'heal 5']}, 
                  '13': {'id': '13', 'name': 'Trap Setter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 7, 'health': 28, 'level': '2', 'type': 1, 'adj_stats': 7.0, 'avg_skill': 6.333333333333333, 'skills': ['counter 8', 'heal all 5', 'weaken 6']}, 
                  '14': {'id': '14', 'name': 'Trap Setter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 9, 'health': 36, 'level': '3', 'type': 1, 'adj_stats': 9.0, 'avg_skill': 8.666666666666666, 'skills': ['counter 10', 'heal all 8', 'weaken all 8']}, '15': {'id': '15', 'name': 'Barrage Tank', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 4, 'health': 17, 'level': '1', 'type': 1, 'adj_stats': 5.25, 'avg_skill': 4.5, 'skills': ['armored 5', 'strike 4']}, '354': {'id': '354', 'name': 'Barrage Tank', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 23, 'level': '2', 'type': 1, 'adj_stats': 9.333333333333334, 'avg_skill': 7.0, 'skills': ['armored 8', 'strike 6']}, '355': {'id': '355', 'name': 'Barrage Tank', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 29, 'level': '3', 'type': 1, 'adj_stats': 11.666666666666666, 'avg_skill': 9.5, 'skills': ['armored 10', 'strike 9']}, '166': {'id': '166', 'name': 'Swift Troops', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 3, 'health': 19, 'level': '1', 'type': 1, 'adj_stats': 5.5, 'avg_skill': 6.0, 'skills': ['rally Imperial 6']}, '167': {'id': '167', 'name': 'Swift Troops', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 24, 'level': '2', 'type': 1, 'adj_stats': 9.333333333333334, 'avg_skill': 6.0, 'skills': ['rally Imperial 7', 'strike 5']}, '168': {'id': '168', 'name': 'Swift Troops', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 29, 'level': '3', 'type': 1, 'adj_stats': 11.333333333333334, 'avg_skill': 8.0, 'skills': ['rally all Imperial 8', 'strike 8']}, '16': {'id': '16', 'name': 'Terminator', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 5, 'health': 22, 'level': '1', 'type': 1, 'adj_stats': 6.75, 'avg_skill': 6.5, 'skills': ['armored 7', 'rally Imperial 6']}, '17': {'id': '17', 'name': 'Terminator', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 6, 'health': 27, 'level': '2', 'type': 1, 'adj_stats': 8.25, 'avg_skill': 7.666666666666667, 'skills': ['armored 8', 'rally all Imperial 7', 'pierce 8']}, '18': {'id': '18', 'name': 'Terminator', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 8, 'health': 33, 'level': '3', 'type': 1, 'adj_stats': 10.25, 'avg_skill': 9.0, 'skills': ['armored 9', 'rally all Imperial 8', 'pierce 10']}, '19': {'id': '19', 'name': 'Terminator', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 9, 'health': 39, 'level': '4', 'type': 1, 'adj_stats': 12.0, 'avg_skill': 10.333333333333334, 'skills': ['armored 10', 'rally all Imperial 9', 'pierce 12']}, '34': {'id': '34', 'name': 'Grunt', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 1, 'health': 5, 'level': '1', 'type': 2, 'adj_stats': 6.0, 'avg_skill': 5.0, 'skills': ['pierce 5']}, '356': {'id': '356', 'name': 'Grunt', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 2, 'health': 7, 'level': '2', 'type': 2, 'adj_stats': 9.0, 'avg_skill': 7.0, 'skills': ['pierce 7']}, '357': {'id': '357', 'name': 'Grunt', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 3, 'health': 10, 'level': '3', 'type': 2, 'adj_stats': 13.0, 'avg_skill': 10.0, 'skills': ['pierce 10']}, '35': {'id': '35', 'name': 'Headhunter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 3, 'health': 14, 'level': '1', 'type': 2, 'adj_stats': 5.666666666666667, 'avg_skill': 5.0, 'skills': ['hunt 5']}, '36': {'id': '36', 'name': 'Headhunter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 18, 'level': '2', 'type': 2, 'adj_stats': 7.333333333333333, 'avg_skill': 7.0, 'skills': ['hunt 7']}, '37': {'id': '37', 'name': 'Headhunter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 22, 'level': '3', 'type': 2, 'adj_stats': 9.0, 'avg_skill': 10.0, 'skills': ['hunt 10']}, '38': {'id': '38', 'name': 'Dread Panzer', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 7, 'health': 24, 'level': '1', 'type': 2, 'adj_stats': 6.2, 'avg_skill': 7.0, 'skills': ['counter 7']}, '358': {'id': '358', 'name': 'Dread Panzer', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 9, 'health': 32, 'level': '2', 'type': 2, 'adj_stats': 8.2, 'avg_skill': 9.0, 'skills': ['counter 9']}, '359': {'id': '359', 'name': 'Dread Panzer', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 12, 'health': 38, 'level': '3', 'type': 2, 'adj_stats': 10.0, 'avg_skill': 11.0, 'skills': ['counter 11']}, '39': {'id': '39', 'name': 'Bombardment Tank', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 10, 'level': '1', 'type': 2, 'adj_stats': 6.5, 'avg_skill': 3.0, 'skills': ['armored 3']}, '40': {'id': '40', 'name': 'Bombardment Tank', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 4, 'health': 13, 'level': '2', 'type': 2, 'adj_stats': 8.5, 'avg_skill': 4.5, 'skills': ['armored 5', 'strike 4']}, '41': {'id': '41', 'name': 'Bombardment Tank', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 5, 'health': 17, 'level': '3', 'type': 2, 'adj_stats': 11.0, 'avg_skill': 6.5, 'skills': ['armored 7', 'strike 6']}, '42': {'id': '42', 'name': 'Combat Specialist', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 15, 'level': '1', 'type': 2, 'adj_stats': 6.333333333333333, 'avg_skill': 6.0, 'skills': ['pierce 6']}, '43': {'id': '43', 'name': 'Combat Specialist', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 20, 'level': '2', 'type': 2, 'adj_stats': 8.666666666666666, 'avg_skill': 6.5, 'skills': ['weaken 5', 'pierce 8']}, '44': {'id': '44', 'name': 'Combat Specialist', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 8, 'health': 24, 'level': '3', 'type': 2, 'adj_stats': 10.666666666666666, 'avg_skill': 10.0, 'skills': ['weaken 8', 'pierce 12']}, 
                  '45': {'id': '45', 'name': 'Hydroblade', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 2, 'health': 9, 'level': '1', 'type': 2, 'adj_stats': 5.5, 'avg_skill': 2.0, 'skills': ['berserk 2']}, 
                  '360': {'id': '360', 'name': 'Hydroblade', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 4, 'health': 11, 'level': '2', 'type': 2, 'adj_stats': 15.0, 'avg_skill': 3.0, 'skills': ['berserk 3']}, 
                  '361': {'id': '361', 'name': 'Hydroblade', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 5, 'health': 13, 'level': '3', 'type': 2, 'adj_stats': 18.0, 'avg_skill': 5.0, 'skills': ['berserk 5']}, 
                  '46': {'id': '46', 'name': 'Scorpinox', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 5, 'health': 19, 'level': '1', 'type': 2, 'adj_stats': 6.0, 'avg_skill': 4.5, 'skills': ['counter 4', 'poison 5']}, 
                  '47': {'id': '47', 'name': 'Scorpinox', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 7, 'health': 23, 'level': '2', 'type': 2, 'adj_stats': 7.5, 'avg_skill': 6.333333333333333, 'skills': ['counter 6', 'avenge 5', 'poison 8']}, 
                  '48': {'id': '48', 'name': 'Scorpinox', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 9, 'health': 28, 'level': '3', 'type': 2, 'adj_stats': 9.25, 'avg_skill': 8.666666666666666, 'skills': ['counter 8', 'avenge 7', 'poison 11']}, 
                  '169': {'id': '169', 'name': 'Mortar Mech', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 6, 'health': 25, 'level': '1', 'type': 2, 'adj_stats': 6.2, 'avg_skill': 6.666666666666667, 'skills': ['strike 6', 'besiege 6', 'pierce 8']}, 
                  '170': {'id': '170', 'name': 'Mortar Mech', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 8, 'health': 31, 'level': '2', 'type': 2, 'adj_stats': 7.8, 'avg_skill': 9.333333333333334, 'skills': ['strike 8', 'besiege 9', 'pierce 11']}, 
                  '171': {'id': '171', 'name': 'Mortar Mech', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 10, 'health': 37, 'level': '3', 'type': 2, 'adj_stats': 9.4, 'avg_skill': 12.333333333333334, 'skills': ['strike 10', 'besiege 12', 'pierce 15']}, 
                  '49': {'id': '49', 'name': 'Blitz Armor', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 4, 'health': 16, 'level': '1', 'type': 2, 'adj_stats': 5.0, 'avg_skill': 5.5, 'skills': ['armored 5', 'rally Raider 6']}, 
                  '50': {'id': '50', 'name': 'Blitz Armor', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 5, 'health': 19, 'level': '2', 'type': 2, 'adj_stats': 6.0, 'avg_skill': 6.5, 'skills': ['armored 6', 'rally Raider 7']}, 
                  '51': {'id': '51', 'name': 'Blitz Armor', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 22, 'level': '3', 'type': 2, 'adj_stats': 9.0, 'avg_skill': 7.5, 'skills': ['armored 7', 'rally Raider 8']}, 
                  '52': {'id': '52', 'name': 'Blitz Armor', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 26, 'level': '4', 'type': 2, 'adj_stats': 10.666666666666666, 'avg_skill': 8.5, 'skills': ['armored 8', 'rally Raider 9']}, 
                  '67': {'id': '67', 'name': 'Devourer', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 6, 'health': 22, 'level': '1', 'type': 3, 'adj_stats': 5.6, 'avg_skill': 4.5, 'skills': ['strike 6', 'avenge 3']}, 
                  '68': {'id': '68', 'name': 'Devourer', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 7, 'health': 26, 'level': '2', 'type': 3, 'adj_stats': 8.25, 'avg_skill': 6.5, 'skills': ['strike 8', 'avenge 5']}, 
                  '69': {'id': '69', 'name': 'Devourer', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 9, 'health': 29, 'level': '3', 'type': 3, 'adj_stats': 9.5, 'avg_skill': 8.5, 'skills': ['strike 10', 'avenge 7']}, 
                  '70': {'id': '70', 'name': 'Locust Swarm', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 14, 'level': '1', 'type': 3, 'adj_stats': 6.0, 'avg_skill': 5.0, 'skills': ['counter 5']}, 
                  '362': {'id': '362', 'name': 'Locust Swarm', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 18, 'level': '2', 'type': 3, 'adj_stats': 7.666666666666667, 'avg_skill': 5.5, 'skills': ['counter 7', 'legion 2']}, 
                  '363': {'id': '363', 'name': 'Locust Swarm', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 7, 'health': 23, 'level': '3', 'type': 3, 'adj_stats': 10.0, 'avg_skill': 7.5, 'skills': ['counter 9', 'legion 3']}, 
                  '71': {'id': '71', 'name': 'Rabid Corruptor', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 11, 'level': '1', 'type': 3, 'adj_stats': 7.0, 'avg_skill': 4.0, 'skills': ['weaken 5', 'poison 3']}, 
                  '364': {'id': '364', 'name': 'Rabid Corruptor', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 4, 'health': 15, 'level': '2', 'type': 3, 'adj_stats': 9.5, 'avg_skill': 6.0, 'skills': ['weaken 6', 'poison 6']}, 
                  '365': {'id': '365', 'name': 'Rabid Corruptor', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 5, 'health': 19, 'level': '3', 'type': 3, 'adj_stats': 12.0, 'avg_skill': 8.0, 'skills': ['weaken 8', 'poison 8']}, 
                  '72': {'id': '72', 'name': 'Annelid Mass', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 9, 'level': '1', 'type': 3, 'adj_stats': 6.0, 'avg_skill': 5.0, 'skills': ['leech 5']}, 
                  '73': {'id': '73', 'name': 'Annelid Mass', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 3, 'health': 12, 'level': '2', 'type': 3, 'adj_stats': 15.0, 'avg_skill': 7.0, 'skills': ['leech 7']}, 
                  '74': {'id': '74', 'name': 'Annelid Mass', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 4, 'health': 14, 'level': '3', 'type': 3, 'adj_stats': 18.0, 'avg_skill': 9.0, 'skills': ['leech 9']}, 
                  '75': {'id': '75', 'name': 'Scavenger', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 4, 'health': 15, 'level': '1', 'type': 3, 'adj_stats': 4.75, 'avg_skill': 4.0, 'skills': ['rally Xeno 4', 'scavenge 2']}, 
                  '76': {'id': '76', 'name': 'Scavenger', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 6, 'health': 18, 'level': '2', 'type': 3, 'adj_stats': 6.0, 'avg_skill': 5.5, 'skills': ['rally all Xeno 5', 'scavenge 3']}, 
                  '77': {'id': '77', 'name': 'Scavenger', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 8, 'health': 21, 'level': '3', 'type': 3, 'adj_stats': 7.25, 'avg_skill': 7.0, 'skills': ['rally all Xeno 6', 'scavenge 4']}, 
                  '78': {'id': '78', 'name': 'Acid Spewer', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 15, 'level': '1', 'type': 3, 'adj_stats': 6.333333333333333, 'avg_skill': 5.0, 'skills': ['poison 5']}, 
                  '79': {'id': '79', 'name': 'Acid Spewer', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 18, 'level': '2', 'type': 3, 'adj_stats': 7.666666666666667, 'avg_skill': 8.0, 'skills': ['pierce 9', 'poison 7']}, 
                  '80': {'id': '80', 'name': 'Acid Spewer', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 21, 'level': '3', 'type': 3, 'adj_stats': 9.0, 'avg_skill': 10.5, 'skills': ['pierce 12', 'poison 9']}, 
                  '81': {'id': '81', 'name': 'Carcass Scrounge', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 2, 'health': 10, 'level': '1', 'type': 3, 'adj_stats': 6.0, 'avg_skill': 0, 'skills': []}, 
                  '366': {'id': '366', 'name': 'Carcass Scrounge', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 14, 'level': '2', 'type': 3, 'adj_stats': 8.5, 'avg_skill': 4.5, 'skills': ['enrage 3', 'rally Xeno 6']}, 
                  '367': {'id': '367', 'name': 'Carcass Scrounge', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 4, 'health': 17, 'level': '3', 'type': 3, 'adj_stats': 10.5, 'avg_skill': 6.5, 'skills': ['enrage 5', 'rally Xeno 8']}, 
                  '172': {'id': '172', 'name': 'Banshee', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 5, 'health': 26, 'level': '1', 'type': 3, 'adj_stats': 6.2, 'avg_skill': 7.0, 'skills': ['rally Xeno 6', 'weaken 8', 'leech 7']}, 
                  '173': {'id': '173', 'name': 'Banshee', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 7, 'health': 33, 'level': '2', 'type': 3, 'adj_stats': 8.0, 'avg_skill': 9.0, 'skills': ['rally Xeno 8', 'weaken 10', 'leech 9']}, 
                  '174': {'id': '174', 'name': 'Banshee', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 9, 'health': 38, 'level': '3', 'type': 3, 'adj_stats': 9.4, 'avg_skill': 10.666666666666666, 'skills': ['rally all Xeno 8', 'weaken 12', 'leech 12']}, 
                  '82': {'id': '82', 'name': 'Brood Walker', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 3, 'health': 19, 'level': '1', 'type': 3, 'adj_stats': 7.333333333333333, 'avg_skill': 5.0, 'skills': ['rally Xeno 5', 'strike 5']}, 
                  '83': {'id': '83', 'name': 'Brood Walker', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 22, 'level': '2', 'type': 3, 'adj_stats': 8.666666666666666, 'avg_skill': 6.0, 'skills': ['rally Xeno 6', 'strike 6']}, 
                  '84': {'id': '84', 'name': 'Brood Walker', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 26, 'level': '3', 'type': 3, 'adj_stats': 10.333333333333334, 'avg_skill': 6.5, 'skills': ['rally all Xeno 6', 'strike 7']}, 
                  '85': {'id': '85', 'name': 'Brood Walker', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 29, 'level': '4', 'type': 3, 'adj_stats': 11.666666666666666, 'avg_skill': 7.5, 'skills': ['rally all Xeno 7', 'strike 8']}, 
                  '100': {'id': '100', 'name': 'Enfeebler', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 2, 'health': 13, 'level': '1', 'type': 4, 'adj_stats': 7.5, 'avg_skill': 4.0, 'skills': ['enfeeble 4']}, 
                  '101': {'id': '101', 'name': 'Enfeebler', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 16, 'level': '2', 'type': 4, 'adj_stats': 9.5, 'avg_skill': 6.0, 'skills': ['enfeeble 6']}, 
                  '102': {'id': '102', 'name': 'Enfeebler', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 4, 'health': 19, 'level': '3', 'type': 4, 'adj_stats': 11.5, 'avg_skill': 8.0, 'skills': ['enfeeble 8']}, 
                  '103': {'id': '103', 'name': 'Xeno Mauler', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 7, 'health': 27, 'level': '1', 'type': 4, 'adj_stats': 6.8, 'avg_skill': 6.0, 'skills': ['strike 6']}, 
                  '368': {'id': '368', 'name': 'Xeno Mauler', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 9, 'health': 33, 'level': '2', 'type': 4, 'adj_stats': 8.4, 'avg_skill': 6.0, 'skills': ['strike all 6']}, 
                  '369': {'id': '369', 'name': 'Xeno Mauler', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 11, 'health': 39, 'level': '3', 'type': 4, 'adj_stats': 10.0, 'avg_skill': 8.0, 'skills': ['strike all 8']}, 
                  '104': {'id': '104', 'name': 'Enclave Parasite', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 4, 'health': 18, 'level': '1', 'type': 4, 'adj_stats': 5.5, 'avg_skill': 5.0, 'skills': ['counter 5', 'leech 5']}, 
                  '370': {'id': '370', 'name': 'Enclave Parasite', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 22, 'level': '2', 'type': 4, 'adj_stats': 9.0, 'avg_skill': 7.5, 'skills': ['counter 8', 'leech 7']}, 
                  '371': {'id': '371', 'name': 'Enclave Parasite', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 25, 'level': '3', 'type': 4, 'adj_stats': 10.333333333333334, 'avg_skill': 9.5, 'skills': ['counter 10', 'leech 9']}, 
                  '105': {'id': '105', 'name': 'Exogrunt', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 2, 'health': 12, 'level': '1', 'type': 4, 'adj_stats': 7.0, 'avg_skill': 4.0, 'skills': ['strike 4']}, 
                  '372': {'id': '372', 'name': 'Exogrunt', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 15, 'level': '2', 'type': 4, 'adj_stats': 9.0, 'avg_skill': 6.0, 'skills': ['strike 6']}, 
                  '373': {'id': '373', 'name': 'Exogrunt', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 4, 'health': 18, 'level': '3', 'type': 4, 'adj_stats': 11.0, 'avg_skill': 8.0, 'skills': ['strike 8']}, 
                  '106': {'id': '106', 'name': 'Cavern Smelter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 6, 'health': 20, 'level': '1', 'type': 4, 'adj_stats': 5.2, 'avg_skill': 4.0, 'skills': ['avenge 4']}, 
                  '107': {'id': '107', 'name': 'Cavern Smelter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 8, 'health': 24, 'level': '2', 'type': 4, 'adj_stats': 6.4, 'avg_skill': 6.0, 'skills': ['avenge 6']}, 
                  '108': {'id': '108', 'name': 'Cavern Smelter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 10, 'health': 28, 'level': '3', 'type': 4, 'adj_stats': 7.6, 'avg_skill': 8.0, 'skills': ['avenge 8']}, 
                  '109': {'id': '109', 'name': 'Dracus Wyrm', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 5, 'health': 20, 'level': '1', 'type': 4, 'adj_stats': 6.25, 'avg_skill': 6.0, 'skills': ['poison 6']}, 
                  '110': {'id': '110', 'name': 'Dracus Wyrm', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 23, 'level': '2', 'type': 4, 'adj_stats': 9.333333333333334, 'avg_skill': 9.0, 'skills': ['poison 9']}, 
                  '111': {'id': '111', 'name': 'Dracus Wyrm', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 7, 'health': 27, 'level': '3', 'type': 4, 'adj_stats': 11.333333333333334, 'avg_skill': 12.0, 'skills': ['poison 12']}, 
                  '112': {'id': '112', 'name': 'Tunneller', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 3, 'health': 19, 'level': '1', 'type': 4, 'adj_stats': 7.333333333333333, 'avg_skill': 6.0, 'skills': ['besiege 6', 'pierce 6']}, 
                  '113': {'id': '113', 'name': 'Tunneller', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 23, 'level': '2', 'type': 4, 'adj_stats': 9.333333333333334, 'avg_skill': 8.5, 'skills': ['besiege 8', 'pierce 9']}, 
                  '114': {'id': '114', 'name': 'Tunneller', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 7, 'health': 28, 'level': '3', 'type': 4, 'adj_stats': 11.666666666666666, 'avg_skill': 11.0, 'skills': ['besiege 10', 'pierce 12']}, 
                  '175': {'id': '175', 'name': 'Achawin', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 16, 'level': '1', 'type': 4, 'adj_stats': 6.666666666666667, 'avg_skill': 4.5, 'skills': ['counter 5', 'weaken 4']}, 
                  '176': {'id': '176', 'name': 'Achawin', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 20, 'level': '2', 'type': 4, 'adj_stats': 8.333333333333334, 'avg_skill': 7.0, 'skills': ['counter 8', 'weaken 6']}, 
                  '177': {'id': '177', 'name': 'Achawin', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 24, 'level': '3', 'type': 4, 'adj_stats': 10.0, 'avg_skill': 9.0, 'skills': ['counter 10', 'weaken 8']}, 
                  '115': {'id': '115', 'name': 'Enclave Remnant', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 4, 'attack': 10, 'health': 32, 'level': '1', 'type': 4, 'adj_stats': 8.4, 'avg_skill': 6.0, 'skills': ['weaken 6', 'besiege 6']}, 
                  '116': {'id': '116', 'name': 'Enclave Remnant', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 4, 'attack': 10, 'health': 36, 'level': '2', 'type': 4, 'adj_stats': 9.2, 'avg_skill': 7.0, 'skills': ['weaken 7', 'besiege all 7']}, 
                  '117': {'id': '117', 'name': 'Enclave Remnant', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 4, 'attack': 12, 'health': 36, 'level': '3', 'type': 4, 'adj_stats': 9.6, 'avg_skill': 7.5, 'skills': ['weaken all 7', 'besiege all 8']}, 
                  '118': {'id': '118', 'name': 'Enclave Remnant', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 4, 'attack': 14, 'health': 40, 'level': '4', 'type': 4, 'adj_stats': 10.8, 'avg_skill': 8.5, 'skills': ['weaken all 8', 'besiege all 9']}, 
                  '133': {'id': '133', 'name': 'Peacekeeper', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 2, 'health': 18, 'level': '1', 'type': 5, 'adj_stats': 6.666666666666667, 'avg_skill': 5.0, 'skills': ['heal 5']}, 
                  '374': {'id': '374', 'name': 'Peacekeeper', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 2, 'health': 22, 'level': '2', 'type': 5, 'adj_stats': 8.0, 'avg_skill': 6.5, 'skills': ['heal 7', 'coalition 3']}, 
                  '375': {'id': '375', 'name': 'Peacekeeper', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 26, 'level': '3', 'type': 5, 'adj_stats': 10.0, 'avg_skill': 10.0, 'skills': ['heal 10', 'coalition 5']}, 
                  '134': {'id': '134', 'name': 'Pylon', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 6, 'health': 26, 'level': '1', 'type': 5, 'adj_stats': 6.4, 'avg_skill': 6.0, 'skills': ['armored 7', 'barrier 5']}, 
                  '135': {'id': '135', 'name': 'Pylon', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 7, 'health': 30, 'level': '2', 'type': 5, 'adj_stats': 7.4, 'avg_skill': 8.0, 'skills': ['armored 9', 'barrier 7']}, 
                  '136': {'id': '136', 'name': 'Pylon', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 8, 'health': 34, 'level': '3', 'type': 5, 'adj_stats': 8.4, 'avg_skill': 10.5, 'skills': ['armored 12', 'barrier 9']}, 
                  '137': {'id': '137', 'name': 'Iron Eagle', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 4, 'health': 20, 'level': '1', 'type': 5, 'adj_stats': 6.0, 'avg_skill': 5.0, 'skills': ['armored 5']}, 
                  '376': {'id': '376', 'name': 'Iron Eagle', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 6, 'health': 24, 'level': '2', 'type': 5, 'adj_stats': 7.5, 'avg_skill': 7.0, 'skills': ['armored 7']}, 
                  '377': {'id': '377', 'name': 'Iron Eagle', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 8, 'health': 28, 'level': '3', 'type': 5, 'adj_stats': 9.0, 'avg_skill': 9.0, 'skills': ['armored 9']}, 
                  '138': {'id': '138', 'name': 'Havenship', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 14, 'level': '1', 'type': 5, 'adj_stats': 8.5, 'avg_skill': 4.5, 'skills': ['armored 4', 'pierce 5']}, 
                  '378': {'id': '378', 'name': 'Havenship', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 4, 'health': 16, 'level': '2', 'type': 5, 'adj_stats': 10.0, 'avg_skill': 6.0, 'skills': ['armored 5', 'pierce 7']}, 
                  '379': {'id': '379', 'name': 'Havenship', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 5, 'health': 18, 'level': '3', 'type': 5, 'adj_stats': 11.5, 'avg_skill': 8.0, 'skills': ['armored 6', 'pierce 10']}, 
                  '139': {'id': '139', 'name': 'Reconnoiter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 5, 'health': 21, 'level': '1', 'type': 5, 'adj_stats': 6.5, 'avg_skill': 6.0, 'skills': ['rally Righteous 7', 'weaken 5']}, 
                  '140': {'id': '140', 'name': 'Reconnoiter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 6, 'health': 25, 'level': '2', 'type': 5, 'adj_stats': 7.75, 'avg_skill': 8.0, 'skills': ['rally Righteous 9', 'weaken 7']}, 
                  '141': {'id': '141', 'name': 'Reconnoiter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 7, 'health': 29, 'level': '3', 'type': 5, 'adj_stats': 9.0, 'avg_skill': 10.0, 'skills': ['rally Righteous 11', 'weaken 9']}, 
                  '142': {'id': '142', 'name': 'Credo Defender', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 2, 'health': 19, 'level': '1', 'type': 5, 'adj_stats': 7.0, 'avg_skill': 4.5, 'skills': ['armored 4', 'besiege 5']}, 
                  '143': {'id': '143', 'name': 'Credo Defender', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 21, 'level': '2', 'type': 5, 'adj_stats': 8.333333333333334, 'avg_skill': 6.5, 'skills': ['armored 6', 'besiege 7']}, 
                  '144': {'id': '144', 'name': 'Credo Defender', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 25, 'level': '3', 'type': 5, 'adj_stats': 10.333333333333334, 'avg_skill': 8.5, 'skills': ['armored 8', 'besiege 9']}, 
                  '145': {'id': '145', 'name': 'Partisan', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 9, 'level': '1', 'type': 5, 'adj_stats': 4.5, 'avg_skill': 2.5, 'skills': ['heal Righteous 4', 'fortify 1']}, 
                  '146': {'id': '146', 'name': 'Partisan', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 0, 'health': 11, 'level': '2', 'type': 5, 'adj_stats': 11.0, 'avg_skill': 4.0, 'skills': ['heal Righteous 6', 'fortify 2']}, 
                  '147': {'id': '147', 'name': 'Partisan', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 0, 'health': 14, 'level': '3', 'type': 5, 'adj_stats': 14.0, 'avg_skill': 5.5, 'skills': ['heal Righteous 8', 'fortify 3']}, 
                  '178': {'id': '178', 'name': 'Sentry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 8, 'health': 7, 'level': '1', 'type': 5, 'adj_stats': 7.5, 'avg_skill': 0, 'skills': []}, 
                  '179': {'id': '179', 'name': 'Sentry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 9, 'health': 8, 'level': '2', 'type': 5, 'adj_stats': 8.5, 'avg_skill': 6.0, 'skills': ['heal 6']}, 
                  '180': {'id': '180', 'name': 'Sentry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 11, 'health': 9, 'level': '3', 'type': 5, 'adj_stats': 10.0, 'avg_skill': 10.0, 'skills': ['heal 10']}, 
                  '148': {'id': '148', 'name': 'Indebted Veteran', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 3, 'health': 21, 'level': '1', 'type': 5, 'adj_stats': 8.0, 'avg_skill': 3.5, 'skills': ['heal all Righteous 2', 'pierce 5']}, 
                  '149': {'id': '149', 'name': 'Indebted Veteran', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 25, 'level': '2', 'type': 5, 'adj_stats': 9.666666666666666, 'avg_skill': 5.0, 'skills': ['heal all Righteous 3', 'pierce 7']}, 
                  '150': {'id': '150', 'name': 'Indebted Veteran', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 25, 'level': '3', 'type': 5, 'adj_stats': 10.0, 'avg_skill': 6.5, 'skills': ['heal all Righteous 4', 'pierce 9']}, 
                  '151': {'id': '151', 'name': 'Indebted Veteran', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 28, 'level': '4', 'type': 5, 'adj_stats': 11.0, 'avg_skill': 7.5, 'skills': ['heal all Righteous 5', 'pierce 10']}}
        files = parse.find_files('^test_data_1.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.rarity = [1, 2]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        print(cards)
        assert cards == target

    def test_parse_cards_fusion_level_1(self):
        target = {'3': {'id': '3', 'name': 'Infantry', 'rarity': '1', 'adj_stats': 15.0, 'avg_skill': 0.0, 'skills': []}, 
        '351': {'id': '351', 'name': 'Bazooka Marine', 'rarity': '1', 'adj_stats': 12.0, 'avg_skill': 10.0, 'skills': ['pierce 10']}}
        files = parse.find_files('^test_data_2.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.fusion_level = [0]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        print(cards)
        assert cards == target

    def test_parse_cards_fusion_level_2(self):
        target = {}
        files = parse.find_files('^test_data_2.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.fusion_level = [1]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        assert cards == target

    def test_parse_cards_faction_1(self):
        target = {'3': {'id': '3', 'name': 'Infantry', 'rarity': '1', 'adj_stats': 15.0, 'avg_skill': 0.0, 'skills': []}, '351': {'id': '351', 'name': 'Bazooka Marine', 'rarity': '1', 'adj_stats': 12.0, 'avg_skill': 10.0, 'skills': ['pierce 10']}, '353': {'id': '353', 'name': 'Medic', 'rarity': '1', 'adj_stats': 11.0, 'avg_skill': 6.0, 'skills': ['fortify 6']}, '8': {'id': '8', 'name': 'Dreadnaught', 'rarity': '1', 'adj_stats': 9.333333333333334, 'avg_skill': 10.0, 'skills': ['armored 10', 'besiege 10']}, '11': {'id': '11', 'name': 'Rally Infantry', 'rarity': '1', 'adj_stats': 10.5, 'avg_skill': 9.0, 'skills': ['rally 9']}, '14': {'id': '14', 'name': 'Trap Setter', 'rarity': '1', 'adj_stats': 9.0, 'avg_skill': 8.666666666666666, 'skills': ['counter 10', 'heal all 8', 'weaken all 8']}, '355': {'id': '355', 'name': 'Barrage Tank', 'rarity': '1', 'adj_stats': 11.666666666666666, 'avg_skill': 9.5, 'skills': ['armored 10', 'strike 9']}, '168': {'id': '168', 'name': 'Swift Troops', 'rarity': '1', 'adj_stats': 11.333333333333334, 'avg_skill': 8.0, 'skills': ['rally all Imperial 8', 'strike 8']}, '19': {'id': '19', 'name': 'Terminator', 'rarity': '2', 'adj_stats': 12.0, 'avg_skill': 10.333333333333334, 'skills': ['armored 10', 'rally all Imperial 9', 'pierce 12']}, '25': {'id': '25', 'name': 'Tiamat', 'rarity': '3', 'adj_stats': 66.0, 'avg_skill': 84.0, 'skills': ['strike all 72', 'besiege all 90', 'hunt 90']}, '31': {'id': '31', 'name': 'Nimbus', 'rarity': '4', 'adj_stats': 16.666666666666668, 'avg_skill': 11.0, 'skills': ['heal all Imperial 15', 'protect all Imperial 8', 'weaken all 10']}, '385': {'id': '385', 'name': 'Poseidon', 'rarity': '3', 'adj_stats': 17.5, 'avg_skill': 23.333333333333332, 'skills': ['armored 30', 'heal all 20', 'besiege 20']}}
        files = parse.find_files('^test_data_1.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.faction = [1]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        print(cards)
        assert cards == target

    # Cost filter
    def test_parse_cards_faction_2(self):
        target = {}
        files = parse.find_files('^test_data_2.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.faction = [2]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        assert cards == target