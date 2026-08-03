"""Self-Upgrade - Sabunta Kansa Ta Atomatik"""
import json
import shutil
from datetime import datetime
from pathlib import Path

class SelfUpgrader:
    """Yana inganta kansa ta hanyar koyo da sabunta code"""
    
    def __init__(self, agent):
        self.agent = agent
        self.version = "1.0.0"
        self.upgrade_history = []
        self.backup_path = Path('backups')
        self.backup_path.mkdir(exist_ok=True)
    
    def check_for_upgrade(self):
        """Duba ko akwai sabuntawa"""
        print("🔍 Checking for upgrades...")
        
        # 1. Check performance
        performance = self.agent.brain.evaluate_performance() if hasattr(self.agent.brain, 'evaluate_performance') else 0.5
        
        # 2. Check if upgrade needed
        if performance < 0.7:
            print("   Performance below threshold - upgrade needed")
            return self._perform_upgrade()
        else:
            print("   Performance acceptable - no upgrade needed")
            return None
    
    def _perform_upgrade(self):
        """Aiwatar da sabuntawa"""
        print(f"🚀 Upgrading from version {self.version}...")
        
        # 1. Backup current system
        backup_id = self._backup()
        
        # 2. Optimize model
        optimized = self._optimize_model()
        
        # 3. Update knowledge
        self._update_knowledge()
        
        # 4. Increment version
        self.version = self._increment_version()
        
        # Record upgrade
        self.upgrade_history.append({
            'from_version': self.version,
            'to_version': self.version,
            'timestamp': datetime.now().isoformat(),
            'backup': backup_id
        })
        
        print(f"✅ Upgrade complete! Version: {self.version}")
        return {'success': True, 'version': self.version}
    
    def _backup(self):
        """Ƙirƙiri backup na yanzu"""
        backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.backup_path / backup_id
        backup_path.mkdir()
        
        # Backup code
        # (Simplified - would copy entire codebase)
        
        return backup_id
    
    def _optimize_model(self):
        """Inganta model"""
        print("   Optimizing model...")
        # Would implement actual optimization
        return True
    
    def _update_knowledge(self):
        """Sabunta ilimi"""
        print("   Updating knowledge...")
        # Would pull latest knowledge
        return True
    
    def _increment_version(self):
        """Ƙara lambar version"""
        parts = self.version.split('.')
        parts[2] = str(int(parts[2]) + 1)
        return '.'.join(parts)
    
    def get_upgrade_history(self):
        """Samo tarihin sabuntawa"""
        return self.upgrade_history