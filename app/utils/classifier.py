import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from app.utils.training_data import TRAINING_DATA

class HiringClassifier:
    """
    ML Classifier to distinguish between real [Hiring] offers and 
    common Reddit noise (Showcases, Pitches, Questions).
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HiringClassifier, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.model = None
        self._initialized = True
        self.train()

    def train(self):
        """Trains the Naive Bayes model using the provided synthetic dataset."""
        print("[ML] Training Intent Classifier...")
        
        # 1. Prepare Data
        df = pd.DataFrame(TRAINING_DATA)
        X = df['text']
        y = df['label']
        
        # 2. Build Pipeline (TF-IDF + Naive Bayes)
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 2), # Consider both single words and pairs
                stop_words='english',
                lowercase=True
            )),
            ('clf', MultinomialNB(alpha=1.0)) # Laplace smoothing
        ])
        
        # 3. Fit Model
        self.model.fit(X, y)
        print("[ML] Intent Classifier trained and ready!")

    def predict_is_hiring(self, title: str) -> bool:
        """
        Returns True if the model predicts the title is a Legitimate Job Offer.
        """
        if not title:
            return False
            
        # Get probability
        # [0] is noise, [1] is hiring
        probs = self.model.predict_proba([title])[0]
        hiring_prob = probs[1]
        
        # Threshold: we want to be fairly confident it's a job
        is_hired = hiring_prob > 0.45 # Conservative threshold to avoid false negatives
        
        # Debugging (can be silenced)
        if not is_hired and hiring_prob > 0.1:
            safe_title = title[:60].encode('ascii', 'ignore').decode('ascii')
            print(f"[ML REJECT] (Prob: {hiring_prob:.2f}) | {safe_title}...")
            
        return is_hired

# Singleton instance for global use
classifier = HiringClassifier()
