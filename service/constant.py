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
        self.DAMAGE_VIEW = 'damage'
        self.DAMAGE_TAKEN_VIEW = 'damage-taken'

        # taq boss name chinese
        self.Viscidus_name = '维希度斯'

        # taq 法术id
        self.Poison_Bolt_Volley_ability_id = 25991  # 小软毒箭之雨

        # scan task
        self.VISCIDUS_POISON_TICK_TASK = 'viscidus_poison_tick'

    def register_api(self):
        return [self.FIGHT_API, self.EVENT_API, self.TABLES_API]


CONSTANT_SERVICE = ConstantService()
