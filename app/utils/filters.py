def is_aggregator_post(title, description):
    """Detects if a post is from an aggregator bot (e.g., jobboardsearch.com)."""
    text = (title + " " + description).lower()
    
    # Aggregator markers
    bot_markers = [
        "📢", "apply & description 👉", "jobboardsearch.com", "findcontractjobs.com",
        "date posted:", "categories:", "is [hiring] a", "findcontractjobs"
    ]
    
    if any(marker in text for marker in bot_markers):
        return True
        
    return False

def is_job_post(title, description=""):
    title_lower = title.lower()
    
    # 0. BOT REJECTION (Aggregators)
    if is_aggregator_post(title, description):
        return False

    # 1. FORCED REJECTION (Candidate Pitches / For Hire)
    forced_reject = [
        "[for hire]", "for hire", "looking for work", "looking for job", 
        "i am looking", "i'm looking", "i am a", "i'm a", "seeking", 
        "available for", "hire me", "my portfolio", "open to work"
    ]
    
    if any(pattern in title_lower for pattern in forced_reject):
        return False

    # 2. STRONG ACCEPTANCE (Client/Company Hiring)
    strong_hiring = [
        "[hiring]", "we are hiring", "[offer]", "hiring:", "is hiring", 
        "internship opportunity", "job opening"
    ]
    if any(pattern in title_lower for pattern in strong_hiring):
        return True

    # 3. NOISY CONTENT REJECTION
    reject_patterns = [
        "how", "should i", "help", "advice", "question", "vs", "why", "what", "where",
        "can't find", "no job", "job searching", "got a job", "got hired", "burnt out",
        "internship search", "resume", "review my","[FOR HIRING]" ,"how to", "opinion"
    ]
    if any(word in title_lower for word in reject_patterns):
        return False

    # 4. HEURISTIC FOR JOB LISTINGS (Role-based markers)
    job_roles = [
        "developer", "engineer", "designer", "vfx", "animator", "editor", "manager",
        "scientist", "analyst", "nlp", "vision", "researcher", "data", "marketing",
        "sales", "representative", "assistant", "writer", "support", "specialist"
    ]
    if any(role in title_lower for role in job_roles):
        words = title_lower.split()
        if 2 <= len(words) <= 15:
            return True

    return False