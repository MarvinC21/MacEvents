from reader import Entry

class EventEntry():
  def __init__(self, entry: Entry):
    self.entry = entry
    self.id = entry.id
    self.title = entry.title
    self.link = entry.link
    self.time = (self.title.strip("Library hours: ")
                 .upper().replace("A", " A")
                 .replace("-", " - ").replace("P", " P")
                 if self.title.lower().startswith("library hours")
                 else None)
    self.desc = "Unavailable"
    self.coord = None
    self.parse_summary()

  location_coords = {
      "Library": [44.93855, -93.16822],
      "Humanities": [44.93712, -93.16928],
      "Old Main": [44.93857, -93.16888],
      "Carnegie Hall": [44.93874, -93.16914],
      "Olin-Rice Science Center": [44.93676, -93.16896],
      "Markim Hall": [44.94033, -93.16777],
      "Kagin Commons": [44.94069, -93.16782],
      ("Ruth Stricker Dayton Campus Center",
       "John B Davis Lecture Hall"): [44.93946, -93.16783],
      ("Music Building Mairs Concert Hall",
       "Janet Wallace Fine Arts Center",
       "Law Warschaw Gallery"): [44.93749, -93.16959],
      "Weyerhaeuser Memorial Chapel": [44.93966, -93.16867],
      ("Leonard Center", "Shaw Field"): [44.93765, -93.16804],
      "Theater and Dance Building": [44.93715, -93.17003]
  }


  def parse_summary(self):
    summary = self.entry.summary
    sum_split = summary.split(">")

    for sub in sum_split:
      if sub.endswith("strong") and sum_split.index(sub) > 0:
        details_split = sub.split("|")
        self.date = details_split[0].strip()
        if len(details_split) > 2:
          self.time = details_split[1].strip().replace("&#8211;", " -")
        self.location = details_split[len(details_split) - 1].strip("</strong").strip()
        self.coord = self.get_location_coords(self.location)

      if sub.strip().startswith("p") or sub.strip().startswith("span"):
        self.desc = (sub
          .strip()
          .replace("/span","")
          .replace("/p", "")
          .strip(" <p")
          .replace("nbsp;", "")
          .strip("span"))

  def get_location_coords(self, location: str):
    if not location:
      return None
    location = location.lower()
    for key, coord in self.location_coords.items():
        # if key is a tuple of aliases
      if isinstance(key, tuple):
        if any(name.lower() in location for name in key):
          return coord
        # if key is a single name
      elif isinstance(key, str):
        if key.lower() in location:
          return coord
    return None

  def __str__(self):
    return (f"Title: {self.title}\n\n" +
            f"Summary: {self.desc}\n\n" +
            f"Location: {self.location}\n\n" +
            f"Date: {self.date}\n\n" +
            f"Time: {self.time}\n\n" +
            f"Link: {self.link}")