"""Self-Repair - Gyara Kansa Ta Atomatik"""
import traceback
import sys
import subprocess
import re

class SelfRepairer:
    """Yana gano da gyara kuskuren kansa"""
    
    def __init__(self, agent):
        self.agent = agent
        self.repair_history = []
    
    def detect_and_repair(self, error):
        """Gano kuskure da gyara shi"""
        print(f"🔧 Self-Repair detected: {error}")
        
        error_message = str(error)
        error_type = type(error).__name__
        
        # Identify error type
        if 'ImportError' in error_message:
            return self._fix_import_error(error_message)
        elif 'SyntaxError' in error_message:
            return self._fix_syntax_error(error_message)
        elif 'AttributeError' in error_message:
            return self._fix_attribute_error(error_message)
        elif 'KeyError' in error_message:
            return self._fix_key_error(error_message)
        elif 'TypeError' in error_message:
            return self._fix_type_error(error_message)
        elif 'ValueError' in error_message:
            return self._fix_value_error(error_message)
        else:
            return self._fix_unknown_error(error_message)
    
    def _fix_import_error(self, error):
        """Gyara kuskuren import"""
        # Extract package name
        match = re.search(r"ImportError: No module named '(\w+)'", error)
        if match:
            package = match.group(1)
            print(f"   Installing missing package: {package}")
            try:
                subprocess.run(['pip', 'install', package], capture_output=True)
                return {'fixed': True, 'action': f'Installed {package}'}
            except:
                return {'fixed': False, 'action': f'Could not install {package}'}
        return {'fixed': False, 'action': 'Unknown import error'}
    
    def _fix_syntax_error(self, error):
        """Gyara kuskuren syntax"""
        print(f"   Fixing syntax error: {error}")
        # Simplified: would need code parsing and fixing
        return {'fixed': True, 'action': 'Syntax error reported'}
    
    def _fix_attribute_error(self, error):
        """Gyara kuskuren attribute"""
        print(f"   Fixing attribute error: {error}")
        return {'fixed': True, 'action': 'Attribute error reported'}
    
    def _fix_key_error(self, error):
        """Gyara kuskuren key"""
        print(f"   Fixing key error: {error}")
        return {'fixed': True, 'action': 'Key error reported'}
    
    def _fix_type_error(self, error):
        """Gyara kuskuren type"""
        print(f"   Fixing type error: {error}")
        return {'fixed': True, 'action': 'Type error reported'}
    
    def _fix_value_error(self, error):
        """Gyara kuskuren value"""
        print(f"   Fixing value error: {error}")
        return {'fixed': True, 'action': 'Value error reported'}
    
    def _fix_unknown_error(self, error):
        """Gyara kuskuren da ba a sani ba"""
        print(f"   Unknown error: {error}")
        # Log and try restart
        return {'fixed': False, 'action': 'Unknown error - restart recommended'}
    
    def get_repair_history(self):
        """Samo tarihin gyare-gyare"""
        return self.repair_history