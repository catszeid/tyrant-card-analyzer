CREATE TABLE rarity (
    id INTEGER PRIMARY KEY NOT NULL, 
    name TEXT NOT NULL
);
CREATE TABLE type (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL
);
CREATE TABLE trigger (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL
);
CREATE TABLE skill (
    id INTEGER PRIMARY KEY NOT NULL,
    name_xml TEXT,
    name TEXT
);
CREATE TABLE card (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT,
    attack INTEGER,
    health INTEGER,
    cost INTEGER,
    rarity INTEGER,
    card_set INTEGER,
    type INTEGER,
    fusion_level INTEGER DEFAULT 0,
    upgrade_id INTEGER,
    level INTEGER DEFAULT 1,
    FOREIGN KEY (rarity) REFERENCES rarity(id),
    FOREIGN KEY (type) REFERENCES type(id),
    FOREIGN KEY (upgrade_id) REFERENCES card(id)
);
CREATE TABLE card_skill (
    id INTEGER PRIMARY KEY NOT NULL,
    owner_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    x INTEGER,  -- skill power
    y INTEGER, -- skill faction (type) restriction
    n INTEGER, -- units affected
    c INTEGER, -- cooldown in turns
    a INTEGER, -- affect all
    trigger INTEGER, -- alternative trigger
    card_id INTEGER, -- summoned card id
    s INTEGER, -- skill to enhance/evolve
    s2 INTEGER, -- skill evolved to
    FOREIGN KEY (skill_id) REFERENCES skill(id),
    FOREIGN KEY (trigger) REFERENCES trigger(id),
    FOREIGN KEY (s) REFERENCES skill(id),
    FOREIGN KEY (owner_id) REFERENCES card(id),
    FOREIGN KEY (card_id) REFERENCES card(id)
);

INSERT INTO rarity VALUES(1, "Common");
INSERT INTO rarity VALUES(2, "Rare");
INSERT INTO rarity VALUES(3, "Epic");
INSERT INTO rarity VALUES(4, "Legendary");
INSERT INTO rarity VALUES(5, "Mythic");
INSERT INTO rarity VALUES(6, "Vindicator");

INSERT INTO type VALUES(1, "Imperial");
INSERT INTO type VALUES(2, "Raider");
INSERT INTO type VALUES(3, "Xeno");
INSERT INTO type VALUES(4, "Bloodthirsty");
INSERT INTO type VALUES(5, "Righteous");
INSERT INTO type VALUES(6, "Progenitor");

INSERT INTO trigger VALUES(1, "attacked");
INSERT INTO trigger VALUES(2, "death");
INSERT INTO trigger VALUES(3, "play");

INSERT INTO skill VALUES(1, "wall", "Wall");
INSERT INTO skill VALUES(2, "armored", "Armored");
INSERT INTO skill VALUES(3, "counter", "Counter");
INSERT INTO skill VALUES(4, "heal", "Heal");
INSERT INTO skill VALUES(5, "rally", "Rally");
INSERT INTO skill VALUES(6, "strike", "Strike");
INSERT INTO skill VALUES(7, "weaken", "Weaken");
INSERT INTO skill VALUES(8, "besiege", "Siege");
INSERT INTO skill VALUES(9, "pierce", "Pierce");
INSERT INTO skill VALUES(10, "poison", "Poison");
INSERT INTO skill VALUES(11, "leech", "Leech");
INSERT INTO skill VALUES(12, "evade", "Evade");
INSERT INTO skill VALUES(13, "berserk", "Berserk");
INSERT INTO skill VALUES(14, "enfeeble", "Enfeeble");
INSERT INTO skill VALUES(15, "protect", "Protect");
INSERT INTO skill VALUES(16, "enhance", "Enhance");
INSERT INTO skill VALUES(17, "jam", "Jam");
INSERT INTO skill VALUES(18, "corrosive", "Corrosive");
INSERT INTO skill VALUES(19, "inhibit", "Inhibit");
INSERT INTO skill VALUES(20, "flurry", "Flurry");
INSERT INTO skill VALUES(21, "valor", "Valor");
INSERT INTO skill VALUES(22, "overload", "Overload");
INSERT INTO skill VALUES(23, "legion", "Legion");
INSERT INTO skill VALUES(24, "payback", "Payback");
INSERT INTO skill VALUES(25, "avenge", "Avenge");
INSERT INTO skill VALUES(26, "refresh", "Refresh");
INSERT INTO skill VALUES(27, "evolve", "Evolve");
INSERT INTO skill VALUES(28, "venom", "Venom");
INSERT INTO skill VALUES(29, "mend", "Mend");
INSERT INTO skill VALUES(30, "siege", "Mortar");
INSERT INTO skill VALUES(31, "swipe", "Swipe");
INSERT INTO skill VALUES(32, "sunder", "Sunder");
INSERT INTO skill VALUES(33, "enrage", "Enrage");
INSERT INTO skill VALUES(34, "allegiance", "Allegiance");
INSERT INTO skill VALUES(35, "drain", "Drain");
INSERT INTO skill VALUES(36, "stasis", "Stasis");
INSERT INTO skill VAlUES(37, "revenge", "Revenge");
INSERT INTO skill VALUES(38, "mimic", "Mimic");
INSERT INTO skill VALUES(39, "coalition", "Coalition");
INSERT INTO skill VALUES(40, "sabotage", "Sabotage");
INSERT INTO skill VALUES(41, "barrier", "Barrier");
INSERT INTO skill VALUES(42, "entrap", "Entrap");
INSERT INTO skill VALUES(43, "subdue", "Subdue");
INSERT INTO skill VALUES(44, "tribute", "Tribute");
INSERT INTO skill VAlUES(45, "summon", "Summon");
INSERT INTO skill VALUES(46, "bravery", "Bravery");
INSERT INTO skill VALUES(47, "absorb", "Absorb");
INSERT INTO skill VALUES(48, "disease", "Disease");
INSERT INTO skill VALUES(49, "mark", "Mark");
INSERT INTO skill VALUES(50, "fortify", "Fortify");
INSERT INTO skill VALUES(51, "hunt", "Hunt");
INSERT INTO skill VALUES(52, "scavenge", "Scavenge");
INSERT INTO skill VALUES(53, "rupture", "Rupture");
INSERT INTO skill VALUES(54, "flying", "Flying");
INSERT INTO skill VALUES(55, "rush", "Rush");