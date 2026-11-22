# -*- coding: utf-8 -*-
"""
Content that sits on top of the base PROJECTS list in build.py:
corrections (status, honest notes), per-project technical challenges,
game-jam retrospectives, store metrics, the real code samples, and the skills
grid. Everything here is either verifiable (store page, public repos, code in
the private repos) or phrased as a lesson, never as an invented number.

build.py merges ENRICH into PROJECTS at import time.
"""
import os
import re
import html

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# New projects (public, non-game work: shows range beyond Unity)
# --------------------------------------------------------------------------

NEW_PROJECTS = [
    {
        "id": "climb-euw", "title": "CLIMB.EUW",
        "shortDesc": "Web app that tracks a League of Legends SoloQ climb game by game, detects sessions and exports a recap for an AI coach.",
        "description": "A progress tracker for League of Legends ranked play. It follows each game, recomputes the rank from LP changes, detects play sessions and generates a structured recap meant to be pasted into an AI coach. Everything stays in the browser (localStorage): no backend, no account, with JSON export and import. Open source, deployed on GitHub Pages.",
        "category": "App", "engine": "React / Vite", "platform": "Web", "role": "Solo Developer",
        "status": "Released", "year": 2026, "duration": "Ongoing", "teamSize": 1,
        "technologies": ["JavaScript", "React", "Vite", "Recharts", "GitHub Pages"],
        "tags": ["App", "Web"], "featured": False,
        "links": {"demo": "https://romainpitot.github.io/lol-climb-tracker/",
                  "github": "https://github.com/RomainPitot/lol-climb-tracker"},
        "highlights": ["Rank engine driven by LP changes, game by game",
                       "Session detection and structured coach recap",
                       "No backend: data stays in the browser, JSON export/import"],
        "keySystems": ["LP/Rank Engine", "Session Detection", "AI Coach Recap"],
    },
    {
        "id": "game-detector-lol", "title": "GameDetectorLol",
        "shortDesc": "Windows companion app that watches the League of Legends client and game and shows the live match status on CLIMB.EUW.",
        "description": "A small Windows program that runs next to League of Legends and reads two local APIs: the client's (queue, ready check, champion select) and the game's own (to tell \"loading\" from \"actually in game\", since that API only answers once loading is finished). The live status is shown on CLIMB.EUW, and champion selection can be driven from a phone. Ships as an installer through GitHub releases (v1.1.0).",
        "category": "App", "engine": "Python", "platform": "Windows", "role": "Solo Developer",
        "status": "Released", "year": 2026, "duration": "Ongoing", "teamSize": 1,
        "technologies": ["Python", "Local REST APIs", "Windows installer", "GitHub Releases"],
        "tags": ["App", "Desktop"], "featured": False,
        "links": {"github": "https://github.com/RomainPitot/GameDetectorLol"},
        "highlights": ["Live status: queue, ready check, champion select, loading, in game",
                       "Distinguishes loading from in-game using the game's own API",
                       "Installer shipped through GitHub releases"],
        "keySystems": ["Client API Watcher", "Game API Probe", "Installer & Releases"],
    },
]

# --------------------------------------------------------------------------
# Corrections and additions per project id
# --------------------------------------------------------------------------

ENRICH = {
    "legend-of-mulu": {
        "status": "Archived",
        "links": {},
        "note": "Released on The Sandbox in 2023. The studio's own site now lists it as unfinished and on hold while the story continues, so there is no public build to link to.",
        "challenges": [
            ("The platform sets the rules",
             "The Sandbox's editor limits what scripting and assets can do, so the game design had to be rewritten around the toolset instead of the other way round.",
             "I adapted the design to what the platform allows, then built new explorable areas tied to the lore on top of those constraints."),
        ],
    },
    "kissoro": {
        "status": "Archived",
        "links": {},
        "description": "An African strategy board game — \"a game that has traveled through centuries and continents\" — on mobile with single- and multiplayer modes. The original game was created by Masseka years before I joined; I took over its post-production: migrated the project from Unity 2018 to Unity 2022, fixed the regressions that migration caused along with older bugs, and made the UI adapt to different devices.",
        "note": "One of the two games I spent most of my work-study on. It is no longer listed on the stores (the studio removed it after a long time without updates), so there is no link; the work is described here.",
        "challenges": [
            ("A migration that fixes some bugs and creates others",
             "Moving a 2018 codebase to Unity 2022 changed APIs and behaviours. It cleared long-standing problems but introduced new ones, on top of a UI that had to hold up on very different screens.",
             "I worked through the regressions one by one, fixed the older bugs I found on the way, and made the layout adapt to device sizes. I did not track bug counts, so there is no headline number here."),
        ],
    },
    "vaudoo": {
        "shortDesc": "Mobile zombie shooter on Google Play: a presidential candidate raises the dead to win an election, then fights the apocalypse.",
        "description": "A presidential candidate, desperate to win an election, turns to a mystic to make the dead vote — but the revived souls become flesh-hungry zombies, and he has to fight to save the country. A mobile shooter with several environments, upgrades and weapons. I joined for a short work-study stint, a few weeks while waiting for the next project, to fix bugs and make the UI adapt properly to different screen sizes.",
        "facts": [("Google Play", "1k+ downloads")],
        "note": "The download figure is the game's own public number (Google Play, November 2026), not a measure of my share of the work, which was a few weeks of maintenance.",
        "keySystems": ["Adaptive UI", "Bug-fixing pass"],
    },
    "little-cup": {
        "challenges": [
            ("Picking up a prototype nobody owned",
             "The prototype had been abandoned inside the studio. I had to understand someone else's half-finished code before I could build on it.",
             "I revived it and built the shot system (aim, power, technique), the unlockable special shots and the ranking system on my own."),
        ],
    },
    "medieval-skirmish": {
        "description": "A strategic tower defense game: place towers, cast spells like fireball and freeze, and make tactical retreats by shifting towers to attack while moving. Built as the final-year Bachelor project on a 5-person team, following a full development cycle from concept to completion with simulated client feedback rounds. I worked as developer, level designer and game designer.",
    },
    "keep-dancing-to-live": {
        "retro": {
            "constraint": "48 hours, a team of three, and the Global Game Jam 2024 theme \"Make Me Laugh\" — which had to be funny and playable at the same time.",
            "built": "The core gameplay: the rhythm input judging and the state machine that drives the jester's dance moves.",
            "redo": "I would put the input-timing window in front of outside players much earlier. In a rhythm game that feel is the product, and 48 hours leaves little room to retune it at the end.",
        },
    },
    "thermostat-8": {
        "retro": {
            "constraint": "A game jam on the theme \"Elevate\", a team of three.",
            "built": "Gameplay programming for the survival and exploration loop, plus the visual effects pass.",
            "redo": "I would cut the scope to one survival loop and polish its feedback (VFX included) instead of spreading effort across exploration and survival.",
        },
    },
    "falling-bot": {
        "retro": {
            "constraint": "Ludum Dare 48, theme \"Deeper and Deeper\", a team of three, 48 hours.",
            "built": "The visual effects and the UI, including the fuel gauge that carries the risk/reward of the whole game.",
            "redo": "I would build a tuning panel for fuel burn and obstacle density first, so the balance can be adjusted live instead of after each rebuild.",
        },
    },
    "trash-santa": {
        "retro": {
            "constraint": "Global Game Jam 2020, theme \"Repair\", a team of four, 48 hours, and a multiplayer game.",
            "built": "The UI and part of the gameplay programming.",
            "redo": "I would agree on the multiplayer input and rules scaffolding in the first hours, so UI and gameplay stop waiting on each other.",
        },
    },
    "on-air": {
        "role": "Solo Developer",
        "note": "Made during the Epic AI MegaJam, where using AI tools is part of the brief and the process has to be documented. I designed the game and directed the build; Claude Code wrote much of the C++ under my review, and the dev log is public.",
        "retro": {
            "constraint": "A jam window of several days, but I could only work about one day of it. Solo, with AI tools declared and a public dev log required, on the theme \"Director's Cut\".",
            "built": "The design (the 7-second delay as the core mechanic), the architecture, and the integration and playtesting of everything the AI generated.",
            "redo": "With so little time I would have cut a night of content and used the hours for outside playtests. The nightly rule changes are the part a new player has to learn, and I only saw how readable they were once the loop was complete.",
        },
        "challenges": [
            ("A 7-second broadcast delay without a video buffer",
             "The core mechanic needs two monitors showing the same studio, seven seconds apart. Buffering video would be heavy and hard to edit afterwards.",
             "The studio is simulated twice. Each copy poses its actors as a pure function of time, and a director object gives one the clock t and the other t − 7 s. Censorship (bleep, blur, camera cut) is stored on the content timeline rather than on the image, so both copies replay it at their own moment and the on-air monitor stays consistent."),
            ("Blurring a point on a screen inside the game",
             "Clicking on the PREVIEW monitor has to find the matching point in the camera image rendered to it.",
             "The hit's UV coordinates on the monitor mesh give the position in the render target (physics UV-from-hit enabled), which becomes the blur rectangle."),
        ],
    },
    "global-invasion": {
        "facts": [("Unit tests", "~80 (EditMode, NUnit)"), ("Swarm step", "0.25 ms for 300 roaches")],
        "challenges": [
            ("Hundreds of insects over a network",
             "Replicating every roach as a networked object would flood the connection and cost far too much for a swarm of hundreds.",
             "The swarm is simulated locally on every PC, in plain arrays with no per-roach objects (capacity 400). Only events cross the network: a seeded burst of N roaches, a spray cone, a broom hit. I measured 0.25 ms per step for 300 roaches."),
            ("Testing game rules that live inside a netcode project",
             "Rules wired directly into NetworkBehaviours can't be tested without launching a session.",
             "The rules are plain C# with time and randomness passed in (mission clock, nest draw, shop, contamination model); the network classes are thin wrappers around them. That gives about 80 EditMode tests that run in batch mode."),
        ],
        "links": {},
    },
    "shipwrecked-island": {},
    "just-dash": {},
}

# Home page picks (explicit, mixes game and non-game work)
HOME_FEATURED = ["global-invasion", "kissoro", "legend-of-mulu", "on-air", "climb-euw", "vaudoo"]

# Project order shown on the listing: current work first, then the rest.
# (Pager follows PROJECTS order, which build.py keeps as written.)

# --------------------------------------------------------------------------
# Skills with an honest level
# --------------------------------------------------------------------------

SKILL_TIERS = [
    ("Daily", "what I write most weeks", [
        "Unity (URP)", "C#", "Netcode for GameObjects", "NUnit EditMode tests",
        "Custom editor tools", "ScriptableObjects", "UGUI", "Git / GitHub",
    ]),
    ("Used on real projects", "shipped or in a repo", [
        "Steamworks lobbies", "Unreal Engine 5 / C++ (On Air)", "Android builds",
        "NavMesh & agent simulation", "Python tools & automation", "React / Vite web app",
        "VFX & shaders (jam level)", "AI-assisted workflow (Claude Code)",
    ]),
    ("Learning", "not yet on a project", ["Unity DOTS"]),
]

MARQUEE_ITEMS = [
    "Unity", "C#", "Netcode for GameObjects", "Steamworks", "NUnit tests",
    "Unreal Engine 5", "C++", "Python", "React", "Git",
]

# --------------------------------------------------------------------------
# Real code samples (extracted from the repos, comments translated)
# --------------------------------------------------------------------------

def _sample(name):
    with open(os.path.join(HERE, "samples", name), encoding="utf-8") as f:
        return f.read().rstrip() + "\n"


CODE_SAMPLES = [
    {
        "id": "mission-clock", "title": "Mission state machine",
        "project": "Global Invasion", "file": "Mission/MissionClock.cs",
        "tagline": "Day → Night → Dawn → Debrief, on deadlines, with no dependency on Unity or the network.",
        "why": "The rules are plain C# and receive the time as a parameter. The network wrapper feeds it the server clock; the tests feed it any number they want, so the whole mission loop is tested without launching a session.",
        "tags": ["C#", "State machine", "Testable design"],
        "code": _sample("mission_clock.cs"),
    },
    {
        "id": "nest-draw", "title": "Seeded nest & clue draw",
        "project": "Global Invasion", "file": "Mission/NestDraw.cs",
        "tagline": "Picks where the nest is this run and which clues (and decoys) are on site.",
        "why": "Randomness is injected, so the draw is reproducible in tests and only the server rolls the dice. Decoys are chosen with a partial Fisher–Yates shuffle so no single clue is enough on its own.",
        "tags": ["C#", "Procedural", "Server authority"],
        "code": _sample("nest_draw.cs"),
    },
    {
        "id": "swarm-sim", "title": "Local swarm, events on the wire",
        "project": "Global Invasion", "file": "Swarm/SwarmSim.cs",
        "tagline": "Hundreds of roaches simulated on every PC; only events cross the network.",
        "why": "The level is hidden behind an interface so the real game uses physics colliders and the tests use a fake. Data is stored in arrays rather than objects: I measured 0.25 ms per step for 300 roaches.",
        "tags": ["C#", "Netcode", "Performance"],
        "code": _sample("swarm_sim.cs"),
    },
    {
        "id": "turret", "title": "MOBA-style turret targeting",
        "project": "Turret prototype (private repo)", "file": "TurretScript.cs",
        "tagline": "A small early prototype: creeps are targeted before the player, and a locked target is never swapped.",
        "why": "Small on purpose. It shows how I start: one clear rule per piece of code, written first and tuned after. Newer work (above) is where the structure and tests are.",
        "tags": ["C#", "Unity", "Prototype"],
        "code": _sample("turret.cs"),
    },
]

# --------------------------------------------------------------------------
# Minimal C# highlighter (server side: no JS, no dependency)
# --------------------------------------------------------------------------

_KW = set("""public private protected static void class struct enum interface readonly const new return if else for foreach
while switch case break continue null true false this using namespace out ref in is as var int float double bool string
get set override virtual abstract""".split())
_TYPES = set("""Transform Collider Vector2 Vector3 Quaternion Time Random List IList MonoBehaviour MissionPhase MissionClock
NestDraw Math Result Durations SwarmSim ISwarmWorld Settings TurretScript Mathf""".split())

_TOKEN = re.compile(r"(//[^\n]*)|(\"(?:[^\"\\]|\\.)*\")|([A-Za-z_][A-Za-z0-9_]*)|(\d+\.?\d*f?)|([\s\S])")


def highlight_cs(code):
    out = []
    for m in _TOKEN.finditer(code):
        comment, string, ident, num, other = m.groups()
        if comment:
            out.append('<span class="tok-c">%s</span>' % html.escape(comment))
        elif string:
            out.append('<span class="tok-s">%s</span>' % html.escape(string))
        elif ident:
            if ident in _KW:
                out.append('<span class="tok-k">%s</span>' % ident)
            elif ident in _TYPES:
                out.append('<span class="tok-t">%s</span>' % ident)
            else:
                out.append(ident)
        elif num:
            out.append('<span class="tok-n">%s</span>' % num)
        else:
            out.append(html.escape(other))
    return "".join(out)


# --------------------------------------------------------------------------
# Per-project page themes (like an itch.io page, but pushed further).
# mode: dark/light; bg/primary/accent: (hue, saturation %, lightness %);
# font: serif | mono | condensed | rounded | sans; fx: optional CSS effect;
# kicker: small line above the title (taken from the game's own theme or plot).
# --------------------------------------------------------------------------
THEMES = {
    "on-air": {"mode": "dark", "bg": (18, 18, 7), "primary": (6, 82, 56), "accent": (48, 92, 62),
               "font": "mono", "fx": "crt", "kicker": "ON AIR · 1978 · 7-second delay"},
    "global-invasion": {"mode": "dark", "bg": (222, 30, 8), "primary": (38, 92, 60), "accent": (160, 60, 50),
                        "font": "condensed", "fx": "vignette", "kicker": "Investigate by day. Survive the night."},
    "kissoro": {"mode": "dark", "bg": (22, 38, 9), "primary": (32, 88, 56), "accent": (12, 70, 55),
                "font": "serif", "fx": "grain", "kicker": "A board game that crossed centuries and continents"},
    "legend-of-mulu": {"mode": "dark", "bg": (150, 32, 8), "primary": (44, 80, 58), "accent": (172, 55, 48),
                       "font": "serif", "fx": "grain", "kicker": "An adventure on The Sandbox"},
    "vaudoo": {"mode": "dark", "bg": (268, 30, 8), "primary": (96, 78, 52), "accent": (300, 60, 62),
               "font": "condensed", "fx": "vignette", "kicker": "Make the dead vote"},
    "little-cup": {"mode": "light", "bg": (110, 30, 93), "primary": (140, 60, 28), "accent": (28, 85, 42),
                   "font": "rounded", "fx": "", "kicker": "Aim · power · technique"},
    "medieval-skirmish": {"mode": "light", "bg": (40, 42, 88), "primary": (14, 70, 36), "accent": (210, 45, 32),
                          "font": "serif", "fx": "grain", "kicker": "Hold the line"},
    "shipwrecked-island": {"mode": "dark", "bg": (192, 40, 9), "primary": (40, 78, 62), "accent": (170, 65, 48),
                           "font": "rounded", "fx": "vignette", "kicker": "Repair the ship before the saboteur wins"},
    "just-dash": {"mode": "dark", "bg": (250, 40, 10), "primary": (172, 85, 52), "accent": (330, 80, 66),
                  "font": "rounded", "fx": "", "kicker": "Climb. Dash. Don't fall."},
    "keep-dancing-to-live": {"mode": "dark", "bg": (292, 45, 10), "primary": (320, 85, 64), "accent": (52, 95, 60),
                             "font": "condensed", "fx": "", "kicker": "Make me laugh"},
    "thermostat-8": {"mode": "dark", "bg": (205, 40, 9), "primary": (22, 90, 58), "accent": (195, 80, 62),
                     "font": "mono", "fx": "snow", "kicker": "Elevate"},
    "falling-bot": {"mode": "dark", "bg": (232, 40, 7), "primary": (186, 90, 55), "accent": (48, 95, 58),
                    "font": "mono", "fx": "rain", "kicker": "Deeper and deeper"},
    "trash-santa": {"mode": "dark", "bg": (350, 35, 9), "primary": (4, 78, 58), "accent": (140, 55, 50),
                    "font": "rounded", "fx": "snow", "kicker": "Repair"},
    "climb-euw": {"mode": "dark", "bg": (214, 45, 8), "primary": (44, 62, 58), "accent": (190, 80, 50),
                  "font": "sans", "fx": "", "kicker": "SoloQ, game by game"},
    "game-detector-lol": {"mode": "dark", "bg": (214, 45, 8), "primary": (188, 85, 52), "accent": (44, 62, 58),
                          "font": "mono", "fx": "", "kicker": "Is the game live?"},
}
