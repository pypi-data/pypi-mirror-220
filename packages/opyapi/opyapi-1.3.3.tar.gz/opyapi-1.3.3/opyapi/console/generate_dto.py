from os import path

from cleo.commands.command import Command
from cleo.helpers import argument, option

from .dto_generator.generator import DtoGenerator


class GenerateDtoCommand(Command):
    """
    Generates dto classes from openapi file.

    generate:dto
        { openapi-path : Path to openapi.yml file }
        { --module-path=dto.py : Path to module file where generated classes will be stored, keep in mind this file will be automatically replaced! }
        { --class-suffix= : Adds optional suffix for each class}
        { --snake-case : Converts property names to snake case }

    """
    name = 'generate:dto'
    arguments = [
        argument(
            "openapi-path",
            description="path to openapi defintion file",
        )
    ]

    options = [
        option(
            long_name="module-path",
            description="Path to module file where generated classes will be stored, keep in mind this file will be automatically replaced!",
            flag=False,
            default="dto.py"
        ),
        option(
            long_name="class-suffix",
            description="Adds optional suffix for each class",
        ),
        option(
            long_name="snake-case",
            description="Converts property names to snake case",
        ),

    ]

    def handle(self):
        openapi_path = self.argument("openapi-path")
        module_path = self.option("module-path")
        class_suffix = self.option("class-suffix")
        snake_case = self.option("snake-case")

        if not path.isfile(openapi_path):
            self.line_error(f"<error>Could not read openapi file `{openapi_path}`.</error>")
            return 1

        if not path.isfile(module_path):
            self.line_error(f"<error>Output module `{module_path}` does not exists.</error>")
            return 1

        self.info(f"Generating dto classes from `{openapi_path}`...")

        dto_generator = DtoGenerator(
            openapi_path,
            module_path,
            snake_case,
            str(class_suffix) if class_suffix else "",
        )
        dto_generator.generate(lambda msg: self.info(msg), lambda msg: self.line_error(msg))
