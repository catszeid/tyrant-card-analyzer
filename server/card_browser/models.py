from django.db import models

class Faction(models.Model): # unitType
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Rarity(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Skill(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200, default="", null=True)
    desc_all = models.CharField(max_length=200, default="", null=True)
    desc_faction = models.CharField(max_length=200, default="", null=True)
    desc_all_faction = models.CharField(max_length=200, default="", null=True)
    order = models.IntegerField(default=100000, null=True)
    target = models.IntegerField(default=0, null=True) # sabotage_target
    upkeep = models.IntegerField(default=0, null=True) # enhance_upkeep
    hidden = models.IntegerField(default=0, null=True) # hidden
    # unit_override : Assault (Enrage)
    def __str__(self):
        return self.name

class Skill_Attributes(models.Model):
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    all = models.IntegerField(blank=True, null=True)
    c = models.IntegerField(blank=True, null=True)
    s = models.IntegerField(blank=True, null=True)
    s2 = models.IntegerField(blank=True, null=True)
    n = models.IntegerField(blank=True, null=True)
    card_id = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.skill_id.id
    
class Card_Set(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Card(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    attack = models.IntegerField(default=None, blank=True, null=True)
    health = models.IntegerField(blank=True, null=True)
    cost = models.IntegerField(default=None, blank=True, null=True)
    rarity = models.ForeignKey(Rarity, on_delete=models.DO_NOTHING)
    card_set = models.ForeignKey(Card_Set, on_delete=models.DO_NOTHING, blank=True, null=True)
    faction = models.ForeignKey(Faction, on_delete=models.DO_NOTHING)
    fusion_level = models.IntegerField(default=0)
    upgrade_id = models.IntegerField(default=None, blank=True, null=True)
    level = models.IntegerField(default=1)
    def __str__(self):
        return f"*{self.rarity}* {self.name}-{self.level} [{self.id}] {'/'*self.fusion_level} - ({self.cost})[{self.attack}, {self.health}]"

class Card_Skill(models.Model):
    owner_id = models.ForeignKey(Card, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    x = models.IntegerField(default=None, blank=True, null=True)
    y = models.IntegerField(default=None, blank=True, null=True)
    all = models.IntegerField(default=None, blank=True, null=True)
    c = models.IntegerField(default=None, blank=True, null=True)
    s = models.CharField(max_length=100, blank=True, null=True)
    s2 = models.CharField(max_length=100, blank=True, null=True)
    n = models.IntegerField(default=None, blank=True, null=True)
    trigger = models.CharField(max_length=100, default=None, blank=True, null=True)
    card_id = models.IntegerField(default=None, blank=True, null=True)
    def __str__(self):
        return f"Card: {self.owner_id.id}, Skill: {self.skill_id.id}"
