import copy
import IPython  # type: ignore
from IPython.core.display_functions import display  # type: ignore
import ipywidgets  # type: ignore
import nbformat
import jupytext    # type: ignore
import os
import random
import re
from typing import Any, List
from nbconvert.preprocessors import ExecutePreprocessor  # type: ignore

from code_randomizer import Randomizer


Notebook = Any


class ExecutionError(RuntimeError):
    pass

class Exercizer(ipywidgets.VBox):
    def __init__(self, exercizes: List[str]):
        self.exercizes = sorted(exercizes)

        # View
        border_layout = ipywidgets.Layout(border="solid", padding="1ex")
        self.exercize_zone = ipywidgets.Output(layout=border_layout)
        self.answer_zone = ipywidgets.Text()
        self.run_button = ipywidgets.Button(
            description="Valider", button_style="primary", icon="check"
        )
        self.name_label = ipywidgets.Label()
        self.result_label = ipywidgets.Label()
        self.randomize_button = ipywidgets.Button(
            icon="dice",
            description="Variante",
            tooltip="Tire aléatoirement une autre variante du même exercice",
            button_style="primary",
            layout={"width": "fit-content"},
        )
        self.next_button = ipywidgets.Button(
            icon="caret-right",
            description="Exercice suivant",
            button_style="primary",
            layout={"width": "fit-content"},
        )
        self.previous_button = ipywidgets.Button(
            icon="caret-left",
            description="Exercice précédent",
            button_style="primary",
            layout={"width": "fit-content"},
        )
        self.random_button = ipywidgets.Button(
            icon="dice",
            description="Exercice aléatoire",
            tooltip="Tire aléatoirement un exercice",
            button_style="primary",
            layout={"width": "fit-content"},
        )
        self.controler_zone = ipywidgets.VBox(
            [
                ipywidgets.HBox(
                    [
                        self.randomize_button,
                        self.run_button,
                        self.name_label,
                        self.result_label,
                    ]
                ),
                ipywidgets.HBox(
                    [self.previous_button, self.random_button, self.next_button]
                ),
            ]
        )

        # Controler
        self.next_button.on_click(lambda event: self.next_exercize())
        self.previous_button.on_click(lambda event: self.previous_exercize())
        self.random_button.on_click(lambda event: self.random_exercize())
        self.randomize_button.on_click(lambda event: self.randomize_exercize())
        self.run_button.on_click(lambda event: self.run_exercize())

        self.set_exercize(0)
        super().__init__(
            [self.exercize_zone, self.controler_zone], layout=border_layout
        )

    def set_exercize(self, i: int):
        self.exercize_number = i
        self.exercize_name = self.exercizes[self.exercize_number]
        self.notebook = self.randomize_notebook(jupytext.read(self.exercize_name))
        self.display_exercize(self.notebook)
        language = self.notebook.metadata["kernelspec"]["language"]
        self.name_label.value = f'{self.exercize_name} ({language})'
        self.result_label.value = ""

    def next_exercize(self):
        self.set_exercize((self.exercize_number + 1) % len(self.exercizes))

    def previous_exercize(self):
        self.set_exercize((self.exercize_number - 1) % len(self.exercizes))

    def random_exercize(self):
        self.set_exercize(random.randint(0, len(self.exercizes) - 1))

    def randomize_exercize(self):
        self.set_exercize(self.exercize_number)

    def run_exercize(self):
        self.result_label.value = "🟡 Exécution en cours"
        # self.result_label.style.background = "orange"
        self.run_button.disabled = True
        try:
            success = self.run_notebook(
                self.notebook,
                answer=self.answer_zone.value,
                dir=os.path.dirname(self.exercize_name),
            )
            self.result_label.value = (
                "✅ Bonne réponse" if success else "❌ Mauvaise réponse"
            )
            # self.result_label.style.background = "green" if success else "red"
        except ExecutionError:
            self.result_label.value = "❌ Erreur à l'exécution"
            # self.result_label.style.background = "red"
        finally:
            self.run_button.disabled = False

    def display_exercize(self, notebook):
        with self.exercize_zone:
            self.exercize_zone.clear_output(wait=True)
            for cell in notebook.cells:
                if cell["metadata"].get("nbgrader", {}).get("solution", False):
                    self.answer_zone.value = ""
                    display(self.answer_zone)
                elif cell["cell_type"] == "markdown":
                    display(IPython.display.Markdown(cell["source"]))
                else:
                    if "hide-cell" not in cell["metadata"].get("tags", []):
                        display(IPython.display.Code(cell["source"]))

    def randomize_notebook(self, notebook: Notebook) -> Notebook:
        notebook = copy.deepcopy(notebook)
        language = notebook.metadata["kernelspec"]["language"]
        randomizer = Randomizer(language=language)
        for cell in notebook.cells:
            cell["source"] = randomizer.randomize(
                text=cell["source"], is_code=(cell["cell_type"] == "code")
            )
        return notebook

    def run_notebook(self, notebook: Notebook, answer: str, dir: str) -> bool:
        notebook = copy.deepcopy(notebook)
        kernel_name = notebook["metadata"]["kernelspec"]["name"]
        for i, cell in enumerate(notebook.cells):
            # If Autograded code cell
            if cell["cell_type"] == "code" and cell["metadata"].get("nbgrader", {}).get(
                "solution", False
            ):
                if "tags" in cell["metadata"] and "output" in cell["metadata"]["tags"]:
                    if "python" in kernel_name:
                        code = "answer = " + answer
                    else:
                        code = "auto answer = " + answer + ";"
                else:
                    code = answer
                notebook.cells[i] = nbformat.v4.new_code_cell(code)
        ep = ExecutePreprocessor(timeout=600, kernel_name=kernel_name, allow_errors=True)

        owd = os.getcwd()
        try:
            os.chdir(dir)
            result = ep.preprocess(notebook)
        finally:
            os.chdir(owd)

        success = True
        for cell in result[0]["cells"]:
            # If this is a code cell and execution errored
            if cell["cell_type"] == "code" and any(
                output["output_type"] == "error" for output in cell["outputs"]
            ):
                if cell["metadata"].get("nbgrader", {}).get("grade", False):
                    # If Autograded tests cell
                    success = False
                # elif cell["metadata"].get("nbgrader", {}).get("solution", False):
                # TODO: handle autograded answer cell failure
                else:
                    # TODO: handle
                    raise ExecutionError("Execution failed")
        return success