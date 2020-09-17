class ConstantService():
    def __init__(self):
        # boss and boss minion id
        self.The_Prophet_Skeram = 15263
        self.Princess_Yauj = 15543
        self.Lord_Kri = 15511
        self.Vem = 15544
        self.Battleguard_Sartura = 15516
        self.Sarturas_Royal_Guard = 15984
        self.Fankriss_The_Unyielding = 15510
        self.Vekniss_Hatchling = 15962
        self.Viscidus = 15299

        # wcl apis
        self.FIGHT_API = '/v1/report/fights/'
        self.EVENT_API = '/v1/report/events/'
        self.TABLES_API = '/v1/report/tables/'

        # wcl api view
        self.DAMAGE_VIEW = 'damage-done'
        self.DAMAGE_TAKEN_VIEW = 'damage-taken'
        self.HEALING_VIEW = 'healing'
        self.CASTS_VIEW = 'casts'
        self.DISPELS_VIEW = 'dispels'

        # taq boss name chinese
        self.Viscidus_name = '维希度斯'
        self.Hururan_name = '哈霍兰公主'
        self.Ouro_name = '奥罗'
        self.Cthun_name = '克苏恩'
        self.Twins_name = '双子皇帝'

        # taq 法术id
        self.Poison_Bolt_Volley_ability_id = 25991  # 小软毒箭之雨
        self.Nature_Protection_id = 7254  # 小自然抗
        self.Major_Nature_Protection_id = 17546  # 大自然抗
        self.Greater_Blessing_Of_Kings = 25898 # 强效王者祝福
        self.Melee = 1 # 平砍技能id

        # scan task
        self.VISCIDUS_POISON_TICK_TASK = 'viscidus_poison_tick'
        self.BOSS_NATURE_PROTECTION = 'boss_nature_protection'

        # taq trash id
        self.TAQ_UNAVAILABLE_TRASH_NAME = ['其拉甲虫', '其拉蝎虫', '甲壳虫', '蝎子', '蟑螂']

    def register_api(self):
        return [self.FIGHT_API, self.EVENT_API, self.TABLES_API]


CONSTANT_SERVICE = ConstantService()
