"""
SUNA-ALSHAM Configuration
Configurações do sistema e agentes
"""

import os
from typing import Optional


class CoreAgentConfig:
    """Configuração do Core Agent AutoML."""
    
    def __init__(self):
        # Configurações básicas
        self.enabled = True
        self.min_improvement_percentage = float(os.getenv('SUNA_ALSHAM_CORE_MIN_IMPROVEMENT', '5.0'))
        
        # Configurações AutoML
        self.optuna_trials = int(os.getenv('OPTUNA_TRIALS', '15'))
        self.automl_timeout = int(os.getenv('AUTOML_TIMEOUT', '180'))
        
        # Configurações de ambiente
        self.environment = os.getenv('SUNA_ENV', 'production')
        self.debug = os.getenv('SUNA_ALSHAM_DEBUG', 'false').lower() == 'true'
        
        # Configurações de logging
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')


class SUNAAlshamConfig:
    """Configuração geral do sistema SUNA-ALSHAM."""
    
    def __init__(self):
        # Sistema
        self.auto_start = os.getenv('SUNA_ALSHAM_AUTO_START', 'true').lower() == 'true'
        self.evolution_interval = int(os.getenv('SUNA_ALSHAM_EVOLUTION_INTERVAL', '60'))
        self.version = os.getenv('SUNA_ALSHAM_VERSION', '2.1.0')
        
        # Database
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        # Agentes
        self.core_agent = CoreAgentConfig()


# Instância global de configuração
config = SUNAAlshamConfig()

