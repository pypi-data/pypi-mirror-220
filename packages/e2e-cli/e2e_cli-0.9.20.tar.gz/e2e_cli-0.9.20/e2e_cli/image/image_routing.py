import subprocess

from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core import show_messages, constants
from e2e_cli.image.image_crud.image import ImageCrud
from e2e_cli.image.image_listing.image_list import ImageListing


class ImageRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, parsing_errors):
        if (self.arguments.args.image_commands is None):
            show_messages.show_parsing_error(parsing_errors)
            subprocess.call([constants.E2E_CLI, constants.IMAGE, constants._HELP])

        elif (self.arguments.args.image_commands is not None):
            image_operations = ImageCrud(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if image_operations.possible:
                operation = image_operations.caller(
                    self.arguments.args.image_commands)
                if operation:
                    operation()

        # elif self.arguments.args.list_by == 'image_type':
        #     image_operations=ImageListing(alias=self.arguments.args.alias)
        #     if(image_operations.possible):
        #                 try:
        #                    image_operations.all()
        #                 except KeyboardInterrupt:
        #                     print(" ")

        else:
            print("command not found")
            show_messages.show_parsing_error(parsing_errors)
