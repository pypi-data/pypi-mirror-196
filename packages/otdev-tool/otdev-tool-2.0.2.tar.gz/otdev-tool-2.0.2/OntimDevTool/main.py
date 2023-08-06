from pyfiglet import Figlet
import argparse
from OntimDevTool import G_version
from OntimDevTool.diag_port_controller import open_diag_port, close_diag_port
from OntimDevTool.auth_controller import authorise, edl, offline_auth_01_get_nonce, offline_auth_02_get_sign, offline_auth_03_set_permission

FUNCTIONLIST = ["open_diag", "close_diag", "authorise", "edl", 
                "offline_auth_01_get_nonce", "offline_auth_02_get_sign", "offline_auth_03_set_permission"]

def print_logo():
    # logo = Figlet().renderText(f"Ontim Tool      {version}")
    logo = f"Ontim Tool      {G_version}"
    print(logo)

def main():
    """
    Command line main entry

    Start OntimDevTool

    * list all functions supported.
    ```
    otdev-tool -l
    ```

    * open diag port
    ```
    otdev-tool -p sunfire -f open_diag_port
    ```

    * close diag port
    ```
    otdev-tool -p sunfire -f close_diag_port
    ```
 
    * authorise
    ```
    otdev-tool -p sunfire -f authorise
    ```
    """
    print_logo()
    parser = argparse.ArgumentParser(prog='otdev-tool')

    parser.add_argument('-l', '--list', dest='list_functions', action='store_true', help='List all functions supported.')
    parser.add_argument('-p', '--project', dest='project', default='sunfire', help='Set project, default is sunfire.')
    parser.add_argument('-f', '--function', dest='function', help="Set function you'd like to call.")
    parser.add_argument('-o', '--offline', dest='offline_para', help="Set additional paramater for offline auth.")

    args = parser.parse_args()

    if args.list_functions:
        print(f"Functions supported: {FUNCTIONLIST}")
        parser.print_usage()
        return

    if args.project:
        project = args.project
    else:
        project = "sunfire"

    if args.function:
        function = args.function
        function_hub(project, function, args.offline_para)
    else:
        parser.print_help()
        return

def function_hub(project, function, offline_para):
    print(f"start run tools, project: {project}, function: {function}")
    if function == FUNCTIONLIST[0]:
        open_diag_port(project)
    elif function == FUNCTIONLIST[1]:
        close_diag_port()
    elif function == FUNCTIONLIST[2]:
        authorise(project)
    elif function == FUNCTIONLIST[3]:
        edl(project)
    elif function == FUNCTIONLIST[4]:
        offline_auth_01_get_nonce()
    elif function == FUNCTIONLIST[5]:
        offline_auth_02_get_sign(offline_para)
    elif function == FUNCTIONLIST[6]:
        offline_auth_03_set_permission(offline_para)
    else:
        print(f"unsupport function: {function}")


if __name__ == "__main__":
    main()
