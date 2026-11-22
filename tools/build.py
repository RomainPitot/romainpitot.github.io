# -*- coding: utf-8 -*-
"""
Static site generator for the Pitot Engine portfolio.

This is a *build-time* convenience script (run locally with `python tools/build.py`)
that outputs plain, dependency-free HTML files. Nothing about the deployed site
requires Python or Node — GitHub Actions just uploads the generated files as-is.

Re-run this script after editing PROJECTS / SYSTEMS / SKILLS below, then commit
the regenerated HTML.
"""
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_extra as X

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _compute_asset_version():
    """Hash of the CSS/JS assets, used as a ?v= cache-busting query string
    so browsers pick up changes immediately instead of serving a stale
    cached copy after a redeploy."""
    h = hashlib.sha256()
    for rel in ("assets/css/style.css", "assets/js/main.js", "assets/js/i18n.js", "assets/js/field.js"):
        path = os.path.join(ROOT, rel)
        if os.path.exists(path):
            with open(path, "rb") as f:
                h.update(f.read())
    return h.hexdigest()[:10]


ASSET_VERSION = _compute_asset_version()

SITE_NAME = "romain.pitot"
AUTHOR = "Romain Pitot"
YEAR = "2026"

REAL_GITHUB = "https://github.com/romainpitot"
REAL_LINKEDIN = "https://linkedin.com/in/romain-pitot"
CONTACT_EMAIL = "romainpitot.dev@gmail.com"
FORMSPREE_ENDPOINT = "https://formspree.io/f/mkjnwagj"


def email_link(cls="", label_prefix=""):
    """Address split in two data attributes and assembled by main.js, so it is
    not sitting in the HTML for harvesting bots. Without JS the visitor sees
    a readable 'user [at] host' and can still use the form."""
    user, host = CONTACT_EMAIL.split("@")
    return ('<a class="%s" href="contact.html" data-mail data-u="%s" data-h="%s">%s%s [at] %s</a>'
            % (cls, user, host, label_prefix, user, host))

# --------------------------------------------------------------------------
# Icons (Feather Icons, MIT licensed — inline so the site has zero runtime
# dependency on an icon font/CDN).
# --------------------------------------------------------------------------
ICONS = {
    "menu": '<line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>',
    "x": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    "arrow-right": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    "github": '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
    "mail": '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22 6 12 13 2 6"/>',
    "package": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',
    "map": '<polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/>',
    "save": '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2" ry="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "wifi": '<path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/>',
    "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "monitor": '<rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>',
    "external-link": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>',
    "user": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "play": '<polygon points="5 3 19 12 5 21 5 3"/>',
    "send": '<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>',
    "folder": '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
    "arrow-up": '<line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/>',
    "arrow-left": '<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>',
}


def icon(name, cls="icon"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, ICONS[name])


# --------------------------------------------------------------------------
# Content data (transcribed from the live Base44 build — see /tools/README
# in this folder for provenance notes).
# --------------------------------------------------------------------------

PROJECTS = [
    # --- Work-study projects (Masseka Games Studio, Toulouse — Oct 2022-Oct 2024) ---
    {
        "id": "legend-of-mulu", "title": "The Legend of Mulu",
        "shortDesc": "Exploration game on The Sandbox: a young girl tracks down sorcerers who stole her village's sacred artifacts.",
        "description": "An exploration game built on The Sandbox platform, set in Africa. Players control Mulu, a girl sent far from her village to recover sacred artifacts stolen by sorcerers. Worked as game designer, developer, level designer and artist: adapted the game design to The Sandbox's constraints, built new explorable areas integrated with the lore, and contributed artwork.",
        "category": "Work", "engine": "The Sandbox / Unity", "platform": "The Sandbox", "role": "Game Designer, Developer, Level Designer, Artist",
        "status": "Released", "year": 2023, "duration": "Work-study", "teamSize": 2,
        "technologies": ["C#", "Unity", "The Sandbox", "Level Design"],
        "tags": ["Work", "Adventure"], "featured": True,
        "links": {"demo": "https://www.sandbox.game/en/experiences/The%20Legend%20Of%20Mulu/823bbdd4-8cab-4394-b8fb-bad31be27b7d/page/"},
        "highlights": ["Game design adapted to The Sandbox's toolset", "New lore-integrated explorable areas", "Contributed environment art"],
        "keySystems": ["Level Streaming", "Quest/Artifact Tracking", "Sandbox Scripting"],
        "image": "legend-of-mulu-1.jpg",
        "gallery": ["legend-of-mulu-2.jpg", "legend-of-mulu-3.jpg", "legend-of-mulu-4.jpg"],
    },
    {
        "id": "kissoro", "title": "Kissoro Tribal Game",
        "shortDesc": "African strategy board game on mobile — migrated from Unity 2018 to 2022 and stabilized across devices.",
        "description": "An African strategy board game — \"a game that has traveled through centuries and continents\" — brought to mobile with single- and multiplayer modes. Took over post-production on an existing title: migrated the project from Unity 2018 to Unity 2022, resolved the resulting compatibility issues, fixed longstanding bugs, and ensured adaptive behaviour across devices.",
        "category": "Work", "engine": "Unity", "platform": "Mobile (Android/iOS)", "role": "Unity Developer (maintenance)",
        "status": "Released", "year": 2023, "duration": "Work-study", "teamSize": 1,
        "technologies": ["C#", "Unity", "Mobile"],
        "tags": ["Work", "Mobile"], "featured": False,
        "links": {"playstore": "https://play.google.com/store/apps/details?id=com.masseka.game.studio&hl=fr"},
        "highlights": ["Migrated Unity 2018 → 2022 codebase", "Fixed longstanding compatibility bugs", "Adaptive UI across device sizes"],
        "keySystems": ["Board Game Rules Engine", "Cross-device UI Scaling"],
        "image": "kissoro-2.jpg",
        "gallery": ["kissoro-1.jpg"],
    },
    {
        "id": "vaudoo", "title": "Vaudoo",
        "shortDesc": "Mobile action-strategy game: a presidential candidate raises the dead to win an election, then fights the zombie apocalypse.",
        "description": "A presidential candidate, desperate to win an election, turns to a mystic to make the dead vote — but the revived souls become flesh-hungry zombies, forcing a fight to save the nation. Blends action and strategy, with every decision mattering during the horde battles. Joined for a short work-study stint to fix bugs and make the UI properly adaptive across screen sizes.",
        "category": "Work", "engine": "Unity", "platform": "Mobile (Android)", "role": "Unity Developer (maintenance)",
        "status": "Released", "year": 2023, "duration": "A few weeks", "teamSize": 1,
        "technologies": ["C#", "Unity", "Mobile", "UGUI"],
        "tags": ["Work", "Mobile"], "featured": False,
        "links": {"playstore": "https://play.google.com/store/apps/details?id=com.messeka.Vaudoo&hl=fr"},
        "highlights": ["Adaptive UI across device sizes", "Bug fixing pass on an existing codebase"],
        "keySystems": ["Horde Combat Loop", "Adaptive UI"],
    },
    {
        "id": "little-cup", "title": "Little Cup",
        "shortDesc": "Mobile penalty-shootout game: aim, power and technique against increasingly skilled goalkeepers.",
        "description": "A penalty-focused sports game where you play an elite striker challenging increasingly skilled goalkeepers across varied weather conditions, stadiums and crowd dynamics. Precision and strategy around aim, power and technique matter, with unlockable special shots, player customization and a ranking system. Revived and built out solo from an abandoned internal prototype during the work-study.",
        "category": "Work", "engine": "Unity", "platform": "Mobile", "role": "Developer (solo)",
        "status": "Prototype", "year": 2023, "duration": "Work-study", "teamSize": 1,
        "technologies": ["C#", "Unity", "Mobile"],
        "tags": ["Work", "Sports"], "featured": False,
        "links": {},
        "highlights": ["Revived an abandoned prototype solo", "Aim/power/technique shot system", "Unlockables and ranking system"],
        "keySystems": ["Shot Aiming System", "Ranking/Progression"],
    },
    # --- School projects (Bachelor, E-Artsup Toulouse — Sept 2019-Sept 2022) ---
    {
        "id": "medieval-skirmish", "title": "Medieval Skirmish",
        "shortDesc": "Tower defense where you place towers and cast spells (fireball, freeze) to hold off waves of enemies.",
        "description": "A strategic tower defense game: place towers, cast spells like fireball and freeze, and make tactical retreats by shifting towers to attack while moving. Built as the final-year Bachelor project, following a full development cycle from concept to completion with simulated client feedback rounds. Worked as developer, level designer and game designer on a 5-person team.",
        "category": "School", "engine": "Unity", "platform": "PC", "role": "Developer, Level Designer, Game Designer",
        "status": "Prototype", "year": 2022, "duration": "Final-year project", "teamSize": 5,
        "technologies": ["C#", "Unity", "Design Patterns", "Git"],
        "tags": ["School", "Tower Defense"], "featured": True,
        "links": {},
        "highlights": ["Full dev cycle with simulated client feedback", "Spell system (fireball, freeze)", "Tower repositioning while attacking"],
        "keySystems": ["Wave Manager", "Spell/Ability System", "Tower Placement & Pathing"],
    },
    {
        "id": "shipwrecked-island", "title": "Shipwrecked Island",
        "shortDesc": "Multiplayer horror survival: gather resources and repair your ship before the hidden saboteur stops you.",
        "description": "A shipwrecked pirate stranded on a mysterious island with a lurking monster. Together with crewmates, gather resources and repair the ship to escape — but one crew member is a hidden saboteur secretly working against the group. A school project in the multiplayer horror/social-deduction space, built with Netcode. Worked on UI and part of the core gameplay mechanics.",
        "category": "School", "engine": "Unity", "platform": "PC", "role": "UI & Gameplay Programmer",
        "status": "Prototype", "year": 2022, "duration": "School project", "teamSize": 4,
        "technologies": ["C#", "Unity", "Netcode", "UGUI"],
        "tags": ["School", "Multiplayer"], "featured": False,
        "links": {},
        "highlights": ["Multiplayer social-deduction gameplay loop", "Netcode-driven crew/saboteur mechanics", "UI for shared crew objectives"],
        "keySystems": ["Netcode Session Sync", "Saboteur Role Logic", "Resource Gathering"],
    },
    {
        "id": "just-dash", "title": "Just Dash",
        "shortDesc": "Mobile platformer mixing Doodle Jump's vertical momentum with Celeste's precision dashing.",
        "description": "A mobile platformer where a nimble robot navigates challenging levels using a dash ability, blending \"the vertical momentum of Doodle Jump and the precision platforming of Celeste.\" Dash resets are limited and must be earned through skillful moves, so timing and strategy matter to reach the goal. Developed part of the core gameplay as a school project.",
        "category": "School", "engine": "Unity", "platform": "Mobile", "role": "Gameplay Programmer",
        "status": "Released", "year": 2022, "duration": "School project", "teamSize": 3,
        "technologies": ["C#", "Unity", "Mobile"],
        "tags": ["School", "Platformer"], "featured": False,
        "links": {"demo": "https://drive.google.com/file/d/17z5dnXX2XskFLim2g4_lbbTyLSIla8EJ/view"},
        "highlights": ["Limited-resource dash mechanic", "Momentum-based vertical platforming"],
        "keySystems": ["Dash/Resource System", "Procedural-feel Level Momentum"],
    },
    # --- Game jams ---
    {
        "id": "keep-dancing-to-live", "title": "Keep Dancing to Live",
        "shortDesc": "Rhythm game: dance ridiculously as the king's jester, or it's off with your head. Global Game Jam 2024 — \"Make Me Laugh.\"",
        "description": "A rhythm game where you play the king's jester, performing ridiculous dance moves on a wooden board to entertain the court and survive — fail to amuse, and it's off with your head. Built in 48 hours at the Global Game Jam 2024, on the theme \"Make Me Laugh.\" Developed the core gameplay mechanics.",
        "category": "Game Jam", "engine": "Unity", "platform": "PC", "role": "Gameplay Programmer",
        "status": "Released", "year": 2024, "duration": "48 hours", "teamSize": 3,
        "technologies": ["C#", "Unity"],
        "tags": ["Game Jam", "Rhythm"], "featured": True,
        "links": {"itch": "https://jules-gilli.itch.io/keep-dancing-to-live"},
        "highlights": ["Global Game Jam 2024 — \"Make Me Laugh\"", "Rhythm/timing-based dance mechanic", "Built and shipped in 48 hours"],
        "keySystems": ["Rhythm Input Judge", "Dance Move State Machine"],
        "image": "keep-dancing-to-live-1.jpg",
        "gallery": ["keep-dancing-to-live-2.jpg"],
    },
    {
        "id": "thermostat-8", "title": "Thermostat 8",
        "shortDesc": "Exploration survival game built for a game jam on the theme \"Elevate.\"",
        "description": "A singleplayer exploration survival game built during a game jam on the theme \"Elevate.\" Worked on gameplay development and visual effects.",
        "category": "Game Jam", "engine": "Unity", "platform": "PC", "role": "Gameplay & VFX",
        "status": "Released", "year": 2021, "duration": "Game jam", "teamSize": 3,
        "technologies": ["C#", "Unity", "VFX"],
        "tags": ["Game Jam", "Survival"], "featured": False,
        "links": {"itch": "https://phobosrandom.itch.io/thermostat-8"},
        "highlights": ["Game jam theme: \"Elevate\"", "Survival/exploration gameplay loop", "Visual effects work"],
        "keySystems": ["Survival Resource Loop", "VFX Pass"],
        "image": "thermostat-8-1.jpg",
        "gallery": ["thermostat-8-2.jpg"],
    },
    {
        "id": "falling-bot", "title": "Falling Bot",
        "shortDesc": "Pilot an energy-constrained robot descending through caverns. Ludum Dare 48 — \"Deeper and Deeper.\"",
        "description": "Pilot a robot descending through caverns while managing limited fuel and dodging or destroying obstacles — run out of fuel or crash, and it's game over. Built during Ludum Dare 48 on the theme \"Deeper and Deeper.\" Worked on visual effects and UI.",
        "category": "Game Jam", "engine": "Unity", "platform": "PC", "role": "VFX & UI",
        "status": "Released", "year": 2021, "duration": "48 hours", "teamSize": 3,
        "technologies": ["C#", "Unity", "VFX", "UGUI"],
        "tags": ["Game Jam", "Arcade"], "featured": False,
        "links": {"itch": "https://phobosrandom.itch.io/falling-bot"},
        "highlights": ["Ludum Dare 48 — \"Deeper and Deeper\"", "Fuel-management risk/reward loop", "Visual effects and UI"],
        "keySystems": ["Fuel/Resource Management", "Obstacle Spawner"],
        "image": "falling-bot-1.jpg",
    },
    {
        "id": "trash-santa", "title": "Trash Santa",
        "shortDesc": "Chaotic multiplayer game about stealing presents from unsuspecting kids. Global Game Jam 2020 — \"Repair.\"",
        "description": "A chaotic multiplayer game where players steal as many presents as possible from unsuspecting kids. Built in 48 hours at the Global Game Jam 2020, on the theme \"Repair.\" Worked on UI development and gameplay programming.",
        "category": "Game Jam", "engine": "Unity", "platform": "PC", "role": "UI & Gameplay Programmer",
        "status": "Released", "year": 2020, "duration": "48 hours", "teamSize": 4,
        "technologies": ["C#", "Unity", "Multiplayer", "UGUI"],
        "tags": ["Game Jam", "Multiplayer"], "featured": False,
        "links": {"itch": "https://phobosrandom.itch.io/trash-santa"},
        "highlights": ["Global Game Jam 2020 — \"Repair\"", "Local multiplayer chaos gameplay", "UI built under 48-hour constraint"],
        "keySystems": ["Local Multiplayer Loop", "Steal/Score Tracking"],
    },
    # --- Personal ---
    {
        "id": "global-invasion", "title": "Global Invasion",
        "shortDesc": "Steam co-op for 1-4 players: exterminators investigate infested houses by day and survive the swarm by night.",
        "description": "A cooperative first-person game for one to four players, in the spirit of Phasmophobia and Lethal Company. A team of pest-control agents investigates an infested home by day, hunting clues to find the hidden nest, then prepares and survives the night while the nest breeds, before destroying it at dawn. Steam lobbies and invitations, team votes on contracts, a supply truck shop, tools in hand (broom, UV lamp, spray, sticky traps, radio) and a swarm simulated locally on each machine so hundreds of insects stay cheap over the network. A solo personal project built from scratch to explore multiplayer systems end to end.",
        "category": "Personal", "engine": "Unity", "platform": "PC", "role": "Solo Developer",
        "status": "WIP", "year": 2026, "duration": "Ongoing", "teamSize": 1,
        "technologies": ["C#", "Unity 6", "Netcode for GameObjects", "Steamworks", "Multiplayer"],
        "tags": ["Personal", "Multiplayer"], "featured": False,
        "links": {},
        "highlights": ["Day/night investigate-then-survive loop", "Steam co-op lobby, voting and networked missions", "Locally simulated swarm: events over the wire, not insects"],
        "keySystems": ["Mission Clock (day/night)", "Random Nest & Clue Draw", "Swarm Simulation", "Co-op Netcode"],
        "image": "global-invasion-1.jpg",
    },
    {
        "id": "on-air", "title": "On Air",
        "shortDesc": "Live TV, 1978, seven-second delay: you direct the control room and cut everything before it airs. Epic AI MegaJam 2026 — \"Director's Cut.\"",
        "description": "Unreal Engine 5 game made for the Epic AI MegaJam 2026, in about one day of actual work inside the jam window (I was unavailable for much of it) (theme \"Director's Cut\"). You are the director of a tiny 1978 TV channel: everything the studio films shows on your PREVIEW monitor seven seconds before it goes on air. Bleep the swears on the tape, blur the rival brand, cut to another camera when a streaker runs in, and keep complaints down while ratings go up — except the audience secretly loves a scandal. Three live nights add one new tool or rule each, and the game ends on the Director's Cut: the version that never aired. Solo entry, with AI tools declared on the submission page.",
        "category": "Game Jam", "engine": "Unreal", "platform": "PC", "role": "Solo Developer",
        "status": "Released", "year": 2026, "duration": "~1 day of work", "teamSize": 1,
        "technologies": ["C++", "Unreal Engine 5", "UMG", "Game Jam"],
        "tags": ["Game Jam", "Arcade"], "featured": False,
        "links": {"itch": "https://romain-pitot.itch.io/on-air", "video": "https://youtu.be/pXM-Qu8bEsg"},
        "highlights": ["Epic AI MegaJam 2026 — \"Director's Cut\"", "7-second broadcast delay as the core mechanic", "Rules that change each night, with decoys you must let air"],
        "keySystems": ["Delayed Broadcast Tape", "Incident Scoring", "Nightly Rule Set"],
        "image": "on-air-1.jpg",
        "gallery": ["on-air-2.jpg", "on-air-3.jpg"],
    },
]


# Corrections, challenges, jam retrospectives and the non-game projects live in
# content_extra.py; merge them into the base list here.
PROJECTS.extend(X.NEW_PROJECTS)
for _p in PROJECTS:
    _p.update(X.ENRICH.get(_p["id"], {}))
SKILL_TIERS = X.SKILL_TIERS
MARQUEE_ITEMS = X.MARQUEE_ITEMS

EDUCATION = [
    ("Master Video Game Developer & Rendering Systems", "Gaming Campus, Lyon — alternance at Masseka Games Studio, Toulouse", "Oct 2022 – Oct 2024"),
    ("Bachelor's, Game Design & Video Games (Creative Coding)", "E-Artsup, Toulouse", "Sep 2019 – Sep 2022"),
]


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

BADGE_COLOR = {
    "Game Jam": "badge-cat-jam",
    "Prototype": "badge-cat-proto",
    "Tool": "badge-cat-tool",
    "Tools": "badge-cat-tool",
    "Released": "badge-cat-released",
    "Work": "badge-cat-tool",
    "School": "badge-cat-released",
    "Personal": "badge-cat-jam",
    "WIP": "",
    "Archived": "badge-cat-archived",
    "App": "badge-cat-tool",
}


def badge(text):
    cls = BADGE_COLOR.get(text, "")
    return '<span class="badge %s">%s</span>' % (cls, text)


def corner_badges(status, tags):
    values = [status] + tags[:2]
    return "".join(badge(v) for v in values)


def tech_tags(tech, cap=4):
    shown = tech[:cap]
    rest = len(tech) - cap
    html = "".join('<span class="tag">%s</span>' % t for t in shown)
    if rest > 0:
        html += '<span class="tag tag-more">+%d</span>' % rest
    return html


def all_tech_tags(tech):
    return "".join('<span class="tag">%s</span>' % t for t in tech)


def cover_class(category):
    return {
        "Game Jam": "cover-gamejam",
        "Prototype": "cover-prototype",
        "Tool": "cover-tool",
        "Work": "cover-tool",
        "School": "cover-released",
        "Personal": "cover-personal",
        "App": "cover-tool",
    }.get(category, "cover-prototype")


def project_cover_src(p):
    """Real screenshot when there is one, otherwise the generated typographic
    poster, so every card carries the same visual weight."""
    return p.get("image") or ("%s-cover.jpg" % p["id"])


def project_link_buttons(links, size_cls="btn-sm"):
    out = []
    if links.get("github"):
        out.append('<a class="btn btn-outline %s" href="%s" target="_blank" rel="noopener noreferrer">%s Source on GitHub</a>' % (size_cls, links["github"], icon("github")))
    if links.get("itch"):
        out.append('<a class="btn btn-outline %s" href="%s" target="_blank" rel="noopener noreferrer">%s Play on itch.io</a>' % (size_cls, links["itch"], icon("play")))
    if links.get("video"):
        out.append('<a class="btn btn-outline %s" href="%s" target="_blank" rel="noopener noreferrer">%s Watch the trailer</a>' % (size_cls, links["video"], icon("play")))
    if links.get("playstore"):
        out.append('<a class="btn btn-outline %s" href="%s" target="_blank" rel="noopener noreferrer">%s Get it on Google Play</a>' % (size_cls, links["playstore"], icon("external-link")))
    if links.get("demo"):
        out.append('<a class="btn btn-outline %s" href="%s" target="_blank" rel="noopener noreferrer">%s Open it</a>' % (size_cls, links["demo"], icon("external-link")))
    return "".join(out)


def project_by_id(pid):
    for p in PROJECTS:
        if p["id"] == pid:
            return p
    raise KeyError(pid)


# --------------------------------------------------------------------------
# Reusable blocks
# --------------------------------------------------------------------------

SITE_URL = "https://romainpitot.github.io"


def html_head(title, description, depth, canonical_path=""):
    canonical = SITE_URL + "/" + canonical_path
    return """<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%(title)s</title>
  <meta name="description" content="%(description)s">
  <link rel="canonical" href="%(canonical)s">
  <meta name="theme-color" content="#13161f">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="romain.pitot">
  <meta property="og:locale" content="en_GB">
  <meta property="og:title" content="%(title)s">
  <meta property="og:description" content="%(description)s">
  <meta property="og:url" content="%(canonical)s">
  <meta property="og:image" content="%(site)s/assets/img/og-cover.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Romain Pitot — Unity / C# developer">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="%(title)s">
  <meta name="twitter:description" content="%(description)s">
  <meta name="twitter:image" content="%(site)s/assets/img/og-cover.jpg">
  <link rel="icon" href="%(depth)sassets/img/favicon.svg" type="image/svg+xml">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; font-src 'self'; connect-src 'self' https://formspree.io; form-action https://formspree.io; base-uri 'self'; object-src 'none'">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <link rel="preload" href="%(depth)sassets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="%(depth)sassets/fonts/jetbrains-mono-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="%(depth)sassets/css/style.css?v=%(v)s">
""" % {"title": title, "description": description, "depth": depth, "canonical": canonical,
       "v": ASSET_VERSION, "site": SITE_URL}


def header_html(active, depth):
    nav_items = [
        ("home", "nav.home", "Home", depth + "index.html"),
        ("projects", "nav.projects", "Projects", depth + "projects.html"),
        ("code", "nav.code", "Code", depth + "code.html"),
        ("about", "nav.about", "About", depth + "about.html"),
        ("contact", "nav.contact", "Contact", depth + "contact.html"),
    ]
    links = []
    for key, i18n_key, label, href in nav_items:
        current = ' aria-current="page"' if key == active else ""
        links.append('<a href="%s"%s data-i18n="%s">%s</a>' % (href, current, i18n_key, label))
    return """<header class="site-header">
    <div class="nav-inner">
      <a class="brand" href="%(home)s">
        <span class="brand-icon">%(code_icon)s</span>
        romain<span class="dot">.</span>pitot
      </a>
      <nav class="main-nav" id="main-nav"><span class="nav-indicator" aria-hidden="true"></span>%(links)s</nav>
      <div class="nav-right">
        <button class="lang-toggle" type="button" aria-label="FR — passer en français">FR</button>
        <button class="nav-toggle" type="button" aria-label="Toggle menu" aria-expanded="false" aria-controls="main-nav">
          <span class="icon-menu">%(menu_icon)s</span>
          <span class="icon-close" hidden>%(close_icon)s</span>
        </button>
      </div>
    </div>
  </header>
""" % {
        "home": depth + "index.html",
        "code_icon": icon("code"),
        "links": "".join(links),
        "menu_icon": icon("menu"),
        "close_icon": icon("x"),
    }


def footer_html(depth):
    nav = [
        ("Home", depth + "index.html"),
        ("Projects", depth + "projects.html"),
        ("Code", depth + "code.html"),
        ("About", depth + "about.html"),
        ("Contact", depth + "contact.html"),
    ]
    nav_links = "".join('<a href="%s">%s</a>' % (href, label) for label, href in nav)

    return """<footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col footer-about">
          <div class="footer-brand">%(code_icon)s romain<span class="dot">.</span>pitot</div>
          <p>Unity &amp; C# developer. Open to work &mdash; available now, any offer.</p>
          <p class="footer-loc font-mono">Toulouse, France</p>
        </div>

        <div class="footer-col">
          <h3>Site</h3>
          <nav class="footer-nav">%(nav)s</nav>
        </div>

        <div class="footer-col">
          <h3>Elsewhere</h3>
          <nav class="footer-nav">
            <a href="%(github)s" target="_blank" rel="noopener noreferrer">%(github_icon)s GitHub</a>
            <a href="%(linkedin)s" target="_blank" rel="noopener noreferrer">%(linkedin_icon)s LinkedIn</a>
            %(email_link)s
            <a href="%(depth)scv.pdf" download>%(dl_icon)s Résumé (PDF)</a>
          </nav>
        </div>
      </div>

      <div class="footer-bottom">
        <span class="footer-copy">&copy; %(year)s Romain Pitot</span>
        <span class="footer-colophon font-mono">Static site &mdash; HTML, CSS and JS, deployed with GitHub Actions</span>
        <a class="footer-top" href="#main">Back to top %(up_icon)s</a>
      </div>
    </div>
  </footer>
""" % {
        "code_icon": icon("code"),
        "nav": nav_links,
        "email_link": email_link("", icon("mail") + " "),
        "linkedin": REAL_LINKEDIN,
        "github": REAL_GITHUB,
        "mail_icon": icon("mail"),
        "linkedin_icon": icon("linkedin"),
        "github_icon": icon("github"),
        "dl_icon": icon("download"),
        "up_icon": icon("arrow-up"),
        "depth": depth,
        "year": YEAR,
    }


def person_jsonld():
    return """<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "%(author)s",
    "jobTitle": "Unity / C# Developer",
    "address": {"@type": "PostalAddress", "addressLocality": "Toulouse", "addressCountry": "FR"},
    "alumniOf": [{"@type": "EducationalOrganization", "name": "Gaming Campus"}, {"@type": "EducationalOrganization", "name": "E-Artsup"}],
    "url": "%(site)s/",
    "sameAs": ["%(github)s", "%(linkedin)s"],
    "knowsAbout": ["Unity", "C#", "Gameplay Programming", "Multiplayer Netcode", "Unreal Engine", "Python", "React"]
  }
  </script>
""" % {"author": AUTHOR, "site": SITE_URL, "github": REAL_GITHUB, "linkedin": REAL_LINKEDIN}


def page(title, description, active, depth, body, canonical_path="", body_attrs=""):
    return """<!DOCTYPE html>
<html lang="en">
<head>
  %(head)s%(jsonld)s</head>
<body%(body_attrs)s>
  %(field)s<div class="noise-overlay" aria-hidden="true"></div>
  <div class="scroll-progress" aria-hidden="true"></div>
  <a class="skip-link" href="#main">Skip to content</a>
  %(header)s
  <main id="main">
  %(body)s
  </main>
  %(footer)s
  <script src="%(depth)sassets/js/i18n.js?v=%(v)s"></script>
  <script src="%(depth)sassets/js/main.js?v=%(v)s"></script>
  %(field_js)s</body>
</html>
""" % {
        "head": html_head(title, description, depth, canonical_path),
        "jsonld": person_jsonld(),
        "header": header_html(active, depth),
        "body": body,
        "footer": footer_html(depth),
        "depth": depth,
        "v": ASSET_VERSION,
        "body_attrs": body_attrs,
        "field": "" if body_attrs else '<canvas class="bg-field" aria-hidden="true"></canvas>' + chr(10) + "  ",
        "field_js": "" if body_attrs else '<script src="%sassets/js/field.js?v=%s"></script>' % (depth, ASSET_VERSION) + chr(10),
    }


def write(rel_path, content):
    full = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("wrote", rel_path)


# --------------------------------------------------------------------------
# Mini visual widgets for each system card (pure CSS/HTML, no images)
# --------------------------------------------------------------------------

def render_code_block(c):
    return """<article class="code-sample reveal" id="%(id)s">
    <header class="code-head">
      <div class="code-meta"><span class="code-project">%(project)s</span><span class="font-mono code-path">%(file)s</span></div>
      <h2>%(title)s</h2>
      <p class="code-tagline">%(tagline)s</p>
    </header>
    <div class="code-window">
      <div class="code-bar"><span class="font-mono">%(file)s</span><button class="code-copy" type="button" data-copy>Copy</button></div>
      <pre tabindex="0"><code>%(code)s</code></pre>
    </div>
    <p class="code-why"><strong>Why it is written this way.</strong> %(why)s</p>
    <div class="tag-row">%(tags)s</div>
  </article>
""" % {
        "id": c["id"], "project": c["project"], "file": c["file"], "title": c["title"],
        "tagline": c["tagline"], "why": c["why"], "code": X.highlight_cs(c["code"]),
        "tags": all_tech_tags(c["tags"]),
    }


def render_code_card(c):
    return """<a class="card system-card reveal" href="code.html#%(id)s">
    <div class="system-head">
      <span class="system-icon" style="background:hsl(var(--primary) / .15);color:hsl(var(--primary))">%(icon)s</span>
      <div>
        <div class="system-title-row"><h3>%(title)s</h3></div>
        <p class="system-subtitle">%(project)s</p>
      </div>
    </div>
    <p class="system-desc">%(tagline)s</p>
    <div class="tag-row">%(tags)s</div>
    <span class="card-link">Read the code %(arrow)s</span>
  </a>
""" % {"id": c["id"], "icon": icon("code"), "title": c["title"], "project": c["project"],
       "tagline": c["tagline"], "tags": all_tech_tags(c["tags"]), "arrow": icon("arrow-right")}



def render_project_card(p, depth, show_view_overlay=True):
    return """<a class="card project-card reveal" data-project-card data-title="%(title)s" data-year="%(year)s"
     data-tags="%(tagpipe)s" href="%(depth)sprojects/%(id)s.html">
    <div class="project-cover %(coverclass)s">
      <div class="cover-tags">%(badges)s</div>
      %(overlay)s
      %(media)s
    </div>
    <div class="project-body">
      <div class="project-title-row"><h3>%(title)s</h3><span class="project-year">%(year)s</span></div>
      <p class="project-desc">%(desc)s</p>
      <div class="project-meta">
        <span>%(monitor_icon)s %(engine)s</span>
        <span>%(clock_icon)s %(duration)s</span>
        <span>%(users_icon)s %(team)s</span>
      </div>
      <div class="tag-row">%(tech)s</div>
    </div>
  </a>
""" % {
        "title": p["title"], "year": p["year"], "id": p["id"], "depth": depth,
        "tagpipe": "|".join([p["category"]] + p["tags"]),
        "coverclass": cover_class(p["category"]),
        "badges": corner_badges(p["status"], p["tags"]),
        "overlay": ('<div class="project-view">%s View Project</div>' % icon("external-link")) if show_view_overlay else "",
        "media": '<img class="cover-img" src="%sassets/img/projects/%s" alt="%s cover" loading="lazy">' % (
            depth, project_cover_src(p), p["title"]),
        "desc": p["shortDesc"],
        "monitor_icon": icon("monitor"), "engine": p["engine"],
        "clock_icon": icon("clock"), "duration": p["duration"],
        "users_icon": icon("users"), "team": "Solo" if p["teamSize"] == 1 else "%d devs" % p["teamSize"],
        "tech": tech_tags(p["technologies"]),
    }


# --------------------------------------------------------------------------
# Home page
# --------------------------------------------------------------------------

def section_head(num, label, title_html, sub_html="", link_html=""):
    """Editorial section header: 01 —— LABEL / Title / subtitle."""
    return """<div class="section-head">
        <div>
          <div class="section-index">
            <span class="num">%(num)s</span>
            <span class="rule"></span>
            <span class="label">%(label)s</span>
          </div>
          %(title)s
          %(sub)s
        </div>
        %(link)s
      </div>""" % {
        "num": num, "label": label, "title": title_html,
        "sub": sub_html, "link": link_html,
    }


def build_home():
    # Objective selection (most recent first) rather than a subjective "featured"
    # pick, so no project is presented as more important than another.
    featured = [project_by_id(i) for i in X.HOME_FEATURED]
    depth = ""

    hero = """<section class="hero">
    <div class="hero-bg" aria-hidden="true"></div>
    <div class="container">
      <span class="hero-role" data-i18n="hero.title">Gameplay Programmer</span>
      <h1 class="text-glow" data-decrypt><span class="decrypt-seg">Romain</span> <span class="accent decrypt-seg">Pitot</span></h1>
      <div class="badge-row">
        <span class="pill pill-primary">Unity</span>
        <span class="pill pill-accent">C#</span>
        <span class="pill">Gameplay Systems</span>
        <span class="pill">Multiplayer</span>
      </div>
      <p class="hero-tagline" data-i18n="hero.tagline">Unity &amp; C# developer. I build gameplay systems, co-op multiplayer and the tools around them &mdash; two years in a game studio, a solo Steam co-op game in progress.</p>
      <p class="hero-avail"><span class="availability"><span class="dot"></span> <span data-i18n="contact.availability">Open to work &mdash; available now, any offer</span></span></p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="projects.html"><span data-i18n="hero.cta_projects">View Projects</span> %(arrow)s</a>
        <a class="btn btn-outline" href="cv.pdf" download>%(dl)s <span data-i18n="hero.cta_cv">Download CV</span></a>
        <a class="btn btn-outline" href="contact.html">%(mail)s <span data-i18n="hero.cta_contact">Contact me</span></a>
      </div>
      <div class="hero-status font-mono">Toulouse, FR &nbsp;&middot;&nbsp; remote &amp; relocation OK &nbsp;&middot;&nbsp; building a co-op FPS, solo</div>
      <div class="scroll-hint" data-i18n="hero.scroll">Scroll to explore</div>
    </div>
  </section>

  <section class="stats-bar">
    <div class="container stats-grid">
      <div class="stat"><div class="stat-num"><span data-count-to="%(n)d">%(n)d</span></div><div class="stat-label">Projects built</div></div>
      <div class="stat"><div class="stat-num"><span data-count-to="5">5</span></div><div class="stat-label">Game jams</div></div>
      <div class="stat"><div class="stat-num"><span data-count-to="7">7</span>+</div><div class="stat-label">Years on Unity</div></div>
      <div class="stat"><div class="stat-num"><span data-count-to="1">1</span>k+</div><div class="stat-label">Downloads on Google Play (one title)</div></div>
    </div>
  </section>

  <div class="marquee" aria-hidden="true">
    <div class="marquee-track">%(marquee)s%(marquee)s</div>
  </div>
""" % {
        "n": len(PROJECTS),
        "arrow": icon("arrow-right"),
        "dl": icon("download"),
        "mail": icon("mail"),
        "marquee": "".join(
            '<span class="marquee-item"><span class="dot-sep"></span>%s</span>' % m
            for m in MARQUEE_ITEMS
        ),
    }

    featured_cards = "".join(render_project_card(p, depth) for p in featured)

    featured_html = """<section class="section">
    <div class="container">
      %(head)s
      <div class="grid grid-3" data-project-grid>
        %(cards)s
      </div>
    </div>
  </section>
""" % {
        "head": section_head(
            "01", "Selected work",
            '<h2 class="section-title shiny" data-i18n="home.featured_title">Selected Projects</h2>',
            '<p class="section-sub" data-i18n="home.featured_subtitle">A game in progress, a jam entry, a live web app &mdash; the full list is on the projects page</p>',
            '<a class="section-link" href="projects.html"><span data-i18n="home.view_all">View all projects</span> %s</a>' % icon("arrow-right"),
        ),
        "cards": featured_cards,
    }

    systems_html = """<section class="section" style="background:hsl(var(--background-deep) / .4)">
    <div class="container">
      %(head)s
      <div class="grid grid-3">
        %(cards)s
      </div>
    </div>
  </section>
""" % {
        "head": section_head(
            "02", "Code",
            '<h2 class="section-title" data-i18n="home.systems_title">Code you can read</h2>',
            '<p class="section-sub" data-i18n="home.systems_subtitle">Real extracts from my current game, with the reasoning behind them</p>',
            '<a class="section-link" href="code.html"><span data-i18n="home.all_systems">All samples</span> %s</a>' % icon("arrow-right"),
        ),
        "cards": "".join(render_code_card(c) for c in X.CODE_SAMPLES[:3]),
    }

    skills_cols = "".join(
        '<div class="skill-col"><h3>%s</h3><p class="skill-sub">%s</p><ul>%s</ul></div>' % (
            tier.upper(), sub, "".join("<li>%s</li>" % t for t in items)
        )
        for tier, sub, items in SKILL_TIERS
    )
    skills_html = """<section class="section">
    <div class="container">
      %(head)s
      <div class="skills-grid skills-tiers">%(cols)s</div>
    </div>
  </section>
""" % {
        "head": section_head(
            "03", "Toolbox",
            '<h2 class="section-title" data-i18n="home.skills_title">Skills, by how I use them</h2>',
            '<p class="section-sub">Listed by level of use, not as a wall of keywords</p>',
        ),
        "cols": skills_cols,
    }

    about_html = """<section class="section" style="background:hsl(var(--background-deep) / .4)">
    <div class="container">
      %(head)s
      <p class="lead-in reveal-words" style="margin-bottom:36px">I'm Romain, a developer based in Toulouse. Two years of work-study at Masseka Games Studio on mobile games, a Master's in game development, five game jams &mdash; and a co-op Steam game I'm building solo, with lobbies, netcode and game rules covered by tests.</p>
      <div class="two-col">
        <div class="avatar-row reveal">
          <div class="avatar-box">%(user_icon)s</div>
          <div>
            <p style="font-size:1.02rem;font-weight:600;margin-bottom:10px">Jams taught me to finish something in 48 hours; studio work taught me to maintain someone else's code.</p>
            <p style="color:hsl(var(--muted-foreground));font-size:.92rem">Unity and C# are my daily tools. I have also shipped a React web app and a Python Windows tool, so I am open to any developer role, not only games.</p>
          </div>
        </div>
        <div class="cv-card reveal">
          <div class="cv-icon">%(dl)s</div>
          <div>
            <strong>Curriculum Vit&aelig;</strong>
            <p style="color:hsl(var(--muted-foreground));font-size:.85rem;margin-top:4px">Gameplay Programmer &mdash; Unity / C#<br>PDF &middot; Updated 2026</p>
          </div>
          <a class="btn btn-primary btn-block" href="cv.pdf" download>%(dl)s <span data-i18n="hero.cta_cv">Download CV</span></a>
        </div>
      </div>
    </div>
  </section>
""" % {
        "head": section_head(
            "04", "About",
            '<h2 class="section-title" data-i18n="home.about_title">About Me</h2>',
            "",
            '<a class="section-link" href="about.html"><span data-i18n="home.full_profile">Full profile</span> %s</a>' % icon("arrow-right"),
        ),
        "user_icon": icon("user"),
        "dl": icon("download"),
    }

    cta_html = """<section class="section">
    <div class="container">
      <div class="cta-panel reveal">
        <h2>Hiring a developer<br>who <span class="accent">finishes things?</span></h2>
        <p>Available now for any offer: full-time, fixed-term or freelance, in Toulouse, remote or relocating. I answer within two working days.</p>
        <div class="cta-buttons">
          <a class="btn btn-primary" href="contact.html">%(mail)s Get In Touch %(arrow)s</a>
          <a class="btn btn-outline" href="cv.pdf" download>%(dl)s Download CV</a>
        </div>
      </div>
    </div>
  </section>
""" % {"mail": icon("mail"), "arrow": icon("arrow-right"), "dl": icon("download")}

    body = hero + featured_html + systems_html + skills_html + about_html + cta_html
    write("index.html", page(
        "%s — Unity / C# Developer, Toulouse" % AUTHOR,
        "Romain Pitot, Unity and C# developer in Toulouse. Gameplay systems, co-op multiplayer and tools. Two mobile games shipped on Google Play, a Steam co-op game in progress. Open to work.",
        "home", depth, body, "",
    ))


# --------------------------------------------------------------------------
# Projects listing
# --------------------------------------------------------------------------

def build_projects_listing():
    depth = ""
    filters = ["All", "Work", "Personal", "App", "Game Jam", "School"]
    filter_btns = "".join(
        '<button class="filter-btn%(active)s" type="button" data-filter="%(f)s" data-i18n="%(i18n)s">%(f)s</button>' % {
            "active": " active" if f == "All" else "",
            "f": f,
            "i18n": "projects.filter_all" if f == "All" else "",
        }
        for f in filters
    )
    sort_btns = ('<button class="filter-btn active" type="button" data-sort="latest" data-i18n="projects.sort_latest">Latest</button>'
                 '<button class="filter-btn" type="button" data-sort="alpha" data-i18n="projects.sort_alpha">A&ndash;Z</button>')

    cards = "".join(render_project_card(p, depth) for p in PROJECTS)

    body = """<section class="page-hero container">
    <span class="eyebrow" data-i18n-skip>Portfolio</span>
    <h1 data-i18n="projects.title">Projects</h1>
    <p data-i18n="projects.subtitle">Everything I've shipped &mdash; studio work, school projects, jams and one long-running solo build.</p>
    <div class="page-meta font-mono">13 projects &nbsp;&middot;&nbsp; 2020 &rarr; 2026 &nbsp;&middot;&nbsp; Unity &middot; Unreal &middot; C# &middot; C++ &middot; The Sandbox</div>
  </section>
  <section class="section-tight container" data-filter-bar>
    <div class="filter-bar">
      <div class="filter-group">%(filters)s</div>
      <div class="filter-group"><span class="sort-label" data-i18n-skip>Sort:</span>%(sorts)s</div>
    </div>
    <h2 class="sr-only">All projects</h2>
    <div class="grid grid-3" data-project-grid>%(cards)s</div>
  </section>
""" % {"filters": filter_btns, "sorts": sort_btns, "cards": cards}

    write("projects.html", page(
        "Projects — %s" % AUTHOR,
        "All gameplay projects, tools, and game jams by Romain Pitot: procedural generation, AI, netcode and more.",
        "projects", depth, body, "projects.html",
    ))


# --------------------------------------------------------------------------
# Project detail pages
# --------------------------------------------------------------------------

def render_facts(p):
    if not p.get("facts"):
        return ""
    chips = "".join('<div class="fact"><span class="fact-label">%s</span><span class="fact-value">%s</span></div>' % f for f in p["facts"])
    return '<div class="fact-row">%s</div>' % chips


def render_challenges(p):
    if not p.get("challenges"):
        # Visible only to the owner (open any page once with ?owner=1): a reminder
        # to fill in a real challenge. Nothing is shown to visitors.
        return ('<div class="detail-section owner-todo" data-owner-only hidden><h2 data-i18n-skip>Technical challenge '
                '<span class="owner-tag">TODO (visible only to you)</span></h2>'
                '<div class="challenge"><dl><dt>The problem</dt><dd>What was hard here? One concrete obstacle.</dd>'
                '<dt>What I did</dt><dd>How you solved it, in two sentences. Add it in tools/content_extra.py (ENRICH, "challenges").</dd></dl></div></div>')
    items = "".join(
        '<div class="challenge"><h3>%s</h3><dl><dt>The problem</dt><dd>%s</dd><dt>What I did</dt><dd>%s</dd></dl></div>' % c
        for c in p["challenges"]
    )
    return '<div class="detail-section"><h2 data-i18n-skip>Technical challenge</h2>%s</div>' % items


def render_retro(p):
    r = p.get("retro")
    if not r:
        if p.get("category") != "Game Jam":
            return ""
        return ('<div class="detail-section owner-todo" data-owner-only hidden><h2 data-i18n-skip>Jam retrospective '
                '<span class="owner-tag">TODO (visible only to you)</span></h2>'
                '<p>Constraint, what you built, what you would redo. Add it in tools/content_extra.py (ENRICH, "retro").</p></div>')
    return """<div class="detail-section"><h2 data-i18n-skip>Jam retrospective</h2>
      <div class="retro-grid">
        <div class="retro-card"><h3>The constraint</h3><p>%(constraint)s</p></div>
        <div class="retro-card"><h3>What I built</h3><p>%(built)s</p></div>
        <div class="retro-card"><h3>What I would redo</h3><p>%(redo)s</p></div>
      </div></div>""" % r



def _lum(h, s, l):
    import colorsys
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l / 100.0, s / 100.0)
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def _contrast(c1, c2):
    a, b = _lum(*c1), _lum(*c2)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def _readable(c, bgs, dark, target=5.2):
    target = target if dark else target + 2.3  # light pages: margin for the fade-in blend
    """Move the lightness of c until it reads on every background in bgs."""
    h, sat, l = c
    step = 1 if dark else -1
    while l < 98 and l > 2 and min(_contrast((h, sat, l), b) for b in bgs) < target:
        l += step
    return (h, sat, l)


def theme_tokens(t):
    """Turn a compact theme (bg/primary/accent + mode) into the full token set.
    Foreground/background pairs are chosen so text stays above WCAG AA."""
    h, sat, l = t["bg"]
    dark = t["mode"] == "dark"

    def hsl(x):
        return "%d %d%% %d%%" % x

    def on(c):
        return hsl((c[0], 20, 8)) if c[2] >= 46 else hsl((c[0], 30, 96))

    if dark:
        fg, mfg = (h, 25, 95), (h, 18, 72)
        card, sec, mut, bdr, deep = (h, sat, l + 4), (h, sat, l + 9), (h, sat, l + 7), (h, sat - 5, l + 14), (h, sat + 4, max(l - 4, 3))
    else:
        fg, mfg = (h, 30, 12), (h, 18, 28)
        card, sec, mut, bdr, deep = (h, sat, l + 4), (h, sat - 4, l - 6), (h, sat - 4, l - 5), (h, sat - 6, l - 16), (h, sat, l - 5)
    # primary/accent are used as text colour too: push them until they pass AA
    # on the page, card and secondary backgrounds.
    bgs = [t["bg"], card, sec, mut, deep]
    p = _readable(t["primary"], bgs, dark)
    a = _readable(t["accent"], bgs, dark)
    mfg = _readable(mfg, bgs, dark, 5.5)
    tokens = {
        "background": hsl(t["bg"]), "background-deep": hsl(deep), "foreground": hsl(fg),
        "card": hsl(card), "card-foreground": hsl(fg), "primary": hsl(p), "primary-foreground": on(p),
        "secondary": hsl(sec), "secondary-foreground": hsl(mfg), "muted": hsl(mut), "muted-foreground": hsl(mfg),
        "accent": hsl(a), "accent-foreground": on(a), "border": hsl(bdr),
    }
    return "".join("--%s:%s;" % kv for kv in tokens.items())


def theme_body_attrs(p):
    t = X.THEMES.get(p["id"])
    if not t:
        return ""
    return ' class="themed %s font-%s fx-%s" style="%s"' % (t["mode"], t["font"], t["fx"] or "none", theme_tokens(t))


def build_project_detail(p):
    depth = "../"
    others = [o for o in PROJECTS if o["id"] != p["id"]][:3]

    idx = PROJECTS.index(p)
    prev_p = PROJECTS[idx - 1] if idx > 0 else PROJECTS[-1]
    next_p = PROJECTS[idx + 1] if idx < len(PROJECTS) - 1 else PROJECTS[0]
    pager = """<nav class="project-pager">
      <a class="pager-link pager-prev" href="%(prev_id)s.html">
        <span class="pager-dir">%(left)s Previous</span>
        <span class="pager-title">%(prev_title)s</span>
      </a>
      <a class="pager-link pager-next" href="%(next_id)s.html">
        <span class="pager-dir">Next %(right)s</span>
        <span class="pager-title">%(next_title)s</span>
      </a>
    </nav>""" % {
        "prev_id": prev_p["id"], "prev_title": prev_p["title"],
        "next_id": next_p["id"], "next_title": next_p["title"],
        "left": icon("arrow-left"), "right": icon("arrow-right"),
    }

    meta_items = [
        ("Category", p["category"]), ("Engine", p["engine"]), ("Platform", p["platform"]),
        ("Role", p["role"]), ("Duration", p["duration"]),
        ("Team", "Solo" if p["teamSize"] == 1 else "%d devs" % p["teamSize"]),
        ("Status", p["status"]), ("Year", str(p["year"])),
    ]
    meta_html = "".join(
        '<div><span class="detail-meta-label">%s</span><span class="detail-meta-value">%s</span></div>' % m
        for m in meta_items
    )

    body = """<section class="container" style="padding-top:32px">
    <div class="breadcrumb"><a href="../projects.html">&larr; Projects</a> / %(title)s</div>
    <div class="cover-tags" style="position:static;margin-bottom:16px">%(badges)s</div>
    %(kicker)s
    <h1 style="font-size:clamp(1.8rem,4vw,2.6rem);margin-bottom:28px">%(title)s</h1>

    <div class="detail-cover %(coverclass)s">%(cover_media)s</div>

    <div class="detail-meta-grid">%(meta)s</div>

    %(facts)s
    <div class="detail-section">
      <h2 data-i18n-skip>Overview</h2>
      <p>%(description)s</p>
      %(note)s
      %(gallery)s
    </div>

    %(challenges)s
    %(retro)s

    <div class="detail-section">
      <h2 data-i18n-skip>Highlights</h2>
      <ul>%(highlights)s</ul>
    </div>

    <div class="detail-section">
      <h2 data-i18n-skip>Key Systems</h2>
      <div class="tag-row">%(keysystems)s</div>
    </div>

    <div class="detail-section">
      <h2 data-i18n-skip>Technologies</h2>
      <div class="tag-row">%(tech)s</div>
    </div>

    <div class="detail-section">
      <h2 data-i18n-skip>Links</h2>
      <div class="detail-links">%(links)s</div>
    </div>
  </section>

  <section class="container">%(pager)s</section>

  <section class="section container">
    <div class="section-head"><h2 class="section-title" data-i18n-skip>Other projects</h2></div>
    <div class="other-projects">%(others)s</div>
  </section>
""" % {
        "title": p["title"],
        "kicker": ('<p class="theme-kicker font-mono">%s</p>' % X.THEMES[p["id"]]["kicker"]) if p["id"] in X.THEMES else "",
        "badges": corner_badges(p["status"], p["tags"]),
        "coverclass": cover_class(p["category"]),
        "cover_media": '<img class="cover-img" src="%sassets/img/projects/%s" alt="%s cover">' % (
            depth, project_cover_src(p), p["title"]),
        "meta": meta_html,
        "description": p["description"],
        "facts": render_facts(p),
        "note": ('<p class="detail-note">%s</p>' % p["note"]) if p.get("note") else "",
        "challenges": render_challenges(p),
        "retro": render_retro(p),
        "gallery": (
            '<div class="detail-gallery">%s</div>' % "".join(
                '<img src="%sassets/img/projects/%s" alt="%s screenshot" loading="lazy">' % (depth, g, p["title"])
                for g in p["gallery"]
            )
            if p.get("gallery") else ""
        ),
        "highlights": "".join("<li>%s</li>" % h for h in p["highlights"]),
        "keysystems": "".join('<span class="tag">%s</span>' % k for k in p["keySystems"]),
        "tech": all_tech_tags(p["technologies"]),
        "links": project_link_buttons(p["links"], "btn-sm") or '<span style="color:hsl(var(--muted-foreground));font-size:.85rem">No public build or repository &mdash; this one is private or no longer online. I am happy to walk through it in an interview.</span>',
        "others": "".join(render_project_card(o, depth) for o in others),
        "pager": pager,
    }

    write("projects/%s.html" % p["id"], page(
        "%s — %s" % (p["title"], AUTHOR),
        p["shortDesc"],
        "projects", depth, body, "projects/%s.html" % p["id"],
        body_attrs=theme_body_attrs(p),
    ))


# --------------------------------------------------------------------------
# Code page
# --------------------------------------------------------------------------

def build_code():
    depth = ""
    body = """<section class="page-hero container">
    <span class="eyebrow" data-i18n-skip>Code</span>
    <h1 data-i18n="systems.title">Code you can read</h1>
    <p data-i18n="systems.subtitle">Real extracts from my repositories, trimmed, with the reasoning behind them</p>
    <div class="page-meta font-mono">most of my game repos are private &middot; the code below comes straight from them</div>
  </section>
  <section class="section-tight container code-list">%(blocks)s</section>
  <section class="container"><p class="code-foot">Public repositories: <a href="https://github.com/RomainPitot/lol-climb-tracker" target="_blank" rel="noopener noreferrer">lol-climb-tracker</a> (React) and <a href="https://github.com/RomainPitot/GameDetectorLol" target="_blank" rel="noopener noreferrer">GameDetectorLol</a> (Python). I can share access to the private ones during a hiring process.</p></section>
""" % {"blocks": "".join(render_code_block(c) for c in X.CODE_SAMPLES)}

    write("code.html", page(
        "Code samples — %s" % AUTHOR,
        "Real C# extracts from Global Invasion, a Steam co-op game in Unity: a tested mission state machine, a seeded nest draw and a local swarm simulation.",
        "code", depth, body, "code.html",
    ))

    # Old URL: keep it alive with a redirect instead of a 404.
    write("systems.html", """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Moved — Romain Pitot</title>
<link rel="canonical" href="%(site)s/code.html">
<meta http-equiv="refresh" content="0; url=code.html">
<meta name="robots" content="noindex">
</head><body><p>This page moved to <a href="code.html">code.html</a>.</p></body></html>
""" % {"site": SITE_URL})


# --------------------------------------------------------------------------
# About page
# --------------------------------------------------------------------------

def build_about():
    depth = ""
    edu_html = "".join(
        '<div style="margin-bottom:16px"><strong>%s</strong><br>'
        '<span style="color:hsl(var(--muted-foreground));font-size:.9rem">%s &middot; %s</span></div>' % e
        for e in EDUCATION
    )
    tiers = "".join(
        '<div class="skill-col"><h3>%s</h3><p class="skill-sub">%s</p><ul>%s</ul></div>' % (
            t.upper(), sub, "".join("<li>%s</li>" % i for i in items))
        for t, sub, items in SKILL_TIERS
    )

    body = """<section class="page-hero container">
    <span class="eyebrow" data-i18n-skip>About</span>
    <h1 data-i18n="about.title">About Me</h1>
    <p data-i18n="about.subtitle">Unity / C# developer</p>
    <div class="page-meta font-mono">Toulouse, FR &nbsp;&middot;&nbsp; MSc Game Development &nbsp;&middot;&nbsp; 2 years at Masseka Games Studio</div>
  </section>

  <section class="section-tight container">
    <div class="two-col">
      <div class="reveal about-text">
        <p class="about-lead">I'm Romain. I write Unity and C#, and I like turning a game rule into code that can be tested.</p>
        <p>I spent two years in work-study at Masseka Games Studio in Toulouse, mostly on mobile games: migrating <em>Kissoro</em> from Unity 2018 to 2022, fixing bugs and making the UI adapt to different screens on <em>Vaudoo</em> (now at 1k+ downloads on Google Play), reviving an abandoned prototype on my own, and adapting a game to The Sandbox's constraints.</p>
        <p>Outside the studio I took part in five game jams, and I am building <em>Global Invasion</em> alone: a Steam co-op game with lobbies, Netcode for GameObjects and its rules covered by unit tests. I also made a React web app (CLIMB.EUW) and a Python Windows tool that work together, which is why I am open to any developer role and not only games.</p>
        <h2 class="about-h">How I work</h2>
        <ul class="about-list">
          <li>Game rules in plain C# with time and randomness passed in, so they can be tested without launching the game. Network and engine classes stay thin.</li>
          <li>I use AI assistants (Claude Code) as a pair programmer. I decide the design, review what comes back and test it. Where a project relies on AI tools, as in On Air, its page says so.</li>
          <li>Small commits, one branch per feature, and a written plan before a change.</li>
        </ul>
        <p class="font-mono about-based" data-i18n="about.based">Based in France &mdash; Open to remote &amp; relocation</p>

        <h2 class="about-h" data-i18n="about.education_title">Education</h2>
        %(edu)s
      </div>

      <div class="cv-card reveal">
        <div class="cv-icon">%(dl)s</div>
        <div>
          <strong>Curriculum Vit&aelig;</strong>
          <p style="color:hsl(var(--muted-foreground));font-size:.85rem;margin-top:4px">Unity / C# developer<br>PDF &middot; Updated 2026</p>
        </div>
        <a class="btn btn-primary btn-block" href="cv.pdf" download>%(dl)s <span data-i18n="hero.cta_cv">Download CV</span></a>
        <div style="border-top:1px solid hsl(var(--border));margin-top:6px;padding-top:16px">
          <span class="availability"><span class="dot"></span> <span data-i18n="contact.availability">Open to work &mdash; available now, any offer</span></span>
        </div>
      </div>
    </div>
  </section>

  <section class="section container" style="border-top:1px solid hsl(var(--border)/.5)">
    <h2 class="about-h" data-i18n="about.skills_title">Skills, by how I use them</h2>
    <div class="skills-grid skills-tiers" style="margin-bottom:40px">%(tiers)s</div>

    <h2 class="about-h" data-i18n="about.languages_title">Languages</h2>
    <div class="tag-row">
      <span class="tag">French &middot; Native</span>
      <span class="tag">English &middot; Professional</span>
    </div>
  </section>
""" % {"edu": edu_html, "dl": icon("download"), "tiers": tiers}

    write("about.html", page(
        "About — %s" % AUTHOR,
        "About Romain Pitot: Unity and C# developer in Toulouse, MSc Game Development, two years in a game studio, open to any developer role.",
        "about", depth, body, "about.html",
    ))


# --------------------------------------------------------------------------
# Contact page
# --------------------------------------------------------------------------

def build_contact():
    depth = ""
    body = """<section class="page-hero container">
    <span class="eyebrow" data-i18n-skip>Contact</span>
    <h1 data-i18n="contact.title">Get In Touch</h1>
    <p data-i18n="contact.subtitle">Hiring, freelance or just curious about a project &mdash; I reply within two working days</p>
    <div style="margin-top:18px">
      <span class="availability"><span class="dot"></span> <span data-i18n="contact.availability">Open to work &mdash; available now, any offer</span></span>
    </div>
  </section>

  <section class="section-tight container">
    <div class="contact-grid">
      <div class="form-card reveal">
        <h2 data-i18n="contact.form_title">Send a message</h2>
        <form data-contact-form action="%(formspree)s" method="POST">
          <div class="form-row">
            <div class="field"><label for="f-name" data-i18n-skip>Name</label><input id="f-name" type="text" name="name" autocomplete="name" required></div>
            <div class="field"><label for="f-email" data-i18n-skip>Email</label><input id="f-email" type="email" name="email" autocomplete="email" required></div>
          </div>
          <div class="field"><label for="f-subject" data-i18n-skip>Subject (company, role&hellip;)</label><input id="f-subject" type="text" name="subject"></div>
          <div class="field"><label for="f-message" data-i18n-skip>Message</label><textarea id="f-message" name="message" required minlength="10"></textarea></div>
          <input type="hidden" name="_subject" value="New message from romainpitot.github.io">
          <div class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
          <button class="btn btn-primary" type="submit">%(send_icon)s <span data-i18n="contact.send">Send Message</span></button>
          <p data-form-status class="font-mono" role="status" aria-live="polite" style="font-size:.82rem;margin-top:12px" hidden></p>
        </form>
      </div>

      <div class="reveal">
        <div class="connect-card">
          <h2 data-i18n="contact.connect">Connect</h2>
          <div class="connect-item">
            <span class="connect-icon">%(mail_icon)s</span>
            <div><div class="connect-label">Email</div>%(email_link)s</div>
          </div>
          <div class="connect-item">
            <span class="connect-icon">%(li_icon)s</span>
            <div><div class="connect-label">LinkedIn</div><a class="connect-value" href="%(linkedin)s" target="_blank" rel="noopener noreferrer">linkedin.com/in/romain-pitot</a></div>
          </div>
          <div class="connect-item">
            <span class="connect-icon">%(gh_icon)s</span>
            <div><div class="connect-label">GitHub</div><a class="connect-value" href="%(github)s" target="_blank" rel="noopener noreferrer">github.com/romainpitot</a></div>
          </div>
        </div>

        <div class="connect-card">
          <h2>Good to know</h2>
          <ul class="know-list">
            <li><strong>Availability:</strong> immediately</li>
            <li><strong>Contract:</strong> full-time, fixed-term or freelance</li>
            <li><strong>Location:</strong> Toulouse, remote or relocation</li>
            <li><strong>Languages:</strong> French (native), English (professional)</li>
            <li><strong>Reply time:</strong> within two working days</li>
          </ul>
        </div>

        <div class="connect-card">
          <h2 data-i18n="contact.resume">Resume</h2>
          <p style="color:hsl(var(--muted-foreground));font-size:.85rem;margin-bottom:14px">PDF &mdash; Updated 2026</p>
          <a class="btn btn-primary btn-block" href="cv.pdf" download>%(dl_icon)s <span data-i18n="hero.cta_cv">Download CV</span></a>
        </div>
      </div>
    </div>
  </section>
""" % {
        "send_icon": icon("send"), "mail_icon": icon("mail"), "li_icon": icon("linkedin"), "gh_icon": icon("github"),
        "dl_icon": icon("download"), "email_link": email_link("connect-value"), "linkedin": REAL_LINKEDIN,
        "github": REAL_GITHUB, "formspree": FORMSPREE_ENDPOINT,
    }

    write("contact.html", page(
        "Contact — %s" % AUTHOR,
        "Contact Romain Pitot, Unity and C# developer in Toulouse: available now for full-time, fixed-term or freelance work, in person, remote or relocating.",
        "contact", depth, body, "contact.html",
    ))


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def build_robots_and_sitemap():
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE_URL)

    paths = ["", "projects.html", "code.html", "about.html", "contact.html"]
    paths += ["projects/%s.html" % p["id"] for p in PROJECTS]
    urls = "".join(
        "  <url><loc>%s/%s</loc></url>\n" % (SITE_URL, p) for p in paths
    )
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + urls + "</urlset>\n")
    write("sitemap.xml", sitemap)


def build_404():
    depth = ""
    body = """<section class="page-hero container error-page" style="text-align:center;padding:110px 24px 120px">
    <div class="error-code font-mono" aria-hidden="true">404</div>
    <h1>NullReferenceException</h1>
    <p style="margin:14px auto 8px;max-width:520px">Object reference not set to an instance of a page. This route doesn't exist &mdash; it may have moved, or the link is out of date.</p>
    <pre class="error-trace font-mono" aria-hidden="true">   at Portfolio.Router.Resolve(string path)
   at Portfolio.Program.Main()</pre>
    <div class="cta-buttons" style="margin-top:30px">
      <a class="btn btn-primary" href="index.html">%(arrow)s Back to home</a>
      <a class="btn btn-outline" href="projects.html">Browse projects</a>
    </div>
  </section>
""" % {"arrow": icon("arrow-right")}
    write("404.html", page(
        "Page not found — %s" % AUTHOR,
        "This page doesn't exist.",
        "", depth, body,
    ))


def main():
    build_home()
    build_projects_listing()
    for p in PROJECTS:
        build_project_detail(p)
    build_code()
    build_about()
    build_contact()
    build_404()
    build_robots_and_sitemap()


if __name__ == "__main__":
    main()
