# Curated dataset for training the Reddit Job Intent Classifier
# Labels: 1 = Legitimate Job Offer/Hiring, 0 = Noise (Showcase, Advice, Question, Pitch)

TRAINING_DATA = [
    # Positive Examples (Hiring/Offers)
    {"text": "[Hiring] Senior Motion Graphics Artist for Fintech Startup", "label": 1},
    {"text": "We are hiring a Remote React Developer - $120k/yr", "label": 1},
    {"text": "[Hiring] Social Media Manager for e-commerce brand", "label": 1},
    {"text": "Graphic Design Internship Opportunity (Paid)", "label": 1},
    {"text": "Looking for a After Effects animator to join our team", "label": 1},
    {"text": "[Hiring] VFX Artist for short film project", "label": 1},
    {"text": "Is hiring a full-time Senior Python Engineer", "label": 1},
    {"text": "Urgent recruitment: Video Editor needed for YouTube channel", "label": 1},
    {"text": "[Offer] Senior Backend Developer position", "label": 1},
    {"text": "[HIRING] Junior Designer - Remote - UK Based", "label": 1},
    {"text": "Remote Job - Senior Software Engineer at Stripe", "label": 1},
    {"text": "Python Backend Developer needed for 3 month contract", "label": 1},
    {"text": "Hiring: Cinema 4D Artist for 3D commercial", "label": 1},
    {"text": "3D Generalist position open at Blur Studio", "label": 1},
    {"text": "[Hiring] Lead Web Developer for agency", "label": 1},
    {"text": "[Hiring] Data Scientist - Machine Learning & NLP - Remote", "label": 1},
    {"text": "Hiring: Senior AI Engineer (PyTorch/Tensorflow) - $150k+", "label": 1},
    {"text": "Data Analyst needed for 6-month contract | Python & SQL", "label": 1},
    {"text": "[HIRING] Computer Vision Researcher for Robotics Startup", "label": 1},
    {"text": "Looking for an NLP specialist to help with LLM fine-tuning", "label": 1},
    {"text": "[Hiring] Marketing Manager for e-commerce brand", "label": 1},
    {"text": "Customer Support Representative (Remote) - $20/hr", "label": 1},
    {"text": "Content Writer needed for Tech Blog - Paid project", "label": 1},
    {"text": "[Hiring] Sales Development Representative - Entry Level", "label": 1},
    {"text": "Virtual Assistant for daily tasks - $15/hr", "label": 1},
    {"text": "I'm looking for a freelance data scientist for a 3-month project", "label": 1},
    {"text": "Our team is hiring a Senior AI Engineer! Join us.", "label": 1},
    {"text": "Looking to hire a part-time video editor for my YouTube channel", "label": 1},
    
    # Negative Examples (Showcase/Experiments - The user's pain point)
    {"text": "Blender + AR experiment... cursed or cool?", "label": 0},
    {"text": "My first attempt at a vfx shot in After Effects", "label": 0},
    {"text": "Check out this render I made over the weekend!", "label": 0},
    {"text": "Blender Fluid Simulation - feedback appreciated", "label": 0},
    {"text": "Is this a good enough portfolio for a job?", "label": 0},
    {"text": "Finally finished my first 3D character in Blender", "label": 0},
    {"text": "messing around merging two characters in Blender", "label": 0},
    {"text": "testing it in AR... and this came out of nowhere", "label": 0},
    {"text": "Showcase: Real-time hair simulation in Unreal Engine", "label": 0},
    {"text": "Just a small project I worked on for fun", "label": 0},
    {"text": "WIP: Sculpting Wolverine in Blender", "label": 0},
    {"text": "Experimenting with geometry nodes", "label": 0},
    {"text": "How I built a RAG pipeline in one weekend", "label": 0},
    {"text": "Check out my new AI-generated art series", "label": 0},
    {"text": "Thinking of switching from Data Science to Web Dev", "label": 0},
    
    # Negative Examples (Aggregator Bots - User's pain point)
    {"text": "📢 is [hiring] a Data Analyst - jobboardsearch.com", "label": 0},
    {"text": "Apply & Description 👉 https://jobboardsearch.com/redirect", "label": 0},
    {"text": "Company: Date Posted: Categories: #data #remote", "label": 0},
    {"text": "findcontractjobs.com hiring bot post", "label": 0},
    {"text": "[Hiring] New job on aggregator site: Python Developer", "label": 0},
    
    # Negative Examples (Candidate Pitches / For Hire)
    {"text": "[For Hire] Professional Video Editor looking for gigs", "label": 0},
    {"text": "Freelance Designer available for work - DM me!", "label": 0},
    {"text": "I am a Python developer looking for a job", "label": 0},
    {"text": "Looking for Full-Time Opportunities | Frontend Developer", "label": 0},
    {"text": "Hire me: I know Blender, Photoshop and Premiere", "label": 0},
    {"text": "Communication design student looking for freelance gigs", "label": 0},
    {"text": "Open to work: Senior React Engineer", "label": 0},
    {"text": "My resume for review - help me get hired!", "label": 0},
    {"text": "[For Hire] Entry level Data Analyst looking for work", "label": 0},
    {"text": "Senior ML Engineer looking for remote opportunities", "label": 0},
    
    # Negative Examples (Questions / Advice / Meta)
    {"text": "How much should I charge for a motion graphics project?", "label": 0},
    {"text": "What is the best way to learn Blender in 2026?", "label": 0},
    {"text": "Why is the job market so bad for VFX artists right now?", "label": 0},
    {"text": "Is anyone actually getting hired on Reddit lately?", "label": 0},
    {"text": "Advice needed: Should I learn Python or Javascript?", "label": 0},
    {"text": "Help! Blender keeps crashing when I render", "label": 0},
    {"text": "Discussion: The future of AI in animation", "label": 0},
    {"text": "Question: What SQL skills are needed for Data Science jobs?", "label": 0},
    {"text": "Which ML framework is better: PyTorch or JAX?", "label": 0},
    
    # Borderline but Noise
    {"text": "Latest Motion Graphics showreel", "label": 0},
    {"text": "Free Blender textures for everyone", "label": 0},
    {"text": "Top 10 Blender tips for beginners", "label": 0},
    {"text": "My journey from 498 to 795 followers in 2 months", "label": 0},
    {"text": "Top 5 Data Science datasets for your portfolio", "label": 0}
]
