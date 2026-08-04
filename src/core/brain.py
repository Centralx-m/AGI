"""
Core Brain - The AI's Decision-Making Engine
============================================

This is the central intelligence of the AI agent. It:
- Understands any task given to it
- Identifies the domain (finance, business, healthcare, etc.)
- Creates execution plans
- Executes tasks
- Learns from experience
"""

import json
import hashlib
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

from .memory import CoreMemory


class TaskEmbedding:
    """Task Embedding - Converts tasks to numbers"""
    
    def __init__(self, embedding_dim: int = 256):
        self.embedding_dim = embedding_dim
    
    def encode(self, text: str) -> np.ndarray:
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        embedding = np.frombuffer(hash_bytes[:self.embedding_dim], dtype=np.uint8).astype(np.float32)
        embedding = embedding / 255.0 * 2 - 1
        return embedding


class UniversalBrain:
    """Universal Brain - Handles ANY task, ANY domain"""
    
    def __init__(self, memory: CoreMemory):
        self.memory = memory
        self.embedder = TaskEmbedding()
        self.domains = self._initialize_domains()
        self.current_domain = None
        self.current_task = None
        self.task_history = []
        self.performance_scores = []
    
    def _initialize_domains(self) -> Dict:
        """Initialize all domain handlers"""
        from ..domains.base import DomainBase
        from ..domains.business import BusinessDomain
        from ..domains.finance import FinanceDomain
        from ..domains.healthcare import HealthcareDomain
        from ..domains.education import EducationDomain
        from ..domains.technology import TechnologyDomain
        from ..domains.legal import LegalDomain
        from ..domains.creative import CreativeDomain
        from ..domains.real_estate import RealEstateDomain
        from ..domains.manufacturing import ManufacturingDomain
        from ..domains.agriculture import AgricultureDomain
        from ..domains.retail import RetailDomain
        from ..domains.transportation import TransportationDomain
        from ..domains.energy import EnergyDomain
        from ..domains.government import GovernmentDomain
        
        return {
            'business': BusinessDomain(),
            'finance': FinanceDomain(),
            'healthcare': HealthcareDomain(),
            'education': EducationDomain(),
            'technology': TechnologyDomain(),
            'legal': LegalDomain(),
            'creative': CreativeDomain(),
            'real_estate': RealEstateDomain(),
            'manufacturing': ManufacturingDomain(),
            'agriculture': AgricultureDomain(),
            'retail': RetailDomain(),
            'transportation': TransportationDomain(),
            'energy': EnergyDomain(),
            'government': GovernmentDomain()
        }
    
    def understand_task(self, task_description: str, context: Optional[Dict] = None) -> Dict:
        """Understand any task"""
        print(f"🎯 Understanding: {task_description[:100]}...")
        
        domain = self._identify_domain(task_description)
        self.current_domain = domain
        
        task_vector = self.embedder.encode(task_description)
        context_vector = self.embedder.encode(json.dumps(context or {}))
        combined = np.concatenate([task_vector, context_vector])
        
        domain_knowledge = self.domains[domain].get_knowledge(task_description)
        similar_tasks = self.memory.remember(task_description)
        plan = self._create_plan(task_description, domain_knowledge, similar_tasks)
        
        return {
            'domain': domain,
            'task_vector': combined.tolist(),
            'knowledge': domain_knowledge,
            'similar_tasks': similar_tasks,
            'plan': plan,
            'task_description': task_description
        }
    
    def _identify_domain(self, task_description: str) -> str:
        """Identify the domain of a task"""
        domain_keywords = {
            'business': ['business', 'management', 'company', 'strategy', 'ceo', 'manager', 'organization'],
            'finance': ['finance', 'trade', 'investment', 'stock', 'market', 'price', 'profit', 'crypto'],
            'healthcare': ['health', 'hospital', 'doctor', 'patient', 'disease', 'medical', 'treatment'],
            'education': ['education', 'school', 'study', 'teach', 'learn', 'student', 'teacher'],
            'technology': ['technology', 'software', 'hardware', 'network', 'computer', 'system'],
            'legal': ['legal', 'law', 'court', 'attorney', 'contract', 'rights', 'justice'],
            'creative': ['creative', 'design', 'art', 'music', 'writing', 'media', 'content'],
            'real_estate': ['estate', 'property', 'land', 'house', 'rent', 'real estate'],
            'manufacturing': ['manufacturing', 'factory', 'production', 'warehouse', 'logistics'],
            'agriculture': ['agriculture', 'farming', 'crop', 'livestock', 'farm'],
            'retail': ['retail', 'store', 'shop', 'sales', 'customer', 'merchandise'],
            'transportation': ['transportation', 'delivery', 'shipping', 'logistics', 'vehicle'],
            'energy': ['energy', 'power', 'electricity', 'solar', 'wind', 'grid'],
            'government': ['government', 'policy', 'regulation', 'public', 'administration']
        }
        
        best_domain = 'business'
        best_score = 0
        
        for domain, keywords in domain_keywords.items():
            score = sum(1 for kw in keywords if kw.lower() in task_description.lower())
            if score > best_score:
                best_score = score
                best_domain = domain
        
        return best_domain
    
    def _create_plan(self, task: str, knowledge: Dict, similar_tasks: List) -> Dict:
        """Create an execution plan"""
        plan = {
            'steps': self._generate_steps(task),
            'tools': self._identify_tools(task),
            'subtasks': self._split_into_subtasks(task),
            'estimated_duration': self._estimate_duration(task),
            'dependencies': []
        }
        return plan
    
    def _generate_steps(self, task: str) -> List[str]:
        steps = [
            "1. Analyze task requirements",
            "2. Gather necessary information",
            "3. Process and analyze data",
            "4. Execute core action",
            "5. Verify results",
            "6. Learn from outcome"
        ]
        
        if 'trading' in task.lower() or 'investment' in task.lower():
            steps.insert(3, "3a. Perform technical analysis")
            steps.insert(4, "3b. Execute trade with risk management")
        
        if 'business' in task.lower():
            steps.insert(3, "3a. Perform market research")
            steps.insert(4, "3b. Generate business strategy")
        
        return steps
    
    def _identify_tools(self, task: str) -> List[str]:
        tools = []
        if any(kw in task.lower() for kw in ['analyze', 'data', 'statistics']):
            tools.append('Data Analysis')
        if any(kw in task.lower() for kw in ['trading', 'market', 'investment']):
            tools.append('Market Analysis')
        if any(kw in task.lower() for kw in ['write', 'create', 'content']):
            tools.append('Content Generation')
        if any(kw in task.lower() for kw in ['code', 'develop', 'program']):
            tools.append('Code Generation')
        if any(kw in task.lower() for kw in ['plan', 'strategy', 'manage']):
            tools.append('Strategic Planning')
        return tools
    
    def _split_into_subtasks(self, task: str) -> List[str]:
        words = task.split()
        subtasks = []
        if len(words) > 15:
            for i in range(0, len(words), 10):
                subtasks.append(' '.join(words[i:i+10]))
        else:
            subtasks = [task]
        return subtasks
    
    def _estimate_duration(self, task: str) -> str:
        word_count = len(task.split())
        if word_count < 10:
            return "5 minutes"
        elif word_count < 30:
            return "30 minutes"
        elif word_count < 50:
            return "2 hours"
        else:
            return "4+ hours"
    
    def execute(self, task_understanding: Dict) -> Dict:
        """Execute the understood task"""
        domain = task_understanding['domain']
        plan = task_understanding['plan']
        
        results = []
        domain_handler = self.domains[domain]
        
        for step in plan['steps']:
            try:
                result = domain_handler.execute_step(step, task_understanding)
                results.append({'step': step, 'status': 'success', 'result': result})
            except Exception as e:
                results.append({'step': step, 'status': 'failed', 'error': str(e)})
        
        final_result = domain_handler.generate_report(results, task_understanding)
        
        return {
            'success': all(r['status'] == 'success' for r in results),
            'results': results,
            'final_result': final_result,
            'domain': domain,
            'plan': plan
        }
    
    def learn_from_execution(self, task_understanding: Dict, execution_result: Dict) -> bool:
        """Learn from task execution"""
        self.memory.add_experience(
            action=task_understanding.get('task_description', 'Unknown'),
            result=json.dumps(execution_result),
            context=task_understanding.get('domain', 'unknown'),
            success=execution_result.get('success', False)
        )
        
        if execution_result.get('success'):
            self.memory.learn_from_text(
                f"Successfully executed: {task_understanding.get('task_description', '')}",
                category=task_understanding.get('domain', 'general')
            )
        
        self.task_history.append({
            'task': task_understanding,
            'result': execution_result,
            'timestamp': datetime.now().isoformat()
        })
        
        return True
    
    def process_task(self, task_description: str, context: Optional[Dict] = None) -> Dict:
        """Complete task processing pipeline"""
        understanding = self.understand_task(task_description, context)
        result = self.execute(understanding)
        self.learn_from_execution(understanding, result)
        return result
    
    def get_status(self) -> Dict:
        return {
            'domains': list(self.domains.keys()),
            'current_domain': self.current_domain,
            'tasks_executed': len(self.task_history),
            'performance': {
                'average_score': np.mean(self.performance_scores) if self.performance_scores else 0,
                'total': len(self.performance_scores)
            }
        }
