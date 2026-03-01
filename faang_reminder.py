"""
FAANG Prep — Daily Email Reminder (GitHub Actions version)
Reads config from config.json in the same repo.
"""

import smtplib, json, os
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ── CONFIG ─────────────────────────────────────────────────────────────────
SENDER_EMAIL = "mithundev.work@gmail.com"
TO_EMAIL     = "mithundev.work@gmail.com"
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

# ── LOAD config.json ───────────────────────────────────────────────────────
def load_config():
    if os.path.exists("config.json"):
        with open("config.json") as f:
            return json.load(f)
    # Default if not found
    return {"current_day": 1, "paused": False, "reminder_time_ist": "07:00", "streak": 0}

def save_config(cfg):
    with open("config.json", "w") as f:
        json.dump(cfg, f, indent=2)

# ── DAY PROBLEMS ───────────────────────────────────────────────────────────
DAY_PROBLEMS = {
    1:  [("Contains Duplicate","Easy"),("Remove Duplicates from Sorted Array","Easy"),("Find the Duplicate Number","Medium")],
    2:  [("Two Sum","Easy"),("Two Sum II","Medium"),("Find Pivot Index","Easy")],
    3:  [("Majority Element","Easy"),("Maximum Subarray (Kadane's)","Medium")],
    4:  [("Largest Subarray with Sum K","Medium"),("Longest Subarray with Sum K","Medium")],
    5:  [("Subarray Sum Equals K","Medium"),("Count Subarrays with Given XOR","Medium")],
    6:  [("Maximum Product Subarray","Medium"),("Minimum Size Subarray Sum","Medium")],
    7:  [("3Sum","Medium"),("Container With Most Water","Medium"),("Practice 2 unseen array problems","Hard")],
    8:  [("Next Permutation","Medium"),("Sort Colors","Medium"),("Set Mismatch","Easy")],
    9:  [("Set Matrix Zeroes","Medium"),("Spiral Matrix","Medium")],
    10: [("Rotate Image","Medium"),("Merge Sorted Arrays Without Extra Space","Hard")],
    11: [("Best Time to Buy and Sell Stock","Easy"),("Max Consecutive Ones","Easy")],
    12: [("Sliding Window Maximum","Hard"),("Longest Consecutive Sequence","Medium")],
    13: [("Solve 3 unseen array problems","Hard"),("Make revision cheatsheet","Easy")],
    14: [("Valid Anagram","Easy"),("Isomorphic Strings","Easy"),("Group Anagrams","Medium"),("Valid Palindrome","Easy")],
    15: [("Reverse String","Easy"),("Reverse Words in a String","Medium"),("Valid Palindrome II","Easy"),("Longest Palindromic Substring","Medium")],
    16: [("Longest Substring Without Repeating Characters","Medium"),("Minimum Window Substring","Hard"),("Permutation in String","Medium")],
    17: [("Find All Anagrams in a String","Medium"),("Longest Repeating Character Replacement","Medium"),("Longest Substring with At Most K Distinct Characters","Hard")],
    18: [("Valid Parentheses","Easy"),("Remove All Adjacent Duplicates In String","Easy"),("Decode String","Medium")],
    19: [("Implement strStr()","Easy"),("Multiply Strings","Medium"),("Remove K Digits","Medium")],
    20: [("Count and Say","Medium"),("Basic Calculator II","Medium")],
    21: [("Design Add and Search Words Data Structure","Medium"),("Solve 2-3 unseen string problems","Hard")],
    22: [("Binary Search","Easy"),("Find Peak Element","Medium"),("Search Insert Position","Easy")],
    23: [("Search in Rotated Sorted Array","Medium"),("Find Minimum in Rotated Sorted Array","Medium"),("Single Element in a Sorted Array","Medium")],
    24: [("Search a 2D Matrix","Medium"),("Matrix Median","Hard"),("Time Based Key-Value Store","Medium")],
    25: [("Koko Eating Bananas","Medium"),("Capacity To Ship Packages Within D Days","Medium"),("Minimum Number of Days to Make m Bouquets","Medium")],
    26: [("Median of Two Sorted Arrays","Hard"),("K-th Element of Two Sorted Arrays","Hard"),("Insert Interval","Medium"),("Merge Intervals","Medium")],
    27: [("Allocate Minimum Number of Pages","Hard"),("Aggressive Cows","Hard")],
    28: [("Revisit Days 2 & 5","Easy"),("2 unseen binary search problems","Medium"),("Take 1 mock test","Hard")],
    29: [("Reverse Linked List","Easy"),("Middle of the Linked List","Easy"),("Merge Two Sorted Lists","Easy")],
    30: [("Remove Nth Node From End of List","Medium"),("Delete Node in a Linked List","Easy"),("Intersection of Two Linked Lists","Easy")],
    31: [("Linked List Cycle","Easy"),("Linked List Cycle II","Medium"),("Palindrome Linked List","Easy")],
    32: [("Add Two Numbers","Medium"),("Reorder List","Medium"),("Rotate List","Medium")],
    33: [("Reverse Linked List II","Medium"),("Reverse Nodes in k-Group","Hard")],
    34: [("Copy List with Random Pointer","Medium"),("LRU Cache","Medium")],
    35: [("Merge k Sorted Lists","Hard"),("Find the Duplicate Number (Floyd's)","Medium"),("Binary Tree to DLL","Hard")],
    36: [("Min Stack","Medium"),("Implement Stack using Queues","Easy"),("Valid Parentheses","Easy")],
    37: [("Implement Queue using Stacks","Easy"),("Evaluate Reverse Polish Notation","Medium"),("Daily Temperatures","Medium")],
    38: [("Next Greater Element I","Easy"),("Next Greater Element II","Medium"),("Next Smaller Element","Medium")],
    39: [("Sliding Window Maximum","Hard"),("First Negative Integer in Every Window","Medium"),("Maximum of All Subarrays","Medium")],
    40: [("Largest Rectangle in Histogram","Hard"),("Trapping Rain Water","Hard"),("Minimum Add to Make Parentheses Valid","Medium")],
    41: [("Remove K Digits","Medium"),("Decode String","Medium"),("Simplify Path","Medium")],
    42: [("LRU Cache","Medium"),("Insert Delete GetRandom O(1)","Medium")],
    43: [("Binary Tree Inorder Traversal","Easy"),("Binary Tree Preorder Traversal","Easy"),("Binary Tree Postorder Traversal","Easy"),("Binary Tree Level Order Traversal","Medium"),("Binary Tree Zigzag Level Order Traversal","Medium")],
    44: [("Binary Tree Right Side View","Medium"),("Left View of Binary Tree","Easy"),("Top View of Binary Tree","Medium"),("Bottom View of Binary Tree","Medium"),("Boundary Traversal of Binary Tree","Hard")],
    45: [("Maximum Width of Binary Tree","Medium"),("Maximum Depth of Binary Tree","Easy"),("Diameter of Binary Tree","Easy"),("Validate Binary Search Tree","Medium")],
    46: [("Balanced Binary Tree","Easy"),("Same Tree","Easy"),("Symmetric Tree","Easy"),("Invert Binary Tree","Easy")],
    47: [("Lowest Common Ancestor of a Binary Tree","Medium"),("LCA of a BST","Easy"),("Search in a BST","Easy")],
    48: [("Construct Binary Tree from Preorder and Inorder","Medium"),("Construct Binary Tree from Inorder and Postorder","Medium"),("Flatten Binary Tree to Linked List","Medium")],
    49: [("Binary Tree Paths","Easy"),("Inorder Successor in BST","Medium"),("Populating Next Right Pointers in Each Node","Medium")],
    50: [("Kth Smallest Element in a BST","Medium"),("Kth Largest Element in a Stream","Easy"),("Binary Search Tree Iterator","Medium")],
    51: [("Serialize and Deserialize Binary Tree","Hard"),("Subtree of Another Tree","Easy"),("Count Good Nodes in Binary Tree","Medium")],
    52: [("Range Minimum Query","Medium"),("Segment Tree Build & Query","Hard")],
    53: [("Implement Trie (Prefix Tree)","Medium"),("Design Add and Search Words Data Structure","Medium")],
    54: [("Word Search","Medium"),("Word Search II","Hard")],
    55: [("Binary Tree Maximum Path Sum","Hard")],
    56: [("Practice problems across trees, trie, segment tree","Hard")],
    57: [("Kth Largest Element in an Array","Medium"),("Last Stone Weight","Easy"),("K Closest Points to Origin","Medium")],
    58: [("Top K Frequent Elements","Medium"),("Top K Frequent Words","Medium"),("Sort Characters By Frequency","Medium")],
    59: [("Task Scheduler","Medium"),("Reorganize String","Medium")],
    60: [("Find Median from Data Stream","Hard"),("Sliding Window Median","Hard")],
    61: [("LFU Cache","Hard"),("Merge k Sorted Lists","Hard")],
    62: [("IPO","Hard"),("Meeting Rooms II","Medium")],
    63: [("Smallest Range Covering Elements from K Lists","Hard"),("Minimum Cost to Connect Sticks","Medium")],
    64: [("Depth-First Search Practice","Medium"),("Breadth-First Search Practice","Medium")],
    65: [("Detect Cycle in an Undirected Graph","Medium")],
    66: [("Detect Cycle in a Directed Graph","Medium"),("Course Schedule (Kahn's Algorithm)","Medium")],
    67: [("Topological Sorting","Medium"),("Course Schedule II","Medium")],
    68: [("Number of Islands","Medium"),("Max Area of Island","Medium"),("Number of Connected Components","Medium")],
    69: [("Surrounded Regions","Medium"),("Pacific Atlantic Water Flow","Medium"),("Rotting Oranges","Medium")],
    70: [("Flood Fill","Easy"),("Is Graph Bipartite?","Medium")],
    71: [("Word Ladder","Hard"),("Word Ladder II","Hard")],
    72: [("Clone Graph","Medium"),("Alien Dictionary","Hard")],
    73: [("Dijkstra's Algorithm","Hard"),("Cheapest Flights Within K Stops","Medium")],
    74: [("M-Coloring Problem","Medium")],
    75: [("Review all graph concepts & patterns","Easy")],
    76: [("Climbing Stairs","Easy"),("Minimum Cost Climbing Stairs","Easy"),("Jump Game","Medium"),("Jump Game II","Medium")],
    77: [("Coin Change","Medium"),("Coin Change II","Medium")],
    78: [("House Robber","Medium"),("House Robber II","Medium"),("Paint House","Medium")],
    79: [("Triangle","Medium"),("Decode Ways","Medium"),("Word Break","Medium"),("Word Break II","Hard")],
    80: [("Longest Increasing Subsequence","Medium"),("Maximum Product Subarray","Medium"),("Longest Palindromic Substring","Medium")],
    81: [("Unique Paths","Medium"),("Unique Paths II","Medium"),("Minimum Path Sum","Medium")],
    82: [("Target Sum","Medium"),("Partition Equal Subset Sum","Medium"),("Palindrome Partitioning","Medium")],
    83: [("Longest Common Subsequence","Medium"),("Edit Distance","Hard")],
    84: [("Ones and Zeroes (0-1 Knapsack)","Hard"),("Rod Cutting Problem","Hard")],
    85: [("Longest Increasing Path in a Matrix","Hard")],
    86: [("Super Egg Drop","Hard"),("Regular Expression Matching","Hard"),("Burst Balloons","Hard")],
    87: [("Review all DP concepts & patterns","Medium")],
}

WEEK_TOPICS = {
    1:"Arrays — Basics",2:"Arrays II",3:"Strings",4:"Sorting & Searching",
    5:"Linked Lists",6:"Stacks & Queues",7:"Trees & BSTs",8:"Adv Trees & Trie",
    9:"Heaps",10:"Graphs I",11:"Graphs II",12:"DP I",13:"DP II"
}

PYTHON_TOPICS = {
    1:"Lists, slicing, enumerate(), zip(), sorted(), lambda",
    2:"Dictionaries, sets, list comprehensions",
    3:"collections.Counter, defaultdict, string methods",
    4:"Sorting algorithms, binary search in Python",
    5:"Classes & OOP — ListNode, Stack, Queue",
    6:"collections.deque, Stack/Queue implementations",
    7:"Recursion — call stack, base case, depth limit",
    8:"Tree node class, recursive traversals from memory",
    9:"heapq module, min/max heap tricks",
    10:"Graph representations, BFS/DFS in Python",
    11:"Union-Find, adjacency list patterns",
    12:"functools.lru_cache, memoization decorators",
    13:"itertools — combinations, permutations, DP helpers",
}

# ── EMAIL HTML ─────────────────────────────────────────────────────────────
def diff_color(d):
    return {"Easy":"#10b981","Medium":"#f59e0b","Hard":"#ef4444"}.get(d,"#888")

def build_email(day, week, topic, python_topic, problems, paused_days=0):
    problems_html = ""
    for i, (name, diff) in enumerate(problems, 1):
        c = diff_color(diff)
        problems_html += f"""
        <tr>
          <td style="padding:10px 14px;border-bottom:1px solid #1e1e2e;font-size:14px;color:#e8e8f0;">{i}. {name}</td>
          <td style="padding:10px 14px;border-bottom:1px solid #1e1e2e;text-align:right;">
            <span style="background:{c}22;color:{c};padding:2px 10px;border-radius:99px;font-size:12px;font-family:monospace;font-weight:700;">{diff.upper()}</span>
          </td>
        </tr>"""

    pct = round((day / 87) * 100)
    bar = round(pct / 2)
    progress_bar = f'<span style="color:#7c3aed;">{"█"*bar}</span>{"░"*(50-bar)}'

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#0a0a0f;font-family:'Segoe UI',Arial,sans-serif;">
<div style="max-width:620px;margin:0 auto;padding:32px 16px;">

  <div style="background:linear-gradient(135deg,#7c3aed22,#00ff8810);border:1px solid #2a2a3a;border-radius:16px;padding:28px 32px;margin-bottom:20px;">
    <div style="font-size:12px;font-family:monospace;color:#7c3aed;letter-spacing:0.1em;margin-bottom:6px;">FAANG PREP TRACKER</div>
    <h1 style="margin:0;font-size:28px;font-weight:800;color:#e8e8f0;letter-spacing:-0.03em;">
      Day <span style="color:#00ff88;">{day}</span> of 87
    </h1>
    <div style="margin-top:8px;font-size:13px;color:#6b6b85;font-family:monospace;">
      {date.today().strftime("%A, %d %B %Y")} &nbsp;·&nbsp; Week {week}: {topic}
    </div>
  </div>

  <div style="background:#111118;border:1px solid #2a2a3a;border-radius:12px;padding:18px 24px;margin-bottom:20px;">
    <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
      <span style="font-size:12px;font-family:monospace;color:#6b6b85;">OVERALL PROGRESS</span>
      <span style="font-size:12px;font-family:monospace;color:#00ff88;">{day}/87 days ({pct}%)</span>
    </div>
    <div style="font-family:monospace;font-size:11px;word-break:break-all;">{progress_bar}</div>
  </div>

  <div style="background:#111118;border:1px solid #f59e0b33;border-radius:12px;padding:18px 24px;margin-bottom:20px;">
    <div style="font-size:11px;font-family:monospace;color:#f59e0b;letter-spacing:0.1em;margin-bottom:6px;">🐍 PYTHON REVISION TODAY</div>
    <div style="font-size:14px;color:#e8e8f0;">{python_topic}</div>
  </div>

  <div style="background:#111118;border:1px solid #2a2a3a;border-radius:12px;overflow:hidden;margin-bottom:20px;">
    <div style="padding:14px 18px;border-bottom:1px solid #2a2a3a;">
      <span style="font-size:11px;font-family:monospace;color:#a78bfa;letter-spacing:0.1em;">💻 TODAY'S PROBLEMS — {len(problems)} problems</span>
    </div>
    <table style="width:100%;border-collapse:collapse;">{problems_html}</table>
  </div>

  <div style="background:#111118;border:1px solid #2a2a3a;border-radius:12px;padding:18px 24px;margin-bottom:20px;">
    <div style="font-size:11px;font-family:monospace;color:#6b6b85;letter-spacing:0.1em;margin-bottom:12px;">📅 TODAY'S SCHEDULE</div>
    <table style="width:100%;border-collapse:collapse;font-size:13px;color:#b0b0c8;font-family:monospace;">
      <tr><td style="padding:5px 10px;color:#6b6b85;">7:00 – 8:30 AM</td><td>🐍 Python Revision</td></tr>
      <tr><td style="padding:5px 10px;color:#6b6b85;">9:00 – 11:00 AM</td><td>💻 DSA Morning Block</td></tr>
      <tr><td style="padding:5px 10px;color:#6b6b85;">11:15 – 1:00 PM</td><td>💻 DSA Deep Practice</td></tr>
      <tr><td style="padding:5px 10px;color:#6b6b85;">2:00 – 3:00 PM</td><td>📝 Revise & Notes</td></tr>
      <tr><td style="padding:5px 10px;color:#6b6b85;">3:00 – 5:00 PM</td><td>💻 DSA Afternoon Block</td></tr>
      <tr><td style="padding:5px 10px;color:#6b6b85;">5:30 – 6:30 PM</td><td>🐍 Python Advanced</td></tr>
      <tr><td style="padding:5px 10px;color:#6b6b85;">6:30 – 7:30 PM</td><td>⏱ Mock / Timed Problem</td></tr>
    </table>
  </div>

  <div style="background:linear-gradient(135deg,#7c3aed15,#00ff8808);border:1px solid #7c3aed44;border-radius:12px;padding:18px 24px;margin-bottom:20px;text-align:center;">
    <div style="font-size:14px;color:#a78bfa;font-style:italic;">"The expert in anything was once a beginner."</div>
    <div style="font-size:11px;color:#6b6b85;margin-top:6px;font-family:monospace;">DAY {day} · {87-day} DAYS LEFT · KEEP GOING 🚀</div>
  </div>

  <div style="text-align:center;font-size:11px;font-family:monospace;color:#3a3a4a;padding-top:8px;">
    FAANG Prep Tracker · Auto-generated daily reminder<br>
    Use your Control Panel to pause, change day, or update time.
  </div>
</div></body></html>"""

# ── MAIN ───────────────────────────────────────────────────────────────────
def main():
    cfg = load_config()

    # Check if paused
    if cfg.get("paused", False):
        print("⏸ Emails are paused — skipping send. Resume via Control Panel.")
        return

    day  = cfg.get("current_day", 1)
    week = (day - 1) // 7 + 1

    topic        = WEEK_TOPICS.get(week, f"Week {week}")
    python_topic = PYTHON_TOPICS.get(week, "Revise previous concepts")
    problems     = DAY_PROBLEMS.get(day, [("Free practice / revision", "Medium")])

    subject = f"🚀 FAANG Prep — Day {day}/87 | {topic} | {date.today().strftime('%d %b')}"
    html    = build_email(day, week, topic, python_topic, problems)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = TO_EMAIL
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, TO_EMAIL, msg.as_string())
        print(f"✅ Email sent — Day {day}/87 to {TO_EMAIL}")
    except Exception as e:
        print(f"❌ Failed: {e}")
        return

    # Auto-advance day
    cfg["current_day"] = min(day + 1, 87)
    save_config(cfg)
    print(f"📅 Advanced to Day {cfg['current_day']} for tomorrow")

if __name__ == "__main__":
    main()
