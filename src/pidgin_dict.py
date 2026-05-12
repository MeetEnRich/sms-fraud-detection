"""
Nigerian Pidgin Normalisation Dictionary
Based on Oyewusi et al. (2021) — extended with admission-specific fraud slang.
Used as Step 2 in the preprocessing pipeline.
"""

# Multi-word phrases must come before single tokens.
# The list is pre-sorted by length descending in preprocessor.py
# so longer phrases are matched and replaced before shorter ones.

PIDGIN_DICT = {

    # ── Admission-specific fraud phrases ─────────────────────────────────────
    "don show":              "has appeared",
    "don come out":          "has been released",
    "don release":           "has been released",
    "don drop":              "has been released",
    "don enter":             "has been approved",
    "e dey expire":          "it is expiring",
    "dey expire":            "is expiring",
    "no waste time":         "do not waste time",
    "make you no":           "ensure you do not",
    "make e":                "let it",
    "sharp sharp":           "immediately",
    "fast fast":             "quickly",
    "now now":               "right now",
    "do am":                 "do it",
    "carry go":              "proceed",
    "no go":                 "do not go",

    # ── JAMB / CAPS specific ─────────────────────────────────────────────────
    "jamb result don":       "jamb result has",
    "caps don":              "caps has",
    "admission don":         "admission has",
    "result don":            "result has",

    # ── Urgency and pressure phrases ─────────────────────────────────────────
    "no delay":              "do not delay",
    "time don reach":        "time has come",
    "time don finish":       "time has expired",
    "e go expire":           "it will expire",
    "before e expire":       "before it expires",

    # ── Common single Pidgin tokens ───────────────────────────────────────────
    "abeg":                  "please",
    "wetin":                 "what",
    "na im":                 "it is",
    "oga":                   "authority",
    "ginger":                "encourage",
    "kasala":                "trouble",
    "tank":                  "thank",
    "tanku":                 "thank you",
    "no be":                 "is not",
    "dem":                   "they",
    "una":                   "you all",
    "wey":                   "that",
    "sef":                   "even",
    "abi":                   "or",
    "sha":                   "just",
    "sabi":                  "know",
    "dey":                   "is",
    "comot":                 "come out",
    "chop":                  "collect",
    "e don":                 "it has",
    "e go":                  "it will",
    "e no":                  "it does not",
    "i no":                  "i do not",
    "you no":                "you do not",
    "nah":                   "is",
    "wahala":                "problem",
    "palava":                "problem",
    "biko":                  "please",
    "oya":                   "now",
    "waka":                  "go",
    "pikin":                 "child",
    "belle":                 "stomach",
    "eye don open":          "has become aware",

    # ── Academic fraud slang ──────────────────────────────────────────────────
    "runz":                  "exam fraud",
    "runs":                  "exam fraud",
    "sorting":               "bribery",
    "expo":                  "exam malpractice",
    "special centre":        "fraudulent exam centre",
    "miracle centre":        "fraudulent exam centre",
    "upgrade":               "result manipulation",
    "wash":                  "result manipulation",

    # ── SMS shorthand common in Nigerian messages ─────────────────────────────
    "ur":                    "your",
    "pls":                   "please",
    "plz":                   "please",
    "msg":                   "message",
    "txt":                   "text",
    "nd":                    "and",
    "nt":                    "not",
    "hv":                    "have",
    "av":                    "have",
    "cn":                    "can",
    "hw":                    "how",
    "whr":                   "where",
    "whn":                   "when",
    "bcoz":                  "because",
    "cos":                   "because",
    "coz":                   "because",
    "dis":                   "this",
    "dat":                   "that",
    "wit":                   "with",
    "b4":                    "before",
    "luv":                   "love",
    "tnx":                   "thanks",
    "thx":                   "thanks",
    "nw":                    "now",
    "hw":                    "how",
    "wud":                   "would",
    "shud":                  "should",
    "cud":                   "could",
    "wanna":                 "want to",
    "gonna":                 "going to",
    "gotta":                 "got to",
}