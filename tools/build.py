# -*- coding: utf-8 -*-
"""
Static site generator for the Pitot Engine portfolio.

This is a *build-time* convenience script (run locally with `python tools/build.py`)
that outputs plain, dependency-free HTML files. Nothing about the deployed site
requires Python or Node — GitHub Actions just uploads the generated files as-is.

Re-run this script after editing PROJECTS / SYSTEMS / SKILLS below, then commit
the regenerated HTML.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_NAME = "Pitot Engine"
AUTHOR = "Romain Pitot"
YEAR = "2026"

REAL_GITHUB = "https://github.com/romainpitot"
REAL_LINKEDIN = "https://linkedin.com/in/romain-pitot"
CONTACT_EMAIL = "romainpitot.dev@gmail.com"
FORMSPREE_ENDPOINT = "https://formspree.io/f/mkjnwagj"

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
}


def icon(name, cls="icon"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, ICONS[name])


# --------------------------------------------------------------------------
# Content data (transcribed from the live Base44 build — see /tools/README
# in this folder for provenance notes).
# --------------------------------------------------------------------------

PROJECTS = [
    {
        "id": "echoes-of-the-rift", "title": "Echoes of the Rift",
        "shortDesc": "Top-down action RPG with procedurally generated dungeons and a modular ability system.",
        "description": "A top-down action RPG built during a 72-hour game jam. Features a fully modular ability system allowing runtime combination of effects, procedurally generated dungeons using BSP partitioning, and a custom AI state machine for enemy behaviors.",
        "category": "Game Jam", "engine": "Unity", "platform": "PC", "role": "Gameplay Programmer",
        "status": "Game Jam", "year": 2024, "duration": "72 hours", "teamSize": 3,
        "technologies": ["C#", "Unity", "Procedural Generation", "AI", "State Machine"],
        "tags": ["Game Jam", "Procedural", "AI"], "featured": True,
        "links": {"github": "https://github.com", "itch": "https://itch.io"},
        "highlights": ["BSP dungeon generation", "Modular ability system", "Custom enemy AI"],
        "keySystems": ["Dungeon Generator", "Ability Compositor", "Enemy State Machine", "Loot Tables"],
    },
    {
        "id": "nexus-tower-defense", "title": "Nexus Tower Defense",
        "shortDesc": "Strategic tower defense with advanced path-finding, tower upgrade trees, and wave scripting.",
        "description": "A feature-complete tower defense game with a custom wave editor, dynamic A* pathfinding that updates in real time as towers are placed, a full tower upgrade tree system, and a modular targeting strategy pattern.",
        "category": "Prototype", "engine": "Unity", "platform": "PC / WebGL", "role": "Solo Developer",
        "status": "Prototype", "year": 2024, "duration": "3 months", "teamSize": 1,
        "technologies": ["C#", "Unity", "A*", "Design Patterns", "WebGL"],
        "tags": ["Tools", "AI", "Prototype"], "featured": True,
        "links": {"github": "https://github.com", "demo": "https://demo.io"},
        "highlights": ["Real-time A* pathfinding", "Tower upgrade tree", "Wave scripting editor"],
        "keySystems": ["Pathfinding Engine", "Wave Manager", "Tower Registry", "UI State Machine"],
    },
    {
        "id": "multiplayer-arena", "title": "Arena Sync",
        "shortDesc": "Fast-paced multiplayer arena shooter with client-side prediction and server reconciliation.",
        "description": "A real-time multiplayer arena prototype exploring netcode fundamentals. Implements client-side prediction, server authority, and lag compensation. Built with Unity Netcode for GameObjects and a custom rollback buffer.",
        "category": "Prototype", "engine": "Unity", "platform": "PC", "role": "Netcode Programmer",
        "status": "Prototype", "year": 2023, "duration": "2 months", "teamSize": 2,
        "technologies": ["C#", "Unity", "Multiplayer", "Netcode", "NGO"],
        "tags": ["Multiplayer", "Prototype"], "featured": True,
        "links": {"github": "https://github.com"},
        "highlights": ["Client-side prediction", "Server reconciliation", "Lag compensation"],
        "keySystems": ["Rollback Buffer", "Input Serializer", "State Snapshot System", "Lobby Manager"],
    },
    {
        "id": "inventory-system-tool", "title": "Modular Inventory System",
        "shortDesc": "Reusable data-driven inventory framework with drag-and-drop, item stacking, and serialization.",
        "description": "A production-ready Unity inventory package built with clean architecture principles. Features a fully data-driven item database using ScriptableObjects, runtime drag-and-drop with grid snapping, item stacking and splitting, and JSON serialization for save/load.",
        "category": "Tool", "engine": "Unity", "platform": "Unity Package", "role": "Tool Developer",
        "status": "Released", "year": 2024, "duration": "6 weeks", "teamSize": 1,
        "technologies": ["C#", "Unity", "ScriptableObjects", "UGUI", "JSON"],
        "tags": ["Tools", "Unity"], "featured": False,
        "links": {"github": "https://github.com"},
        "highlights": ["Data-driven ScriptableObject items", "Grid-based drag and drop", "JSON save/load serialization"],
        "keySystems": ["Item Registry", "Grid Manager", "Serialization Layer", "UI Event System"],
    },
    {
        "id": "velvet-depths", "title": "Velvet Depths",
        "shortDesc": "Narrative horror platformer with dynamic sound-reactive environments and branching story.",
        "description": "A narrative-driven horror platformer created for the Global Game Jam 2024. The environment reacts dynamically to ambient audio using FFT analysis. Features a branching dialogue system and custom shader effects for the horror atmosphere.",
        "category": "Game Jam", "engine": "Unity", "platform": "PC", "role": "Lead Programmer",
        "status": "Game Jam", "year": 2024, "duration": "48 hours", "teamSize": 4,
        "technologies": ["C#", "Unity", "Shaders", "FMOD", "Dialogue System"],
        "tags": ["Game Jam", "Shaders"], "featured": False,
        "links": {"itch": "https://itch.io"},
        "highlights": ["FFT audio-reactive level", "Custom horror shaders", "Branching narrative system"],
        "keySystems": ["Audio Analyzer", "Dialogue Tree", "Shader Controller", "Event Bus"],
    },
    {
        "id": "proc-world-gen", "title": "ProceduralWorld Kit",
        "shortDesc": "Runtime terrain and biome generation toolkit using noise layers, erosion simulation, and LOD.",
        "description": "A Unity editor toolkit for procedurally generating terrain and biomes at runtime. Uses layered Perlin/Simplex noise for heightmaps, a custom hydraulic erosion simulation, biome blending based on temperature/humidity gradients, and LOD mesh generation.",
        "category": "Tool", "engine": "Unity", "platform": "Unity Package", "role": "Systems Programmer",
        "status": "WIP", "year": 2025, "duration": "Ongoing", "teamSize": 1,
        "technologies": ["C#", "Unity", "Compute Shaders", "Procedural Generation", "LOD"],
        "tags": ["Procedural", "Tools"], "featured": False,
        "links": {"github": "https://github.com"},
        "highlights": ["GPU-accelerated noise via Compute Shaders", "Hydraulic erosion simulation", "Biome blending system"],
        "keySystems": ["Noise Compositor", "Erosion Simulator", "Biome Atlas", "LOD Mesh Builder"],
    },
]

SYSTEMS = [
    {
        "id": "inventory-system", "title": "Modular Inventory System", "subtitle": "Data-driven item management framework",
        "category": "Tools", "icon": "package",
        "description": "A production-ready inventory system designed with clean architecture principles. Uses ScriptableObject-based item definitions, a grid-based slot manager, and a full serialization pipeline for save/load.",
        "architecture": "The system follows a Model-View-Controller pattern. The ItemRegistry holds all item definitions as ScriptableObjects. The InventoryModel manages slot state and emits events. The InventoryView listens to events and updates the UI. A SerializationLayer converts the model to/from JSON for persistence.",
        "technologies": ["C#", "Unity", "ScriptableObjects", "UGUI", "JSON", "Events"],
        "challenges": ["Implementing grid-based drag-and-drop with precise collision detection", "Designing a generic item property system without per-type code", "Ensuring save/load integrity with item versioning"],
        "solutions": ["Custom RectTransform overlap detection with slot snapping", "Property bags using ScriptableObject composition", "Schema versioning with migration callbacks"],
        "stats": [("Lines", "~1,200"), ("Tests", "18 unit tests"), ("Reusability", "Drop-in package")],
        "color": "accent", "caption": "MVC · ScriptableObjects",
    },
    {
        "id": "procedural-dungeon", "title": "BSP Dungeon Generator", "subtitle": "Binary Space Partitioning dungeon layout algorithm",
        "category": "Procedural", "icon": "map",
        "description": "A runtime dungeon generation system using Binary Space Partitioning. Produces varied, traversable dungeons with configurable density, guaranteed connectivity, and room-type weighting for boss/treasure rooms.",
        "architecture": "BSP tree recursively splits space into leaf nodes representing rooms. A corridor-carving pass connects sibling nodes. Room metadata is then assigned probabilistically based on tree depth. The generator outputs a TileMap-compatible grid that Unity's Tilemap API populates.",
        "technologies": ["C#", "Unity", "Tilemap API", "Procedural Generation", "Graph Theory"],
        "challenges": ["Guaranteeing all rooms are reachable without backtracking", "Balancing randomness vs. playable level design", "Integrating enemy spawning with room context"],
        "solutions": ["Minimum spanning tree pass over room graph ensures connectivity", "Configurable depth and split-ratio constraints keep layouts playable", "Room type tagging drives spawn tables at level load time"],
        "stats": [("Lines", "~800"), ("Performance", "<2ms per gen"), ("Maps", "∞ unique layouts")],
        "color": "violet", "caption": "BSP · Graph traversal",
    },
    {
        "id": "save-system", "title": "Universal Save System", "subtitle": "Flexible, type-safe game state serialization",
        "category": "Tools", "icon": "save",
        "description": "A flexible save system supporting multiple save slots, auto-save, and type-safe serialization. Components register themselves as saveable via an interface, decoupling persistence logic from gameplay code.",
        "architecture": "SaveableObjects implement ISaveable and register with the SaveManager on Awake. On save, the manager collects JSON blobs from all registered objects and writes them to an encrypted file per slot. On load, each object receives its own data blob and deserializes independently.",
        "technologies": ["C#", "Unity", "JSON.NET", "AES Encryption", "Interfaces"],
        "challenges": ["Avoiding tight coupling between save logic and game objects", "Handling save data migration between game versions", "Performance on large scene counts"],
        "solutions": ["ISaveable interface + SceneContext dependency injection", "Version field + migration strategy pattern", "Async write pipeline with background thread offload"],
        "stats": [("Lines", "~600"), ("Slots", "Unlimited"), ("Overhead", "<0.5ms")],
        "color": "indigo", "caption": "AES · JSON.NET",
    },
    {
        "id": "enemy-ai", "title": "Hierarchical Enemy AI", "subtitle": "Layered behavior tree with utility scoring",
        "category": "AI", "icon": "cpu",
        "description": "A hierarchical AI system combining behavior trees for decision logic with utility scoring for target prioritization. Enemies exhibit patrol, detection, combat, flanking, and retreat behaviors that adapt based on health and squad context.",
        "architecture": "A lightweight behavior tree evaluates each tick: Selector/Sequence/Leaf nodes compose complex behavior. A utility layer weights candidate actions (attack, flank, retreat, call-for-help) using normalized sensor inputs. A steering layer handles movement using Unity's NavMesh with obstacle avoidance layering.",
        "technologies": ["C#", "Unity", "NavMesh", "Behavior Trees", "Utility AI"],
        "challenges": ["Preventing repetitive predictable enemy patterns", "Coordinating group behavior without expensive global queries", "Tuning utility weights without hand-tweaking every enemy type"],
        "solutions": ["Noise-injected utility scores add controlled unpredictability", "Squad blackboard shared via object reference, no global lookup", "Parameterized utility curves on ScriptableObject profiles"],
        "stats": [("Lines", "~2,000"), ("Enemies", "50+ simultaneous"), ("Cost", "<0.8ms at 30 enemies")],
        "color": "violet", "caption": "BT · NavMesh · Utility",
    },
    {
        "id": "ability-system", "title": "Modular Ability System", "subtitle": "Runtime-composable gameplay ability framework",
        "category": "Gameplay", "icon": "zap",
        "description": "A data-driven ability system where abilities are composed from atomic Effect modules at runtime. Supports cooldowns, resource costs, targeting modes, visual feedback hooks, and runtime upgrades without code changes.",
        "architecture": "AbilityDefinition ScriptableObjects hold arrays of AbilityEffect assets. At cast time, a composite executor chains effects in sequence/parallel. Targeting modes (projectile, AOE, raycast, melee) are swappable strategy objects. A visual feedback system subscribes to ability lifecycle events to drive VFX and audio.",
        "technologies": ["C#", "Unity", "ScriptableObjects", "Composition Pattern", "VFX Graph"],
        "challenges": ["Designing effects general enough to compose meaningfully", "Handling targeting across different camera perspectives", "Keeping ability logic testable without a running game"],
        "solutions": ["Atomic effects: Damage, Move, Spawn, Apply Status, Trigger Event", "Camera-agnostic targeting resolvers injected at runtime", "Effect units are pure C# classes, tested independently from MonoBehaviour"],
        "stats": [("Lines", "~1,500"), ("Abilities", "Infinite by composition"), ("Effects", "12 atomic types")],
        "color": "primary", "caption": "Composition · ScriptableObj",
    },
    {
        "id": "netcode-layer", "title": "Netcode Prediction Layer", "subtitle": "Client-side prediction with server reconciliation",
        "category": "Multiplayer", "icon": "wifi",
        "description": "A netcode abstraction layer implementing client-side prediction, authoritative server state, and rollback/reconciliation. Designed as a wrapper around Unity Netcode for GameObjects to simplify deterministic gameplay code.",
        "architecture": "Each frame, the client records input into a circular buffer and simulates locally. The server processes inputs authoritatively and broadcasts state snapshots. The client compares its predicted state against server snapshots and rolls back + re-simulates if divergence exceeds a threshold.",
        "technologies": ["C#", "Unity", "NGO", "Multiplayer", "Ring Buffer", "Rollback"],
        "challenges": ["Achieving visual smoothness during reconciliation corrections", "Keeping the rollback buffer memory-bounded", "Handling physics interactions deterministically"],
        "solutions": ["Visual interpolation layer decoupled from simulation layer", "Fixed-size ring buffer with configurable history depth", "Physics inputs serialized and replayed, not physics state"],
        "stats": [("Lines", "~1,800"), ("Latency masked", "Up to 150ms"), ("Players tested", "2-8")],
        "color": "green", "caption": "Prediction · Rollback · NGO",
    },
]

SKILLS = [
    ("Engine", ["Unity", "WebGL", "Unity DOTS (learning)", "Unreal Engine (secondary)"]),
    ("Languages", ["C#", "HLSL / Shader Lab", "Python (tools)", "C++ (secondary)"]),
    ("Systems", ["Gameplay Systems", "AI / Behavior Trees", "Procedural Generation"]),
    ("Networking", ["Netcode for GameObjects", "Client Prediction", "State Sync"]),
    ("Tools & Workflow", ["Git / GitHub", "ScriptableObjects", "Custom Editor Tools"]),
    ("Patterns", ["MVC / MVVM", "Observer / Event Bus", "Strategy / Factory"]),
]

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
    "WIP": "",
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
    }.get(category, "cover-prototype")


def project_link_buttons(links, size_cls="btn-sm"):
    out = []
    if links.get("github"):
        out.append('<a class="btn btn-outline %s" href="%s" target="_blank" rel="noreferrer">%s GitHub</a>' % (size_cls, links["github"], icon("github")))
    if links.get("itch"):
        out.append('<a class="btn btn-outline %s" href="%s" target="_blank" rel="noreferrer">%s Play on itch.io</a>' % (size_cls, links["itch"], icon("play")))
    if links.get("demo"):
        out.append('<a class="btn btn-outline %s" href="%s" target="_blank" rel="noreferrer">%s Live Demo</a>' % (size_cls, links["demo"], icon("external-link")))
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
  <meta property="og:title" content="%(title)s">
  <meta property="og:description" content="%(description)s">
  <meta property="og:url" content="%(canonical)s">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="%(title)s">
  <meta name="twitter:description" content="%(description)s">
  <link rel="icon" href="%(depth)sassets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="%(depth)sassets/css/style.css">
""" % {"title": title, "description": description, "depth": depth, "canonical": canonical}


def header_html(active, depth):
    nav_items = [
        ("home", "nav.home", "Home", depth + "index.html"),
        ("projects", "nav.projects", "Projects", depth + "projects.html"),
        ("systems", "nav.systems", "Systems", depth + "systems.html"),
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
      <nav class="main-nav" id="main-nav">%(links)s</nav>
      <div class="nav-right">
        <button class="lang-toggle" type="button" aria-label="Switch language">FR</button>
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
    return """<footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-brand">%(code_icon)s romain.pitot &mdash; <span data-i18n="footer.role">gameplay programmer</span></div>
      <div class="footer-social">
        <a href="mailto:%(email)s" aria-label="Email">%(mail_icon)s</a>
        <a href="%(linkedin)s" target="_blank" rel="noreferrer" aria-label="LinkedIn">%(linkedin_icon)s</a>
        <a href="%(github)s" target="_blank" rel="noreferrer" aria-label="GitHub">%(github_icon)s</a>
      </div>
      <div class="footer-copy">&copy; %(year)s Romain Pitot</div>
    </div>
  </footer>
""" % {
        "code_icon": icon("code"),
        "email": CONTACT_EMAIL,
        "linkedin": REAL_LINKEDIN,
        "github": REAL_GITHUB,
        "mail_icon": icon("mail"),
        "linkedin_icon": icon("linkedin"),
        "github_icon": icon("github"),
        "year": YEAR,
    }


def person_jsonld():
    return """<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "%(author)s",
    "jobTitle": "Gameplay Programmer",
    "url": "%(site)s/",
    "sameAs": ["%(github)s", "%(linkedin)s"],
    "knowsAbout": ["Unity", "C#", "Gameplay Programming", "Procedural Generation", "Game AI", "Multiplayer Netcode"]
  }
  </script>
""" % {"author": AUTHOR, "site": SITE_URL, "github": REAL_GITHUB, "linkedin": REAL_LINKEDIN}


def page(title, description, active, depth, body, canonical_path=""):
    return """<!DOCTYPE html>
<html lang="en">
<head>
  %(head)s%(jsonld)s</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  %(header)s
  <main id="main">
  %(body)s
  </main>
  %(footer)s
  <script src="%(depth)sassets/js/i18n.js"></script>
  <script src="%(depth)sassets/js/main.js"></script>
</body>
</html>
""" % {
        "head": html_head(title, description, depth, canonical_path),
        "jsonld": person_jsonld(),
        "header": header_html(active, depth),
        "body": body,
        "footer": footer_html(depth),
        "depth": depth,
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

def system_visual(sid):
    if sid == "inventory-system":
        cells = [1, 1, 1, 0, 1, 0, 0, 0]
        tones = ["hsl(var(--primary) / .5)", "hsl(var(--accent) / .6)", "hsl(var(--violet) / .5)", "hsl(var(--secondary))"]
        slots = "".join(
            '<div class="viz-slot" style="background:%s"></div>' % (tones[i % len(tones)] if c else "")
            for i, c in enumerate(cells)
        )
        return '<div class="viz-grid">%s</div>' % slots
    if sid == "procedural-dungeon":
        heights = [34, 44, 26, 38]
        rooms = "".join('<div class="viz-room" style="height:%dpx"></div>' % h for h in heights)
        return '<div class="viz-bsp">%s</div>' % rooms
    if sid == "save-system":
        return ('<div style="display:flex;flex-direction:column;gap:6px;align-items:flex-start">'
                '<span class="font-mono" style="font-size:.68rem;color:hsl(var(--green))">SLOT 1 &mdash; Active</span>'
                '<span class="font-mono" style="font-size:.68rem;color:hsl(var(--muted-foreground))">SLOT 2 &mdash; Empty</span>'
                '<span class="font-mono" style="font-size:.68rem;color:hsl(var(--muted-foreground))">SLOT 3 &mdash; Empty</span>'
                '</div><div class="viz-json">{ "v": 2, "enc": true }</div>')
    if sid == "enemy-ai":
        return ('<div class="viz-bt">'
                '<span class="viz-node viz-node-root">Selector</span>'
                '<div class="viz-bt-row">'
                '<span class="viz-node">Patrol</span><span class="viz-node">Combat</span>'
                '<span class="viz-node">Retreat</span><span class="viz-node">Attack</span><span class="viz-node">Flank</span>'
                '</div></div>')
    if sid == "ability-system":
        return ('<div class="viz-icons">'
                '<span class="viz-icon-chip">%s</span>'
                '<span class="viz-icon-chip">DMG</span><span class="viz-icon-chip">AOE</span>'
                '<span class="viz-icon-chip">SFX</span><span class="viz-icon-chip">VFX</span><span class="viz-icon-chip">CD</span>'
                '</div>') % icon("zap")
    if sid == "netcode-layer":
        return ('<div class="viz-net">'
                '<div class="viz-net-box">CLIENT<br>Input[]</div>'
                '<span class="viz-arrow">&#8644;</span>'
                '<div class="viz-net-box">SERVER<br>State</div>'
                '</div><span class="visual-caption">Ring Buffer &mdash; 16 frames</span>')
    return ""


# --------------------------------------------------------------------------
# Card renderers
# --------------------------------------------------------------------------

def render_project_card(p, depth, show_view_overlay=True):
    return """<a class="card project-card reveal" data-project-card data-title="%(title)s" data-year="%(year)s"
     data-tags="%(tagpipe)s" href="%(depth)sprojects/%(id)s.html">
    <div class="project-cover %(coverclass)s">
      <div class="cover-tags">%(badges)s</div>
      %(overlay)s
      <span class="cover-icon">%(icon)s</span>
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
        "icon": icon("folder", "icon cover-icon"),
        "desc": p["shortDesc"],
        "monitor_icon": icon("monitor"), "engine": p["engine"],
        "clock_icon": icon("clock"), "duration": p["duration"],
        "users_icon": icon("users"), "team": "Solo" if p["teamSize"] == 1 else "%d devs" % p["teamSize"],
        "tech": tech_tags(p["technologies"]),
    }


def render_system_card(s):
    stats_html = "".join('<span class="stat-chip">%s: %s</span>' % (k, v) for k, v in s["stats"])
    return """<div class="card system-card reveal">
    <div class="system-head">
      <span class="system-icon" style="background:hsl(var(--%(color)s) / .15);color:hsl(var(--%(color)s))">%(icon)s</span>
      <div>
        <div class="system-title-row"><h3>%(title)s</h3>%(cat_badge)s</div>
        <p class="system-subtitle">%(subtitle)s</p>
      </div>
    </div>
    <div class="system-visual">%(visual)s<span class="visual-caption">%(caption)s</span></div>
    <p class="system-desc">%(desc)s</p>
    <div class="tag-row">%(tech)s</div>
    <details class="system-detail">
      <summary>%(arrow_icon)s <span data-i18n="systems.read_more">Architecture deep-dive</span></summary>
      <div class="system-detail-body">
        <div class="system-detail-block">
          <h4 data-i18n="systems.architecture">Architecture</h4>
          <p>%(architecture)s</p>
        </div>
        <div class="system-detail-block">
          <h4 data-i18n="systems.challenges">Challenges</h4>
          <ul>%(challenges)s</ul>
        </div>
        <div class="system-detail-block">
          <h4 data-i18n="systems.solutions">Solutions Implemented</h4>
          <ul>%(solutions)s</ul>
        </div>
        <div class="system-detail-block">
          <h4 data-i18n="systems.stats">Stats</h4>
          <div class="stat-chip-row">%(stats)s</div>
        </div>
      </div>
    </details>
  </div>
""" % {
        "color": s["color"], "icon": icon(s["icon"]), "title": s["title"],
        "cat_badge": '<span class="tag">%s</span>' % s["category"],
        "subtitle": s["subtitle"], "visual": system_visual(s["id"]), "caption": s["caption"],
        "desc": s["description"], "tech": all_tech_tags(s["technologies"]),
        "arrow_icon": icon("arrow-right"),
        "architecture": s["architecture"],
        "challenges": "".join("<li>%s</li>" % c for c in s["challenges"]),
        "solutions": "".join("<li>%s</li>" % c for c in s["solutions"]),
        "stats": stats_html,
    }


# --------------------------------------------------------------------------
# Home page
# --------------------------------------------------------------------------

def build_home():
    featured = [p for p in PROJECTS if p["featured"]]
    depth = ""

    hero = """<section class="hero grid-bg container">
    <span class="hero-role" data-i18n="hero.title">Gameplay Programmer</span>
    <h1 class="text-glow">Romain <span class="accent">Pitot</span></h1>
    <div class="badge-row">
      <span class="pill pill-primary">Unity</span>
      <span class="pill pill-accent">C#</span>
      <span class="pill">Gameplay Systems</span>
      <span class="pill">AI / Netcode</span>
    </div>
    <p class="hero-tagline" data-i18n="hero.tagline">Building interactive systems and gameplay experiences</p>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="projects.html"><span data-i18n="hero.cta_projects">View Projects</span> %(arrow)s</a>
      <a class="btn btn-outline" href="cv.pdf" download>%(dl)s <span data-i18n="hero.cta_cv">Download CV</span></a>
    </div>
    <div class="scroll-hint" data-i18n="hero.scroll">Scroll to explore</div>
  </section>

  <section class="stats-bar">
    <div class="container stats-grid">
      <div class="stat"><div class="stat-num">6+</div><div class="stat-label">Projects Shipped</div></div>
      <div class="stat"><div class="stat-num">3+</div><div class="stat-label">Game Jams</div></div>
      <div class="stat"><div class="stat-num">2+</div><div class="stat-label">Years Unity</div></div>
      <div class="stat"><div class="stat-num">&#8734;</div><div class="stat-label">Systems Built</div></div>
    </div>
  </section>
""" % {"arrow": icon("arrow-right"), "dl": icon("download")}

    featured_html = """<section class="section">
    <div class="container">
      <div class="section-head">
        <div>
          <span class="eyebrow" data-i18n-skip>Selected Work</span>
          <h2 class="section-title" data-i18n="home.featured_title">Featured Projects</h2>
          <p class="section-sub" data-i18n="home.featured_subtitle">A selection of gameplay systems and game jams</p>
        </div>
        <a class="section-link" href="projects.html"><span data-i18n="home.view_all">View all</span> %(arrow)s</a>
      </div>
      <div class="grid grid-3" data-project-grid>
        %(cards)s
      </div>
    </div>
  </section>
""" % {"arrow": icon("arrow-right"), "cards": "".join(render_project_card(p, depth) for p in featured)}

    systems_html = """<section class="section" style="background:hsl(var(--background-deep) / .4)">
    <div class="container">
      <div class="section-head">
        <div>
          <span class="eyebrow" data-i18n-skip>Engineering</span>
          <h2 class="section-title" data-i18n="home.systems_title">Technical Systems</h2>
          <p class="section-sub" data-i18n="home.systems_subtitle">Architecture deep-dives &amp; production-ready frameworks</p>
        </div>
        <a class="section-link" href="systems.html"><span data-i18n="home.all_systems">All systems</span> %(arrow)s</a>
      </div>
      <div class="grid grid-3">
        %(cards)s
      </div>
    </div>
  </section>
""" % {"arrow": icon("arrow-right"), "cards": "".join(render_system_card(s) for s in SYSTEMS)}

    skills_cols = "".join(
        '<div class="skill-col"><h4>%s</h4><ul>%s</ul></div>' % (
            cat.upper(), "".join("<li>%s</li>" % s for s in items)
        )
        for cat, items in SKILLS
    )
    skills_html = """<section class="section">
    <div class="container">
      <div class="section-head">
        <div>
          <span class="eyebrow" data-i18n-skip>Expertise</span>
          <h2 class="section-title" data-i18n="home.skills_title">Core Skills</h2>
        </div>
      </div>
      <div class="skills-grid">%(cols)s</div>
    </div>
  </section>
""" % {"cols": skills_cols}

    about_html = """<section class="section" style="background:hsl(var(--background-deep) / .4)">
    <div class="container">
      <div class="section-head">
        <div>
          <span class="eyebrow" data-i18n-skip>About</span>
          <h2 class="section-title" data-i18n="home.about_title">About Me</h2>
        </div>
        <a class="section-link" href="about.html"><span data-i18n="home.full_profile">Full profile</span> %(arrow)s</a>
      </div>
      <div class="two-col">
        <div class="avatar-row reveal">
          <div class="avatar-box">%(user_icon)s</div>
          <div>
            <p style="font-size:1.05rem;font-weight:600;margin-bottom:10px">I'm a junior gameplay programmer passionate about building the systems that make games fun, responsive, and technically robust.</p>
            <p style="color:hsl(var(--muted-foreground));font-size:.92rem">I hold a Master's degree in Game Development and specialize in Unity and C# with a focus on gameplay systems, AI, procedural generation, and multiplayer networking.</p>
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
""" % {"arrow": icon("arrow-right"), "user_icon": icon("user"), "dl": icon("download")}

    cta_html = """<section class="section">
    <div class="container">
      <div class="cta-panel reveal">
        <span class="availability"><span class="dot"></span> AVAILABLE FOR OPPORTUNITIES</span>
        <h2>Let's build something<br><span class="accent">remarkable.</span></h2>
        <p>Looking for a junior gameplay programmer with a passion for clean architecture and interactive systems.</p>
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
        "%s — Gameplay Programmer" % AUTHOR,
        "Romain Pitot, junior gameplay programmer specialised in Unity & C# — gameplay systems, AI, procedural generation and multiplayer networking.",
        "home", depth, body, "",
    ))


# --------------------------------------------------------------------------
# Projects listing
# --------------------------------------------------------------------------

def build_projects_listing():
    depth = ""
    filters = ["All", "Game Jam", "Prototype", "Tool", "Released"]
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
    <p data-i18n="projects.subtitle">All gameplay projects, tools, and game jams</p>
  </section>
  <section class="section-tight container" data-filter-bar>
    <div class="filter-bar">
      <div class="filter-group">%(filters)s</div>
      <div class="filter-group"><span class="sort-label" data-i18n-skip>Sort:</span>%(sorts)s</div>
    </div>
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

def build_project_detail(p):
    depth = "../"
    others = [o for o in PROJECTS if o["id"] != p["id"]][:3]

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
    <h1 style="font-size:clamp(1.8rem,4vw,2.6rem);margin-bottom:28px">%(title)s</h1>

    <div class="detail-cover %(coverclass)s">
      <span class="cover-category">%(category)s</span>
      <span class="cover-icon">%(icon)s</span>
    </div>

    <div class="detail-meta-grid">%(meta)s</div>

    <div class="detail-section">
      <h2 data-i18n-skip>Overview</h2>
      <p>%(description)s</p>
    </div>

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

  <section class="section container">
    <div class="section-head"><h2 class="section-title" data-i18n-skip>Other projects</h2></div>
    <div class="other-projects">%(others)s</div>
  </section>
""" % {
        "title": p["title"],
        "badges": corner_badges(p["status"], p["tags"]),
        "coverclass": cover_class(p["category"]),
        "category": p["category"],
        "icon": icon("folder", "icon cover-icon"),
        "meta": meta_html,
        "description": p["description"],
        "highlights": "".join("<li>%s</li>" % h for h in p["highlights"]),
        "keysystems": "".join('<span class="tag">%s</span>' % k for k in p["keySystems"]),
        "tech": all_tech_tags(p["technologies"]),
        "links": project_link_buttons(p["links"], "btn-sm") or '<span style="color:hsl(var(--muted-foreground));font-size:.85rem">No public links yet.</span>',
        "others": "".join(render_project_card(o, depth) for o in others),
    }

    write("projects/%s.html" % p["id"], page(
        "%s — %s" % (p["title"], AUTHOR),
        p["shortDesc"],
        "projects", depth, body, "projects/%s.html" % p["id"],
    ))


# --------------------------------------------------------------------------
# Systems page
# --------------------------------------------------------------------------

def build_systems():
    depth = ""
    body = """<section class="page-hero container">
    <span class="eyebrow" data-i18n-skip>Engineering</span>
    <h1 data-i18n="systems.title">Systems</h1>
    <p data-i18n="systems.subtitle">Technical deep-dives into gameplay engineering</p>
  </section>
  <section class="section-tight container">
    <div class="grid grid-3">%(cards)s</div>
  </section>
""" % {"cards": "".join(render_system_card(s) for s in SYSTEMS)}

    write("systems.html", page(
        "Systems — %s" % AUTHOR,
        "Architecture deep-dives into inventory, save systems, procedural generation, AI, abilities and netcode.",
        "systems", depth, body, "systems.html",
    ))


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
    tech_skill_tags = ["Unity", "C#", "Gameplay Systems", "AI / Behavior Trees", "Procedural Generation",
                        "Netcode / Multiplayer", "ShaderLab / HLSL", "ScriptableObjects", "Design Patterns", "Git",
                        "Unreal Engine", "C++"]

    body = """<section class="page-hero container">
    <span class="eyebrow" data-i18n-skip>About</span>
    <h1 data-i18n="about.title">About Me</h1>
    <p data-i18n="about.subtitle">Gameplay Programmer &mdash; Unity / C#</p>
  </section>

  <section class="section-tight container">
    <div class="two-col">
      <div class="reveal">
        <p style="font-size:1.1rem;font-weight:600;margin-bottom:18px">I am a junior gameplay programmer passionate about building the systems that make games fun, responsive, and technically robust.</p>
        <p style="color:hsl(var(--muted-foreground));margin-bottom:14px">I hold a Master's degree in Game Development and specialize in Unity and C# with a focus on gameplay systems, AI, procedural generation, and multiplayer networking.</p>
        <p style="color:hsl(var(--muted-foreground));margin-bottom:14px">I believe great gameplay comes from well-architected systems. I enjoy working at the intersection of design and engineering &mdash; translating game design intent into clean, scalable code.</p>
        <p style="color:hsl(var(--muted-foreground));margin-bottom:24px">Outside of coding, I am an avid gamer and game systems analyst &mdash; breaking down what makes mechanics feel satisfying is both a hobby and a professional methodology.</p>
        <p class="font-mono" style="font-size:.85rem;color:hsl(var(--accent))" data-i18n="about.based">Based in France &mdash; Open to remote &amp; relocation</p>

        <h3 style="font-family:var(--font-mono);font-size:.75rem;letter-spacing:.15em;text-transform:uppercase;color:hsl(var(--primary)/.8);margin:36px 0 16px" data-i18n="about.education_title">Education</h3>
        %(edu)s
      </div>

      <div class="cv-card reveal">
        <div class="cv-icon">%(dl)s</div>
        <div>
          <strong>Curriculum Vit&aelig;</strong>
          <p style="color:hsl(var(--muted-foreground));font-size:.85rem;margin-top:4px">Gameplay Programmer &mdash; Unity / C#<br>PDF &middot; Updated 2026</p>
        </div>
        <a class="btn btn-primary btn-block" href="cv.pdf" download>%(dl)s <span data-i18n="hero.cta_cv">Download CV</span></a>
        <div style="border-top:1px solid hsl(var(--border));margin-top:6px;padding-top:16px">
          <span class="availability"><span class="dot"></span> <span data-i18n="contact.availability">Open to new opportunities</span></span>
        </div>
      </div>
    </div>
  </section>

  <section class="section container" style="border-top:1px solid hsl(var(--border)/.5)">
    <h3 style="font-family:var(--font-mono);font-size:.75rem;letter-spacing:.15em;text-transform:uppercase;color:hsl(var(--primary)/.8);margin-bottom:18px" data-i18n="about.skills_title">Technical Skills</h3>
    <div class="tag-row" style="margin-bottom:40px">%(skilltags)s</div>

    <h3 style="font-family:var(--font-mono);font-size:.75rem;letter-spacing:.15em;text-transform:uppercase;color:hsl(var(--primary)/.8);margin-bottom:18px" data-i18n="about.languages_title">Languages</h3>
    <div class="tag-row">
      <span class="tag">French &middot; Native</span>
      <span class="tag">English &middot; Professional</span>
    </div>
  </section>
""" % {
        "edu": edu_html, "dl": icon("download"),
        "skilltags": "".join('<span class="tag">%s</span>' % s for s in tech_skill_tags),
    }

    write("about.html", page(
        "About — %s" % AUTHOR,
        "About Romain Pitot: junior gameplay programmer, MSc Game Development, Unity/C# specialist.",
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
    <p data-i18n="contact.subtitle">Open to opportunities, collaborations, and interesting projects</p>
    <div style="margin-top:18px">
      <span class="availability"><span class="dot"></span> <span data-i18n="contact.availability">Open to new opportunities</span></span>
    </div>
  </section>

  <section class="section-tight container">
    <div class="contact-grid">
      <div class="form-card reveal">
        <h3 data-i18n="contact.form_title">Send a message</h3>
        <form data-contact-form action="%(formspree)s" method="POST">
          <div class="form-row">
            <div class="field"><label data-i18n-skip>Name</label><input type="text" name="name" required></div>
            <div class="field"><label data-i18n-skip>Email</label><input type="email" name="email" required></div>
          </div>
          <div class="field"><label data-i18n-skip>Subject</label><input type="text" name="subject"></div>
          <div class="field"><label data-i18n-skip>Message</label><textarea name="message" required></textarea></div>
          <input type="hidden" name="_subject" value="New message from romainpitot.github.io">
          <input type="hidden" name="_cc" value="r.pitot@laposte.net">
          <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
          <button class="btn btn-primary" type="submit">%(send_icon)s <span data-i18n="contact.send">Send Message</span></button>
          <p data-form-status class="font-mono" style="font-size:.82rem;margin-top:12px" hidden></p>
        </form>
      </div>

      <div class="reveal">
        <div class="connect-card">
          <h3 data-i18n="contact.connect">Connect</h3>
          <div class="connect-item">
            <span class="connect-icon">%(mail_icon)s</span>
            <div><div class="connect-label">Email</div><a class="connect-value" href="mailto:%(email)s">%(email)s</a></div>
          </div>
          <div class="connect-item">
            <span class="connect-icon">%(li_icon)s</span>
            <div><div class="connect-label">LinkedIn</div><a class="connect-value" href="%(linkedin)s" target="_blank" rel="noreferrer">linkedin.com/in/romain-pitot</a></div>
          </div>
          <div class="connect-item">
            <span class="connect-icon">%(gh_icon)s</span>
            <div><div class="connect-label">GitHub</div><a class="connect-value" href="%(github)s" target="_blank" rel="noreferrer">github.com/romainpitot</a></div>
          </div>
        </div>

        <div class="connect-card">
          <h3 data-i18n="contact.resume">Resume</h3>
          <p style="color:hsl(var(--muted-foreground));font-size:.85rem;margin-bottom:14px">PDF &mdash; Updated 2026</p>
          <a class="btn btn-primary btn-block" href="cv.pdf" download>%(dl_icon)s <span data-i18n="hero.cta_cv">Download CV</span></a>
        </div>

        <p class="font-mono" style="font-size:.8rem;color:hsl(var(--muted-foreground))" data-i18n="about.based">Based in France &mdash; Open to remote &amp; relocation</p>
      </div>
    </div>
  </section>
""" % {
        "send_icon": icon("send"), "mail_icon": icon("mail"), "li_icon": icon("linkedin"), "gh_icon": icon("github"),
        "dl_icon": icon("download"), "email": CONTACT_EMAIL, "linkedin": REAL_LINKEDIN, "github": REAL_GITHUB,
        "formspree": FORMSPREE_ENDPOINT,
    }

    write("contact.html", page(
        "Contact — %s" % AUTHOR,
        "Get in touch with Romain Pitot for junior gameplay programming roles, freelance work, or collaborations.",
        "contact", depth, body, "contact.html",
    ))


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def build_robots_and_sitemap():
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE_URL)

    paths = ["", "projects.html", "systems.html", "about.html", "contact.html"]
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
    body = """<section class="page-hero container" style="text-align:center;padding:120px 24px">
    <span class="eyebrow" data-i18n-skip>404</span>
    <h1>Page not found</h1>
    <p style="margin:0 auto 28px">This page doesn't exist &mdash; it may have moved, or the link is out of date.</p>
    <a class="btn btn-primary" href="index.html">%(arrow)s Back to home</a>
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
    build_systems()
    build_about()
    build_contact()
    build_404()
    build_robots_and_sitemap()


if __name__ == "__main__":
    main()
