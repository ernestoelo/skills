#!/usr/bin/env python3
"""
Orchestrator skill: State machine for managing skill pipelines.
"""

import json
import subprocess
import sys
import yaml
from pathlib import Path
from transitions import Machine

class Orchestrator:
    states = ['analyze_query', 'select_pipeline', 'check_dependencies', 'invoke_skill', 'handle_output', 'iterate_on_error', 'complete']

    def __init__(self, query):
        self.query = query
        self.pipeline = []
        self.current_skill_index = 0
        self.data = {}
        self.max_retries = 3
        self.retries = 0

        self.machine = Machine(model=self, states=Orchestrator.states, initial='analyze_query')
        self.machine.add_transition('analyze', 'analyze_query', 'select_pipeline')
        self.machine.add_transition('select', 'select_pipeline', 'check_dependencies', conditions=['pipeline_selected'])
        self.machine.add_transition('deps_ok', 'check_dependencies', 'invoke_skill')
        self.machine.add_transition('deps_fail', 'check_dependencies', 'iterate_on_error')
        self.machine.add_transition('invoke', 'invoke_skill', 'handle_output')
        self.machine.add_transition('success', 'handle_output', 'check_dependencies', conditions=['has_next_skill'])
        self.machine.add_transition('success', 'handle_output', 'complete', unless=['has_next_skill'])
        self.machine.add_transition('error', 'handle_output', 'iterate_on_error')
        self.machine.add_transition('retry', 'iterate_on_error', 'check_dependencies', conditions=['can_retry'])
        self.machine.add_transition('fail', 'iterate_on_error', 'complete')

    def pipeline_selected(self):
        # Load pipelines and match query
        pipelines_path = Path(__file__).parent.parent / 'references' / 'pipelines.yaml'
        with open(pipelines_path) as f:
            pipelines = yaml.safe_load(f)['pipelines']
        # Simple matching, e.g., if 'pdf' in query, use pdf_processing
        if 'pdf' in self.query.lower():
            self.pipeline = pipelines['pdf_processing']
        elif 'dev' in self.query.lower():
            self.pipeline = pipelines['dev_workflow']
        elif 'diagram' in self.query.lower():
            self.pipeline = pipelines['diagram_creation']
        else:
            self.pipeline = []
        return bool(self.pipeline)

    def has_next_skill(self):
        return self.current_skill_index < len(self.pipeline)

    def can_retry(self):
        return self.retries < self.max_retries

    def on_enter_check_dependencies(self):
        skill = self.pipeline[self.current_skill_index]
        # Map skill to required packages (example, expand as needed)
        skill_deps = {
            'pdf': ['pdftotext'],
            'code-review': ['ruff'],
            'dev-workflow': ['git'],
            'recursive-context': ['pdftotext'],
        }
        deps = skill_deps.get(skill, [])
        all_ok = True
        for dep in deps:
            result = subprocess.run([sys.executable, '../../sys-env/scripts/install_package.py', dep])
            if result.returncode != 0:
                all_ok = False
        if all_ok:
            self.to_deps_ok()
        else:
            self.to_deps_fail()

    def on_enter_invoke_skill(self):
        skill = self.pipeline[self.current_skill_index]
        # Si el skill es recursive-context y el input es PDF o archivo grande, procesar contexto primero
        if skill == 'recursive-context' and self.data.get('file_path', '').endswith('.pdf'):
            print('Procesando contexto PDF con recursive-context...')
        temp_file = Path('/tmp/orchestrator_data.json')
        with open(temp_file, 'w') as f:
            json.dump(self.data, f)
        script_path = Path(__file__).parent.parent / skill / 'scripts' / f'{skill}.py'
        if not script_path.exists():
            script_path = Path(__file__).parent.parent / skill / 'scripts' / 'analyze.py'
        result = subprocess.run([sys.executable, str(script_path), '--input', str(temp_file)], capture_output=True, text=True)
        if result.returncode == 0:
            with open(temp_file) as f:
                self.data.update(json.load(f))
            self.current_skill_index += 1
            self.to_handle_output()
        else:
            self.last_error = result.stderr
            self.to_iterate_on_error()

    def on_enter_iterate_on_error(self):
        print(f"Error en skill {self.pipeline[self.current_skill_index]}: {getattr(self, 'last_error', 'Unknown error')}")
        # Intentar resolver con sys-env si es dependencias, o loggear y reintentar
        self.retries += 1
        if self.can_retry():
            print("Reintentando tras manejar error...")
            self.to_retry()
        else:
            print("Error persistente, abortando pipeline.")
            self.to_fail()

if __name__ == '__main__':
    query = sys.argv[1] if len(sys.argv) > 1 else "default query"
    orch = Orchestrator(query)
    orch.analyze()
    if orch.pipeline_selected():
        orch.select()
        while orch.state != 'complete':
            if orch.state == 'invoke_skill':
                orch.invoke()
            elif orch.state == 'handle_output':
                orch.success()
    print("Orchestration complete:", orch.data)