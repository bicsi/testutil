from dataclasses import dataclass, is_dataclass
from typing import Tuple, List
import yaml 
from pydantic import BaseModel 

class ProblemConfig(BaseModel):
    input_file: str 
    output_file: str 
    time_limit_ms: float 


class GenerationConfig(BaseModel):
    run_deterministic_check: bool 
    num_workers: int
    model_solution: str 
    

class EvaluationConfig(BaseModel):
    timeout_multiplier: float 
    tl_close_range: Tuple[float, float]


class TestsConfig(BaseModel):
    tests_dir: str 
    input_pattern: str 
    answer_pattern: str 
    
    
class CompilerConfig(BaseModel):
    output_dir: str
    gcc: str 
    args: List[str]


class Pattern(BaseModel):
    kind: str 
    pattern: str 


class DiscoveryConfig(BaseModel):
    patterns: List[Pattern]

    

class Config(BaseModel):
    debug: bool 
    temp_dir: str 
    discovery: DiscoveryConfig
    compiler: CompilerConfig
    problem: ProblemConfig
    generation: GenerationConfig 
    tests: TestsConfig
    evaluation: EvaluationConfig
    problem: ProblemConfig
   

def load(*dicts):
    def merge_rec(d1: dict, d2: dict):
        for k, v in d2.items():
            child = d1.get(k, {})
            if isinstance(v, dict):
                merge_rec(child, v)
            else:
                child = v
            d1[k] = child

    def load_rec(typ, d):
        if is_dataclass(typ):
            assert isinstance(d, dict), f"Format error: '{d}'"
            kwargs = {}
            fields = typ.__dataclass_fields__
            for k, v in d.items():
                kwargs[k] = load_rec(fields[k].type, v)
            return typ(**kwargs)
        elif isinstance(typ, List):
            assert False
        return d

    cfg = {}
    for d in dicts:
        merge_rec(cfg, d)
    return Config(**cfg)
