# -*- coding: utf-8 -*-
# Canonical Deadshot league dataset.
# Sources:
#   2015-2023 : transcribed from the user's existing "League Results" sheet (+ embedded screenshots)
#   2024-2025 : transcribed from the two standings/playoff-bracket screenshots supplied 2026-08-23
# reg-season standings rows are ordered by the site's regular-season rank.
# (rank, team, W, L, T, PF, PA, moves)  moves=None where not recorded

SEASON_META = {
    # year: (teams, reg_games, playoff_spots, spots_confirmed)
    2015: (8, 14, 4, True),
    2016: (10, 14, 4, True),
    2017: (10, 13, 6, True),
    2018: (8, 14, 4, True),
    2020: (10, 14, 4, True),
    2021: (10, 15, 4, True),
    2022: (10, 14, 6, True),
    2023: (10, 14, 6, True),
    2024: (10, 14, 6, True),
    2025: (10, 14, 6, True),
}

STANDINGS = {
2015: [
 (1,"Iridocyclitis",13,1,0,1857.68,1461.72,13),
 (2,"MillionMaker",8,6,0,1658.74,1556.88,20),
 (3,"12th Man Records",8,6,0,1544.66,1471.58,16),
 (4,"Azendohsaurus",7,7,0,1560.38,1445.39,7),
 (5,"The Abusementpark",6,8,0,1397.68,1502.47,16),
 (6,"Niko's Nice Team",7,7,0,1435.83,1555.87,9),
 (7,"Stegos Stomp Em",5,9,0,1470.43,1606.37,24),
 (8,"ETHANS BEAST TEAM",2,12,0,1178.54,1503.66,None),
],
2016: [
 (1,"Million's Team",10,4,0,1738.82,1505.04,14),
 (2,"TITSBURG FEELERS",10,4,0,1633.60,1492.28,19),
 (3,"Heroes and Zeroes",9,5,0,1572.72,1558.14,35),
 (4,"Walrus",7,7,0,1624.18,1541.44,8),
 (5,"Supreme",7,7,0,1589.90,1610.60,13),
 (6,"Steeler Virginity",7,7,0,1494.40,1497.58,6),
 (7,"Lil boats fav team",6,8,0,1552.02,1526.74,17),
 (8,"I Got The Jewce",6,8,0,1500.60,1859.80,43),
 (9,"Lick My SeaCocks",4,10,0,1672.16,1511.72,None),
 (10,"Mr. Morganators",4,10,0,1299.62,1574.68,12),
],
2017: [
 (1,"Poison Dart Frogs",9,4,0,1498.38,1447.70,None),
 (2,"Sleep Train",8,5,0,1670.52,1489.86,None),
 (3,"Injury Prone",8,5,0,1620.22,1430.16,None),
 (4,"chaden's Team",7,6,0,1238.96,1290.52,None),
 (5,"Get Jewced Up",6,7,0,1574.48,1511.62,None),
 (6,"Two Gurley's one cup",6,7,0,1362.96,1387.76,None),
 (7,"Gucci gang",6,7,0,1360.42,1428.18,None),
 (8,"Sswallow my Siemian",5,8,0,1394.70,1508.92,None),
 (9,"Clout Gang",5,8,0,1361.64,1504.18,None),
 (10,"Girnk Team",5,8,0,1355.86,1439.24,None),
],
2018: [
 (1,"Injury Prone",10,4,0,1992.88,1785.92,None),
 (2,"brian's Team",9,5,0,1925.48,1792.04,None),
 (3,"FourByFourWheel",8,5,1,1843.26,1810.68,None),
 (4,"Two gurley's one cup",7,7,0,1732.54,1788.44,None),
 (5,"Chase Templeton",6,7,1,1694.90,1709.64,None),
 (6,"Stegostompem",6,8,0,1851.26,1810.38,None),
 (7,"chaden's Team",6,8,0,1632.56,1735.20,None),
 (8,"The End",3,11,0,1534.98,1775.56,None),
],
2020: [
 (1,"Stiizpodswanted",10,4,0,1873.98,1731.80,None),
 (2,"Beats By Ray",9,5,0,1780.74,1605.26,None),
 (3,"OBJ",9,5,0,1749.64,1713.44,None),
 (4,"two gurleys one cup",8,6,0,1888.04,1735.20,None),
 (5,"Stegostompem",8,6,0,1834.16,1744.06,None),
 (6,"Master Trader",8,6,0,1768.72,1701.28,None),
 (7,"iThotWeWereFriends",7,7,0,1829.92,1780.84,None),
 (8,"SAUCE TEAM",5,9,0,1739.42,1796.42,None),
 (9,"sherbsbutthole",4,10,0,1564.58,1798.08,None),
 (10,"The Pharaoh",2,12,0,1416.60,1839.42,None),
],
2021: [
 (1,"NAH G",12,3,0,2117.32,1837.04,43),
 (2,"HunchoCamby",9,6,0,1763.06,1679.20,59),
 (3,"VICTORY",9,6,0,1750.88,1704.54,28),
 (4,"Aaron it out",8,7,0,2062.16,1950.60,30),
 (5,"Hail Chubby",8,7,0,2047.78,1905.96,16),
 (6,"SAUCE TEAM",7,8,0,1872.22,1950.42,20),
 (7,"“Close”~~~ 0.33-0.42",7,8,0,1847.96,1889.38,23),
 (8,"Kevin's Superb Optimal Team",5,10,0,1893.10,1989.52,19),
 (9,"brian's Choice Team",5,10,0,1739.60,1831.20,25),
 (10,"Stegostompem",5,10,0,1553.38,1909.60,51),
],
2022: [
 (1,"SHIESTY SZN",12,2,0,1873.36,1588.14,51),
 (2,"GODDID",10,4,0,1835.32,1707.54,29),
 (3,"Stegostompem",8,6,0,1773.94,1837.62,34),
 (4,"Broncos Country",8,6,0,1710.64,1608.88,38),
 (5,"Poe's Palace",6,8,0,1804.60,1799.80,37),
 (6,"Larryette",6,8,0,1636.40,1674.74,37),
 (7,"5 Hunnid K in the Bank",6,8,0,1553.78,1745.56,23),
 (8,"Hit by Gatsby's Bus",5,9,0,1812.36,1721.54,19),
 (9,"SAUCE TEAM",5,9,0,1705.92,1813.34,5),
 (10,"DO BRONX",4,10,0,1646.38,1855.54,22),
],
2023: [
 (1,"SNIPES",10,4,0,1823.30,1635.70,80),
 (2,"Poe's Palace",9,5,0,1878.46,1738.60,39),
 (3,"Kabul Gearing Bombers",8,6,0,1927.02,1789.50,39),
 (4,"Hench",8,6,0,1763.58,1683.96,28),
 (5,"Broncos Country",8,6,0,1724.14,1715.06,23),
 (6,"Stegostompem",8,6,0,1699.32,1635.58,19),
 (7,"Grimace",6,8,0,1762.94,1806.30,67),
 (8,"MASHALLAH",5,9,0,1694.46,1847.00,9),
 (9,"Walter",5,9,0,1604.44,1825.22,16),
 (10,"Beyond the Abyss",3,11,0,1608.82,1809.56,24),
],
2024: [
 (1,"U gotta BO-lieve",10,4,0,1861.60,1783.70,46),
 (2,"Free Diddy",9,5,0,1885.56,1740.18,23),
 (3,"It's a Love Story",9,5,0,1869.36,1694.72,35),
 (4,"Hench",8,6,0,1825.12,1665.26,36),
 (5,"Poe's Palace",7,7,0,1780.94,1781.36,37),
 (6,"Kabul Gearing Bombers",7,7,0,1684.16,1692.18,39),
 (7,"Stegostompem",6,8,0,1796.58,1865.50,27),
 (8,"SNIPES",6,8,0,1745.36,1811.80,47),
 (9,"The Pharaoh's Disciples",4,10,0,1629.78,1864.90,15),
 (10,"DylansVillans",4,10,0,1624.54,1803.40,21),
],
2025: [
 (1,"Poe's Palace",10,4,0,1754.32,1637.30,38),
 (2,"Hench",9,5,0,1934.46,1647.08,28),
 (3,"U gotta BO-lieve",9,5,0,1757.58,1772.14,34),
 (4,"SNIPES",8,6,0,1619.64,1570.70,56),
 (5,"A Storm Is Coming",7,7,0,1777.84,1753.98,32),
 (6,"Kabul Gearing Bombers",6,8,0,1619.82,1705.82,46),
 (7,"It's a Love Story",6,8,0,1596.22,1746.62,28),
 (8,"DylansVillans",5,9,0,1769.80,1732.26,12),
 (9,"Bring back Gmo",5,9,0,1689.18,1723.02,17),
 (10,"Stegostompem",5,9,0,1682.66,1912.60,34),
],
}

# final placement, 1st -> last
FINAL_PLACE = {
2015: ["Iridocyclitis","MillionMaker","12th Man Records","Azendohsaurus","Stegos Stomp Em","Niko's Nice Team","The Abusementpark","ETHANS BEAST TEAM"],
2016: ["Heroes and Zeroes","Million's Team","Walrus","TITSBURG FEELERS","I Got The Jewce","Steeler Virginity","Lil boats fav team","Supreme","Lick My SeaCocks","Mr. Morganators"],
2017: ["Injury Prone","Poison Dart Frogs","chaden's Team","Sleep Train","Get Jewced Up","Two Gurley's one cup","Gucci gang","Sswallow my Siemian","Clout Gang","Girnk Team"],
2018: ["Injury Prone","FourByFourWheel","brian's Team","Two gurley's one cup","chaden's Team","Chase Templeton","Stegostompem","The End"],
2020: ["Stiizpodswanted","OBJ","two gurleys one cup","Beats By Ray","iThotWeWereFriends","Stegostompem","Master Trader","SAUCE TEAM","sherbsbutthole","The Pharaoh"],
2021: ["VICTORY","NAH G","Aaron it out","HunchoCamby","Hail Chubby","SAUCE TEAM","“Close”~~~ 0.33-0.42","Kevin's Superb Optimal Team","brian's Choice Team","Stegostompem"],
2022: ["Poe's Palace","Stegostompem","GODDID","SHIESTY SZN","Broncos Country","Larryette","SAUCE TEAM","DO BRONX","Hit by Gatsby's Bus","5 Hunnid K in the Bank"],
2023: ["Kabul Gearing Bombers","SNIPES","Poe's Palace","Hench","Stegostompem","Broncos Country","MASHALLAH","Beyond the Abyss","Grimace","Walter"],
2024: ["It's a Love Story","U gotta BO-lieve","Hench","Free Diddy","Poe's Palace","Kabul Gearing Bombers","Stegostompem","SNIPES","The Pharaoh's Disciples","DylansVillans"],
2025: ["Hench","SNIPES","U gotta BO-lieve","Poe's Palace","A Storm Is Coming","Kabul Gearing Bombers","DylansVillans","Stegostompem","It's a Love Story","Bring back Gmo"],
}

UNKNOWN = "?"
MANAGERS = {
2015: {"Iridocyclitis":"Walter Bremer","MillionMaker":"Nathan Wu","12th Man Records":"Giacomo Watson","Azendohsaurus":"Brian Berger","The Abusementpark":"Brian Burke","Niko's Nice Team":"Niko Contreras","Stegos Stomp Em":"Shane Kaiper","ETHANS BEAST TEAM":"Ethan Kracht"},
2016: {"Heroes and Zeroes":"Brian Burke","Million's Team":"Nathan Wu","Walrus":"Brian Berger","TITSBURG FEELERS":"Giacomo Watson","I Got The Jewce":"Shane Kaiper","Steeler Virginity":"Mikey Mainer","Lil boats fav team":"Niko Contreras","Supreme":"Logan Carter","Lick My SeaCocks":"Connor Rhodes","Mr. Morganators":"Walter Bremer"},
2017: {"Injury Prone":"Giacomo Watson","Poison Dart Frogs":"Brian Berger","chaden's Team":"Chaden Snarr","Sleep Train":"Brian Burke","Get Jewced Up":"Shane Kaiper","Two Gurley's one cup":"Chris Cossu","Gucci gang":"Niko Contreras","Sswallow my Siemian":"Nathan Wu","Clout Gang":"Walter Bremer","Girnk Team":"Nick Gearing"},
2018: {"Injury Prone":"Giacomo Watson","FourByFourWheel":"Charlie Watson","brian's Team":"Brian Burke","Two gurley's one cup":"Chris Cossu","chaden's Team":"Chaden Snarr","Chase Templeton":"Walter Bremer","Stegostompem":"Shane Kaiper","The End":"Brian Berger"},
2020: {"Stiizpodswanted":"Niko Contreras","OBJ":"Jonathan Campbell","two gurleys one cup":"Chris Cossu","Beats By Ray":"Brian Burke","iThotWeWereFriends":"Walter Bremer","Stegostompem":"Shane Kaiper","Master Trader":"Chaden Snarr","SAUCE TEAM":"Peter Modlin","sherbsbutthole":"Giacomo Watson","The Pharaoh":"Brian Berger"},
2021: {"VICTORY":"Niko Contreras","NAH G":"Wesley Alpert","Aaron it out":"Chris Cossu","HunchoCamby":"Jonathan Campbell","Hail Chubby":"Walter Bremer","SAUCE TEAM":"Peter Modlin","“Close”~~~ 0.33-0.42":"Brian Berger","Kevin's Superb Optimal Team":"Kevin Krueger","brian's Choice Team":"Brian Burke","Stegostompem":"Shane Kaiper"},
2022: {"Poe's Palace":"Brian Burke","Stegostompem":"Shane Kaiper","GODDID":"Niko Contreras","SHIESTY SZN":"Wesley Alpert","Broncos Country":"Nathan Wu","Larryette":"Kevin Krueger","SAUCE TEAM":"Peter Modlin","DO BRONX":"Walter Bremer","Hit by Gatsby's Bus":"Brian Berger","5 Hunnid K in the Bank":"Chris Cossu"},
2023: {"Kabul Gearing Bombers":"Nick Gearing","SNIPES":"Wesley Alpert","Poe's Palace":"Brian Burke","Hench":"Kevin Krueger","Stegostompem":"Shane Kaiper","Broncos Country":"Nathan Wu","MASHALLAH":"Niko Contreras","Beyond the Abyss":"Brian Berger","Grimace":"Jonathan Campbell","Walter":"Walter Bremer"},
2024: {"It's a Love Story":"Chris Cossu","Hench":"Kevin Krueger","Poe's Palace":"Brian Burke","Kabul Gearing Bombers":"Nick Gearing","Stegostompem":"Shane Kaiper","SNIPES":"Wesley Alpert",
       "U gotta BO-lieve":"Nathan Wu","Free Diddy":"Niko Contreras","The Pharaoh's Disciples":"Brian Berger","DylansVillans":"Dylan McMahon"},
2025: {"Hench":"Kevin Krueger","SNIPES":"Wesley Alpert","Poe's Palace":"Brian Burke","Kabul Gearing Bombers":"Nick Gearing","Stegostompem":"Shane Kaiper","It's a Love Story":"Chris Cossu",
       "U gotta BO-lieve":"Nathan Wu","A Storm Is Coming":"Brian Berger","DylansVillans":"Dylan McMahon","Bring back Gmo":"Niko Contreras"},
}

# Manager attribution confidence per (year, team)
CONFIRMED_2425 = {("It's a Love Story",2024),("Hench",2025)}   # manager name printed on the screenshot
CHAINED = {"Hench","SNIPES","Poe's Palace","Kabul Gearing Bombers","Stegostompem","It's a Love Story"}

# CO-CHAMPIONS: the 2022 final was rendered moot by the cancellation of Bills-Bengals
# (Damar Hamlin, 2 Jan 2023). Managers split 1st place and the winnings.
CO_CHAMPS = {2022: ["Poe's Palace", "Stegostompem"]}

# Every playoff game in league history, read off the brackets embedded in the
# user's original League Results sheet (2015-2023) and the two screenshots supplied
# on 23 Aug 2026 (2024-2025). (season, week, round, teamA, ptsA, teamB, ptsB, void)
PLAYOFF_GAMES = [
 (2015,15,"Semifinal","Iridocyclitis",148.87,"Azendohsaurus",101.00,False),
 (2015,15,"Semifinal","MillionMaker",117.70,"12th Man Records",116.80,False),
 (2015,16,"Final","Iridocyclitis",139.37,"MillionMaker",107.97,False),
 (2015,16,"3rd Place Game","12th Man Records",84.07,"Azendohsaurus",70.90,False),

 (2016,15,"Semifinal","Million's Team",133.64,"Walrus",82.82,False),
 (2016,15,"Semifinal","Heroes and Zeroes",109.88,"TITSBURG FEELERS",89.94,False),
 (2016,16,"Final","Heroes and Zeroes",161.38,"Million's Team",94.78,False),
 (2016,16,"3rd Place Game","Walrus",164.16,"TITSBURG FEELERS",106.86,False),

 (2017,14,"Quarterfinal","chaden's Team",115.44,"Get Jewced Up",104.54,False),
 (2017,14,"Quarterfinal","Injury Prone",148.52,"Two Gurley's one cup",118.08,False),
 (2017,15,"Semifinal","Poison Dart Frogs",152.08,"chaden's Team",89.44,False),
 (2017,15,"Semifinal","Injury Prone",150.14,"Sleep Train",121.62,False),
 (2017,15,"5th Place Game","Get Jewced Up",116.74,"Two Gurley's one cup",104.78,False),
 (2017,16,"Final","Injury Prone",148.08,"Poison Dart Frogs",85.90,False),
 (2017,16,"3rd Place Game","chaden's Team",108.16,"Sleep Train",101.86,False),

 (2018,15,"Semifinal","Injury Prone",114.22,"Two gurley's one cup",100.14,False),
 (2018,15,"Semifinal","FourByFourWheel",125.88,"brian's Team",114.70,False),
 (2018,16,"Final","Injury Prone",144.02,"FourByFourWheel",92.28,False),
 (2018,16,"3rd Place Game","brian's Team",98.92,"Two gurley's one cup",96.30,False),

 (2020,15,"Semifinal","Stiizpodswanted",156.42,"two gurleys one cup",142.64,False),
 (2020,15,"Semifinal","OBJ",141.02,"Beats By Ray",124.02,False),
 (2020,16,"Final","Stiizpodswanted",156.84,"OBJ",123.62,False),
 (2020,16,"3rd Place Game","two gurleys one cup",168.48,"Beats By Ray",91.06,False),

 (2021,16,"Semifinal","NAH G",145.28,"Aaron it out",103.48,False),
 (2021,16,"Semifinal","VICTORY",131.10,"HunchoCamby",129.30,False),
 (2021,17,"Final","VICTORY",132.84,"NAH G",123.72,False),
 (2021,17,"3rd Place Game","Aaron it out",132.56,"HunchoCamby",126.02,False),

 (2022,15,"Quarterfinal","Poe's Palace",142.84,"Broncos Country",109.78,False),
 (2022,15,"Quarterfinal","Stegostompem",131.56,"Larryette",72.30,False),
 (2022,16,"Semifinal","Poe's Palace",121.26,"SHIESTY SZN",117.50,False),
 (2022,16,"Semifinal","Stegostompem",154.48,"GODDID",137.50,False),
 (2022,16,"5th Place Game","Broncos Country",162.80,"Larryette",120.46,False),
 (2022,17,"Final","Poe's Palace",93.12,"Stegostompem",82.50,True),
 (2022,17,"3rd Place Game","GODDID",100.38,"SHIESTY SZN",81.90,False),

 (2023,15,"Quarterfinal","Hench",124.20,"Broncos Country",65.06,False),
 (2023,15,"Quarterfinal","Kabul Gearing Bombers",151.32,"Stegostompem",136.12,False),
 (2023,16,"Semifinal","SNIPES",147.90,"Hench",126.90,False),
 (2023,16,"Semifinal","Kabul Gearing Bombers",108.04,"Poe's Palace",95.88,False),
 (2023,16,"5th Place Game","Stegostompem",158.92,"Broncos Country",113.44,False),
 (2023,17,"Final","Kabul Gearing Bombers",179.98,"SNIPES",144.92,False),
 (2023,17,"3rd Place Game","Poe's Palace",132.46,"Hench",106.20,False),

 (2024,15,"Quarterfinal","Hench",163.38,"Poe's Palace",100.44,False),
 (2024,15,"Quarterfinal","It's a Love Story",146.86,"Kabul Gearing Bombers",131.72,False),
 (2024,16,"Semifinal","U gotta BO-lieve",150.54,"Hench",127.16,False),
 (2024,16,"Semifinal","It's a Love Story",128.88,"Free Diddy",127.08,False),
 (2024,16,"5th Place Game","Poe's Palace",205.42,"Kabul Gearing Bombers",109.72,False),
 (2024,17,"Final","It's a Love Story",164.50,"U gotta BO-lieve",115.66,False),
 (2024,17,"3rd Place Game","Hench",137.38,"Free Diddy",98.78,False),

 (2025,15,"Quarterfinal","SNIPES",165.00,"A Storm Is Coming",119.50,False),
 (2025,15,"Quarterfinal","U gotta BO-lieve",159.90,"Kabul Gearing Bombers",93.90,False),
 (2025,16,"Semifinal","SNIPES",157.80,"Poe's Palace",105.82,False),
 (2025,16,"Semifinal","Hench",201.36,"U gotta BO-lieve",180.80,False),
 (2025,16,"5th Place Game","A Storm Is Coming",155.26,"Kabul Gearing Bombers",100.40,False),
 (2025,17,"Final","Hench",142.92,"SNIPES",111.32,False),
 (2025,17,"3rd Place Game","U gotta BO-lieve",157.24,"Poe's Palace",99.08,False),
]

# H2H_SEED was removed 2026-08-28: it duplicated the 2024/2025 rows of
# PLAYOFF_GAMES exactly, was referenced by nothing, and could only ever drift
# out of step with the real table. verify.py now cross-checks PLAYOFF_GAMES
# against the weekly game logs instead.

MANAGER_ORDER = ["Brian Berger","Brian Burke","Shane Kaiper","Chris Cossu","Niko Contreras","Walter Bremer",
 "Nathan Wu","Giacomo Watson","Peter Modlin","Jonathan Campbell","Kevin Krueger","Wesley Alpert",
 "Ethan Kracht","Charlie Watson","Connor Rhodes","Nick Gearing","Mikey Mainer","Logan Carter","Chaden Snarr","Dylan McMahon"]
