"""
Core Brain - The AI's Decision-Making Engine
============================================

This is the central intelligence of the AI agent. It:
- Understands any task given to it
- Identifies the domain (finance, business, healthcare, etc.)
- Creates execution plans
- Executes tasks
- Learns from experience

The brain is domain-agnostic - it can handle ANY task.
"""

import json
import hashlib
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

from .memory import CoreMemory


class TaskEmbedding:
    """
    Task Embedding - Converts tasks to numbers
    ------------------------------------------
    
    Every task is converted to a numerical vector (embedding).
    This allows the AI to:
    - Compare tasks (find similar tasks)
    - Store tasks in memory
    - Process tasks mathematically
    
    The embedding preserves the semantic meaning of the task.
    """
    
    def __init__(self, embedding_dim: int = 256):
        """
        Initialize the task embedder
        
        Args:
            embedding_dim: Size of the embedding vector (256 is a good default)
        """
        self.embedding_dim = embedding_dim
    
    def encode(self, text: str) -> np.ndarray:
        """
        Convert text to an embedding vector
        
        This uses a simple hash-based method. In production, you'd use
        something like sentence-transformers for better quality.
        
        The hash method is deterministic - same text always gives same vector.
        
        Args:
            text: The text to encode
        
        Returns:
            np.ndarray: Numerical representation (embedding)
        """
        # Hash the text to get deterministic bytes
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert hash to floats between -1 and 1
        embedding = np.frombuffer(hash_bytes[:self.embedding_dim], dtype=np.uint8).astype(np.float32)
        embedding = embedding / 255.0 * 2 - 1
        
        return embedding


class UniversalBrain:
    """
    Universal Brain - Handles ANY task, ANY domain
    ----------------------------------------------
    
    This is the main AI brain that can process any task.
    
    Key features:
    1. Domain Identification: Figures out what domain the task is in
    2. Task Understanding: Breaks down the task and creates a plan
    3. Execution: Carries out the plan
    4. Learning: Learns from the results
    
    The brain has specialized handlers for different domains,
    but can also handle general tasks.
    """
    
    def __init__(self, memory: CoreMemory):
        """
        Initialize the universal brain
        
        Args:
            memory: The core memory system for knowledge and experience
        """
        self.memory = memory
        self.embedder = TaskEmbedding()
        
        # Initialize domain handlers
        # These are specialized systems for different domains
        self.domains = self._initialize_domains()
        
        # Brain state tracking
        self.current_domain = None
        self.current_task = None
        self.task_history = []  # All tasks ever executed
        self.performance_scores = []  # Performance history
        
        print(" Universal Brain initialized")
        print(f"   Domains: {len(self.domains)}")
        print(f"   Embedding dimension: {self.embedder.embedding_dim}")
    
    def _initialize_domains(self) -> Dict:
        """
        Initialize all domain handlers
        
        Each domain handler has specialized knowledge and skills.
        This makes the brain capable of handling any task.
        
        Returns:
            Dict: Dictionary of domain handlers
        """
        # Import domain handlers
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
        
        # Return all domains in a dictionary
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
    
    def understand_task(self, task_description: str, 
                        context: Optional[Dict] = None) -> Dict:
        """
        Understand a task and create an execution plan
        
        This is the first step in processing any task:
        1. Identify the domain
        2. Encode the task and context
        3. Get domain knowledge
        4. Recall similar tasks from memory
        5. Create an execution plan
        
        Args:
            task_description: What needs to be done
            context: Additional information (optional)
        
        Returns:
            Dict: Task understanding with domain, plan, and knowledge
        """
        print(f" Understanding: {task_description[:100]}...")
        
        # Step 1: Identify the domain
        # The AI figures out what type of task this is
        domain = self._identify_domain(task_description)
        self.current_domain = domain
        print(f"   Domain: {domain}")
        
        # Step 2: Encode the task and context into vectors
        # This converts text to numbers the AI can process
        task_vector = self.embedder.encode(task_description)
        context_vector = self.embedder.encode(json.dumps(context or {}))
        
        # Combine task and context
        combined = np.concatenate([task_vector, context_vector])
        
        # Step 3: Get domain-specific knowledge
        # This gives the AI specialized knowledge for this domain
        domain_knowledge = self.domains[domain].get_knowledge(task_description)
        
        # Step 4: Recall similar tasks from memory
        # The AI remembers what it did before
        similar_tasks = self.memory.remember(task_description)
        
        # Step 5: Create an execution plan
        # The AI plans how to execute the task
        plan = self._create_plan(task_description, domain_knowledge, similar_tasks)
        
        # Return everything
        return {
            'domain': domain,
            'task_vector': combined.tolist(),
            'knowledge': domain_knowledge,
            'similar_tasks': similar_tasks,
            'plan': plan,
            'task_description': task_description
        }
    
    def _identify_domain(self, task_description: str) -> str:
        """
        Identify what domain a task belongs to
        
        This uses keyword matching to find the best domain.
        In production, you'd use ML for better accuracy.
        
        Args:
            task_description: The task text
        
        Returns:
            str: The identified domain name
        """
        # Keywords for each domain
        # The more keywords match, the higher the score
        domain_keywords = {
            'business': ['business', 'management', 'company', 'strategy', 'ceo', 'manager', 
                        'organization', 'enterprise', 'corporate', 'startup'],
            'finance': ['finance', 'trade', 'investment', 'stock', 'market', 'price', 
                       'profit', 'crypto', 'bitcoin', 'currency', 'fund'],
            'healthcare': ['health', 'hospital', 'doctor', 'patient', 'disease', 'medical', 
                          'treatment', 'therapy', 'surgery', 'clinic'],
            'education': ['education', 'school', 'study', 'teach', 'learn', 'student', 
                         'teacher', 'curriculum', 'course', 'training'],
            'technology': ['technology', 'software', 'hardware', 'network', 'computer', 
                          'system', 'programming', 'code', 'database', 'cloud'],
            'legal': ['legal', 'law', 'court', 'attorney', 'contract', 'rights', 
                     'justice', 'judge', 'lawsuit', 'compliance'],
            'creative': ['creative', 'design', 'art', 'music', 'writing', 'media', 
                        'content', 'creative', 'visual', 'audio'],
            'real_estate': ['estate', 'property', 'land', 'house', 'rent', 'real estate', 
                          'mortgage', 'appraisal', 'construction'],
            'manufacturing': ['manufacturing', 'factory', 'production', 'warehouse', 
                            'logistics', 'supply chain', 'assembly', 'machinery'],
            'agriculture': ['agriculture', 'farming', 'crop', 'livestock', 'farm', 
                           'harvest', 'soil', 'irrigation'],
            'retail': ['retail', 'store', 'shop', 'sales', 'customer', 'merchandise', 
                      'inventory', 'checkout'],
            'transportation': ['transportation', 'delivery', 'shipping', 'logistics', 
                              'vehicle', 'fleet', 'cargo'],
            'energy': ['energy', 'power', 'electricity', 'solar', 'wind', 'grid', 
                      'renewable', 'utility'],
            'government': ['government', 'policy', 'regulation', 'public', 'administration', 
                          'municipal', 'federal']
        }
        
        # Find the domain with the most keyword matches
        best_domain = 'business'  # Default domain
        best_score = 0
        
        for domain, keywords in domain_keywords.items():
            # Count how many keywords are in the task description
            score = sum(1 for kw in keywords 
                       if kw.lower() in task_description.lower())
            if score > best_score:
                best_score = score
                best_domain = domain
        
        return best_domain
    
    def _create_plan(self, task: str, knowledge: Dict, 
                     similar_tasks: List) -> Dict:
        """
        Create a step-by-step execution plan
        
        This breaks down the task into manageable steps.
        
        Args:
            task: The task to execute
            knowledge: Domain knowledge
            similar_tasks: Similar tasks from memory
        
        Returns:
            Dict: The execution plan
        """
        # Generic steps that apply to any task
        steps = [
            "1. Analyze task requirements",
            "2. Gather necessary information",
            "3. Process and analyze data",
            "4. Execute core action",
            "5. Verify results",
            "6. Learn from outcome"
        ]
        
        # Add domain-specific steps based on the task type
        # Trading tasks need extra market analysis steps
        if 'trading' in task.lower() or 'investment' in task.lower():
            steps.insert(3, "3a. Perform technical analysis")
            steps.insert(4, "3b. Execute trade with risk management")
        
        # Business tasks need strategy steps
        if 'business' in task.lower():
            steps.insert(3, "3a. Perform market research")
            steps.insert(4, "3b. Generate business strategy")
        
        # Plan structure
        plan = {
            'steps': steps,
            'tools': self._identify_tools(task),
            'subtasks': self._split_into_subtasks(task),
            'estimated_duration': self._estimate_duration(task),
            'dependencies': []  # Tasks that need to be done first
        }
        
        return plan
    
    def _identify_tools(self, task: str) -> List[str]:
        """
        Identify what tools are needed for this task
        
        Args:
            task: The task description
        
        Returns:
            List[str]: Required tools
        """
        tools = []
        
        # Match keywords to tools
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
        """
        Split a complex task into smaller subtasks
        
        This helps when tasks are very large or complex.
        
        Args:
            task: The task description
        
        Returns:
            List[str]: Subtasks
        """
        words = task.split()
        subtasks = []
        
        # If the task is longer than 15 words, split it
        if len(words) > 15:
            for i in range(0, len(words), 10):
                subtasks.append(' '.join(words[i:i+10]))
        else:
            subtasks = [task]
        
        return subtasks
    
    def _estimate_duration(self, task: str) -> str:
        """
        Estimate how long the task will take
        
        This is based on the complexity of the task.
        
        Args:
            task: The task description
        
        Returns:
            str: Estimated duration
        """
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
        """
        Execute the understood task
        
        This carries out the plan created in understand_task().
        
        Args:
            task_understanding: The task understanding from understand_task()
        
        Returns:
            Dict: Execution results
        """
        domain = task_understanding['domain']
        plan = task_understanding['plan']
        
        print(f" Executing in domain: {domain}")
        print(f"   Steps: {len(plan['steps'])}")
        print(f"   Tools: {plan['tools']}")
        
        results = []
        domain_handler = self.domains[domain]
        
        # Execute each step
        for step in plan['steps']:
            try:
                # Let the domain handler execute the step
                result = domain_handler.execute_step(step, task_understanding)
                results.append({
                    'step': step,
                    'status': 'success',
                    'result': result
                })
            except Exception as e:
                # If any step fails, record the error
                results.append({
                    'step': step,
                    'status': 'failed',
                    'error': str(e)
                })
        
        # Generate a final report
        final_result = domain_handler.generate_report(results, task_understanding)
        
        return {
            'success': all(r['status'] == 'success' for r in results),
            'results': results,
            'final_result': final_result,
            'domain': domain,
            'plan': plan
        }
    
    def learn_from_execution(self, task_understanding: Dict, 
                            execution_result: Dict) -> bool:
        """
        Learn from the execution results
        
        This is how the AI improves over time:
        1. It stores the experience (success or failure)
        2. It records the outcome
        3. It updates its knowledge
        
        Args:
            task_understanding: The task understanding
            execution_result: The execution result
        
        Returns:
            bool: True if learning was successful
        """
        print(" Learning from execution...")
        
        # Store the experience
        self.memory.add_experience(
            action=task_understanding.get('task_description', 'Unknown'),
            result=json.dumps(execution_result),
            context=task_understanding.get('domain', 'unknown'),
            success=execution_result.get('success', False)
        )
        
        # If successful, store the knowledge
        if execution_result.get('success'):
            self.memory.learn_from_text(
                f"Successfully executed: {task_understanding.get('task_description', '')}",
                category=task_understanding.get('domain', 'general'),
                source='self_execution'
            )
        
        # Record the task in history
        self.task_history.append({
            'task': task_understanding,
            'result': execution_result,
            'timestamp': datetime.now().isoformat()
        })
        
        return True
    
    def get_status(self) -> Dict:
        """
        Get the current status of the brain
        
        Returns:
            Dict: Brain status information
        """
        # Calculate average performance
        avg_performance = np.mean(self.performance_scores) if self.performance_scores else 0
        
        return {
            'domains': list(self.domains.keys()),
            'current_domain': self.current_domain,
            'tasks_executed': len(self.task_history),
            'performance': {
                'average_score': avg_performance,
                'total': len(self.performance_scores)
            }
        }