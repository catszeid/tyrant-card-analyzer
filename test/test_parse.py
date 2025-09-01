import parse
import random

class TestParse:
    test_folder = 'test'

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
        target = {'3': {'id': '3', 'name': 'Infantry', 'rarity': '1', 'adj_stats': 15.0, 'avg_skill': 0.0, 'skills': []}, 
        '351': {'id': '351', 'name': 'Bazooka Marine', 'rarity': '1', 'adj_stats': 12.0, 'avg_skill': 10.0, 'skills': ['pierce 10']}}
        files = parse.find_files('^test_data_2.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        assert cards == target
    
    def test_parse_cards_set_1(self):
        target = {'385': {'id': '385', 'name': 'Poseidon', 'rarity': '3', 'adj_stats': 17.5, 'avg_skill': 23.333333333333332, 'skills': ['armored 30', 'heal all 20', 'besiege 20']}}
        files = parse.find_files('^test_data_1.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.set = [9000]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
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
        target = {'31': {'id': '31', 'name': 'Nimbus', 'rarity': '4', 'adj_stats': 16.666666666666668, 'avg_skill': 11.0, 'skills': ['heal all Imperial 15', 'protect all Imperial 8', 'weaken all 10']}, '64': {'id': '64', 'name': 'Omega', 'rarity': '4', 'adj_stats': 33.0, 'avg_skill': 30.0, 'skills': ['strike all 30', 'weaken all 30', 'besiege all 30']}, '97': {'id': '97', 'name': 'Malgoth', 'rarity': '4', 'adj_stats': 18.75, 'avg_skill': 15.0, 'skills': ['heal all Xeno 15', 'rally all Xeno 15', 'berserk 15']}, '130': {'id': '130', 'name': 'Apex', 'rarity': '4', 'adj_stats': 33.75, 'avg_skill': 41.0, 'skills': ['poison 55', 'strike all 18', 'refresh 50']}, '163': {'id': '163', 'name': 'Benediction', 'rarity': '4', 'adj_stats': 15.0, 'avg_skill': 21.0, 'skills': ['evade 3', 'rally all Righteous 18', 'besiege all 15']}}
        files = parse.find_files('^test_data_1.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.rarity = [4]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
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
        target = {
            '3': {'id': '3', 'name': 'Infantry', 'rarity': '1', 'adj_stats': 15.0, 'avg_skill': 0.0, 'skills': []}, 
            '351': {'id': '351', 'name': 'Bazooka Marine', 'rarity': '1', 'adj_stats': 12.0, 'avg_skill': 10.0, 'skills': ['pierce 10']}, 
            '353': {'id': '353', 'name': 'Medic', 'rarity': '1', 'adj_stats': 11.0, 'avg_skill': 6.0, 'skills': ['fortify 6']}, 
            '8': {'id': '8', 'name': 'Dreadnaught', 'rarity': '1', 'adj_stats': 9.333333333333334, 'avg_skill': 10.0, 'skills': ['armored 10', 'besiege 10']}, 
            '11': {'id': '11', 'name': 'Rally Infantry', 'rarity': '1', 'adj_stats': 10.5, 'avg_skill': 9.0, 'skills': ['rally 9']}, 
            '14': {'id': '14', 'name': 'Trap Setter', 'rarity': '1', 'adj_stats': 9.0, 'avg_skill': 8.666666666666666, 'skills': ['counter 10', 'heal all 8', 'weaken all 8']}, 
            '355': {'id': '355', 'name': 'Barrage Tank', 'rarity': '1', 'adj_stats': 11.666666666666666, 'avg_skill': 9.5, 'skills': ['armored 10', 'strike 9']}, 
            '168': {'id': '168', 'name': 'Swift Troops', 'rarity': '1', 'adj_stats': 11.333333333333334, 'avg_skill': 8.0, 'skills': ['rally all Imperial 8', 'strike 8']}, 
            '19': {'id': '19', 'name': 'Terminator', 'rarity': '2', 'adj_stats': 12.0, 'avg_skill': 10.333333333333334, 'skills': ['armored 10', 'rally all Imperial 9', 'pierce 12']}, 
            '357': {'id': '357', 'name': 'Grunt', 'rarity': '1', 'adj_stats': 13.0, 'avg_skill': 10.0, 'skills': ['pierce 10']}, 
            '37': {'id': '37', 'name': 'Headhunter', 'rarity': '1', 'adj_stats': 9.0, 'avg_skill': 10.0, 'skills': ['hunt 10']}, 
            '359': {'id': '359', 'name': 'Dread Panzer', 'rarity': '1', 'adj_stats': 10.0, 'avg_skill': 11.0, 'skills': ['counter 11']}, 
            '41': {'id': '41', 'name': 'Bombardment Tank', 'rarity': '1', 'adj_stats': 11.0, 'avg_skill': 6.5, 'skills': ['armored 7', 'strike 6']}, 
            '44': {'id': '44', 'name': 'Combat Specialist', 'rarity': '1', 'adj_stats': 10.666666666666666, 'avg_skill': 10.0, 'skills': ['weaken 8', 'pierce 12']}, 
            '361': {'id': '361', 'name': 'Hydroblade', 'rarity': '1', 'adj_stats': 18.0, 'avg_skill': 5.0, 'skills': ['berserk 5']}, 
            '48': {'id': '48', 'name': 'Scorpinox', 'rarity': '1', 'adj_stats': 9.25, 'avg_skill': 8.666666666666666, 'skills': ['counter 8', 'avenge 7', 'poison 11']}, 
            '171': {'id': '171', 'name': 'Mortar Mech', 'rarity': '1', 'adj_stats': 9.4, 'avg_skill': 12.333333333333334, 'skills': ['strike 10', 'besiege 12', 'pierce 15']}, 
            '52': {'id': '52', 'name': 'Blitz Armor', 'rarity': '2', 'adj_stats': 10.666666666666666, 'avg_skill': 8.5, 'skills': ['armored 8', 'rally Raider 9']}, 
            '69': {'id': '69', 'name': 'Devourer', 'rarity': '1', 'adj_stats': 9.5, 'avg_skill': 8.5, 'skills': ['strike 10', 'avenge 7']}, 
            '363': {'id': '363', 'name': 'Locust Swarm', 'rarity': '1', 'adj_stats': 10.0, 'avg_skill': 7.5, 'skills': ['counter 9', 'legion 3']}, 
            '365': {'id': '365', 'name': 'Rabid Corruptor', 'rarity': '1', 'adj_stats': 12.0, 'avg_skill': 8.0, 'skills': ['weaken 8', 'poison 8']}, 
            '74': {'id': '74', 'name': 'Annelid Mass', 'rarity': '1', 'adj_stats': 18.0, 'avg_skill': 9.0, 'skills': ['leech 9']}, 
            '77': {'id': '77', 'name': 'Scavenger', 'rarity': '1', 'adj_stats': 7.25, 'avg_skill': 7.0, 'skills': ['rally all Xeno 6', 'scavenge 4']}, 
            '80': {'id': '80', 'name': 'Acid Spewer', 'rarity': '1', 'adj_stats': 9.0, 'avg_skill': 10.5, 'skills': ['pierce 12', 'poison 9']}, 
            '367': {'id': '367', 'name': 'Carcass Scrounge', 'rarity': '1', 'adj_stats': 10.5, 'avg_skill': 6.5, 'skills': ['enrage 5', 'rally Xeno 8']}, 
            '174': {'id': '174', 'name': 'Banshee', 'rarity': '1', 'adj_stats': 9.4, 'avg_skill': 10.666666666666666, 'skills': ['rally all Xeno 8', 'weaken 12', 'leech 12']}, 
            '85': {'id': '85', 'name': 'Brood Walker', 'rarity': '2', 'adj_stats': 11.666666666666666, 'avg_sarity': '1', 'adj_stats': 10.5, 'avg_skill': 6.5, 'skills': ['enrage 5', 'rally Xeno 8']},  
            '174': {'id': '174', 'name': 'Banshee', 'rarity': '1', 'adj_stats': 9.4, 'avg_skill': 10.666666666666666, 'skills': ['rally all Xeno 8', 'weaken 12', 'leech 12']}, 
            '85': {'id': '85', 'name': 'Brood Walker', 'rarity': '2', 'adj_stats': 11.666666666666666, 'avg_skill': 7.5, 'skills': ['rally all Xeno 7', 'strike 8']}, 
            '102': {'id': '102', 'name': 'Enfeebler', 'rarity': '1', 'adj_stats': 11.5, 'avg_skill': 8.0, 'skills': ['enfeeble 8']}, 
            '369': {'id': '369', 'name': 'Xeno Mauler', 'rarity': '1', 'adj_stats': 10.0, 'avg_skill': 8.0, 'skills': ['strike all 8']}, 
            '371': {'id': '371', 'name': 'Enclave Parasite', 'rarity': '1', 'adj_stats': 10.333333333333334, 'avg_skill': 9.5, 'skills': ['counter 10', 'leech 9']}, 
            '373': {'id': '373', 'name': 'Exogrunt', 'rarity': '1', 'adj_stats': 11.0, 'avg_skill': 8.0, 'skills': ['strike 8']}, 
            '108': {'id': '108', 'name': 'Cavern Smelter', 'rarity': '1', 'adj_stats': 7.6, 'avg_skill': 8.0, 'skills': ['avenge 8']}, 
            '111': {'id': '111', 'name': 'Dracus Wyrm', 'rarity': '1', 'adj_stats': 11.333333333333334, 'avg_skill': 12.0, 'skills': ['poison 12']}, 
            '114': {'id': '114', 'name': 'Tunneller', 'rarity': '1', 'adj_stats': 11.666666666666666, 'avg_skill': 11.0, 'skills': ['besiege 10', 'pierce 12']}, 
            '177': {'id': '177', 'name': 'Achawin', 'rarity': '1', 'adj_stats': 10.0, 'avg_skill': 9.0, 'skills': ['counter 10', 'weaken 8']}, 
            '118': {'id': '118', 'name': 'Enclave Remnant', 'rarity': '2', 'adj_stats': 10.8, 'avg_skill': 8.5, 'skills': ['weaken all 8', 'besiege all 9']}, 
            '375': {'id': '375', 'name': 'Peacekeeper', 'rarity': '1', 'adj_stats': 10.0, 'avg_skill': 10.0, 'skills': ['heal 10', 'coalition 5']}, 
            '136': {'id': '136', 'name': 'Pylon', 'rarity': '1', 'adj_stats': 8.4, 'avg_skill': 10.5, 'skills': ['armored 12', 'barrier 9']}, 
            '377': {'id': '377', 'name': 'Iron Eagle', 'rarity': '1', 'adj_stats': 9.0, 'avg_skill': 9.0, 'skills': ['armored 9']}, 
            '379': {'id': '379', 'name': 'Havenship', 'rarity': '1', 'adj_stats': 11.5, 'avg_skill': 8.0, 'skills': ['armored 6', 'pierce 10']}, 
            '141': {'id': '141', 'name': 'Reconnoiter', 'rarity': '1', 'adj_stats': 9.0, 'avg_skill': 10.0, 'skills': ['rally Righteous 11', 'weaken 9']}, 
            '144': {'id': '144', 'name': 'Credo Defender', 'rarity': '1', 'adj_stats': 10.333333333333334, 'avg_skill': 8.5, 'skills': ['armored 8', 'besiege 9']}, 
            '147': {'id': '147', 'name': 'Partisan', 'rarity': '1', 'adj_stats': 14.0, 'avg_skill': 5.5, 'skills': ['heal Righteous 8', 'fortify 3']}, 
            '180': {'id': '180', 'name': 'Sentry', 'rarity': '1', 'adj_stats': 10.0, 'avg_skill': 10.0, 'skills': ['heal 10']}, 
            '151': {'id': '151', 'name': 'Indebted Veteran', 'rarity': '2', 'adj_stats': 11.0, 'avg_skill': 7.5, 'skills': ['heal all Righteous 5', 'pierce 10']}
        }
        files = parse.find_files('^test_data_1.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.rarity = [1, 2]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
        assert cards == target

    def test_parse_cards_fusion_level_1(self):
        target = {'3': {'id': '3', 'name': 'Infantry', 'rarity': '1', 'adj_stats': 15.0, 'avg_skill': 0.0, 'skills': []}, 
        '351': {'id': '351', 'name': 'Bazooka Marine', 'rarity': '1', 'adj_stats': 12.0, 'avg_skill': 10.0, 'skills': ['pierce 10']}}
        files = parse.find_files('^test_data_2.xml$', folder=self.test_folder)
        parser = parse.setup_argparser()
        args = parser.parse_args()
        args.fusion_level = [0]
        cards = parse.parse_cards(files, args, folder=self.test_folder)
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
