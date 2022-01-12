def getCompetitiveStats(pageHTML: str):
  indexes = []
  data = []

  win_percent_index = pageHTML.find("Win %")
  win_percent_index = pageHTML.find("value", win_percent_index) + 23
  indexes.append(win_percent_index)
  
  wins_index = pageHTML.find("valorant-winloss")
  wins_index = pageHTML.find("text-anchor", wins_index) + 44
  indexes.append(wins_index)

  losses_index = pageHTML.find("text-anchor", wins_index) + 44
  indexes.append(losses_index)

  tier_index = pageHTML.find("Rating")
  tier_index = pageHTML.find("value", tier_index) + 30
  indexes.append(tier_index)

  KAD_index = pageHTML.find("KAD Ratio")
  KAD_index = pageHTML.find("value", KAD_index) + 39
  indexes.append(KAD_index)

  dmg_round_index = pageHTML.find("Damage/Round")
  dmg_round_index = pageHTML.find("value", dmg_round_index) + 23
  indexes.append(dmg_round_index)

  KD_index = pageHTML.find("K/D Ratio")
  KD_index = pageHTML.find("value", KD_index) + 23
  indexes.append(KD_index)

  headshots_percent_index = pageHTML.find("Headshots")
  headshots_percent_index = pageHTML.find("value", headshots_percent_index) + 23
  indexes.append(headshots_percent_index)

  kills_index = pageHTML.find("\"Kills\"")
  kills_index = pageHTML.find("value", kills_index) + 23
  indexes.append(kills_index)

  deaths_index = pageHTML.find("Deaths")
  deaths_index = pageHTML.find("value", deaths_index) + 23
  indexes.append(deaths_index)
  
  kills_round_index = pageHTML.find("Kills/Round")
  kills_round_index = pageHTML.find("value", kills_round_index) + 23
  indexes.append(kills_round_index)

  most_kills_index = pageHTML.find("Most Kills (Match)")
  most_kills_index = pageHTML.find("value", most_kills_index) + 23
  indexes.append(most_kills_index)

  agent_index = pageHTML.find("agent__name") + 45
  indexes.append(agent_index)

  print("Found indexes")

  for num in indexes:
    j = num
    end = 0
    while True:
      j += 1
      if pageHTML[j] == "<":
        end = j
        break
    info = pageHTML[num:end].replace("\n", "").replace(" ", "")
    if indexes.index(num) == 3:
      for i in info:
        if i in ["1", "2", "3"]:
          info = info[:info.index(i)] + " " + i
    data.append(info)

  print("Acquired Data")

  field1 = "**Rank: **" + data[3] + "\n\n**KAD Ratio: **" + data[4] + "\n\n**Wins/Losses: **" + data[1] + "W" + " " + data[2] + "L⠀⠀" + "\n\n**Kills: **" + data[8] + "\n\n**Headshots: **" + data[7] + "" "\n\n**DMG/Round: **" + data[5] + ""

  field2 = "**KD Ratio: **" + data[6] + "\n\n**Win rate: **" + data[0] + "\n\n**Deaths: **" + data[9] + "\n\n**Most Kills (Match): **" + data[11] + "\n\n**Kills/Round: **" + data[10] + "\n\n**Most Played Agent: **" + data[12] + ""

  return field1, field2