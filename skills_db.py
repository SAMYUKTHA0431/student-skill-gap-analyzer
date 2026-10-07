"""Knowledge base: job roles, required skill levels (1-5), importance weights (1-3)
and learning suggestions. Edit this file to add your own roles/skills."""

ROLES = {
    "Data Analyst": {
        "Python": (4, 3), "SQL": (4, 3), "Statistics": (3, 2),
        "Excel": (3, 1), "Data Visualization": (3, 2), "Communication": (3, 1),
    },
    "Web Developer": {
        "HTML/CSS": (4, 2), "JavaScript": (4, 3), "Python": (3, 1),
        "Databases": (3, 2), "Git": (3, 1), "Problem Solving": (3, 2),
    },
    "Cyber Security Analyst": {
        "Networking": (4, 3), "Cryptography": (3, 3), "Linux": (3, 2),
        "Python": (3, 1), "Ethical Hacking": (3, 2), "Problem Solving": (3, 1),
    },
    "Network Engineer": {
        "Networking": (5, 3), "Linux": (3, 2), "Socket Programming": (3, 2),
        "Network Simulation": (3, 2), "Python": (2, 1), "Communication": (3, 1),
    },
    "AI/ML Engineer": {
        "Python": (5, 3), "Mathematics": (4, 3), "Machine Learning": (4, 3),
        "Statistics": (3, 2), "Data Visualization": (3, 1), "Git": (3, 1),
    },
    "Software Engineer": {
        "Python": (4, 2), "Data Structures": (4, 3), "Databases": (3, 2),
        "Git": (3, 1), "Problem Solving": (4, 3), "Communication": (3, 1),
    },
}

RESOURCES = {
    "Python": "Build 3 small projects; practise daily on HackerRank/LeetCode (easy-medium).",
    "SQL": "Practise joins, group-by and sub-queries on a sample database (SQLite/MySQL).",
    "Statistics": "Revise mean/variance/probability; do exercises on Khan Academy.",
    "Excel": "Learn pivot tables, lookups and charts using a real dataset.",
    "Data Visualization": "Make dashboards using matplotlib / Power BI on a public dataset.",
    "Communication": "Give a 5-minute talk each week; write short technical summaries.",
    "HTML/CSS": "Clone 2 landing pages; learn flexbox and grid.",
    "JavaScript": "Complete a JS course and build a to-do app and a weather app.",
    "Databases": "Design an ER diagram and implement it in MySQL/SQLite.",
    "Git": "Use Git/GitHub for every project: branch, commit, pull request.",
    "Problem Solving": "Solve 2 coding problems per day; review editorial solutions.",
    "Networking": "Revise OSI/TCP-IP, subnetting and routing; use Packet Tracer.",
    "Cryptography": "Implement Caesar, DES, RSA, Diffie-Hellman and SHA from scratch.",
    "Linux": "Practise shell commands, permissions and scripting on Ubuntu.",
    "Ethical Hacking": "Practise legal labs on TryHackMe / Hack The Box (beginner rooms).",
    "Socket Programming": "Write TCP/UDP client-server programs (echo, chat, DNS).",
    "Network Simulation": "Simulate TCP/UDP traffic in NS2 / Packet Tracer and analyse results.",
    "Mathematics": "Revise linear algebra, calculus and probability for ML.",
    "Machine Learning": "Finish an ML course; build a classifier with scikit-learn.",
    "Data Structures": "Implement arrays, lists, trees, graphs; solve topic-wise problems.",
}
