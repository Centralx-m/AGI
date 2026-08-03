"""Core Memory & Knowledge Base"""
import json
import pickle
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
import numpy as np

class KnowledgeGraph:
    """Knowledge Graph for storing concepts and relationships"""
    
    def __init__(self, storage_path='knowledge/knowledge_graph.json'):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.graph = self._load()
    
    def _load(self) -> Dict:
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {'nodes': [], 'edges': [], 'concepts': {}}
    
    def _save(self) -> None:
        with open(self.storage_path, 'w') as f:
            json.dump(self.graph, f, indent=2)
    
    def add_concept(self, name: str, category: str, description: str, source: Optional[str] = None) -> bool:
        """Add a new concept"""
        if name not in self.graph['concepts']:
            self.graph['concepts'][name] = {
                'category': category,
                'description': description,
                'source': source,
                'added': datetime.now().isoformat(),
                'connections': []
            }
            self.graph['nodes'].append(name)
            self._save()
            return True
        return False
    
    def add_relation(self, concept1: str, concept2: str, relation_type: str) -> bool:
        """Add a relationship between concepts"""
        if concept1 in self.graph['concepts'] and concept2 in self.graph['concepts']:
            self.graph['edges'].append({
                'source': concept1,
                'target': concept2,
                'type': relation_type
            })
            self.graph['concepts'][concept1]['connections'].append({
                'to': concept2,
                'type': relation_type
            })
            self._save()
            return True
        return False
    
    def get_related(self, concept: str, max_distance: int = 2) -> List[str]:
        """Find related concepts"""
        related = set()
        if concept in self.graph['concepts']:
            for conn in self.graph['concepts'][concept]['connections']:
                related.add(conn['to'])
                if max_distance >= 2:
                    for sub_conn in self.graph['concepts'].get(conn['to'], {}).get('connections', []):
                        related.add(sub_conn['to'])
        return list(related)
    
    def get_summary(self) -> Dict:
        """Get knowledge graph summary"""
        return {
            'total_concepts': len(self.graph['concepts']),
            'total_edges': len(self.graph['edges']),
            'categories': list(set(c['category'] for c in self.graph['concepts'].values()))
        }


class NeuralMemory:
    """Neural Memory - Vector database for storing learned information"""
    
    def __init__(self, storage_path='knowledge/memory.db'):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use simple dictionary for memory (no external dependencies)
        self.memory = {
            'experiences': [],
            'knowledge': [],
            'patterns': [],
            'embeddings': {}
        }
        
        self._load()
    
    def _load(self):
        """Load memory from disk"""
        memory_file = self.storage_path / 'memory.json'
        if memory_file.exists():
            with open(memory_file, 'r') as f:
                self.memory = json.load(f)
    
    def _save(self):
        """Save memory to disk"""
        with open(self.storage_path / 'memory.json', 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def _get_embedding(self, text: str) -> List[float]:
        """Simple embedding function (hash-based)"""
        import hashlib
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        embedding = np.frombuffer(hash_bytes[:64], dtype=np.uint8).astype(np.float32)
        embedding = embedding / 255.0  # Normalize to 0-1
        embedding = embedding * 2 - 1  # Normalize to -1 to 1
        return embedding.tolist()
    
    def store_experience(self, experience: str, metadata: Optional[Dict] = None) -> str:
        """Store an experience"""
        doc_id = f"exp_{datetime.now().timestamp()}"
        embedding = self._get_embedding(experience)
        
        entry = {
            'id': doc_id,
            'text': experience,
            'embedding': embedding,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        
        self.memory['experiences'].append(entry)
        self.memory['embeddings'][doc_id] = embedding
        self._save()
        return doc_id
    
    def store_knowledge(self, text: str, category: str, source: Optional[str] = None) -> str:
        """Store knowledge"""
        doc_id = f"know_{datetime.now().timestamp()}"
        embedding = self._get_embedding(text)
        
        entry = {
            'id': doc_id,
            'text': text,
            'embedding': embedding,
            'category': category,
            'source': source,
            'timestamp': datetime.now().isoformat()
        }
        
        self.memory['knowledge'].append(entry)
        self.memory['embeddings'][doc_id] = embedding
        self._save()
        return doc_id
    
    def recall_similar(self, query: str, top_n: int = 5, collection: str = 'knowledge') -> List[Dict]:
        """Recall similar items"""
        query_embedding = self._get_embedding(query)
        
        # Get items from collection
        items = self.memory.get(collection, [])
        
        # Compute similarity scores
        scored_items = []
        for item in items:
            item_embedding = item.get('embedding', [])
            if item_embedding:
                # Cosine similarity
                similarity = np.dot(query_embedding, item_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(item_embedding) + 1e-8
                )
                scored_items.append((similarity, item))
        
        # Sort by similarity and return top_n
        scored_items.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored_items[:top_n]]
    
    def get_summary(self) -> Dict:
        """Get memory summary"""
        return {
            'total_experiences': len(self.memory['experiences']),
            'total_knowledge': len(self.memory['knowledge']),
            'total_patterns': len(self.memory['patterns'])
        }


class ExperienceDatabase:
    """Database for storing all experiences - successes and failures"""
    
    def __init__(self, storage_path='knowledge/experiences.json'):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()
    
    def _load(self) -> Dict:
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {'successes': [], 'failures': [], 'all': []}
    
    def _save(self) -> None:
        with open(self.storage_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_experience(self, action: str, result: str, context: str, success: bool) -> Dict:
        """Add a new experience"""
        experience = {
            'id': len(self.data['all']) + 1,
            'action': action,
            'result': result,
            'context': context,
            'success': success,
            'timestamp': datetime.now().isoformat()
        }
        
        self.data['all'].append(experience)
        if success:
            self.data['successes'].append(experience)
        else:
            self.data['failures'].append(experience)
        
        self._save()
        return experience
    
    def get_lessons(self, limit: int = 20) -> List[Dict]:
        """Extract lessons from failures"""
        lessons = []
        for failure in self.data['failures'][-limit:]:
            lessons.append({
                'what_went_wrong': failure['result'],
                'context': failure['context'],
                'lesson': f"Don't {failure['action']} when {failure['context']}"
            })
        return lessons
    
    def get_best_practices(self, limit: int = 20) -> List[Dict]:
        """Extract best practices from successes"""
        practices = []
        for success in self.data['successes'][-limit:]:
            practices.append({
                'action': success['action'],
                'context': success['context'],
                'result': success['result']
            })
        return practices
    
    def get_summary(self) -> Dict:
        """Get experience summary"""
        return {
            'total': len(self.data['all']),
            'successes': len(self.data['successes']),
            'failures': len(self.data['failures']),
            'success_rate': len(self.data['successes']) / max(1, len(self.data['all']))
        }


class CoreMemory:
    """Core Memory - Combines all memory systems"""
    
    def __init__(self):
        self.knowledge_graph = KnowledgeGraph()
        self.neural_memory = NeuralMemory()
        self.experience_db = ExperienceDatabase()
        print("🧠 Core Memory initialized")
    
    def learn_from_text(self, text: str, category: str, source: Optional[str] = None) -> bool:
        """Learn from text"""
        self.neural_memory.store_knowledge(text, category, source)
        return True
    
    def remember(self, query: str, top_n: int = 5) -> List[Dict]:
        """Recall relevant knowledge"""
        return self.neural_memory.recall_similar(query, top_n)
    
    def add_experience(self, action: str, result: str, context: str, success: bool) -> Dict:
        """Add an experience"""
        return self.experience_db.add_experience(action, result, context, success)
    
    def get_summary(self) -> Dict:
        """Get memory summary"""
        return {
            'knowledge_graph': self.knowledge_graph.get_summary(),
            'neural_memory': self.neural_memory.get_summary(),
            'experience_db': self.experience_db.get_summary()
        }