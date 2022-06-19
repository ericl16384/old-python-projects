def pluralize(x):
    "May not always be accurate. Add exceptions as you find them. See https://www.grammarly.com/blog/plural-nouns/"

    # Add to this
    exceptions = {
        "bus": "buses",
        "gas": "gasses",
        "roof": "roofs",
        "halo": "halos",
        "fish": "fish",
        "belief": "beliefs",
        "chef": "chefs",
        "chief": "chiefs",
        "photo": "photos",
        "piano": "pianos",
        "child": "children",
        "goose": "geese",
        "man": "men",
        "woman": "women",
        "tooth": "teeth",
        "foot": "feet",
        "mouse": "mice",
        "person": "people",
        "series": "series",
        "species": "species",
        "deer": "deer"
    }

    # Handle caps
    lower = x.lower()

    # Handle exceptions
    for i in exceptions.keys():
        if lower == i:
            return exceptions[i]

    
    if lower.endswith("y") and len(x) >= 2:
        for i in ["a", "e", "i", "o", "u"]:
            if lower[-2] == i:
                return x+"s"
        return x[:-1]+"es"
    
    if lower.endswith("us"):
        return x[:-2]+"i"
    
    if lower.endswith("is"):
        return x[:-2]+"es"
    
    if lower.endswith("on"):
        return x[:-2]+"a"
    
    for i in ["f", "fe"]:
        if lower.endswith(i):
            return x[:-1]+"ves"

    for i in ["s", "sh", "ch", "x", "z", "o"]:
        if lower.endswith(i):
            return x+"es"

    # Default
    return x+"s"

# Test set
for i in [
    "cat",
    "bus",
    "gas",
    "wolf",
    "roof",
    "city",
    "boy",
    "potato",
    "halo",
    "cactus",
    "analysis",
    "phenomenon",
    "fish"
]:
    print(f"{i}    {pluralize(i)}")

# You can test it
while True:
    print(pluralize(input("> ")))