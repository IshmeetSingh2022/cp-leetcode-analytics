from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from collections import defaultdict

from app.dependencies.database import get_db
from app.models.submission import Submission

router = APIRouter(prefix="/topics", tags=["Topics"])

# ─────────────────────────────────────────────────────────────────
# 📚 IMPORTANT TOPICS + QUESTIONS
# Har topic mein:
#   - tag: Codeforces ka exact tag (matching ke liye)
#   - label: display name
#   - problems: important CF problems list
#     - pid: problem_id jaise DB mein store hota hai "1234A"
#     - name: problem ka naam
#     - rating: difficulty
# ─────────────────────────────────────────────────────────────────
TOPICS = [
    {
        "tag":   "binary search",
        "label": "Binary Search",
        "problems": [
            { "pid": "702C",  "name": "Cellular Network",         "rating": 1600 },
            { "pid": "812C",  "name": "Sagheer and Nubian Market", "rating": 1700 },
            { "pid": "1201C", "name": "Maximum Median",           "rating": 1700 },
            { "pid": "1351C", "name": "Ball in Berland",          "rating": 1700 },
            { "pid": "760B",  "name": "Frodo and pillows",        "rating": 1500 },
        ],
    },
    {
        "tag":   "two pointers",
        "label": "Two Pointers",
        "problems": [
            { "pid": "676C",  "name": "Vasya and String",         "rating": 1600 },
            { "pid": "1033C", "name": "Cram Time",                "rating": 1500 },
            { "pid": "1209D", "name": "Segment Intersections",    "rating": 2000 },
            { "pid": "1732C", "name": "Trimming the Tree",        "rating": 1600 },
        ],
    },
    {
        "tag":   "dp",
        "label": "Dynamic Programming",
        "problems": [
            { "pid": "1542C", "name": "Странный алгоритм сортировки", "rating": 1600 },
            { "pid": "1473C", "name": "No More Inversions",       "rating": 1800 },
            { "pid": "1096D", "name": "Easy Problem",             "rating": 1900 },
            { "pid": "1017C", "name": "The Phone Number",         "rating": 1700 },
            { "pid": "978F",  "name": "Heaps",                    "rating": 2000 },
            { "pid": "1463D", "name": "Pairs",                    "rating": 1700 },
        ],
    },
    {
        "tag":   "graphs",
        "label": "Graphs",
        "problems": [
            { "pid": "1442C", "name": "Graph Transpositions",     "rating": 1700 },
            { "pid": "1027F", "name": "Session in BSU",           "rating": 1900 },
            { "pid": "1033E", "name": "Hidden Bipartite Graph",   "rating": 2100 },
            { "pid": "653E",  "name": "Garden",                   "rating": 2100 },
            { "pid": "1037D", "name": "Valid BFS?",               "rating": 1900 },
        ],
    },
    {
        "tag":   "greedy",
        "label": "Greedy",
        "problems": [
            { "pid": "1369C", "name": "RationalLee",              "rating": 1700 },
            { "pid": "1443C", "name": "The Football Season",      "rating": 1600 },
            { "pid": "1077C", "name": "Skyscrapers",              "rating": 1700 },
            { "pid": "1092D", "name": "Great Plan",               "rating": 1800 },
            { "pid": "1102C", "name": "Doors Breaking and Repairing","rating": 1600 },
        ],
    },
    {
        "tag":   "dfs and similar",
        "label": "DFS / Tree Problems",
        "problems": [
            { "pid": "1017E", "name": "The Supersonic Rocket",    "rating": 2000 },
            { "pid": "1092F", "name": "Tree with Maximum Cost",   "rating": 2000 },
            { "pid": "1099F", "name": "Maximum Weight Subset",    "rating": 2100 },
            { "pid": "1324F", "name": "Maximum White Subtree",    "rating": 2000 },
            { "pid": "600D",  "name": "Area of Two Circles' Intersection","rating": 1900 },
        ],
    },
    {
        "tag":   "sortings",
        "label": "Sorting",
        "problems": [
            { "pid": "1374D", "name": "Zero-One Array",           "rating": 1600 },
            { "pid": "1369B", "name": "AccurateLee",              "rating": 1600 },
            { "pid": "1156D", "name": "0-1-2 MST",               "rating": 1800 },
            { "pid": "939E",  "name": "Maximize!",                "rating": 1900 },
        ],
    },
    {
        "tag":   "shortest paths",
        "label": "Shortest Paths (Dijkstra)",
        "problems": [
            { "pid": "1547G", "name": "How Many Paths?",          "rating": 2000 },
            { "pid": "1486E", "name": "Paired Payment",           "rating": 2000 },
            { "pid": "1468J", "name": "Road Reform",              "rating": 2000 },
            { "pid": "1059E", "name": "Split the Tree",           "rating": 2100 },
        ],
    },
    {
        "tag":   "dsu",
        "label": "Union Find (DSU)",
        "problems": [
            { "pid": "1249D", "name": "Too Many Segments",        "rating": 1900 },
            { "pid": "1209G", "name": "Into Blocks",              "rating": 1900 },
            { "pid": "1012B", "name": "Chemical table",           "rating": 1900 },
            { "pid": "566D",  "name": "Restructuring Company",    "rating": 1700 },
        ],
    },
    {
        "tag":   "hashing",
        "label": "Hashing",
        "problems": [
            { "pid": "1063F", "name": "String Journey",           "rating": 2400 },
            { "pid": "1200E", "name": "Compress Words",           "rating": 1900 },
            { "pid": "1063B", "name": "Labyrinth",                "rating": 1900 },
        ],
    },
    {
        "tag":   "backtracking",
        "label": "Backtracking",
        "problems": [
            { "pid": "1097F", "name": "Alex and a TV Show",       "rating": 2700 },
            { "pid": "1239B", "name": "Walk on Matrix",           "rating": 1900 },
            { "pid": "793D",  "name": "Presents in Bankopolis",   "rating": 2200 },
        ],
    },
    {
        "tag":   "bitmasks",
        "label": "Bit Manipulation",
        "problems": [
            { "pid": "1097F", "name": "Alex and a TV Show",       "rating": 2700 },
            { "pid": "1055F", "name": "Make It One",              "rating": 2400 },
            { "pid": "1209H", "name": "Moving to the Capital",    "rating": 2300 },
        ],
    },
]


# ─────────────────────────────────────────────────────────────────
# GET /topics/tracker
# User ke solved problems check karke har topic ka status do
# ─────────────────────────────────────────────────────────────────
@router.get("/tracker")
def get_tracker(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id

    # Is user ki saari submissions fetch karo
    subs = db.query(Submission).filter_by(user_id=user_id).all()

    # Solved problem IDs ka set banao — O(1) lookup ke liye
    # sirf "OK" ya "AC" verdict wale
    solved_pids = {
        s.problem_id
        for s in subs
        if s.verdict in ("OK", "AC")
    }

    # Har tag ke liye total solved count — topic level badge ke liye
    # { "binary search": 5, "dp": 12 }
    tag_solved_count = defaultdict(int)
    for s in subs:
        if s.verdict not in ("OK", "AC"):
            continue
        tags = [t.strip() for t in s.tags.split(",")] if s.tags else []
        for tag in tags:
            if tag:
                tag_solved_count[tag] += 1

    # Har topic ke liye result build karo
    result = []
    for topic in TOPICS:
        tag         = topic["tag"]
        total_solved = tag_solved_count[tag]  # us tag mein total kitne solve kiye

        # Har important problem ka solved status check karo
        problems_with_status = []
        for p in topic["problems"]:
            problems_with_status.append({
                "pid":    p["pid"],
                "name":   p["name"],
                "rating": p["rating"],
                # solved_pids mein hai toh True, warna False
                "solved": p["pid"] in solved_pids,
            })

        # Topic level stats
        imp_solved = sum(1 for p in problems_with_status if p["solved"])
        imp_total  = len(problems_with_status)

        result.append({
            "tag":          tag,
            "label":        topic["label"],
            "total_solved": total_solved,   # CF pe overall kitne solve kiye
            "imp_solved":   imp_solved,     # important problems mein se kitne
            "imp_total":    imp_total,      # total important problems
            "problems":     problems_with_status,
        })

    return result
