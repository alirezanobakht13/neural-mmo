from pdb import set_trace as T

from neural_mmo.forge.blade import core
from neural_mmo.forge.blade.core import config


class RLlibConfig:
   '''Base config for RLlib Models

   Extends core Config, which contains environment, evaluation,
   and non-RLlib-specific learning parameters'''

   @property
   def MODEL(self):
      return self.__class__.__name__

   #Paths
   EXPERIMENT_DIR          = 'experiment'
  
   #Hardware Scale
   NUM_GPUS_PER_WORKER     = 0
   NUM_GPUS                = 1
   NUM_WORKERS             = 1
   LOCAL_MODE              = False
   LOAD                    = True

   #Memory/Batch Scale
   TRAIN_EPOCHS            = 10000
   LSTM_BPTT_HORIZON       = 16
   NUM_SGD_ITER            = 1

   #Model
   SCRIPTED                = None
   N_AGENT_OBS             = 100
   NPOLICIES               = 1
   HIDDEN                  = 64
   EMBED                   = 64

   #Reward
   TEAM_SPIRIT             = 0.0
   ACHIEVEMENT_SCALE       = 1.0/15.0

   DEV_COMBAT = False


class LargeMaps(core.Config, RLlibConfig, config.AllGameSystems):
   '''Large scale Neural MMO training setting

   Features up to 1000 concurrent agents and 1000 concurrent NPCs,
   1km x 1km maps, and 5/10k timestep train/eval horizons

   This is the default setting as of v1.5 and allows for large
   scale multiagent research even on relatively modest hardware'''

   #Memory/Batch Scale
   NUM_WORKERS             = 16
   TRAIN_BATCH_SIZE        = 32 * NUM_WORKERS #Bug? This gets doubled
   ROLLOUT_FRAGMENT_LENGTH = 32
   SGD_MINIBATCH_SIZE      = 256

   #Horizon
   TRAIN_HORIZON           = 8192
   EVALUATION_HORIZON      = 8192


class SmallMaps(config.SmallMaps, RLlibConfig, config.AllGameSystems):
   '''Small scale Neural MMO training setting

   Features up to 128 concurrent agents and 32 concurrent NPCs,
   60x60 maps (excluding the border), and 1000 timestep train/eval horizons.
   
   This setting is modeled off of v1.1-v1.4 It is appropriate as a quick train
   task for new ideas, a transfer target for agents trained on large maps,
   or as a primary research target for PCG methods.'''

   #Memory/Batch Scale
   NUM_WORKERS             = 32
   TRAIN_BATCH_SIZE        = 256 * NUM_WORKERS #Bug? This gets doubled
   ROLLOUT_FRAGMENT_LENGTH = 32
   SGD_MINIBATCH_SIZE      = min(128, TRAIN_BATCH_SIZE)
 
   #Horizon
   TRAIN_HORIZON           = 1024
   EVALUATION_HORIZON      = 1024

   NTILE                   = 16

   ORE_RESPAWN       = 0.01
   '''Probability that a harvested ore tile will regenerate each tick'''

   TREE_RESPAWN      = 0.01
   '''Probability that a harvested tree tile will regenerate each tick'''

   CRYSTAL_RESPAWN   = 0.01
   '''Probability that a harvested crystal tile will regenerate each tick'''

   HERB_RESPAWN      = 0.01
   '''Probability that a harvested herb tile will regenerate each tick'''

   FISH_RESPAWN      = 0.01
   '''Probability that a harvested fish tile will regenerate each tick'''


   N_AMMUNITION      = 3
   '''Number of inventory spaces for ammunition'''

   N_CONSUMABLES     = 6
   '''Number of inventory spaces for ammunition'''

   N_LOOT            = 8
   '''Number of inventory spaces for ammunition'''

   N_ITEM            = 10


   SPAWN_CLUSTERS          = 15
   SPAWN_UNIFORMS          = 50

   DEV_COMBAT = True

   @staticmethod
   def EQUIPMENT_DEFENSE(level):
      return level / 4

   @staticmethod
   def EQUIPMENT_OFFENSE(level):
      return level / 4

   @staticmethod
   def DAMAGE_AMMUNITION(level):
      return level // 5 + 1, level // 3 + 1

   @staticmethod
   def DAMAGE_MELEE(level):
      return round(10 + level*70/99)

   @staticmethod
   def DAMAGE_RANGE(level):
      return round(3 + level*32/99)

   @staticmethod
   def DAMAGE_MAGE(level):
      return round(1 + level*24/99)

   @staticmethod
   def RESTORE(level):
      return level

class Debug(SmallMaps, config.AllGameSystems):
   '''Debug Neural MMO training setting

   A version of the SmallMap setting with greatly reduced batch parameters.
   Only intended as a tool for identifying bugs in the model or environment'''
   LOAD                    = False
   LOCAL_MODE              = True
   NUM_WORKERS             = 1

   SGD_MINIBATCH_SIZE      = 100
   TRAIN_BATCH_SIZE        = 400
   TRAIN_HORIZON           = 200
   EVALUATION_HORIZON      = 50

   HIDDEN                  = 2
   EMBED                   = 2

### AICrowd competition settings
class Competition(config.AllGameSystems, config.Achievement): pass
class CompetitionRound1(SmallMaps, Competition):
   @property
   def SPAWN(self):
      return self.SPAWN_CONCURRENT

   NENT                    = 128
   NPOP                    = 1

class CompetitionRound2(SmallMaps, Competition):
   @property
   def SPAWN(self):
      return self.SPAWN_CONCURRENT

   NENT                    = 128
   NPOP                    = 16
   COOPERATIVE             = True

class CompetitionRound3(LargeMaps, Competition):
   @property
   def SPAWN(self):
      return self.SPAWN_CONCURRENT

   NENT                    = 1024
   NPOP                    = 32
   COOPERATIVE             = True


### NeurIPS Experiments
class SmallMultimodalSkills(SmallMaps, config.AllGameSystems): pass
class LargeMultimodalSkills(LargeMaps, config.AllGameSystems): pass


class MagnifyExploration(SmallMaps, config.Resource, config.Progression):
   pass
class Population4(MagnifyExploration):
   NENT  = 256
class Population32(MagnifyExploration):
   NENT  = 256
class Population256(MagnifyExploration):
   NENT  = 256


class DomainRandomization16384(SmallMaps, config.AllGameSystems):
   TERRAIN_TRAIN_MAPS=16384
class DomainRandomization256(SmallMaps, config.AllGameSystems):
   TERRAIN_TRAIN_MAPS=256
class DomainRandomization32(SmallMaps, config.AllGameSystems):
   TERRAIN_TRAIN_MAPS=32
class DomainRandomization1(SmallMaps, config.AllGameSystems):
   TERRAIN_TRAIN_MAPS=1


class TeamBased(MagnifyExploration, config.Combat):
   NENT                    = 128
   NPOP                    = 32
   COOPERATIVE             = True
   TEAM_SPIRIT             = 0.5

   @property
   def SPAWN(self):
      return self.SPAWN_CONCURRENT
