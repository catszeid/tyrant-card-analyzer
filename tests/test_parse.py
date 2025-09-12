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

    def test_parse_cards_rarity_1(self):
        target = {'26': {'id': '26', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 30, 'level': '1', 'type': 1, 'adj_stats': 11.333333333333334, 'avg_skill': 5.0, 'skills': ['heal 6', 'weaken 4'], 'upgrade_id': '27'}, '27': {'id': '27', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 30, 'level': '2', 'type': 1, 'adj_stats': 12.0, 'avg_skill': 6.0, 'skills': ['heal Imperial 8', 'weaken all 4'], 'upgrade_id': '28'}, '28': {'id': '28', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 34, 'level': '3', 'type': 1, 'adj_stats': 13.333333333333334, 'avg_skill': 6.5, 'skills': ['heal all Imperial 8', 'weaken all 5'], 'upgrade_id': '29'}, '29': {'id': '29', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 8, 'health': 34, 'level': '4', 'type': 1, 'adj_stats': 14.0, 'avg_skill': 7.333333333333333, 'skills': ['heal all Imperial 10', 'protect Imperial 6', 'weaken all 6'], 'upgrade_id': '30'}, '30': {'id': '30', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 8, 'health': 37, 'level': '5', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 8.666666666666666, 'skills': ['heal all Imperial 12', 'protect all Imperial 6', 'weaken all 8'], 'upgrade_id': '31'}, '31': {'id': '31', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 10, 'health': 40, 'level': '6', 'type': 1, 'adj_stats': 16.666666666666668, 'avg_skill': 11.0, 'skills': ['heal all Imperial 15', 'protect all Imperial 8', 'weaken all 10'], 'upgrade_id': None}, 
                  '59': {'id': '59', 'name': 'Omega', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 43, 'level': '1', 'type': 2, 'adj_stats': 21.5, 'avg_skill': 19.0, 'skills': ['strike all 19', 'weaken all 19', 'besiege all 19'], 'upgrade_id': '60'}, '60': {'id': '60', 'name': 'Omega', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 48, 'level': '2', 'type': 2, 'adj_stats': 24.0, 'avg_skill': 21.0, 'skills': ['strike all 21', 'weaken all 21', 'besiege all 21'], 'upgrade_id': '61'}, '61': {'id': '61', 'name': 'Omega', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 52, 'level': '3', 'type': 2, 'adj_stats': 26.0, 'avg_skill': 24.0, 'skills': ['strike all 24', 'weaken all 24', 'besiege all 24'], 'upgrade_id': '62'}, '62': {'id': '62', 'name': 'Omega', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 57, 'level': '4', 'type': 2, 'adj_stats': 28.5, 'avg_skill': 26.0, 'skills': ['strike all 26', 'weaken all 26', 'besiege all 26'], 'upgrade_id': '63'}, '63': {'id': '63', 'name': 'Omega', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 61, 'level': '5', 'type': 2, 'adj_stats': 30.5, 'avg_skill': 28.0, 'skills': ['strike all 28', 'weaken all 28', 'besiege all 28'], 'upgrade_id': '64'}, '64': {'id': '64', 'name': 'Omega', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 1, 'attack': 0, 'health': 66, 'level': '6', 'type': 2, 'adj_stats': 33.0, 'avg_skill': 30.0, 'skills': ['strike all 30', 'weaken all 30', 'besiege all 30'], 'upgrade_id': None}, 
                  '92': {'id': '92', 'name': 'Malgoth', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 6, 'health': 40, 'level': '1', 'type': 3, 'adj_stats': 11.5, 'avg_skill': 7.0, 'skills': ['heal Xeno 8', 'rally all Xeno 6'], 'upgrade_id': '93'}, '93': {'id': '93', 'name': 'Malgoth', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 9, 'health': 45, 'level': '2', 'type': 3, 'adj_stats': 13.5, 'avg_skill': 8.0, 'skills': ['heal all Xeno 8', 'rally all Xeno 8'], 'upgrade_id': '94'}, '94': {'id': '94', 'name': 'Malgoth', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 9, 'health': 50, 'level': '3', 'type': 3, 'adj_stats': 14.75, 'avg_skill': 10.0, 'skills': ['heal all Xeno 10', 'rally all Xeno 10'], 'upgrade_id': '95'}, '95': {'id': '95', 'name': 'Malgoth', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 12, 'health': 50, 'level': '4', 'type': 3, 'adj_stats': 15.5, 'avg_skill': 12.0, 'skills': ['heal all Xeno 12', 'rally all Xeno 12'], 'upgrade_id': '96'}, '96': {'id': '96', 'name': 'Malgoth', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 12, 'health': 55, 'level': '5', 'type': 3, 'adj_stats': 16.75, 'avg_skill': 12.0, 'skills': ['heal all Xeno 13', 'rally all Xeno 13', 'berserk 10'], 'upgrade_id': '97'}, '97': {'id': '97', 'name': 'Malgoth', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 60, 'level': '6', 'type': 3, 'adj_stats': 18.75, 'avg_skill': 15.0, 'skills': ['heal all Xeno 15', 'rally all Xeno 15', 'berserk 15'], 'upgrade_id': None}, 
                  '125': {'id': '125', 'name': 'Apex', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 10, 'health': 80, 'level': '1', 'type': 4, 'adj_stats': 22.5, 'avg_skill': 25.666666666666668, 'skills': ['poison 35', 'strike 12', 'refresh 30'], 'upgrade_id': '126'}, '126': {'id': '126', 'name': 'Apex', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 80, 'level': '2', 'type': 4, 'adj_stats': 23.75, 'avg_skill': 30.0, 'skills': ['poison 40', 'strike 15', 'refresh 35'], 'upgrade_id': '127'}, '127': {'id': '127', 'name': 'Apex', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 90, 'level': '3', 'type': 4, 'adj_stats': 26.25, 'avg_skill': 34.0, 'skills': ['poison 45', 'strike 17', 'refresh 40'], 'upgrade_id': '128'}, '128': {'id': '128', 'name': 'Apex', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 100, 'level': '4', 'type': 4, 'adj_stats': 28.75, 'avg_skill': 34.0, 'skills': ['poison 45', 'strike 17', 'refresh 40'], 'upgrade_id': '129'}, '129': {'id': '129', 'name': 'Apex', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 20, 'health': 100, 'level': '5', 'type': 4, 'adj_stats': 30.0, 'avg_skill': 37.333333333333336, 'skills': ['poison 50', 'strike all 17', 'refresh 45'], 'upgrade_id': '130'}, '130': {'id': '130', 'name': 'Apex', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 3, 'attack': 25, 'health': 110, 'level': '6', 'type': 4, 'adj_stats': 33.75, 'avg_skill': 41.0, 'skills': ['poison 55', 'strike all 18', 'refresh 50'], 'upgrade_id': None}, 
                  '158': {'id': '158', 'name': 'Benediction', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 4, 'attack': 5, 'health': 40, 'level': '1', 'type': 5, 'adj_stats': 9.0, 'avg_skill': 9.0, 'skills': ['rally Righteous 9'], 'upgrade_id': '159'}, '159': {'id': '159', 'name': 'Benediction', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 4, 'attack': 7, 'health': 43, 'level': '2', 'type': 5, 'adj_stats': 10.0, 'avg_skill': 9.0, 'skills': ['rally Righteous 11', 'besiege 7'], 'upgrade_id': '160'}, '160': {'id': '160', 'name': 'Benediction', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 4, 'attack': 9, 'health': 48, 'level': '3', 'type': 5, 'adj_stats': 11.4, 'avg_skill': 10.0, 'skills': ['evade 1', 'rally Righteous 13', 'besiege all 7'], 'upgrade_id': '161'}, '161': {'id': '161', 'name': 'Benediction', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 4, 'attack': 11, 'health': 52, 'level': '4', 'type': 5, 'adj_stats': 12.6, 'avg_skill': 11.333333333333334, 'skills': ['evade 1', 'rally Righteous 15', 'besiege all 9'], 'upgrade_id': '162'}, '162': {'id': '162', 'name': 'Benediction', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 4, 'attack': 13, 'health': 56, 'level': '5', 'type': 5, 'adj_stats': 13.8, 'avg_skill': 15.666666666666666, 'skills': ['evade 2', 'rally all Righteous 15', 'besiege all 12'], 'upgrade_id': '163'}, '163': {'id': '163', 'name': 'Benediction', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 4, 'attack': 15, 'health': 60, 'level': '6', 'type': 5, 'adj_stats': 15.0, 'avg_skill': 21.0, 'skills': ['evade 3', 'rally all Righteous 18', 'besiege all 15'], 'upgrade_id': None}}
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
        target = {'1': {'id': '1', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 1, 'health': 6, 'level': '1', 'type': 1, 'adj_stats': 7.0, 'avg_skill': 0, 'skills': [], 'upgrade_id': '2'}, 
                  '2': {'id': '2', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 2, 'health': 9, 'level': '2', 'type': 1, 'adj_stats': 11.0, 'avg_skill': 0, 'skills': [], 'upgrade_id': '3'}, 
                  '3': {'id': '3', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 3, 'health': 12, 'level': '3', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 0, 'skills': [], 'upgrade_id': None}, 
                  '4': {'id': '4', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 9, 'level': '1', 'type': 1, 'adj_stats': 6.0, 'avg_skill': 5.0, 'skills': ['pierce 5'], 'upgrade_id': '350'}, 
                  '350': {'id': '350', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 5, 'health': 14, 'level': '2', 'type': 1, 'adj_stats': 9.5, 'avg_skill': 7.0, 'skills': ['pierce 7'], 'upgrade_id': '351'}, 
                  '351': {'id': '351', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 6, 'health': 18, 'level': '3', 'type': 1, 'adj_stats': 12.0, 'avg_skill': 10.0, 'skills': ['pierce 10'], 'upgrade_id': None}, 
                  '16': {'id': '16', 'name': 'Terminator', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 5, 'health': 22, 'level': '1', 'type': 1, 'adj_stats': 6.75, 'avg_skill': 6.5, 'skills': ['armored 7', 'rally Imperial 6'], 'upgrade_id': '17'}, 
                  '17': {'id': '17', 'name': 'Terminator', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 6, 'health': 27, 'level': '2', 'type': 1, 'adj_stats': 8.25, 'avg_skill': 7.666666666666667, 'skills': ['armored 8', 'rally all Imperial 7', 'pierce 8'], 'upgrade_id': '18'}, 
                  '18': {'id': '18', 'name': 'Terminator', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 8, 'health': 33, 'level': '3', 'type': 1, 'adj_stats': 10.25, 'avg_skill': 9.0, 'skills': ['armored 9', 'rally all Imperial 8', 'pierce 10'], 'upgrade_id': '19'}, 
                  '19': {'id': '19', 'name': 'Terminator', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 9, 'health': 39, 'level': '4', 'type': 1, 'adj_stats': 12.0, 'avg_skill': 10.333333333333334, 'skills': ['armored 10', 'rally all Imperial 9', 'pierce 12'], 'upgrade_id': None}, 
                  '34': {'id': '34', 'name': 'Grunt', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 1, 'health': 5, 'level': '1', 'type': 2, 'adj_stats': 6.0, 'avg_skill': 5.0, 'skills': ['pierce 5'], 'upgrade_id': '356'}, 
                  '356': {'id': '356', 'name': 'Grunt', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 2, 'health': 7, 'level': '2', 'type': 2, 'adj_stats': 9.0, 'avg_skill': 7.0, 'skills': ['pierce 7'], 'upgrade_id': '357'}, 
                  '357': {'id': '357', 'name': 'Grunt', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 3, 'health': 10, 'level': '3', 'type': 2, 'adj_stats': 13.0, 'avg_skill': 10.0, 'skills': ['pierce 10'], 'upgrade_id': None}, 
                  '35': {'id': '35', 'name': 'Headhunter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 3, 'health': 14, 'level': '1', 'type': 2, 'adj_stats': 5.666666666666667, 'avg_skill': 5.0, 'skills': ['hunt 5'], 'upgrade_id': '36'}, 
                  '36': {'id': '36', 'name': 'Headhunter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 18, 'level': '2', 'type': 2, 'adj_stats': 7.333333333333333, 'avg_skill': 7.0, 'skills': ['hunt 7'], 'upgrade_id': '37'}, 
                  '37': {'id': '37', 'name': 'Headhunter', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 22, 'level': '3', 'type': 2, 'adj_stats': 9.0, 'avg_skill': 10.0, 'skills': ['hunt 10'], 'upgrade_id': None}, 
                  '49': {'id': '49', 'name': 'Blitz Armor', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 4, 'health': 16, 'level': '1', 'type': 2, 'adj_stats': 5.0, 'avg_skill': 5.5, 'skills': ['armored 5', 'rally Raider 6'], 'upgrade_id': '50'}, 
                  '50': {'id': '50', 'name': 'Blitz Armor', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 5, 'health': 19, 'level': '2', 'type': 2, 'adj_stats': 6.0, 'avg_skill': 6.5, 'skills': ['armored 6', 'rally Raider 7'], 'upgrade_id': '51'}, 
                  '51': {'id': '51', 'name': 'Blitz Armor', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 22, 'level': '3', 'type': 2, 'adj_stats': 9.0, 'avg_skill': 7.5, 'skills': ['armored 7', 'rally Raider 8'], 'upgrade_id': '52'}, 
                  '52': {'id': '52', 'name': 'Blitz Armor', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 26, 'level': '4', 'type': 2, 'adj_stats': 10.666666666666666, 'avg_skill': 8.5, 'skills': ['armored 8', 'rally Raider 9'], 'upgrade_id': None}, 
                  '67': {'id': '67', 'name': 'Devourer', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 6, 'health': 22, 'level': '1', 'type': 3, 'adj_stats': 5.6, 'avg_skill': 4.5, 'skills': ['strike 6', 'avenge 3'], 'upgrade_id': '68'}, 
                  '68': {'id': '68', 'name': 'Devourer', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 7, 'health': 26, 'level': '2', 'type': 3, 'adj_stats': 8.25, 'avg_skill': 6.5, 'skills': ['strike 8', 'avenge 5'], 'upgrade_id': '69'}, 
                  '69': {'id': '69', 'name': 'Devourer', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 3, 'attack': 9, 'health': 29, 'level': '3', 'type': 3, 'adj_stats': 9.5, 'avg_skill': 8.5, 'skills': ['strike 10', 'avenge 7'], 'upgrade_id': None}, 
                  '70': {'id': '70', 'name': 'Locust Swarm', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 14, 'level': '1', 'type': 3, 'adj_stats': 6.0, 'avg_skill': 5.0, 'skills': ['counter 5'], 'upgrade_id': '362'}, 
                  '362': {'id': '362', 'name': 'Locust Swarm', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 18, 'level': '2', 'type': 3, 'adj_stats': 7.666666666666667, 'avg_skill': 5.5, 'skills': ['counter 7', 'legion 2'], 'upgrade_id': '363'}, 
                  '363': {'id': '363', 'name': 'Locust Swarm', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 7, 'health': 23, 'level': '3', 'type': 3, 'adj_stats': 10.0, 'avg_skill': 7.5, 'skills': ['counter 9', 'legion 3'], 'upgrade_id': None}, 
                  '82': {'id': '82', 'name': 'Brood Walker', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 3, 'health': 19, 'level': '1', 'type': 3, 'adj_stats': 7.333333333333333, 'avg_skill': 5.0, 'skills': ['rally Xeno 5', 'strike 5'], 'upgrade_id': '83'}, 
                  '83': {'id': '83', 'name': 'Brood Walker', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 22, 'level': '2', 'type': 3, 'adj_stats': 8.666666666666666, 'avg_skill': 6.0, 'skills': ['rally Xeno 6', 'strike 6'], 'upgrade_id': '84'}, 
                  '84': {'id': '84', 'name': 'Brood Walker', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 26, 'level': '3', 'type': 3, 'adj_stats': 10.333333333333334, 'avg_skill': 6.5, 'skills': ['rally all Xeno 6', 'strike 7'], 'upgrade_id': '85'}, 
                  '85': {'id': '85', 'name': 'Brood Walker', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 29, 'level': '4', 'type': 3, 'adj_stats': 11.666666666666666, 'avg_skill': 7.5, 'skills': ['rally all Xeno 7', 'strike 8'], 'upgrade_id': None}, 
                  '100': {'id': '100', 'name': 'Enfeebler', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 2, 'health': 13, 'level': '1', 'type': 4, 'adj_stats': 7.5, 'avg_skill': 4.0, 'skills': ['enfeeble 4'], 'upgrade_id': '101'}, 
                  '101': {'id': '101', 'name': 'Enfeebler', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 16, 'level': '2', 'type': 4, 'adj_stats': 9.5, 'avg_skill': 6.0, 'skills': ['enfeeble 6'], 'upgrade_id': '102'}, 
                  '102': {'id': '102', 'name': 'Enfeebler', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 4, 'health': 19, 'level': '3', 'type': 4, 'adj_stats': 11.5, 'avg_skill': 8.0, 'skills': ['enfeeble 8'], 'upgrade_id': None}, 
                  '103': {'id': '103', 'name': 'Xeno Mauler', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 7, 'health': 27, 'level': '1', 'type': 4, 'adj_stats': 6.8, 'avg_skill': 6.0, 'skills': ['strike 6'], 'upgrade_id': '368'}, 
                  '368': {'id': '368', 'name': 'Xeno Mauler', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 9, 'health': 33, 'level': '2', 'type': 4, 'adj_stats': 8.4, 'avg_skill': 6.0, 'skills': ['strike all 6'], 'upgrade_id': '369'}, 
                  '369': {'id': '369', 'name': 'Xeno Mauler', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 11, 'health': 39, 'level': '3', 'type': 4, 'adj_stats': 10.0, 'avg_skill': 8.0, 'skills': ['strike all 8'], 'upgrade_id': None}, 
                  '115': {'id': '115', 'name': 'Enclave Remnant', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 4, 'attack': 10, 'health': 32, 'level': '1', 'type': 4, 'adj_stats': 8.4, 'avg_skill': 6.0, 'skills': ['weaken 6', 'besiege 6'], 'upgrade_id': '116'}, 
                  '116': {'id': '116', 'name': 'Enclave Remnant', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 4, 'attack': 10, 'health': 36, 'level': '2', 'type': 4, 'adj_stats': 9.2, 'avg_skill': 7.0, 'skills': ['weaken 7', 'besiege all 7'], 'upgrade_id': '117'}, 
                  '117': {'id': '117', 'name': 'Enclave Remnant', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 4, 'attack': 12, 'health': 36, 'level': '3', 'type': 4, 'adj_stats': 9.6, 'avg_skill': 7.5, 'skills': ['weaken all 7', 'besiege all 8'], 'upgrade_id': '118'}, 
                  '118': {'id': '118', 'name': 'Enclave Remnant', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 4, 'attack': 14, 'health': 40, 'level': '4', 'type': 4, 'adj_stats': 10.8, 'avg_skill': 8.5, 'skills': ['weaken all 8', 'besiege all 9'], 'upgrade_id': None}, 
                  '133': {'id': '133', 'name': 'Peacekeeper', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 2, 'health': 18, 'level': '1', 'type': 5, 'adj_stats': 6.666666666666667, 'avg_skill': 5.0, 'skills': ['heal 5'], 'upgrade_id': '374'}, 
                  '374': {'id': '374', 'name': 'Peacekeeper', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 2, 'health': 22, 'level': '2', 'type': 5, 'adj_stats': 8.0, 'avg_skill': 6.5, 'skills': ['heal 7', 'coalition 3'], 'upgrade_id': '375'}, 
                  '375': {'id': '375', 'name': 'Peacekeeper', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 26, 'level': '3', 'type': 5, 'adj_stats': 10.0, 'avg_skill': 10.0, 'skills': ['heal 10', 'coalition 5'], 'upgrade_id': None}, 
                  '134': {'id': '134', 'name': 'Pylon', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 6, 'health': 26, 'level': '1', 'type': 5, 'adj_stats': 6.4, 'avg_skill': 6.0, 'skills': ['armored 7', 'barrier 5'], 'upgrade_id': '135'}, 
                  '135': {'id': '135', 'name': 'Pylon', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 7, 'health': 30, 'level': '2', 'type': 5, 'adj_stats': 7.4, 'avg_skill': 8.0, 'skills': ['armored 9', 'barrier 7'], 'upgrade_id': '136'}, 
                  '136': {'id': '136', 'name': 'Pylon', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 4, 'attack': 8, 'health': 34, 'level': '3', 'type': 5, 'adj_stats': 8.4, 'avg_skill': 10.5, 'skills': ['armored 12', 'barrier 9'], 'upgrade_id': None}, 
                  '148': {'id': '148', 'name': 'Indebted Veteran', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 3, 'health': 21, 'level': '1', 'type': 5, 'adj_stats': 8.0, 'avg_skill': 3.5, 'skills': ['heal all Righteous 2', 'pierce 5'], 'upgrade_id': '149'}, 
                  '149': {'id': '149', 'name': 'Indebted Veteran', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 25, 'level': '2', 'type': 5, 'adj_stats': 9.666666666666666, 'avg_skill': 5.0, 'skills': ['heal all Righteous 3', 'pierce 7'], 'upgrade_id': '150'}, 
                  '150': {'id': '150', 'name': 'Indebted Veteran', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 25, 'level': '3', 'type': 5, 'adj_stats': 10.0, 'avg_skill': 6.5, 'skills': ['heal all Righteous 4', 'pierce 9'], 'upgrade_id': '151'}, 
                  '151': {'id': '151', 'name': 'Indebted Veteran', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 2, 'attack': 5, 'health': 28, 'level': '4', 'type': 5, 'adj_stats': 11.0, 'avg_skill': 7.5, 'skills': ['heal all Righteous 5', 'pierce 10'], 'upgrade_id': None}}
        files = parse.find_files('^test_data_1.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.rarity = [1, 2]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        print(cards)
        assert cards == target

    def test_parse_cards_fusion_level_1(self):
        target = {'1': {'id': '1', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 1, 'health': 6, 'level': '1', 'type': 1, 'adj_stats': 7.0, 'avg_skill': 0, 'skills': [], 'upgrade_id': '2'}, '2': {'id': '2', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 2, 'health': 9, 'level': '2', 'type': 1, 'adj_stats': 11.0, 'avg_skill': 0, 'skills': [], 'upgrade_id': '3'}, 
                  '3': {'id': '3', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 3, 'health': 12, 'level': '3', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 0, 'skills': [], 'upgrade_id': None}, '4': {'id': '4', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 9, 'level': '1', 'type': 1, 'adj_stats': 6.0, 'avg_skill': 5.0, 'skills': ['pierce 5'], 'upgrade_id': '350'}, 
                  '350': {'id': '350', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 5, 'health': 14, 'level': '2', 'type': 1, 'adj_stats': 9.5, 'avg_skill': 7.0, 'skills': ['pierce 7'], 'upgrade_id': '351'}, 
                  '351': {'id': '351', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 6, 'health': 18, 'level': '3', 'type': 1, 'adj_stats': 12.0, 'avg_skill': 10.0, 'skills': ['pierce 10'], 'upgrade_id': None}}
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
        target = {'1': {'id': '1', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 1, 'health': 6, 'level': '1', 'type': 1, 'adj_stats': 7.0, 'avg_skill': 0, 'skills': [], 'upgrade_id': '2'}, 
                  '2': {'id': '2', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 2, 'health': 9, 'level': '2', 'type': 1, 'adj_stats': 11.0, 'avg_skill': 0, 'skills': [], 'upgrade_id': '3'}, 
                  '3': {'id': '3', 'name': 'Infantry', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 0, 'attack': 3, 'health': 12, 'level': '3', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 0, 'skills': [], 'upgrade_id': None}, 
                  '4': {'id': '4', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 3, 'health': 9, 'level': '1', 'type': 1, 'adj_stats': 6.0, 'avg_skill': 5.0, 'skills': ['pierce 5'], 'upgrade_id': '350'}, 
                  '350': {'id': '350', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 5, 'health': 14, 'level': '2', 'type': 1, 'adj_stats': 9.5, 'avg_skill': 7.0, 'skills': ['pierce 7'], 'upgrade_id': '351'}, 
                  '351': {'id': '351', 'name': 'Bazooka Marine', 'set': '1000', 'rarity': '1', 'fusion_level': 0, 'cost': 1, 'attack': 6, 'health': 18, 'level': '3', 'type': 1, 'adj_stats': 12.0, 'avg_skill': 10.0, 'skills': ['pierce 10'], 'upgrade_id': None}, 
                  '16': {'id': '16', 'name': 'Terminator', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 5, 'health': 22, 'level': '1', 'type': 1, 'adj_stats': 6.75, 'avg_skill': 6.5, 'skills': ['armored 7', 'rally Imperial 6'], 'upgrade_id': '17'}, 
                  '17': {'id': '17', 'name': 'Terminator', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 6, 'health': 27, 'level': '2', 'type': 1, 'adj_stats': 8.25, 'avg_skill': 7.666666666666667, 'skills': ['armored 8', 'rally all Imperial 7', 'pierce 8'], 'upgrade_id': '18'}, 
                  '18': {'id': '18', 'name': 'Terminator', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 8, 'health': 33, 'level': '3', 'type': 1, 'adj_stats': 10.25, 'avg_skill': 9.0, 'skills': ['armored 9', 'rally all Imperial 8', 'pierce 10'], 'upgrade_id': '19'}, 
                  '19': {'id': '19', 'name': 'Terminator', 'set': '1000', 'rarity': '2', 'fusion_level': 0, 'cost': 3, 'attack': 9, 'health': 39, 'level': '4', 'type': 1, 'adj_stats': 12.0, 'avg_skill': 10.333333333333334, 'skills': ['armored 10', 'rally all Imperial 9', 'pierce 12'], 'upgrade_id': None}, 
                '20': {'id': '20', 'name': 'Tiamat', 'set': '1000', 'rarity': '3', 'fusion_level': 0, 'cost': 1, 'attack': 39, 'health': 47, 'level': '1', 'type': 1, 'adj_stats': 43.0, 'avg_skill': 55.0, 'skills': ['strike all 47', 'besiege all 59', 'hunt 59'], 'upgrade_id': '21'}, 
                '21': {'id': '21', 'name': 'Tiamat', 'set': '1000', 'rarity': '3', 'fusion_level': 0, 'cost': 1, 'attack': 43, 'health': 52, 'level': '2', 'type': 1, 'adj_stats': 47.5, 'avg_skill': 60.666666666666664, 'skills': ['strike all 52', 'besiege all 65', 'hunt 65'], 'upgrade_id': '22'}, 
                '22': {'id': '22', 'name': 'Tiamat', 'set': '1000', 'rarity': '3', 'fusion_level': 0, 'cost': 1, 'attack': 48, 'health': 57, 'level': '3', 'type': 1, 'adj_stats': 52.5, 'avg_skill': 67.0, 'skills': ['strike all 57', 'besiege all 72', 'hunt 72'], 'upgrade_id': '23'}, 
                '23': {'id': '23', 'name': 'Tiamat', 'set': '1000', 'rarity': '3', 'fusion_level': 0, 'cost': 1, 'attack': 52, 'health': 62, 'level': '4', 'type': 1, 'adj_stats': 57.0, 'avg_skill': 72.66666666666667, 'skills': ['strike all 62', 'besiege all 78', 'hunt 78'], 'upgrade_id': '24'}, 
                '24': {'id': '24', 'name': 'Tiamat', 'set': '1000', 'rarity': '3', 'fusion_level': 0, 'cost': 1, 'attack': 56, 'health': 67, 'level': '5', 'type': 1, 'adj_stats': 61.5, 'avg_skill': 78.33333333333333, 'skills': ['strike all 67', 'besiege all 84', 'hunt 84'], 'upgrade_id': '25'}, 
                '25': {'id': '25', 'name': 'Tiamat', 'set': '1000', 'rarity': '3', 'fusion_level': 0, 'cost': 1, 'attack': 60, 'health': 72, 'level': '6', 'type': 1, 'adj_stats': 66.0, 'avg_skill': 84.0, 'skills': ['strike all 72', 'besiege all 90', 'hunt 90'], 'upgrade_id': None}, 
                '26': {'id': '26', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 4, 'health': 30, 'level': '1', 'type': 1, 'adj_stats': 11.333333333333334, 'avg_skill': 5.0, 'skills': ['heal 6', 'weaken 4'], 'upgrade_id': '27'}, 
                '27': {'id': '27', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 30, 'level': '2', 'type': 1, 'adj_stats': 12.0, 'avg_skill': 6.0, 'skills': ['heal Imperial 8', 'weaken all 4'], 'upgrade_id': '28'}, 
                '28': {'id': '28', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 6, 'health': 34, 'level': '3', 'type': 1, 'adj_stats': 13.333333333333334, 'avg_skill': 6.5, 'skills': ['heal all Imperial 8', 'weaken all 5'], 'upgrade_id': '29'}, 
                '29': {'id': '29', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 8, 'health': 34, 'level': '4', 'type': 1, 'adj_stats': 14.0, 'avg_skill': 7.333333333333333, 'skills': ['heal all Imperial 10', 'protect Imperial 6', 'weaken all 6'], 'upgrade_id': '30'}, 
                '30': {'id': '30', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 8, 'health': 37, 'level': '5', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 8.666666666666666, 'skills': ['heal all Imperial 12', 'protect all Imperial 6', 'weaken all 8'], 'upgrade_id': '31'}, 
                '31': {'id': '31', 'name': 'Nimbus', 'set': '1000', 'rarity': '4', 'fusion_level': 0, 'cost': 2, 'attack': 10, 'health': 40, 'level': '6', 'type': 1, 'adj_stats': 16.666666666666668, 'avg_skill': 11.0, 'skills': ['heal all Imperial 15', 'protect all Imperial 8', 'weaken all 10'], 'upgrade_id': None}, 
                '380': {'id': '380', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 45, 'level': '1', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15'], 'upgrade_id': '381'}, 
                '381': {'id': '381', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 45, 'level': '2', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15'], 'upgrade_id': '382'}, 
                '382': {'id': '382', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 45, 'level': '3', 'type': 1, 'adj_stats': 15.0, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15'], 'upgrade_id': '383'}, 
                '383': {'id': '383', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 55, 'level': '4', 'type': 1, 'adj_stats': 17.5, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15'], 'upgrade_id': '384'}, 
                '384': {'id': '384', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 55, 'level': '5', 'type': 1, 'adj_stats': 17.5, 'avg_skill': 16.666666666666668, 'skills': ['armored 20', 'heal all 15', 'besiege 15'], 'upgrade_id': '385'}, 
                  '385': {'id': '385', 'name': 'Poseidon', 'set': '9000', 'rarity': '3', 'fusion_level': 0, 'cost': 3, 'attack': 15, 'health': 55, 'level': '6', 'type': 1, 'adj_stats': 17.5, 'avg_skill': 23.333333333333332, 'skills': ['armored 30', 'heal all 20', 'besiege 20'], 'upgrade_id': None}}
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