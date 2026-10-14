# -*- coding: utf-8 -*-
"""2026, the live season, typed from Brian's Yahoo screenshots on 14 Oct 2026.

Kept apart from data.py and the weekly logs on purpose: export.py does not read this file,
so nothing on the site changes until the season is wired in. It exists to check the Yahoo
feed against when the connection lands, and to start building the live section on.

Week 5 was not in the screenshots. Its scores are worked out from the standings totals
minus weeks 1-4, and its pairings from whose points-for matches whose points-against
(check_2026.py does this and checks it all adds up). Its projections are unknown.

NFL teams in the draft lists are each player's team as Yahoo showed it in October 2026,
not necessarily his team on draft day.
"""

# who owns each team (The Curse and Medellin confirmed by Brian, 14 Oct 2026)
MGR2026 = {
    "Kabul Gearing Bombers": "Nick Gearing", "Poe's Palace": "Brian Burke",
    "DylansVillans": "Dylan McMahon", "Hench": "Kevin Krueger",
    "Stegostompem": "Shane Kaiper", "SNIPES": "Wesley Alpert",
    "U gotta BO-lieve": "Nathan Wu", "It's a Love Story": "Chris Cossu",
    "The Curse": "Brian Berger", "Medellin": "Niko Contreras",
}

# (week, teamA, actualA, projA, teamB, actualB, projB, bracket) as in the weekly logs
W2026 = [
(1,"The Curse",114.72,108.83,"SNIPES",106.86,123.06,''),
(1,"DylansVillans",180.06,127.08,"Kabul Gearing Bombers",137.96,122.46,''),
(1,"Poe's Palace",179.96,123.84,"Stegostompem",150.90,129.28,''),
(1,"It's a Love Story",136.02,121.77,"Hench",102.80,126.24,''),
(1,"Medellin",135.26,125.61,"U gotta BO-lieve",103.94,119.83,''),
(2,"The Curse",94.02,112.40,"Medellin",144.42,122.52,''),
(2,"DylansVillans",140.18,122.55,"Stegostompem",103.14,129.60,''),
(2,"Poe's Palace",123.30,121.31,"SNIPES",100.56,128.89,''),
(2,"It's a Love Story",113.66,119.53,"U gotta BO-lieve",130.48,124.68,''),
(2,"Hench",87.18,114.30,"Kabul Gearing Bombers",177.12,128.97,''),
(3,"The Curse",84.66,108.73,"U gotta BO-lieve",121.96,113.44,''),
(3,"DylansVillans",127.14,133.41,"SNIPES",149.24,125.63,''),
(3,"Poe's Palace",121.14,125.44,"Medellin",133.54,130.02,''),
(3,"It's a Love Story",91.62,125.13,"Kabul Gearing Bombers",120.36,131.77,''),
(3,"Hench",141.08,116.06,"Stegostompem",134.50,129.17,''),
(4,"The Curse",193.66,113.55,"Poe's Palace",127.88,128.45,''),
(4,"DylansVillans",117.52,125.31,"Medellin",78.00,119.48,''),
(4,"It's a Love Story",133.66,133.07,"Stegostompem",159.34,135.41,''),
(4,"Hench",157.58,129.24,"SNIPES",130.30,132.71,''),
(4,"Kabul Gearing Bombers",135.22,129.90,"U gotta BO-lieve",117.18,131.55,''),
]

# week 6, not yet played: (teamA, projA, teamB, projB)
UPCOMING2026 = {6: [
("The Curse",117.07,"Hench",138.85), ("DylansVillans",122.41,"Poe's Palace",138.22),
("It's a Love Story",118.69,"Medellin",115.45), ("SNIPES",128.32,"Kabul Gearing Bombers",118.32),
("Stegostompem",122.38,"U gotta BO-lieve",130.11)]}

# standings after week 5, as Yahoo showed them (last update Wed Oct 14 03:01am EDT)
# team: (rank, w, l, t, pf, pa, streak, waiver, moves)
STANDINGS2026_WK5 = {
"Kabul Gearing Bombers": (1,3,2,0,719.16,655.20,'L1',6,12),
"Poe's Palace":          (2,3,2,0,714.20,726.58,'W1',4,11),
"DylansVillans":         (3,3,2,0,690.30,606.70,'L1',7,9),
"The Curse":             (4,3,2,0,625.42,626.52,'W2',2,9),
"Hench":                 (5,3,2,0,613.98,698.02,'W3',5,19),
"Medellin":              (6,3,2,0,611.30,561.96,'L2',8,4),
"Stegostompem":          (7,2,3,0,727.04,743.38,'W2',3,16),
"SNIPES":                (8,2,3,0,636.30,639.14,'W1',9,22),
"U gotta BO-lieve":      (9,2,3,0,621.48,630.72,'L2',1,5),
"It's a Love Story":     (10,1,4,0,591.36,662.32,'L4',10,7),
}

# trades: (date, teamA, players A received, teamB, players B received)
TRADES2026 = [
("Sep 15","Poe's Palace",["Isaiah Likely"],"SNIPES",["Rome Odunze"]),
("Sep 29","Kabul Gearing Bombers",["Colston Loveland","Ashton Jeanty","Puka Nacua"],"Hench",["Kyren Williams","Tyler Warren","CeeDee Lamb","Matthew Golden"]),
("Oct 13","It's a Love Story",["Bijan Robinson","Dontayvion Wicks"],"SNIPES",["Parker Washington","Jonathan Taylor"]),
("Oct 13","It's a Love Story",["RJ Harvey","Jalen Coker"],"Medellin",["Jeremiyah Love"]),
]

def _d(team, picks):
    return [(n, team, p, nfl, pos) for n, p, nfl, pos in picks]

# drafts: (overall pick, team, player, NFL team, position)
DRAFT2026 = sorted(
 _d("Stegostompem",[(1,"Jahmyr Gibbs","DET","RB"),(20,"Derrick Henry","BAL","RB"),(21,"Malik Nabers","NYG","WR"),(40,"Tetairoa McMillan","CAR","WR"),(41,"Emeka Egbuka","TB","WR"),(60,"Terry McLaurin","WAS","WR"),(61,"Jayden Daniels","WAS","QB"),(80,"Rhamondre Stevenson","NE","RB"),(81,"Harold Fannin Jr.","CLE","TE"),(100,"Jordan Mason","MIN","RB"),(101,"Jordyn Tyson","NO","WR"),(120,"Rachaad White","WAS","RB"),(121,"Tyler Allgeier","ARI","RB"),(140,"Philadelphia","PHI","DEF"),(141,"Jason Myers","SEA","K")])
+_d("SNIPES",[(2,"Bijan Robinson","ATL","RB"),(19,"Brock Bowers","LV","TE"),(22,"George Pickens","DAL","WR"),(39,"Jaylen Waddle","DEN","WR"),(42,"Bucky Irving","TB","RB"),(59,"Jadarian Price","SEA","RB"),(62,"Carnell Tate","TEN","WR"),(79,"Jonathon Brooks","CAR","RB"),(82,"Justin Herbert","LAC","QB"),(99,"Alec Pierce","IND","WR"),(102,"Dak Prescott","DAL","QB"),(119,"Xavier Worthy","KC","WR"),(122,"Woody Marks","HOU","RB"),(139,"Harrison Mevis","LAR","K"),(142,"Baltimore","BAL","DEF")])
+_d("Medellin",[(3,"Ja'Marr Chase","CIN","WR"),(18,"Omarion Hampton","LAC","RB"),(23,"Trey McBride","ARI","TE"),(38,"DeVonta Smith","PHI","WR"),(43,"Garrett Wilson","NYJ","WR"),(58,"Bhayshul Tuten","JAX","RB"),(63,"TreVeyon Henderson","NE","RB"),(78,"Caleb Williams","CHI","QB"),(83,"Quentin Johnston","LAC","WR"),(98,"Michael Pittman Jr.","PIT","WR"),(103,"RJ Harvey","DEN","RB"),(118,"Jalen Coker","CAR","WR"),(123,"Patrick Mahomes","KC","QB"),(138,"Eddy Pineiro","SF","K"),(143,"Pittsburgh","PIT","DEF")])
+_d("Hench",[(4,"Puka Nacua","LAR","WR"),(17,"Ashton Jeanty","LV","RB"),(24,"Drake London","ATL","WR"),(37,"Colston Loveland","CHI","TE"),(44,"Cam Skattebo","NYG","RB"),(57,"Jameson Williams","DET","WR"),(64,"MarShawn Lloyd","GB","RB"),(77,"Trevor Lawrence","JAX","QB"),(84,"De'Zhaun Stribling","SF","WR"),(97,"Jayden Reed","GB","WR"),(104,"Brandon Aubrey","DAL","K"),(117,"Romeo Doubs","NE","WR"),(124,"Mike Washington Jr.","LV","RB"),(137,"Keaton Mitchell","LAC","RB"),(144,"Los Angeles","LAC","DEF")])
+_d("Poe's Palace",[(5,"Christian McCaffrey","SF","RB"),(16,"Kenneth Walker III","KC","RB"),(25,"Nico Collins","HOU","WR"),(36,"Ladd McConkey","LAC","WR"),(45,"Lamar Jackson","BAL","QB"),(56,"Christian Watson","GB","WR"),(65,"Rome Odunze","CHI","WR"),(76,"Kyle Pitts Sr.","ATL","TE"),(85,"Blake Corum","LAR","RB"),(96,"Chris Godwin Jr.","TB","WR"),(105,"J.K. Dobbins","DEN","RB"),(116,"KC Concepcion Jr.","CLE","WR"),(125,"Los Angeles","LAR","DEF"),(136,"Jacksonville","JAX","DEF"),(145,"Evan McPherson","CIN","K")])
+_d("DylansVillans",[(6,"Jaxon Smith-Njigba","SEA","WR"),(15,"Justin Jefferson","MIN","WR"),(26,"Breece Hall","NYJ","RB"),(35,"Travis Etienne Jr.","NO","RB"),(46,"D'Andre Swift","CHI","RB"),(55,"Davante Adams","LAR","WR"),(66,"Joe Burrow","CIN","QB"),(75,"Brian Thomas Jr.","JAX","WR"),(86,"Dalton Kincaid","BUF","TE"),(95,"Chuba Hubbard","CAR","RB"),(106,"Wan'Dale Robinson","TEN","WR"),(115,"Chris Rodriguez Jr.","JAX","RB"),(126,"Deebo Samuel Sr.","SF","WR"),(135,"Cam Little","JAX","K"),(146,"Minnesota","MIN","DEF")])
+_d("U gotta BO-lieve",[(7,"James Cook III","BUF","RB"),(14,"De'Von Achane","MIA","RB"),(27,"Chris Olave","NO","WR"),(34,"Rashee Rice","KC","WR"),(47,"DJ Moore","BUF","WR"),(54,"David Montgomery","HOU","RB"),(67,"Jaylen Warren","PIT","RB"),(74,"George Kittle","SF","TE"),(87,"Michael Wilson","ARI","WR"),(94,"Makai Lemon","PHI","WR"),(107,"Kyle Monangai","CHI","RB"),(114,"Houston","HOU","DEF"),(127,"Jared Goff","DET","QB"),(134,"Ka'imi Fairbairn","HOU","K"),(147,"Travis Kelce","KC","TE")])
+_d("It's a Love Story",[(8,"Jonathan Taylor","IND","RB"),(13,"Saquon Barkley","PHI","RB"),(28,"Tee Higgins","CIN","WR"),(33,"Jeremiyah Love","ARI","RB"),(48,"Tucker Kraft","GB","TE"),(53,"Parker Washington","JAX","WR"),(68,"Jalen Hurts","PHI","QB"),(73,"DK Metcalf","PIT","WR"),(88,"Stefon Diggs","WAS","WR"),(93,"Josh Jacobs","GB","RB"),(108,"Josh Downs","IND","WR"),(113,"Aaron Jones Sr.","MIN","RB"),(128,"Tank Bigsby","PHI","RB"),(133,"Seattle","SEA","DEF"),(148,"Trey Smack","GB","K")])
+_d("Kabul Gearing Bombers",[(9,"Amon-Ra St. Brown","DET","WR"),(12,"CeeDee Lamb","DAL","WR"),(29,"Kyren Williams","LAR","RB"),(32,"Josh Allen","BUF","QB"),(49,"Tyler Warren","IND","TE"),(52,"Quinshon Judkins","CLE","RB"),(69,"Mike Evans","SF","WR"),(72,"Tony Pollard","TEN","RB"),(89,"Jacory Croskey-Merritt","WAS","RB"),(92,"Jordan Addison","MIN","WR"),(109,"Zach Charbonnet","SEA","RB"),(112,"Matthew Golden","GB","WR"),(129,"Denver","DEN","DEF"),(132,"Khalil Shakir","BUF","WR"),(149,"Wil Lutz","DEN","K")])
+_d("The Curse",[(10,"A.J. Brown","NE","WR"),(11,"Chase Brown","CIN","RB"),(30,"Javonte Williams","DAL","RB"),(31,"Zay Flowers","BAL","WR"),(50,"Drake Maye","NE","QB"),(51,"Luther Burden III","CHI","WR"),(70,"Sam LaPorta","DET","TE"),(71,"Marvin Harrison Jr.","HOU","WR"),(90,"Rico Dowdle","PIT","RB"),(91,"Courtland Sutton","DEN","WR"),(110,"Brian Robinson","ATL","RB"),(111,"Kenny Gainwell","TB","RB"),(130,"Denzel Boston","CLE","WR"),(131,"Cameron Dicker","LAC","K"),(150,"New England","NE","DEF")]))

DRAFT2025 = sorted(
 _d("A Storm Is Coming",[(1,"Ja'Marr Chase","CIN","WR"),(20,"Brock Bowers","LV","TE"),(21,"Jonathan Taylor","IND","RB"),(40,"Joe Burrow","CIN","QB"),(41,"Chuba Hubbard","CAR","RB"),(60,"Zay Flowers","BAL","WR"),(61,"Isiah Pacheco","DET","RB"),(80,"Braelon Allen","NYJ","RB"),(81,"Jaylen Warren","PIT","RB"),(100,"Khalil Shakir","BUF","WR"),(101,"Tucker Kraft","GB","TE"),(120,"Hollywood Brown","PHI","WR"),(121,"Joe Mixon","HOU","RB"),(140,"DeMario Douglas","NE","WR"),(141,"Cameron Dicker","LAC","K")])
+_d("Stegostompem",[(2,"CeeDee Lamb","DAL","WR"),(19,"Josh Jacobs","GB","RB"),(22,"Trey McBride","ARI","TE"),(39,"Kenneth Walker III","KC","RB"),(42,"Tetairoa McMillan","CAR","WR"),(59,"Jameson Williams","DET","WR"),(62,"Emeka Egbuka","TB","WR"),(79,"Ricky Pearsall","SF","WR"),(82,"Dak Prescott","DAL","QB"),(99,"Jordan Addison","MIN","WR"),(102,"Nick Chubb","HOU","RB"),(119,"Cam Skattebo","NYG","RB"),(122,"Brandon Aiyuk","SF","WR"),(139,"Justin Fields","KC","QB"),(142,"Evan McPherson","CIN","K")])
+_d("U gotta BO-lieve",[(3,"Bijan Robinson","ATL","RB"),(18,"Amon-Ra St. Brown","DET","WR"),(23,"A.J. Brown","NE","WR"),(38,"Alvin Kamara","NO","RB"),(43,"James Conner","ARI","RB"),(58,"George Pickens","DAL","WR"),(63,"David Montgomery","HOU","RB"),(78,"Stefon Diggs","WAS","WR"),(83,"Evan Engram","DEN","TE"),(98,"Austin Ekeler","WAS","RB"),(103,"Broncos","DEN","DEF"),(118,"Drake Maye","NE","QB"),(123,"Justin Herbert","LAC","QB"),(138,"Marvin Mims Jr.","DEN","WR"),(143,"Wil Lutz","DEN","K")])
+_d("Poe's Palace",[(4,"Saquon Barkley","PHI","RB"),(17,"De'Von Achane","MIA","RB"),(24,"George Kittle","SF","TE"),(37,"Davante Adams","LAR","WR"),(44,"Marvin Harrison Jr.","HOU","WR"),(57,"Rashee Rice","KC","WR"),(64,"Chris Olave","NO","WR"),(77,"Jakobi Meyers","JAX","WR"),(84,"Travis Etienne Jr.","NO","RB"),(97,"Cooper Kupp","SEA","WR"),(104,"Kyler Murray","MIN","QB"),(117,"Keenan Allen","IND","WR"),(124,"Javonte Williams","DAL","RB"),(137,"Jake Bates","DET","K"),(144,"Bengals","CIN","DEF")])
+_d("Bring back Gmo",[(5,"Christian McCaffrey","SF","RB"),(16,"Malik Nabers","NYG","WR"),(25,"Ladd McConkey","LAC","WR"),(36,"Jayden Daniels","WAS","QB"),(45,"Terry McLaurin","WAS","WR"),(56,"Tony Pollard","TEN","RB"),(65,"Sam LaPorta","DET","TE"),(76,"Jaylen Waddle","DEN","WR"),(85,"J.K. Dobbins","DEN","RB"),(96,"Rome Odunze","CHI","WR"),(105,"Rhamondre Stevenson","NE","RB"),(116,"Baker Mayfield","TB","QB"),(125,"Dalton Kincaid","BUF","TE"),(136,"Steelers","PIT","DEF"),(145,"Chase McLaughlin","TB","K")])
+_d("Kabul Gearing Bombers",[(6,"Jahmyr Gibbs","DET","RB"),(15,"Drake London","ATL","WR"),(26,"Kyren Williams","LAR","RB"),(35,"Jalen Hurts","PHI","QB"),(46,"Garrett Wilson","NYJ","WR"),(55,"Calvin Ridley","TEN","WR"),(66,"Tyrone Tracy Jr.","NYG","RB"),(75,"T.J. Hockenson","MIN","TE"),(86,"Deebo Samuel Sr.","SF","WR"),(95,"Josh Downs","IND","WR"),(106,"Keon Coleman","BUF","WR"),(115,"Jerome Ford","ARI","RB"),(126,"Jared Goff","DET","QB"),(135,"Ravens","BAL","DEF"),(146,"Jake Moody","BAL","K")])
+_d("DylansVillans",[(7,"Justin Jefferson","MIN","WR"),(14,"Nico Collins","HOU","WR"),(27,"James Cook III","BUF","RB"),(34,"Josh Allen","BUF","QB"),(47,"TreVeyon Henderson","NE","RB"),(54,"DeVonta Smith","PHI","WR"),(67,"DJ Moore","BUF","WR"),(74,"Aaron Jones Sr.","MIN","RB"),(87,"Jacory Croskey-Merritt","WAS","RB"),(94,"David Njoku","LAC","TE"),(107,"Chris Godwin Jr.","TB","WR"),(114,"Tank Bigsby","PHI","RB"),(127,"Michael Pittman Jr.","PIT","WR"),(134,"Eagles","PHI","DEF"),(147,"Ka'imi Fairbairn","HOU","K")])
+_d("It's a Love Story",[(8,"Ashton Jeanty","LV","RB"),(13,"Derrick Henry","BAL","RB"),(28,"Lamar Jackson","BAL","QB"),(33,"Tyreek Hill","MIA","WR"),(48,"DK Metcalf","PIT","WR"),(53,"D'Andre Swift","CHI","RB"),(68,"Jerry Jeudy","CLE","WR"),(73,"Travis Kelce","KC","TE"),(88,"Jauan Jennings","MIN","WR"),(93,"Kaleb Johnson","GB","RB"),(108,"Brian Robinson","ATL","RB"),(113,"Tyler Allgeier","ARI","RB"),(128,"Christian Kirk","SF","WR"),(133,"Chris Boswell","PIT","K"),(148,"Packers","GB","DEF")])
+_d("Hench",[(9,"Brian Thomas Jr.","JAX","WR"),(12,"Puka Nacua","LAR","WR"),(29,"Jaxon Smith-Njigba","SEA","WR"),(32,"Omarion Hampton","LAC","RB"),(49,"Breece Hall","NYJ","RB"),(52,"Xavier Worthy","KC","WR"),(69,"Bo Nix","DEN","QB"),(72,"Jordan Mason","MIN","RB"),(89,"Zach Charbonnet","SEA","RB"),(92,"Tyler Warren","IND","TE"),(109,"Jaydon Blue","PHI","RB"),(112,"Jayden Reed","GB","WR"),(129,"Brandon Aubrey","DAL","K"),(132,"Quinshon Judkins","CLE","RB"),(149,"Jayden Higgins","HOU","WR")])
+_d("SNIPES",[(10,"Bucky Irving","TB","RB"),(11,"Chase Brown","CIN","RB"),(30,"Tee Higgins","CIN","WR"),(31,"Mike Evans","SF","WR"),(50,"RJ Harvey","DEN","RB"),(51,"Courtland Sutton","DEN","WR"),(70,"Travis Hunter","JAX","WR"),(71,"Matthew Golden","GB","WR"),(90,"Patrick Mahomes","KC","QB"),(91,"Mark Andrews","BAL","TE"),(110,"Rachaad White","WAS","RB"),(111,"Colston Loveland","CHI","TE"),(130,"Harrison Butker","KC","K"),(131,"Jordan Love","GB","QB"),(150,"Cardinals","ARI","DEF")]))
