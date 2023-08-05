"""CLI Tool to write whole paremeter set EDrive device using .pck file."""
import logging
from edcon.edrive.parameter_set import ParameterSet
from edcon.edrive.parameter_mapping import ParameterMap


def add_parameter_set_load_parser(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_pnu = subparsers.add_parser('parameter-set-load')
    parser_pnu.set_defaults(func=parameter_set_load_func)

    parser_pnu.add_argument("file",
                            help="Parameter set to write.")


def parameter_set_load_func(com, args):
    """Executes subcommand based on provided arguments"""
    parameter_set = ParameterSet(args.file)
    parameter_map = ParameterMap()

    counter = 0
    for parameter in parameter_set:
        pnu = int(parameter_map[parameter.uid()].pnu)
        status = com.write_pnu_raw(
            pnu=pnu, subindex=parameter.subindex, num_elements=1, value=parameter.value)
        if status:
            counter += 1
        else:
            logging.error(
                f"Setting {parameter.uid()} (PNU: {pnu}) at subindex {parameter.subindex} "
                f"to {parameter.value} failed")

    print(f"{counter} PNUs succesfully written!")
